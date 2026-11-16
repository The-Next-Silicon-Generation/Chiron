Phase: alpha. An audit of the project, not a feature build.
Agents: developer (audits and fixes), reviewer (evaluates the developer).
Source of truth: docs/architecture/ARCHITECTURE.md and docs/conventions/CONVENTIONS.md. Every finding and every fix is judged against them.
Orchestrator: not built yet but assume it will exist later. In this task the main console session takes its role: it follows this task file, delegates to the agents and passes handoffs between them. It never writes or fixes code itself.
CLAUDE.md: not written yet, so skip it (agents too). Use this task, ARCHITECTURE and CONVENTIONS as guidance.
Report: progress/T000 REPOSITORY HEAL.md.
1. Audit (developer)
Review the whole repository and list every failure or weakness:
Contradicts ARCHITECTURE or CONVENTIONS (stack, API type, services, Docker/compose, CI/CD).
Broken: config that does not run, missing or empty files, wrong paths or references.
Weak: incomplete harness files (agents, skills, hooks, task template), security issues. The missing orchestrator and the empty CLAUDE.md are expected at this stage: do not report them. Write every finding in the report, then stop for human approval of the list.
2. Fix loop (one approved finding at a time)
developer fixes the finding and hands off: finding id, files changed, how it now matches the docs.
The console (as orchestrator) sends the handoff to reviewer.
reviewer evaluates the fix and the developer's work . AUTHORIZED / REJECTED with reasons.
if REJECTED  developer redoes the fix using the reviewer's reasons . back to step 2.
Repeat until AUTHORIZED. Only then move to the next finding.
Reviewer criteria
The fix solves the finding and matches ARCHITECTURE and CONVENTIONS.
No changes outside the finding's scope and no new features.
The developer followed its own workflow and handoff template.
Rules
The reviewer never modifies anything the developer produced: it only evaluates, explains and writes its own report lines.
No new features in this task. A finding that needs one is marked DEFERRED.
A case the docs do not cover is logged as doc-gap, never decided silently.
Do not edit ARCHITECTURE.md, CONVENTIONS.md or CLAUDE.md; propose changes in the report.
Report format (progress/T000 REPOSITORY HEAL.md)
# T000 — Alpha audit report — YYYY-MM-DD
## Findings
| ID | Severity | Type | File | Doc reference | Description | Status |
| F01 | blocker/major/minor | failure/weakness/doc-gap | <path> | ARCH §x / CONV §x | ... | open/fixed/deferred |
## Fix log
- F01 · round 1 · developer: <what changed> · reviewer: REJECTED — <reasons>
- F01 · round 2 · developer: <what changed> · reviewer: AUTHORIZED
## Summary
Findings: N · fixed: N · deferred: N · review rounds: N