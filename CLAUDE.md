# Chirón
 
> Foundation file for every agent and every human on the team.
> Read it fully before touching any spec or code.
> if a spec conflicts with code, **the spec wins** and the code is wrong.
 
## Goal
 
Chiron its a health solutions provided to astronauts who lives on the 
space station.To get a more extended view of the main project consult;

`docs/architectures/ARCHITECTURES.md`
 

## Architecture

An a hybrid model of fusioning Machine learning with deterministic software, all this on a
micro-services layout.
 
## Repo layout
 
```
harness/
  CLAUDE.md                        The initial route for guidance
  docs/                            Where the specs lives
    architecture/ARCHITECTURE.md   The explaination of how the code is built.
    conventions/CONVENTIONS.md     The conventions agreed to use on the project
.claude/agents/                    one file per agent
    developer.md                   An agent for development task
    reviewer                       An agent dedicated to contrast the SDD vs the agent code writed
    tester                         An agent that builds the test from the produced code
    qa                             An agent that runs the test and gives feedback of the results
.claude/skills                     The folder for full skills maded from
    triage-qa-findings/            An skill for giving a human view of the findings (preferred qa skill)
    modification-contrast/         An skill for contrast the real code vs what the agents do (preferred reviewer skill)
app/                               backend-core service (Python, FastAPI)
vital_ml/                          The predictive model (see architecture.md)
tasks/                             The main to do list for the objective accomplish
progress/                          The full log decisions per task (see conventions.md)
frontend/                          Frontend-core monitor view
compose.yaml                       Runtime containers
.github/workflows/                 CI an CD workflow

```
 
## Agents:

When the task needs to build code: Use developer agent
When the task needs to build the test code: Use tester
When the task has built code always: Use reviewer with it skill
When the task have the full test code: Use QA with it skill
 
# Acceptance criteria
A task is done when **all** of these hold:
 
- [ ] The acceptance criteria it claims have tests, and they pass.
- [ ] Lint and all tests of that component pass
- [ ] Message formats match the contract field by field.
- [ ] `reviewer` approved and a person merged.
## Glossary
 
| Term | Meaning |
|---|---|
| Vitals | `hr` (bpm), `spo2` (%), `sbp` (mmHg), `resp` (breaths/min, **not** the EKG R-R interval), `temp` (°C) |
| Window (W) | last 300 s of 1 Hz readings the model reads |
| Horizon (H) | the 120 s the model predicts |
| Baseline | the astronaut's personal reference: median of the first 120 s, or set by the flight surgeon |
| Delta | change between the start of the window and the end of the forecast, relative to baseline. Calculated, not learned |
| Danger score | delta projected onto the vital's dangerous direction (e.g. SpO2 falling) |
| Zones | `normal` / `watch` / `alert`, with persistence (N steps) and hysteresis |
| Confidence | from the width of the p10–p90 forecast band; below 0.8 → defer to NEWS2 |
| NEWS2 | deterministic early-warning score; the safety net that works without ML |
| Warm-up | first ~300 s per astronaut, no predictions yet |
| Safe mode | NEWS2-only operation when ML is unavailable |
| Shock index | HR / SBP; its delta flags crossed trends (HR up while SBP down) |
| [FILL] | [FILL: any team term agents keep getting wrong] |
