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


def test_catalogo_siempre_en_contexto_y_fuera_del_indice(assistant):
    assert assistant.retriever.overview, "el catálogo debe cargarse"
    assert all(c.source != "catalogo.md" for c in assistant.retriever.chunks)
    res = assistant.ask("¿Qué servicios tienen?", thread_id="t-cat")
    assert "catalogo.md" in {r["source"] for r in res["retrieved"]}


def test_operaciones_se_recuperan():
    from assistant.config import get_settings
    from assistant.embeddings import get_embedder
    from assistant.ingest import load_documents
    from assistant.retriever import HybridRetriever

    settings = get_settings()
    retriever = HybridRetriever(load_documents(settings.docs_dir), get_embedder(settings))
    results, _ = retriever.search("transferir a otro banco desde la app, ¿cuánto cuesta?", k=4)
    assert "operaciones.md" in {r.chunk.source for r in results}


def test_abstencion_mide_comportamiento_no_frase():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
    from run_eval import declines_without_inventing

    assert declines_without_inventing("Banco Andino no ofrece crédito hipotecario. Sí tenemos Préstamo Personal.")
    assert not declines_without_inventing("No ofrecemos hipotecario, pero la TEA sería 12%.")
    assert not declines_without_inventing("El crédito hipotecario tiene una TEA de 9%.")
