"""Chiron backend API.

Minimal backend (T000 F05): FastAPI app (CONV §2) with a health probe and one
websocket endpoint for astronaut <-> server real-time streaming (CONV §1).

Websocket contract (TEMPORARY, see progress/T000 REPOSITORY HEAL.md, F28):
a client sends one JSON object per message,
    {"astronaut_id": str, "vitals": {...}, "name"?: str, "ts"?: int, "ml"?: {...}}
Valid messages are relayed unchanged to every other connected client.
Invalid messages are answered to the sender only with {"error": "..."}.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Chiron backend")

_clients: set[WebSocket] = set()


def _is_valid(message: object) -> bool:
    """Check the minimal shape of a vitals message."""
    return (
        isinstance(message, dict)
        and isinstance(message.get("astronaut_id"), str)
        and message["astronaut_id"] != ""
        and isinstance(message.get("vitals"), dict)
    )


@app.get("/health")
def health() -> dict:
    """Liveness probe."""
    return {"status": "ok"}


@app.websocket("/ws/vitals")
async def vitals(websocket: WebSocket) -> None:
    """Receive vitals messages and relay them to the other connected clients."""
    await websocket.accept()
    _clients.add(websocket)
    try:
        while True:
            try:
                message = await websocket.receive_json()
            except (ValueError, KeyError):
                # ValueError: text frame is not JSON; KeyError: binary frame.
                await websocket.send_json({"error": "invalid JSON"})
                continue
            if not _is_valid(message):
                await websocket.send_json({"error": "invalid message"})
                continue
            for client in list(_clients):
                if client is websocket:
                    continue
                try:
                    await client.send_json(message)
                except Exception:
                    _clients.discard(client)
    except WebSocketDisconnect:
        pass
    finally:
        _clients.discard(websocket)
