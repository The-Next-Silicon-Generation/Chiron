#!/usr/bin/env bash
# Chiron verification entry point (mirrors .github/workflows/ci.yml, CONV §3).
# Usage: bash harness/verify.sh [--fast|--full]
#   --fast (default): backend import smoke, pytest (if tests exist), compose config
#   --full:           --fast + docker builds of both images + ML image checks
# Does not install anything. Set PYTHON to choose the interpreter (default: python3, then python).
set -euo pipefail

MODE="${1:---fast}"
case "$MODE" in
  --fast|--full) ;;
  *) echo "Usage: bash harness/verify.sh [--fast|--full]" >&2; exit 2 ;;
esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1

PY="${PYTHON:-}"
if [ -z "$PY" ]; then
  if command -v python3 >/dev/null 2>&1 && python3 -c "" >/dev/null 2>&1; then PY=python3; else PY=python; fi
fi

RESULTS=()
FAILED=0
record() { # status name [note]
  RESULTS+=("$1  $2${3:+ ($3)}")
  if [ "$1" = "FAIL" ]; then FAILED=1; fi
}
run() { # name command...
  local name="$1"; shift
  echo "==> $name"
  if "$@"; then record PASS "$name"; else record FAIL "$name"; fi
}

# --- fast checks ---
run "backend import smoke (app.main:app)" "$PY" -c "from app.main import app; print(app.title)"

if find tests -name 'test_*.py' 2>/dev/null | grep -q .; then
  run "pytest tests" "$PY" -m pytest tests
else
  echo "notice: no tests/test_*.py yet; test step skipped (same as CI)."
  record SKIP "pytest tests" "no tests yet"
fi

HAVE_DOCKER=0
if command -v docker >/dev/null 2>&1; then HAVE_DOCKER=1; fi
if [ "$HAVE_DOCKER" = 1 ]; then
  run "docker compose config" docker compose config -q
else
  echo "notice: docker CLI not found; compose config skipped."
  record SKIP "docker compose config" "docker not installed"
fi

# --- full checks ---
if [ "$MODE" = "--full" ]; then
  if [ "$HAVE_DOCKER" = 1 ] && docker info >/dev/null 2>&1; then
    run "build backend image" docker build -t chiron:verify -f Dockerfile .
    run "backend image import" docker run --rm chiron:verify python -c "from app.main import app; print(app.title)"
    run "build ML image" docker build -t chiron-ml:verify -f ml_worker/Dockerfile ml_worker
    run "ML image checks (pip check, autogluon.tabular, ml_service)" \
      docker run --rm chiron-ml:verify sh -c "pip check && python -c 'import autogluon.tabular; import ml_service'"
  else
    echo "notice: no Docker daemon available; image builds and ML image checks skipped."
    for n in "build backend image" "backend image import" "build ML image" "ML image checks (pip check, autogluon.tabular, ml_service)"; do
      record SKIP "$n" "no Docker daemon"
    done
  fi
fi

echo
echo "===== verify.sh $MODE summary ====="
printf '%s\n' "${RESULTS[@]}"
if [ "$FAILED" = 1 ]; then echo "RESULT: FAIL"; exit 1; fi
echo "RESULT: PASS"
