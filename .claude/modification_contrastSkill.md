---
name: modification_contrast
description: Security triage skill for the reviewer agent. Compares and contrasts bandit output against the developer output, the task requirements and the existing codebase. Use it at the Pre-Handoff checkpoint, or whenever the task mentions bandit, security scan, vulnerabilities or false positives.
---

# Purpose
Add a security check to the reviewer's comparison of developer output vs. requirements. Read-only: report findings, never fix them.

# Workflow
1. Receive the task, checkpoint and developer output. If the checkpoint is Pre-Schema there is no code to scan: report it and stop.
2. Search for the bandit tool dependency. If it is missing, stop and report it in the hand-off.
3. Execute bandit -r DebianConfReplication/opt/apps/Debian_VMmanager
4. Verify the output and compact the repeated threats into a summary with only 1 threat per type (keep the count and every file:line location).
5. Compare and contrast each threat against the developer output and the Acceptance Criteria, using git diff / git blame on the cited lines:
   - Introduced by this change vs. pre-existing.
   - Inside the task scope vs. scope drift.
6. Use references/triage-policy.md to guide yourself on how to categorize the threats
7. Use references/output-format.md to give the format of the response (reviewer hand-off)

# Constraints
- Do not edit the code, this is a only read skill. Bash is only for bandit and read-only git commands.
- Use the documentation mentioned above.
- Never classify a finding by elimination alone.
- If material security uncertainty remains, use DEFER instead of FALSE_POSITIVE.
- Support every finding with file:line evidence.
- If the spec or contract is unclear or contradicts the code, stop and ask. Never guess.
- Report required corrections, never implement them.