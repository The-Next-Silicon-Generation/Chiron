# Output format

QA returns feedback in two places:

1. **`progress/LOG.md`**: append one entry per QA run using `templates/log-entry.md`. This is the permanent record.
2. **Handoff to the orchestrator**: the final message, using `templates/handoff.md`.

Both must match: the same verdict, the same bug ids and the same next owner.

## Bug ids
- Format `B0xx`, numbered after the highest id already in `progress/LOG.md`.
- One id per distinct failure. If the same root cause makes several tests fail, use one bug and list the tests.

## Field rules
- **Repro**: a command that can be copied and run, e.g. `pytest chiron/tests/test_api.py::test_health -x`.
- **Expected**: what the spec or AC says, with its id when there is one.
- **Actual**: at most 5 relevant output lines, not the whole log.
- **Location**: `file:line` in product code for a PRODUCT_BUG, in the test for a TEST_BUG.

## Routing
- Every check is PASS → READY, next owner is the orchestrator.
- At least one PRODUCT_BUG → NOT READY, next owner is the developer.
- Only TEST_BUG / FLAKY → NOT READY, next owner is the tester.
- Only ENV_ISSUE / SPEC_UNCLEAR → NOT READY, next owner is the orchestrator.
