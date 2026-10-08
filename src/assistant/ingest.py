"""Ingesta y chunking de documentos Markdown.

Estrategia: un chunk por sección (encabezado "## "), con el título del documento y de la
sección antepuestos para dar contexto al embedding. Las secciones largas se dividen por
oraciones con solapamiento, para no cortar una cifra de su contexto.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    id: str
    text: str
    source: str
    section: str


def _split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _window(sentences: list[str], max_chars: int, overlap: int) -> list[str]:
    parts, current = [], []
    for sent in sentences:
        if current and len(" ".join(current + [sent])) > max_chars:
            parts.append(" ".join(current))
            current = current[-overlap:] if overlap else []
        current.append(sent)
    if current:
        parts.append(" ".join(current))
    return parts


def chunk_markdown(path: Path, max_chars: int = 600, overlap_sentences: int = 1) -> list[Chunk]:
    raw = path.read_text(encoding="utf-8")
    title_match = re.search(r"^# (.+)$", raw, flags=re.M)
    title = title_match.group(1).strip() if title_match else path.stem
    chunks: list[Chunk] = []
    for block in re.split(r"^## ", raw, flags=re.M)[1:]:
        section, _, body = block.partition("\n")
        body = " ".join(line.strip() for line in body.splitlines() if line.strip() and not line.startswith(">"))
        for i, part in enumerate(_window(_split_sentences(body), max_chars, overlap_sentences)):
            chunks.append(Chunk(
                id=f"{path.stem}::{section.strip()}::{i}",
                text=f"{title} — {section.strip()}: {part}",
                source=path.name,
                section=section.strip(),
            ))
    return chunks


def load_documents(docs_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(docs_dir.glob("*.md")):
        chunks.extend(chunk_markdown(path))
    if not chunks:
        raise ValueError(f"No se encontraron documentos en {docs_dir}")
    return chunks
