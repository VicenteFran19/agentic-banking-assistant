"""Clientes de LLM.

- OpenAIChat: modelo real (por defecto gpt-4o-mini).
- FakeLLM: simulador determinista para correr pruebas y CI sin API key ni costo.
  No pretende ser inteligente: solo permite validar el flujo del agente de punta a punta.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass

from .config import Settings
from .text import content_tokens, normalize


@dataclass
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    model: str


class BaseLLM:
    model: str = "base"

    def chat(self, system: str, user: str, json_mode: bool = False) -> LLMResponse:  # pragma: no cover
        raise NotImplementedError


class OpenAIChat(BaseLLM):
    def __init__(self, model: str):
        from openai import OpenAI

        self.client = OpenAI()
        self.model = model

    def chat(self, system: str, user: str, json_mode: bool = False) -> LLMResponse:
        kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            **kwargs,
        )
        usage = resp.usage
        return LLMResponse(
            text=resp.choices[0].message.content or "",
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            model=self.model,
        )


def _approx_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


class FakeLLM(BaseLLM):
    model = "fake-llm"

    SIM_WORDS = ("simula", "simular", "cuota", "cuanto pagaria", "cuanto pagare", "calcula")
    HANDOFF_WORDS = ("asesor", "persona", "humano", "fraude", "reconozco")
    OFF_TOPIC_WORDS = ("futbol", "partido", "receta", "ceviche", "politica", "clima", "chiste", "pelicula", "elecciones")
    AMBIGUOUS_WORDS = ("tasa", "tea", "trea", "plazo", "monto", "requisito", "requisitos", "comision", "interes")
    PRODUCT_WORDS = ("prestamo", "credito", "tarjeta", "membresia", "cuenta", "ahorro", "ahorros",
                     "deposito", "capital", "personal", "negocio", "hipotecario", "vehicular")

    def chat(self, system: str, user: str, json_mode: bool = False) -> LLMResponse:
        task = re.search(r"\[TASK:(\w+)\]", system)
        task = task.group(1) if task else "ANSWER"
        handler = getattr(self, f"_{task.lower()}")
        text = handler(user)
        return LLMResponse(text, _approx_tokens(system + user), _approx_tokens(text), self.model)

    # --- tareas -------------------------------------------------------------
    def _route(self, user: str) -> str:
        msg = normalize(user.split("MENSAJE:")[-1])
        history = normalize(user.split("MENSAJE:")[0])
        words = set(re.findall(r"[a-zñ]+", msg))
        history_words = set(re.findall(r"[a-zñ]+", history))
        if words & set(self.OFF_TOPIC_WORDS):
            route = "out_of_scope"
        elif words & set(self.HANDOFF_WORDS):
            route = "handoff"
        elif any(w in msg for w in self.SIM_WORDS):
            route = "simulator"
        elif words & set(self.AMBIGUOUS_WORDS) and not (words | history_words) & set(self.PRODUCT_WORDS):
            route = "clarify"
        else:
            route = "rag"
        return json.dumps({"route": route, "reason": "reglas del modo offline"})

    def _extract(self, user: str) -> str:
        text = normalize(user).replace(",", "")
        monto = re.search(r"s/\s*(\d+(?:\.\d+)?)", text)
        tea = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
        plazo = re.search(r"(-?\d+(?:\.\d+)?)\s*mes", text)
        return json.dumps({
            "monto": float(monto.group(1)) if monto else None,
            "tea": float(tea.group(1)) if tea else None,
            "plazo_meses": float(plazo.group(1)) if plazo else None,
        })

    def _answer(self, user: str) -> str:
        question = user.split("PREGUNTA:")[-1]
        context = user.split("CONTEXTO:")[-1].split("PREGUNTA:")[0]
        q_tokens = set(content_tokens(question))
        if not q_tokens:
            return "NO_INFO"
        # Abstención: si buena parte de la pregunta no aparece en el contexto, no responder.
        coverage = len(q_tokens & set(content_tokens(context))) / len(q_tokens)
        if coverage < 0.5:
            return "NO_INFO"
        best: list[tuple[float, str, str]] = []
        for block in context.split("[fuente: ")[1:]:
            source, _, body = block.partition("]")
            for sent in re.split(r"(?<=[.!?])\s+|\n", body):
                s_tokens = set(content_tokens(sent))
                if s_tokens:
                    best.append((len(q_tokens & s_tokens) / len(q_tokens), sent.strip(), source.split("|")[0].strip()))
        best.sort(key=lambda x: x[0], reverse=True)
        if not best or best[0][0] < 0.5:
            return "NO_INFO"
        chosen = [b for b in best[:2] if b[0] >= 0.34]
        sources = sorted({b[2] for b in chosen})
        return " ".join(b[1] for b in chosen) + " " + " ".join(f"[fuente: {s}]" for s in sources)

    def _judge(self, user: str) -> str:
        answer = user.split("RESPUESTA:")[-1]
        context = user.split("CONTEXTO:")[-1].split("RESPUESTA:")[0]
        a_tokens = [t for t in content_tokens(re.sub(r"\[fuente:[^\]]*\]", "", answer))]
        c_tokens = set(content_tokens(context))
        score = sum(t in c_tokens for t in a_tokens) / len(a_tokens) if a_tokens else 1.0
        return json.dumps({"faithfulness": round(score, 3), "unsupported_claims": []})


def get_llm(settings: Settings) -> BaseLLM:
    if settings.provider == "fake":
        return FakeLLM()
    return OpenAIChat(settings.chat_model)


def parse_json(text: str) -> dict:
    """Parseo tolerante: algunos modelos envuelven el JSON en ```."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.S)
        return json.loads(match.group(0)) if match else {}
