# Triage policy

Classify every failing check into exactly one category. You need positive evidence for the category you pick.

| Category | When | Evidence required | Next owner |
|---|---|---|---|
| PRODUCT_BUG | The product code behaves differently from the spec/AC | Spec or AC line + the code at `file:line` that violates it | developer |
| TEST_BUG | The test asserts something the spec does not require, or is wrongly written | Spec or AC line showing that the code's behavior is the correct one | tester |
| ENV_ISSUE | Missing dependency, port in use, Docker not running, network | The error message points to the environment, not to the code | orchestrator |
| FLAKY | It fails and passes on re-runs with no changes | Results of at least 2 runs (e.g. 1 fail / 1 pass) | tester |
| SPEC_UNCLEAR | The spec is ambiguous, or contradicts itself or the code | Quote the conflicting lines | orchestrator (Open questions) |

## Rules
- Run every failure again once before classifying it.
- A failure in a protected guarantee (4 clinical scenarios, JSON contract, referee rule, `/health`) is always a blocker, whatever its category.
- ENV_ISSUE and FLAKY still make the verdict NOT READY. Report them; don't hide them.
- If the evidence for the category is missing, use SPEC_UNCLEAR and explain what is missing.
- Never guess. Never pick a category because "the others don't fit".

## Quick signals (hints, not proof)
- `ModuleNotFoundError`, `connection refused`, `port is already allocated`, `Cannot connect to the Docker daemon` → probably ENV_ISSUE.
- `AssertionError` whose expected value matches the spec → probably PRODUCT_BUG.
- `AssertionError` whose expected value is not in the spec → check for TEST_BUG or SPEC_UNCLEAR.
- `TimeoutError` or ordering-dependent results → re-run, maybe FLAKY.

Confirm a hint with the evidence in the table before you use it.
