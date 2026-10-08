"""Normalización de texto en español usada por BM25 y por el LLM simulado."""
from __future__ import annotations

import re
import unicodedata

STOPWORDS = {
    "a", "al", "algo", "con", "cual", "cuales", "cuanto", "cuanta", "cuantos", "cuantas",
    "de", "del", "el", "ella", "en", "es", "esta", "este", "hay", "la", "las", "lo", "los",
    "me", "mi", "mis", "para", "pero", "por", "que", "se", "si", "sin", "son", "su", "sus",
    "tu", "tus", "un", "una", "uno", "y", "o", "como", "donde", "cuando", "quiero", "puedo",
    "tengo", "tienen", "tiene", "necesito", "hola", "le", "les", "ya", "muy", "mas", "pasa",
}


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def normalize(text: str) -> str:
    return strip_accents(text.lower())


def tokenize(text: str) -> list[str]:
    """Tokens en minúscula, sin tildes, conservando números como 150,000 o 3.5."""
    return re.findall(r"\d+(?:[.,]\d+)*%?|[a-zñ]+", normalize(text))


def stem(token: str) -> str:
    """Stemming mínimo (plural en español) suficiente para el modo offline."""
    if len(token) > 4 and token.endswith("es"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s"):
        return token[:-1]
    return token


def content_tokens(text: str) -> list[str]:
    return [stem(t) for t in tokenize(text) if t not in STOPWORDS and len(t) > 1]
