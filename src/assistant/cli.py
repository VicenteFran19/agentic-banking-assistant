"""Chat interactivo en terminal: python -m assistant.cli (desde src/) o `make chat`."""
from __future__ import annotations

import uuid

from .service import Assistant


def main() -> None:
    assistant = Assistant()
    thread_id = uuid.uuid4().hex
    print(f"Asistente Banco Andino (demo) · proveedor: {assistant.settings.provider} · escribe 'salir' para terminar\n")
    while True:
        try:
            message = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if message.lower() in {"salir", "exit", "quit"}:
            break
        if not message:
            continue
        res = assistant.ask(message, thread_id)
        print(f"\nAsistente [{res['route']}]: {res['answer']}")
        print(f"   ↳ fuentes: {res['sources'] or '-'} · costo: ${res['cost_usd']:.6f} · {res['latency_ms']} ms\n")


if __name__ == "__main__":
    main()
