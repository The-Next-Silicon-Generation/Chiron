---
name: run-stack
description: Start the Chiron stack locally with Docker Compose (backend `chiron` on port 8080, ML service `autogluon`) and check that both services are healthy. Use when asked to run, start or bring up the app.
---

# Run the stack
1. From the repo root: `docker compose up -d --build` (builds both images locally from `Dockerfile` and `ml_worker/Dockerfile`).
   To use the published images instead, see the container-creation skill (`docker login ghcr.io`, `IMAGE_TAG`, `docker compose pull`).
2. Wait until both services are healthy: `docker compose ps` must show `healthy` for `autogluon` and `chiron` (`chiron` starts only after `autogluon` is healthy).
3. Check the backend: `curl http://localhost:8080/health` returns `{"status":"ok"}`.
4. Live data: websocket `ws://localhost:8080/ws/vitals`. Dashboard: open `frontend/index.html` (add `?mode=mock` for the offline demo).
5. Stop: `docker compose down`.

Ports, paths and the message contract are TEMPORARY decisions (T2, T5, T6, T7, T10, T18) recorded in `progress/T000 REPOSITORY HEAL.md`.
