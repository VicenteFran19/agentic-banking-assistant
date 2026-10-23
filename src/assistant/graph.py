"""Grafo del agente con LangGraph.

    START -> guard_in -> (bloqueado?) -> router -> rag | simulator | clarify | handoff | out_of_scope
          -> guard_out -> END

La memoria de conversación se persiste por thread_id con un checkpointer de LangGraph.
Privacidad: el texto llega a este grafo YA enmascarado (ver service.Assistant.ask), porque el
checkpointer guarda la entrada antes de ejecutar cualquier nodo. guard_in vuelve a enmascarar
como defensa en profundidad.
"""
from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from . import prompts
from .config import Settings
from .guardrails import cited_sources, citations_grounded, detect_injection, mask_pii
from .llm import BaseLLM, LLMResponse, parse_json
from .retriever import HybridRetriever
from .routing import refine_route
from .tools import format_simulation, simulate_loan, validate_loan_params

ROUTES = ("rag", "simulator", "clarify", "handoff", "out_of_scope")
MAX_HISTORY_MESSAGES = 20  # tope de mensajes guardados por thread (10 turnos)


def _append_capped(left: list[dict] | None, right: list[dict] | None) -> list[dict]:
    """Reducer de memoria: agrega los mensajes nuevos y conserva solo los más recientes."""
    return ((left or []) + (right or []))[-MAX_HISTORY_MESSAGES:]


class AgentState(TypedDict, total=False):
    user_input: str
    question: str
    pii_masked: bool
    route_corrected: bool
    route: str
    answer: str
    sources: list[str]
    retrieved: list[dict]
    usage: list[dict]
    history: Annotated[list[dict], _append_capped]


def _usage(resp: LLMResponse, kind: str) -> dict:
    return {"kind": kind, "model": resp.model, "input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens}


def _history_text(history: list[dict], turns: int) -> str:
    recent = history[-2 * turns:]
    return "\n".join(f"{h['role']}: {h['content']}" for h in recent) or "(sin historial)"


def build_graph(llm: BaseLLM, retriever: HybridRetriever, settings: Settings):
    products = sorted({c.text.split(" — ")[0].replace(" (Banco Andino Demo)", "")
                       for c in retriever.chunks if not c.source.startswith("canales")})

    router_prompt = prompts.ROUTER.replace("<PRODUCTOS>", ", ".join(products))

    def guard_in(state: AgentState) -> dict:
        question, masked = mask_pii(state["user_input"])
        update: dict[str, Any] = {"user_input": question, "question": question,
                                  "pii_masked": bool(state.get("pii_masked")) or masked, "route_corrected": False, "usage": [],
                                  "sources": [], "retrieved": [], "route": "", "answer": ""}
        if detect_injection(question):
            update.update(route="blocked", answer=prompts.BLOCKED_MSG)
        return update

    def router(state: AgentState) -> dict:
        user = f"HISTORIAL:\n{_history_text(state.get('history', []), settings.history_turns)}\n\nMENSAJE: {state['question']}"
        resp = llm.chat(router_prompt, user, json_mode=True)
        route = parse_json(resp.text).get("route", "rag")
        route = route if route in ROUTES else "rag"
        route, corrected = refine_route(route, state["question"], state.get("history", []))
        return {"route": route, "route_corrected": corrected, "usage": state["usage"] + [_usage(resp, "router")]}

    def rag(state: AgentState) -> dict:
        question = state["question"]
        query = question
        history = state.get("history", [])
        # Preguntas de seguimiento cortas ("¿y el plazo?") se enriquecen con la pregunta anterior.
        if len(question.split()) < 6 and history:
            prev_user = [h["content"] for h in history if h["role"] == "user"]
            if prev_user:
                query = f"{prev_user[-1]} {question}"
        results, emb_tokens = retriever.search(query, k=settings.top_k)
        context = "\n\n".join(f"[fuente: {r.chunk.source} | {r.chunk.section}] {r.chunk.text}" for r in results)
        user = (f"HISTORIAL:\n{_history_text(history, settings.history_turns)}\n\n"
                f"CONTEXTO:\n{context}\n\nPREGUNTA: {question}")
        resp = llm.chat(prompts.ANSWER, user)
        usage = state["usage"] + [_usage(resp, "answer"),
                                  {"kind": "embedding", "model": "embedding", "input_tokens": emb_tokens, "output_tokens": 0}]
        retrieved = [{"source": r.chunk.source, "section": r.chunk.section, "text": r.chunk.text,
                      "score": r.score, "vector_rank": r.vector_rank, "bm25_rank": r.bm25_rank} for r in results]
        answer = resp.text.strip()
        if "NO_INFO" in answer:
            return {"answer": prompts.NO_INFO_MSG, "sources": [], "retrieved": retrieved, "usage": usage}
        return {"answer": answer, "sources": cited_sources(answer), "retrieved": retrieved, "usage": usage}

    def simulator(state: AgentState) -> dict:
        user = f"HISTORIAL:\n{_history_text(state.get('history', []), settings.history_turns)}\n\nMENSAJE: {state['question']}"
        resp = llm.chat(prompts.EXTRACT, user, json_mode=True)
        params = parse_json(resp.text)
        usage = state["usage"] + [_usage(resp, "extract")]
        values, problems = validate_loan_params(params)
        if problems:  # nunca llega a simulate_loan un valor faltante, fuera de rango o mal formado
            return {"answer": " ".join(problems), "sources": ["simulador"], "usage": usage}
        sim = simulate_loan(values["monto"], values["tea"], values["plazo_meses"])
        return {"answer": format_simulation(sim), "sources": ["simulador"], "usage": usage}

    def clarify(state: AgentState) -> dict:
        return {"answer": prompts.CLARIFY_MSG.format(products=", ".join(products))}

    def handoff(state: AgentState) -> dict:
        return {"answer": prompts.HANDOFF_MSG}

    def out_of_scope(state: AgentState) -> dict:
        return {"answer": prompts.OUT_OF_SCOPE_MSG}

    def guard_out(state: AgentState) -> dict:
        answer = state["answer"]
        sources = state.get("sources", [])
        if state["route"] == "rag" and answer != prompts.NO_INFO_MSG:
            retrieved_sources = {r["source"] for r in state.get("retrieved", [])}
            if not citations_grounded(answer, retrieved_sources):
                # Sin cita, o citando un archivo que no se recuperó = posible alucinación -> abstención
                answer, sources = prompts.NO_INFO_MSG, []
        answer, _ = mask_pii(answer)
        return {"answer": answer, "sources": sources,
                "history": [{"role": "user", "content": state["question"]},
                            {"role": "assistant", "content": answer}]}

    graph = StateGraph(AgentState)
    for name, fn in [("guard_in", guard_in), ("router", router), ("rag", rag), ("simulator", simulator),
                     ("clarify", clarify), ("handoff", handoff), ("out_of_scope", out_of_scope), ("guard_out", guard_out)]:
        graph.add_node(name, fn)
    graph.add_edge(START, "guard_in")
    graph.add_conditional_edges("guard_in", lambda s: "guard_out" if s["route"] == "blocked" else "router",
                                {"guard_out": "guard_out", "router": "router"})
    graph.add_conditional_edges("router", lambda s: s["route"], {r: r for r in ROUTES})
    for r in ROUTES:
        graph.add_edge(r, "guard_out")
    graph.add_edge("guard_out", END)
    return graph.compile(checkpointer=MemorySaver())
