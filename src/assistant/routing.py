"""Respaldo determinista del router.

El LLM decide los casos difíciles; este módulo corrige dos errores caros y fáciles de detectar:
1. Pedir aclaración cuando el mensaje (o el historial) ya identifica un único producto.
   Una aclaración innecesaria agrega un turno y frustra al cliente.
2. Marcar como "fuera de alcance" una pregunta bancaria sobre un producto que no está en el
   catálogo. Debe ir al RAG, que se abstiene y ofrece un asesor en vez de rechazar al cliente.
"""
from __future__ import annotations

import re

from .text import normalize

# Palabras que identifican sin ambigüedad un producto del catálogo, o uno que no existe
# (hipotecario, vehicular): en ese caso el RAG se abstiene correctamente.
PRODUCT_PATTERNS = [
    r"prestamo personal", r"credito personal", r"capital de trabajo", r"para mi negocio",
    r"tarjeta", r"membresia", r"cuenta de ahorro", r"cuenta ahorro", r"ahorros?",
    r"deposito", r"plazo fijo", r"hipotecari[oa]", r"vehicular",
]


def mentions_specific_product(text: str) -> bool:
    norm = normalize(text)
    return any(re.search(rf"\b{p}\b", norm) for p in PRODUCT_PATTERNS)


BANKING_TERMS = re.compile(
    r"\b(prestamos?|creditos?|tarjetas?|cuentas?|ahorros?|depositos?|tasas?|tea|trea|cuotas?|"
    r"hipotecari[oa]s?|vehicular|leasing|seguros?|banco|bancari[oa]s?|transferencias?|agencias?)\b"
)


def is_banking_question(text: str) -> bool:
    return bool(BANKING_TERMS.search(normalize(text)))


def refine_route(route: str, question: str, history: list[dict]) -> tuple[str, bool]:
    """Devuelve (ruta final, si fue corregida)."""
    if route == "out_of_scope":
        return ("rag", True) if is_banking_question(question) else (route, False)
    if route != "clarify":
        return route, False
    recent_user = " ".join(h["content"] for h in history[-6:] if h["role"] == "user")
    if mentions_specific_product(question) or mentions_specific_product(recent_user):
        return "rag", True
    return route, False


FRAUD_TERMS = re.compile(
    r"\b(fraude|estafa|clonad[oa]s?|clonaron|robaron|robo|hackearon|cargos?|consumos?|"
    r"no (los |las )?reconozco|no (los |las )?hice|no autorice)\b"
)


def is_fraud_report(text: str) -> bool:
    """True si el mensaje reporta un posible fraude (para agregar el consejo de bloquear la tarjeta)."""
    return bool(FRAUD_TERMS.search(normalize(text)))