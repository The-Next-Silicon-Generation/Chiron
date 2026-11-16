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
Feedback logged: yes — `progress/LOG.md` entry "<heading>" (checked with scripts/check-log.sh)
Next owner: developer (PRODUCT_BUG) / tester (TEST_BUG, FLAKY) / orchestrator (READY, ENV_ISSUE, SPEC_UNCLEAR)
Open questions: none / list of spec contradictions
