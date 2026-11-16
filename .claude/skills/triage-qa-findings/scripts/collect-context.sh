#!/usr/bin/env bash
# Lists the files changed against main and suggests --fast or --full.
# Read-only: it changes nothing.
set -euo pipefail

BASE="${1:-main}"

echo "== Changed files (git diff ${BASE}...HEAD --stat) =="
git diff "${BASE}...HEAD" --stat

CHANGED="$(git diff "${BASE}...HEAD" --name-only)"

if echo "$CHANGED" | grep -Eiq '(^|/)(Dockerfile[^/]*|docker-compose[^/]*\.ya?ml)$|(^|/)(main|app|server|entrypoint)\.(py|sh)$|health'; then
  echo
  echo "Suggested scope: --full (Docker, compose, entrypoints or /health changed)"
else
  echo
  echo "Suggested scope: --fast"
fi
