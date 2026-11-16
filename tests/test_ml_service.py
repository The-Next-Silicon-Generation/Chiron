"""ML service tests (ml_worker/ml_service.py): /health with and without model artifacts (T4, T5)."""

import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ML_WORKER = Path(__file__).resolve().parents[1] / "ml_worker"


def load_service(monkeypatch, model_path):
    monkeypatch.setenv("MODEL_PATH", str(model_path))
    monkeypatch.syspath_prepend(str(ML_WORKER))
    sys.modules.pop("ml_service", None)
    return importlib.import_module("ml_service")


def test_health_without_model(monkeypatch, tmp_path):
    service = load_service(monkeypatch, tmp_path)
    response = TestClient(service.app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_present": False}


def test_health_with_model(monkeypatch, tmp_path):
    (tmp_path / "predictor.pkl").write_bytes(b"x")
    service = load_service(monkeypatch, tmp_path)
    response = TestClient(service.app).get("/health")
    assert response.json() == {"status": "ok", "model_present": True}
