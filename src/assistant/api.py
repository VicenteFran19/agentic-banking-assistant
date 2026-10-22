"""API REST con FastAPI. Ejecutar: uvicorn assistant.api:app --app-dir src --reload"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .service import Assistant
from .config import get_settings

state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["assistant"] = Assistant()
    yield
    state.clear()


app = FastAPI(title="Agentic Banking Assistant", version="1.0.0", lifespan=lifespan)

# CORS: permite que el frontend (p. ej. en Vercel) llame a la API desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    thread_id: str | None = None


class ChatResponse(BaseModel):
    thread_id: str
    answer: str
    route: str
    sources: list[str]
    pii_masked: bool
    cost_usd: float
    latency_ms: float


@app.get("/health")
def health() -> dict:
    a = state["assistant"]
    return {"status": "ok", "provider": a.settings.provider, "chunks": len(a.chunks)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> dict:
    return state["assistant"].ask(req.message, req.thread_id)
