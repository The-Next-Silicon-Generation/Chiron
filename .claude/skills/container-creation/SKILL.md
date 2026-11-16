---
name: container-creation
description: The workflow to publish Chiron container images to GitHub Container Registry (GHCR) and to pull them. Use when asked how images are built, tagged, published or pulled.
---

# Workflow
1. Images are published by CI/CD, not by hand: a push to `main` runs `.github/workflows/ci.yml` (tests and image builds); when it succeeds, `.github/workflows/cd.yml` builds and pushes both images using `GITHUB_TOKEN`.
2. Image names: `ghcr.io/the-next-silicon-generation/chiron` (backend, root `Dockerfile`) and `ghcr.io/the-next-silicon-generation/chiron-ml` (ML service, `ml_worker/Dockerfile`).
3. Tags: `sha-<full commit sha>` (never changes) and `latest` (moves); published only from `main`.
4. Packages are private: run `docker login ghcr.io` (GitHub user + a token with `read:packages`) before pulling.
5. Use a published image with compose: `export IMAGE_TAG=sha-<full commit sha>`, then `docker compose pull`, then `docker compose up -d` (without IMAGE_TAG the tag is `latest`).
6. Do not run `docker compose push` by hand: it would overwrite the `latest` images published by CD.

Names and tags are TEMPORARY decisions (T11, T12, T21; private packages = human decision 6) recorded in `progress/T000 REPOSITORY HEAL.md`.
