# T0xx <Name>
Phase: <alpha / beta / ...>. <One line: what this task is, and what it is not.>
Agents: <agent> (<role in this task>), ... (only agents that exist in .claude/agents/)
Source of truth: docs/architecture/ARCHITECTURE.md and docs/conventions/CONVENTIONS.md. Sections that apply: <ARCH §x, CONV §x>.
Orchestrator: <who takes the orchestrator role>. It follows this task file, delegates to the agents and passes handoffs between them. It never writes or fixes code itself.
CLAUDE.md: <read / skip, and why>.
Progress file: progress/<same name as this task file> (CONV §4).

## Goal
<One or two lines.>

## Scope
- <Files / areas the agents may change.>

## Out of scope
- <What must not be touched in this task; related tasks or findings.>

## Acceptance criteria
Every agent handoff cites these AC ids.
- AC01: <verifiable criterion> · Doc reference: <ARCH §x / CONV §x / none>
- AC02: <...> · Doc reference: <...>

## Steps
1. <Step> (<agent>) · handoff to: <agent / orchestrator>
2. <Step> (<agent>) · handoff to: <...>
Stop for human approval at: <step / none>.

## Rules
- Do not edit ARCHITECTURE.md, CONVENTIONS.md or CLAUDE.md, unless this task is explicitly about them and the human approved it; otherwise propose changes in the progress file.
- A case the docs do not cover is logged as doc-gap, never decided silently.
- <Task-specific rules.>

## Progress file format
# T0xx — <Name> — YYYY-MM-DD
## <Task-specific sections, e.g. Findings / Decisions>
## Fix log
- <AC or finding id> · round N · developer: <what changed> · reviewer: AUTHORIZED / REJECTED — <reasons>
## QA feedback
- YYYY-MM-DD · <AC ids> · qa: READY / NOT READY — <summary; bugs B0xx>
(qa appends entries only under this heading, newest last, and never edits other sections.)
## Summary
<Counts, e.g. AC passed: N/N · review rounds: N>
