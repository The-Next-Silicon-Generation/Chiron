"""Chiron ML (anomaly detection) service.

Minimal service skeleton (T000 F04): it only exposes a health probe.
Trained AutoGluon model artifacts are mounted read-only at MODEL_PATH.
"""

import os
from pathlib import Path

from fastapi import FastAPI

MODEL_PATH = Path(os.environ.get("MODEL_PATH", "/app/AutogluonModels"))

app = FastAPI(title="Chiron ML service")


@app.get("/health")
def health() -> dict:
    """Report liveness and whether model artifacts are present."""
    model_present = MODEL_PATH.is_dir() and any(MODEL_PATH.iterdir())
    return {"status": "ok", "model_present": model_present}
