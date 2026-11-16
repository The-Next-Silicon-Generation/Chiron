# Chiron

Chiron is a health solution for astronauts living on the space station: it lets the crew measure their vital signs and alerts when an anomaly is detected. It runs as microservices in Docker images, routed by Docker Compose on an Ubuntu host.

- Architecture: [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- Conventions: [docs/conventions/CONVENTIONS.md](docs/conventions/CONVENTIONS.md)

## Project status — NASA Space Apps Challenge submission

**Challenge:** *Create Health Monitoring Software for Astronauts on Space Missions.*

This repository is the state of Chiron at the hackathon deadline. The team built it with Spec-Driven Development (SDD): the specs came first, and agents and people write code from them.

**What was delivered**
- **The full SDD foundation:** architecture ([ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)), conventions ([CONVENTIONS.md](docs/conventions/CONVENTIONS.md)), [CLAUDE.md](CLAUDE.md) with the glossary and acceptance criteria, the agent harness in `.claude/` (developer, reviewer, tester, QA, plus skills and a guard hook), and the task and progress log in `tasks/` and `progress/`.
- **Backend skeleton** (`app/`, FastAPI): health probe and the `/ws/vitals` websocket that checks and relays vitals messages.
- **ML service skeleton** (`ml_worker/`): health probe and the mount point for the trained model. It does not serve predictions yet.
- **Monitoring dashboard** (`frontend/`): crew selector, vital-sign charts and the triage classifier view, running on simulated data.
- **Infrastructure:** Docker images, Docker Compose, tests, and CI/CD that publishes the images to GHCR.

**What is not finished**
- **Because of the time we had, the frontend could not be connected to the backend.** The dashboard shows simulated data; the full pipeline (vitals stream → backend → predictive model → triage → dashboard) is not wired end to end. This repository is as far as we could get in the time available.
- The predictive model works, and NEWS2, the backend triage and the contextual model are still specs only.

**Development after the deadline**
Work continues in a separate branch, where the backend is being developed until it works. **That branch will not be merged into `main`**, so that this submission stays as it was at the deadline and follows the hackathon rules.

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
