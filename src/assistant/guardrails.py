"""Guardrails de entrada y salida.

Entrada: enmascarado de datos personales (PII) antes de enviar texto al LLM y detección de
intentos de prompt injection. Salida: re-enmascarado de PII y verificación de que una respuesta
del RAG cite sus fuentes (si no, se reemplaza por una respuesta segura: preferimos abstenernos
antes que alucinar).
"""
from __future__ import annotations

import re

from .text import normalize

PII_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("[EMAIL]", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("[TARJETA]", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    ("[TELEFONO]", re.compile(r"(?:\+?51[ -]?)?\b9\d{2}[ -]?\d{3}[ -]?\d{3}\b")),
    ("[DNI]", re.compile(r"(?<!S/ )(?<!S/)\b\d{8}\b")),
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


def cited_sources(answer: str) -> list[str]:
    """Extrae los archivos citados. Acepta [fuente: a.md | Sección] y [fuente: a.md, b.md]."""
    sources: set[str] = set()
    for citation in re.findall(r"\[fuente:\s*([^\]]+)\]", answer):
        sources.update(re.findall(r"[\w-]+\.md", citation))
    return sorted(sources)
