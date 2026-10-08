"""Respaldo determinista del router: los casos reales que fallaron con gpt-4o-mini."""
import json

import pytest

from assistant.config import get_settings
from assistant.graph import build_graph
from assistant.llm import FakeLLM, LLMResponse
from assistant.routing import refine_route


@pytest.mark.parametrize("question", [
    "¿Cuál es el plazo máximo del préstamo personal?",            # q05 real
    "¿Qué ingreso mínimo piden para el préstamo personal?",       # q06 real
    "¿Cuál es la TEA del préstamo personal?",                     # q07 real
    "Mi DNI es [DNI], ¿cuánto cuesta la membresía de la tarjeta?",  # q25 real (ya enmascarado)
    "¿Cuál es la tasa del crédito hipotecario?",                  # producto inexistente -> RAG se abstiene
])
def test_corrige_clarify_si_el_producto_es_unico(question):
    assert refine_route("clarify", question, []) == ("rag", True)


@pytest.mark.parametrize("question", [
    "¿Cuál es la tasa?",
    "¿Cuál es el monto máximo que puedo pedir?",
    "¿Cuál es el monto máximo del préstamo?",  # dos préstamos en el catálogo: sí es ambiguo
    "¿y el plazo?",
])
def test_mantiene_clarify_si_es_ambiguo(question):
    assert refine_route("clarify", question, []) == ("clarify", False)


def test_usa_el_historial_para_desambiguar():
    history = [{"role": "user", "content": "Quiero info del préstamo personal"},
               {"role": "assistant", "content": "..."}]
    assert refine_route("clarify", "¿y la tasa?", history) == ("rag", True)


def test_no_toca_otras_rutas():
    assert refine_route("handoff", "préstamo personal", []) == ("handoff", False)


class AlwaysClarifyLLM(FakeLLM):
    """Simula un router demasiado cauteloso, como el gpt-4o-mini de la evaluación."""

    def _route(self, user: str) -> str:
        return json.dumps({"route": "clarify"})


def test_el_grafo_corrige_un_router_que_siempre_pide_aclaracion(assistant):
    graph = build_graph(AlwaysClarifyLLM(), assistant.retriever, get_settings())
    cfg = {"configurable": {"thread_id": "t-overcautious"}}
    state = graph.invoke({"user_input": "¿Cuál es la TEA del préstamo personal?"}, config=cfg)
    assert state["route"] == "rag" and state["route_corrected"]
    assert "prestamo_personal.md" in [r["source"] for r in state["retrieved"]]
    ambiguous = graph.invoke({"user_input": "¿Cuál es la tasa?"}, config={"configurable": {"thread_id": "t-amb"}})
    assert ambiguous["route"] == "clarify" and not ambiguous["route_corrected"]


def test_el_router_recibe_el_catalogo():
    seen = {}

    class SpyLLM(FakeLLM):
        def chat(self, system, user, json_mode=False):
            if "[TASK:ROUTE]" in system:
                seen["system"] = system
            return super().chat(system, user, json_mode)

    from assistant.service import Assistant
    a = Assistant()
    graph = build_graph(SpyLLM(), a.retriever, a.settings)
    graph.invoke({"user_input": "¿Cuál es la tasa?"}, config={"configurable": {"thread_id": "t-spy"}})
    assert "<PRODUCTOS>" not in seen["system"]
    assert "Préstamo Personal" in seen["system"] and "Tarjeta de Crédito Andina Clásica" in seen["system"]


@pytest.mark.parametrize("question", [
    "¿Tienen crédito hipotecario?",      # q26 real
    "¿Ofrecen leasing para empresas?",
    "¿Venden seguros de vida?",
])
def test_corrige_out_of_scope_en_preguntas_bancarias(question):
    assert refine_route("out_of_scope", question, []) == ("rag", True)


@pytest.mark.parametrize("question", [
    "¿Quién ganará las elecciones presidenciales en Perú?",
    "Dame una receta de ceviche",
    "¿Quién ganó el partido de fútbol ayer?",
])
def test_mantiene_out_of_scope_en_temas_no_bancarios(question):
    assert refine_route("out_of_scope", question, []) == ("out_of_scope", False)


class AlwaysOutOfScopeLLM(FakeLLM):
    def _route(self, user: str) -> str:
        return json.dumps({"route": "out_of_scope"})


def test_el_grafo_corrige_out_of_scope_bancario(assistant):
    graph = build_graph(AlwaysOutOfScopeLLM(), assistant.retriever, get_settings())
    state = graph.invoke({"user_input": "¿Tienen crédito hipotecario?"},
                         config={"configurable": {"thread_id": "t-oos"}})
    assert state["route"] == "rag" and state["route_corrected"]
