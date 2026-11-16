name: triage-qa-findings
description: QA workflow to run the tester's tests, triage every failure, log the feedback in progress/LOG.md and return a READY / NOT READY handoff to the orchestrator.
---

# Workflow

## Obtain the feedback
1. Read the task file `tasks/T0xx.md` to get its acceptance criteria (AC ids) and read the tester's instructions to know which tests to run. If either is missing or contradicts the code, stop and ask.
2. Run `git diff main...HEAD --stat` to see the changed files and pick the scope:
   - `--fast` by default.
   - `--full` when Dockerfiles, `docker-compose.yaml`, service entrypoints or `/health` routes changed.
   Write down why you picked it.
3. Execute `bash harness/verify.sh --fast` (or `--full`) and keep the raw output.
4. Group the results by suite: tests (root), `vitals_ml/tests`, `chiron/tests`, docker-compose validity, stack `/health` (only with `--full`). Mark each one PASS / FAIL / SKIPPED (with a reason).
5. For every FAIL:
   - Re-run only that test once to rule out flakiness.
   - Find the code location (`file:line`) from the traceback.
   - Keep the 5 most relevant output lines.
6. Use `references/triage-policy.md` to classify each failure.
7. Check every AC id of the task against the results, including the protected guarantees (4 clinical scenarios, JSON contract, referee rule, services answer `/health`).

## Return the feedback
8. Append an entry to `progress/LOG.md` following `references/output-format.md` (LOG entry section).
9. Re-read `progress/LOG.md` and confirm the entry is there. If it isn't, write it again before continuing.
10. Return the handoff to the orchestrator following `references/output-format.md` (Handoff section).

# Constraints

- This skill only reads code. Never edit product code or tests. The only file you may write is `progress/LOG.md`.
- Never create tests. Only run the ones the tester gave you.
- Never mark a check PASS without running it. Anything you didn't run is SKIPPED, with a reason.
- Every bug needs a repro command, the expected result, the actual result and `file:line`. Otherwise it is not a valid report.
- Never classify a failure by elimination alone.
- If it's still unclear whether the code or the test is wrong, use SPEC_UNCLEAR, not TEST_BUG.
- READY only if every check is PASS.

.claude/skills/qa-feedback/references/triage-policy.md
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

.claude/skills/qa-feedback/references/output-format.md
# Output format

## 1. LOG entry (append to `progress/LOG.md`)

```
## YYYY-MM-DD — QA of T0xx — <one-line subject>
Verdict: READY / NOT READY
Command: `bash harness/verify.sh --fast|--full` (<why>)
Bugs:
- B0xx [CATEGORY] <test name>
  - Repro: `<command>`
  - Expected: <...>
  - Actual: <5 most relevant output lines>
  - Location: `file:line`
Next owner: developer / tester / orchestrator
```

If there are no bugs, write `Bugs: none`.

## 2. Handoff (returned to the orchestrator)

```
Task: T0xx (QA of T0xx — <what was verified>)
Verdict: READY / NOT READY
Command run: `bash harness/verify.sh --fast|--full` (<why --full was or wasn't needed>)
Results:
- tests (root): PASS / FAIL / SKIPPED (reason)
- vitals_ml/tests: PASS / FAIL / SKIPPED (reason)
- chiron/tests: PASS / FAIL / SKIPPED (reason)
- docker-compose.yaml is valid: PASS / FAIL / SKIPPED (reason)
- stack /health (only with --full): PASS / FAIL / SKIPPED (reason)
Files: <output of `git diff main...HEAD --stat`> + `progress/LOG.md`
Bugs: none / list
- B0xx [CATEGORY] <test name> — Repro: <command> · Expected: <...> · Actual: <...> · Location: `file:line`
Acceptance:
- AC1: PASS / FAIL
- ...
- Protected guarantees (4 clinical scenarios, JSON contract, referee rule, /health): PASS / FAIL
Feedback logged: yes — `progress/LOG.md` entry "<heading>" (re-read and confirmed)
Next owner: developer (PRODUCT_BUG) / tester (TEST_BUG, FLAKY) / orchestrator (READY, ENV_ISSUE, SPEC_UNCLEAR)
Open questions: none / list of spec contradictions
```

## Routing
- Every check is PASS → READY, next owner is the orchestrator.
- At least one PRODUCT_BUG → NOT READY, next owner is the developer.
- Only TEST_BUG / FLAKY → NOT READY, next owner is the tester.
- Only ENV_ISSUE / SPEC_UNCLEAR → NOT READY, next owner is the orchestrator.

Once the skill is in place, you can cut the Workflow and Handoff sections in Q&A.md down to one line: "Follow the qa-feedback skill." That keeps the procedure in one place.