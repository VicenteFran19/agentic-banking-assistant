"""Recuperación híbrida: búsqueda vectorial (Chroma) + léxica (BM25), fusionadas con RRF.

Por qué híbrida: los embeddings capturan sinónimos y paráfrasis ("pagar por adelantado" ~
"pago anticipado"), mientras que BM25 es fuerte con términos exactos y cifras ("TEA", "0800",
"360 días"). Reciprocal Rank Fusion combina ambos rankings sin calibrar escalas de score.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass

import chromadb
from chromadb.config import Settings as ChromaSettings
from rank_bm25 import BM25Okapi

from .embeddings import BaseEmbedder
from .ingest import Chunk
from .text import content_tokens


@dataclass
class Retrieved:
    chunk: Chunk
    score: float
    vector_rank: int | None
    bm25_rank: int | None


class HybridRetriever:
    def __init__(self, chunks: list[Chunk], embedder: BaseEmbedder, candidates: int = 10, rrf_k: int = 60):
        self.chunks = chunks
        self.by_id = {c.id: c for c in chunks}
        self.embedder = embedder
        self.candidates = candidates
        self.rrf_k = rrf_k
        self.bm25 = BM25Okapi([content_tokens(c.text) for c in chunks])

        client = chromadb.EphemeralClient(settings=ChromaSettings(anonymized_telemetry=False))
        self.collection = client.create_collection(
            name=f"docs-{uuid.uuid4().hex[:8]}", metadata={"hnsw:space": "cosine"}
        )
        vectors, self.index_tokens = embedder.embed([c.text for c in chunks])
        self.collection.add(
            ids=[c.id for c in chunks],
            embeddings=vectors,
            documents=[c.text for c in chunks],
            metadatas=[{"source": c.source, "section": c.section} for c in chunks],
        )

    def search(self, query: str, k: int = 4) -> tuple[list[Retrieved], int]:
        """Devuelve (top-k fusionados, tokens de embedding consumidos por la consulta)."""
        n = min(self.candidates, len(self.chunks))
        query_vec, tokens = self.embedder.embed([query])
        vec_res = self.collection.query(query_embeddings=query_vec, n_results=n)
        vector_ids = vec_res["ids"][0]

        bm25_scores = self.bm25.get_scores(content_tokens(query))
        bm25_order = sorted(range(len(self.chunks)), key=lambda i: bm25_scores[i], reverse=True)
        bm25_ids = [self.chunks[i].id for i in bm25_order[:n] if bm25_scores[i] > 0]

        fused: dict[str, float] = {}
        for ranking in (vector_ids, bm25_ids):
            for rank, cid in enumerate(ranking, start=1):
                fused[cid] = fused.get(cid, 0.0) + 1.0 / (self.rrf_k + rank)

        top = sorted(fused.items(), key=lambda x: x[1], reverse=True)[:k]
        results = [
            Retrieved(
                chunk=self.by_id[cid],
                score=round(score, 5),
                vector_rank=vector_ids.index(cid) + 1 if cid in vector_ids else None,
                bm25_rank=bm25_ids.index(cid) + 1 if cid in bm25_ids else None,
            )
            for cid, score in top
        ]
        return results, tokens
