"""Guardrails de entrada y salida.

Entrada: enmascarado de datos personales (PII) antes de enviar texto al LLM y detección de
intentos de prompt injection. Salida: re-enmascarado de PII y verificación de que una respuesta
del RAG cite sus fuentes (si no, se reemplaza por una respuesta segura: preferimos abstenernos
antes que alucinar).
"""
from __future__ import annotations

import re

from .text import normalize

# Un número precedido de S/, S/., US$ o $, o seguido de "soles"/"dólares", es un monto y no un DNI.
_NOT_AFTER_CURRENCY = r"(?<!s/ )(?<!s/)(?<!s/\. )(?<!s/\.)(?<!\$ )(?<!\$)"
_NOT_BEFORE_CURRENCY = r"(?!\s*(?:soles|nuevos soles|d[oó]lares|usd|pen)\b)"

PII_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("[EMAIL]", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    # CCI: 20 dígitos (antes que tarjeta, que solo cubre 13-19).
    ("[CCI]", re.compile(r"\b(?:\d[ -]?){19}\d\b")),
    ("[TARJETA]", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    ("[TELEFONO]", re.compile(r"(?:\+?51[ -]?)?\b9\d{2}[ -]?\d{3}[ -]?\d{3}\b")),
    ("[DNI]", re.compile(rf"{_NOT_AFTER_CURRENCY}\b(?:\d{{8}}|\d{{2}}\.\d{{3}}\.\d{{3}})\b{_NOT_BEFORE_CURRENCY}",
                         flags=re.I)),
]

INJECTION_PATTERNS = [
    r"ignora (todas )?(tus|las) (instrucciones|reglas)",
    r"ignore (all )?(previous|your) instructions",
    r"(muestra|revela|dime|ensena)(me)? (tu|el) (system )?prompt",
    r"system prompt",
    r"actua como (si no tuvieras|un hacker|dan)",
    r"jailbreak",
    r"modo desarrollador",
]


def mask_pii(text: str) -> tuple[str, bool]:
    masked = text
    for token, pattern in PII_PATTERNS:
        masked = pattern.sub(token, masked)
    return masked, masked != text


def detect_injection(text: str) -> bool:
    norm = normalize(text)
    return any(re.search(p, norm) for p in INJECTION_PATTERNS)


def has_citation(answer: str) -> bool:
    return bool(re.search(r"\[fuente:\s*[^\]]+\]", answer))


def citations_grounded(answer: str, retrieved_sources: set[str]) -> bool:
    """True si la respuesta cita al menos una fuente y TODAS fueron efectivamente recuperadas.

    Evita que pase una cita inventada ("[fuente: inventado.md]") solo por tener el formato correcto.
    """
    cited = cited_sources(answer)
    return bool(cited) and set(cited) <= retrieved_sources


def cited_sources(answer: str) -> list[str]:
    """Extrae los archivos citados. Acepta [fuente: a.md | Sección] y [fuente: a.md, b.md]."""
    sources: set[str] = set()
    for citation in re.findall(r"\[fuente:\s*([^\]]+)\]", answer):
        sources.update(re.findall(r"[\w-]+\.md", citation))
    return sorted(sources)
