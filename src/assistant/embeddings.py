"""Embeddings: OpenAI en modo real y un vectorizador local (hashing de n-gramas) en modo offline."""
from __future__ import annotations

import numpy as np

from .config import Settings
from .text import normalize


class BaseEmbedder:
    model: str = "base"

    def embed(self, texts: list[str]) -> tuple[list[list[float]], int]:  # pragma: no cover
        """Devuelve (vectores, tokens consumidos)."""
        raise NotImplementedError


class OpenAIEmbedder(BaseEmbedder):
    def __init__(self, model: str):
        from openai import OpenAI

        self.client = OpenAI()
        self.model = model

    def embed(self, texts: list[str]) -> tuple[list[list[float]], int]:
        resp = self.client.embeddings.create(model=self.model, input=texts)
        vectors = [d.embedding for d in sorted(resp.data, key=lambda d: d.index)]
        return vectors, resp.usage.total_tokens


class HashEmbedder(BaseEmbedder):
    """Embedding local y determinista con n-gramas de caracteres. Sin red ni costo."""

    model = "hashing-char-ngrams"

    def __init__(self, n_features: int = 1024):
        from sklearn.feature_extraction.text import HashingVectorizer

        self.vectorizer = HashingVectorizer(
            n_features=n_features, analyzer="char_wb", ngram_range=(3, 5),
            alternate_sign=False, norm="l2", preprocessor=normalize,
        )

    def embed(self, texts: list[str]) -> tuple[list[list[float]], int]:
        matrix = self.vectorizer.transform(texts).toarray().astype(np.float32)
        return matrix.tolist(), 0


def get_embedder(settings: Settings) -> BaseEmbedder:
    if settings.provider == "fake":
        return HashEmbedder()
    return OpenAIEmbedder(settings.embedding_model)
