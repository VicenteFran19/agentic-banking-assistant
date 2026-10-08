from fastapi.testclient import TestClient

from assistant.api import app


def test_health_y_chat():
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        res = client.post("/chat", json={"message": "¿Cuál es la TREA de la cuenta de ahorros?"})
        assert res.status_code == 200
        body = res.json()
        assert body["route"] == "rag" and body["thread_id"]


def test_valida_mensaje_vacio():
    with TestClient(app) as client:
        assert client.post("/chat", json={"message": ""}).status_code == 422
