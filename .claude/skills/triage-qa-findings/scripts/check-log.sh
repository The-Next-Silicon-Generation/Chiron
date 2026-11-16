#!/usr/bin/env bash
# Checks that progress/LOG.md has a complete QA entry for the given task.
# Usage: check-log.sh T0xx [path/to/LOG.md]
set -uo pipefail

TASK="${1:?usage: check-log.sh T0xx [LOG.md]}"
LOG="${2:-progress/LOG.md}"

[ -f "$LOG" ] || { echo "FAIL: $LOG not found"; exit 1; }

# Take the last entry for this task: from its heading to the next "## " heading.
LAST_START="$(grep -n "^## .*QA of ${TASK}" "$LOG" | tail -1 | cut -d: -f1)"
[ -n "$LAST_START" ] || { echo "FAIL: no '## ... QA of ${TASK}' entry in $LOG"; exit 1; }
ENTRY="$(tail -n +"$LAST_START" "$LOG" | awk 'NR>1 && /^## /{exit} {print}')"

status=0
for field in "Verdict:" "Command:" "Bugs:" "Next owner:"; do
  if ! grep -q "^${field}" <<<"$ENTRY"; then
    echo "FAIL: missing '${field}'"
    status=1
  fi
done

if grep -q "^Verdict: NOT READY" <<<"$ENTRY"; then
  for field in "Repro:" "Expected:" "Actual:" "Location:"; do
    if ! grep -q "${field}" <<<"$ENTRY"; then
      echo "FAIL: NOT READY entry has no '${field}' on its bugs"
      status=1
    fi
  done
fi

if grep -Eq '<[^>]+>|T0xx|B0xx|YYYY-MM-DD' <<<"$ENTRY"; then
  echo "FAIL: template placeholders still in the entry"
  status=1
fi

[ $status -eq 0 ] && echo "OK: entry for ${TASK} found and complete (line ${LAST_START})"
exit $status
