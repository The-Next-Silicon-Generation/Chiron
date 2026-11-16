# Chiron

Chiron is a health solution for astronauts living on the space station: it lets the crew measure their vital signs and alerts when an anomaly is detected. It runs as microservices in Docker images, routed by Docker Compose on an Ubuntu host.

- Architecture: [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- Conventions: [docs/conventions/CONVENTIONS.md](docs/conventions/CONVENTIONS.md)

Ports, paths, image names and the message contract below are TEMPORARY decisions (T1-T22) recorded in [progress/T000 REPOSITORY HEAL.md](progress/T000%20REPOSITORY%20HEAL.md) until the docs define them.

## Run
1. `docker compose up -d --build` (backend `chiron` + ML service `autogluon`).
2. `docker compose ps` until both services are `healthy`.
3. Backend health: `curl http://localhost:8080/health` returns `{"status":"ok"}`.
4. Live data: websocket `ws://localhost:8080/ws/vitals`. Dashboard: open `frontend/index.html` (add `?mode=mock` for the offline demo).
5. The ML service is not published to the host (port 8001 is internal); reach it with `docker compose exec autogluon ...`.
6. Stop: `docker compose down`.

## Verify
- `bash harness/verify.sh --fast` (import smoke, tests, compose config) or `--full` (adds image builds; needs a Docker daemon).
- Tests only: `pip install -r requirements.txt -r requirements-dev.txt`, then `python -m pytest tests`.

## Images (GHCR)
- CI/CD publishes `ghcr.io/the-next-silicon-generation/chiron` and `ghcr.io/the-next-silicon-generation/chiron-ml` from `main` (tags `sha-<full commit sha>` and `latest`).
- Packages are private: `docker login ghcr.io` first, then `export IMAGE_TAG=sha-<full commit sha>`, `docker compose pull`, `docker compose up -d`.
- Do not run `docker compose push` by hand: it would overwrite the images published by CD.
