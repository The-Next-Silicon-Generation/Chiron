---
name: run-tests
description: Run the Chiron verification script (the same checks as CI). Use when asked to test or verify the repository.
---

# Run the checks
1. `bash harness/verify.sh --fast` (default; works from any directory): backend import smoke, `pytest tests` if `tests/test_*.py` exist, `docker compose config -q`.
2. `bash harness/verify.sh --full`: everything in `--fast` plus both image builds and the ML image checks (`pip check`, `import autogluon.tabular`, `import ml_service`). Needs a running Docker daemon; without one those checks are SKIPPED.
3. The script installs nothing: the backend dependencies (`requirements.txt`) must already be installed. Choose the interpreter with `PYTHON=<path>`.
4. Read the summary: any FAIL makes the script exit 1. Report every SKIP together with its reason.
