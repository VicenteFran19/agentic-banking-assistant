import pytest

from assistant.config import get_settings
from assistant.ingest import load_documents


def test_chunks_tienen_fuente_y_seccion():
    chunks = load_documents(get_settings().docs_dir)
    assert len(chunks) > 10
    assert all(c.source.endswith(".md") and c.section for c in chunks)
    assert all("Datos ficticios" not in c.text for c in chunks)  # el disclaimer no se indexa


@pytest.mark.parametrize("query,expected", [
    ("monto máximo del préstamo de capital de trabajo", "prestamo_capital_trabajo.md"),
    ("membresía anual de la tarjeta", "tarjeta_credito.md"),
    ("TREA del depósito a 360 días", "deposito_plazo.md"),
    ("horario de agencias los sábados", "canales_y_reclamos.md"),
])
def test_recuperacion_hibrida(assistant, query, expected):
    results, _ = assistant.retriever.search(query, k=4)
    assert expected in [r.chunk.source for r in results]
    assert all(r.vector_rank or r.bm25_rank for r in results)
