"""Fachada del asistente: arma índice, LLM y grafo, y expone ask() con costo y latencia."""
from __future__ import annotations

import time
import uuid

from .config import Settings, get_settings
from .embeddings import get_embedder
from .graph import build_graph
from .guardrails import mask_pii
from .ingest import load_documents
from .llm import get_llm
from .retriever import HybridRetriever


class Assistant:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.llm = get_llm(self.settings)
        self.embedder = get_embedder(self.settings)
        self.chunks = load_documents(self.settings.docs_dir)
        self.retriever = HybridRetriever(self.chunks, self.embedder, self.settings.candidates, self.settings.rrf_k)
        self.graph = build_graph(self.llm, self.retriever, self.settings)

    def cost_usd(self, usage: list[dict]) -> float:
        s = self.settings
        if s.provider == "fake":
            return 0.0
        total = 0.0
        for u in usage:
            if u["kind"] == "embedding":
                total += u["input_tokens"] * s.price_embedding_per_1m / 1e6
            else:
                total += u["input_tokens"] * s.price_input_per_1m / 1e6 + u["output_tokens"] * s.price_output_per_1m / 1e6
        return total

    def ask(self, message: str, thread_id: str | None = None) -> dict:
        thread_id = thread_id or uuid.uuid4().hex
        start = time.perf_counter()
        # Enmascarar ANTES del grafo: el checkpointer persiste la entrada tal como llega.
        safe_message, masked = mask_pii(message)
        state = self.graph.invoke({"user_input": safe_message, "pii_masked": masked},
                                  config={"configurable": {"thread_id": thread_id}})
        latency_ms = (time.perf_counter() - start) * 1000
        usage = state.get("usage", [])
        return {
            "thread_id": thread_id,
            "answer": state["answer"],
            "route": state["route"],
            "route_corrected": state.get("route_corrected", False),
            "sources": state.get("sources", []),
            "retrieved": state.get("retrieved", []),
            "pii_masked": state.get("pii_masked", False),
            "input_tokens": sum(u["input_tokens"] for u in usage if u["kind"] != "embedding"),
            "output_tokens": sum(u["output_tokens"] for u in usage),
            "cost_usd": round(self.cost_usd(usage), 6),
            "latency_ms": round(latency_ms, 1),
        }
