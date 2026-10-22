"""Configuración central leída desde variables de entorno (ver .env.example)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_dotenv() -> None:
    """Carga un .env simple sin dependencias externas (no sobreescribe variables existentes)."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.split(" #", 1)[0].strip().strip('"').strip("'")  # quita comentarios en línea
        os.environ.setdefault(key.strip(), value)


@dataclass
class Settings:
    provider: str = "openai"  # "openai" o "fake" (modo offline para pruebas y CI)
    chat_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    top_k: int = 4
    candidates: int = 10  # candidatos por retriever antes de la fusión RRF
    rrf_k: int = 60
    history_turns: int = 3
    # Precios en USD por millón de tokens. Verifica los precios vigentes de OpenAI.
    price_input_per_1m: float = 0.15
    price_output_per_1m: float = 0.60
    price_embedding_per_1m: float = 0.02
    # Orígenes permitidos para CORS (frontend). "*" permite cualquiera; en producción usa la URL de Vercel.
    allowed_origins: list[str] = field(default_factory=lambda: ["*"])
    docs_dir: Path = field(default_factory=lambda: ROOT / "data" / "docs")


def get_settings() -> Settings:
    _load_dotenv()
    env = os.environ
    return Settings(
        provider=env.get("LLM_PROVIDER", "openai").strip().lower(),
        chat_model=env.get("CHAT_MODEL", "gpt-4o-mini"),
        embedding_model=env.get("EMBEDDING_MODEL", "text-embedding-3-small"),
        top_k=int(env.get("TOP_K", "4")),
        candidates=int(env.get("CANDIDATES", "10")),
        price_input_per_1m=float(env.get("PRICE_INPUT_PER_1M", "0.15")),
        price_output_per_1m=float(env.get("PRICE_OUTPUT_PER_1M", "0.60")),
        price_embedding_per_1m=float(env.get("PRICE_EMBEDDING_PER_1M", "0.02")),
        allowed_origins=[o.strip() for o in env.get("ALLOWED_ORIGINS", "*").split(",") if o.strip()],
    )
