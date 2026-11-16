"""Backend tests (app/main.py): /health and the /ws/vitals relay (T6, T7, T9, T10)."""

from fastapi.testclient import TestClient

from app.main import app

VALID = {
    "astronaut_id": "A-01",
    "name": "Ares",
    "ts": 1731700000000,
    "vitals": {"spo2": 97, "hr": 74, "rr": 16, "urine": 52, "bv": 98},
}


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_message_is_relayed_to_other_client():
    client = TestClient(app)
    with client.websocket_connect("/ws/vitals") as viewer, client.websocket_connect("/ws/vitals") as sender:
        sender.send_json(VALID)
        assert viewer.receive_json() == VALID


def test_non_json_text_is_rejected():
    with TestClient(app).websocket_connect("/ws/vitals") as ws:
        ws.send_text("not json")
        assert ws.receive_json() == {"error": "invalid JSON"}


def test_binary_frame_is_rejected():
    with TestClient(app).websocket_connect("/ws/vitals") as ws:
        ws.send_bytes(b"\x00")
        assert ws.receive_json() == {"error": "invalid JSON"}


def test_invalid_shapes_are_rejected_and_connection_stays_open():
    with TestClient(app).websocket_connect("/ws/vitals") as ws:
        for bad in ({"vitals": {}}, {"astronaut_id": "", "vitals": {}}, {"astronaut_id": "A-01"}, [VALID]):
            ws.send_json(bad)
            assert ws.receive_json() == {"error": "invalid message"}
