"""Verifica los adaptadores de OpenAI con un cliente simulado (sin red ni API key)."""
from types import SimpleNamespace

import openai

from assistant.embeddings import OpenAIEmbedder
from assistant.llm import OpenAIChat


class _FakeClient:
    def __init__(self, *args, **kwargs):
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._chat))
        self.embeddings = SimpleNamespace(create=self._embed)
        self.calls = []

    def _chat(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='{"route": "rag"}'))],
            usage=SimpleNamespace(prompt_tokens=120, completion_tokens=8),
        )

    def _embed(self, model, input):
        data = [SimpleNamespace(index=i, embedding=[0.1, 0.2]) for i in reversed(range(len(input)))]
        return SimpleNamespace(data=data, usage=SimpleNamespace(total_tokens=7))


def test_openai_chat_usa_json_mode_y_temperatura_cero(monkeypatch):
    monkeypatch.setattr(openai, "OpenAI", _FakeClient)
    llm = OpenAIChat("gpt-4o-mini")
    resp = llm.chat("sistema", "usuario", json_mode=True)
    call = llm.client.calls[0]
    assert call["temperature"] == 0 and call["response_format"] == {"type": "json_object"}
    assert (resp.input_tokens, resp.output_tokens, resp.model) == (120, 8, "gpt-4o-mini")


def test_openai_embeddings_respeta_orden_y_tokens(monkeypatch):
    monkeypatch.setattr(openai, "OpenAI", _FakeClient)
    vectors, tokens = OpenAIEmbedder("text-embedding-3-small").embed(["a", "b", "c"])
    assert len(vectors) == 3 and tokens == 7
