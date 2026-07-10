---
kata: 5.D.1
date: 2026-07-10
role: developer
consumes_from: Artefacts/300-design/06-spec.md · Artefacts/400-arch/05-patterns.md · Artefacts/400-arch/06-nfrs.md
sandbox: logsum-sandbox (local, ~/projects/logsum-sandbox)
deliverables: CLAUDE.md · context-load-check.md
---

# 01 — Repo Context File (CLAUDE.md)

## Challenge summary
An AI coding session without repo rules starts from guesses. The first engineering
move is to write the small context file the agent sees every time, then prove it
loaded that file.

## What was done
Created `logsum-sandbox` as a standalone local git repo. Wrote `CLAUDE.md` at repo
root from the brief below — 22 lines, four sections, no invented frameworks.

## CLAUDE.md brief
- **Project context**: tiny CLI that summarises synthetic `events.csv` logs.
- **Conventions**: code in `src/`, tests in `tests/`, data in `data/`.
- **Utilities to prefer**: Python 3.11 stdlib, `ruff`, `pytest`.
- **Escalation gates**: stop before dependencies; synthetic data only;
  never overwrite `spec.md` after sign-off without asking.

## Verification (step 4)
Fresh-session simulation: read CLAUDE.md, summarised each section by name,
cited the filename. Result saved in `logsum-sandbox/context-load-check.md`.

## Line count
22 / 30 max.

## Failure modes avoided
| Risk | How avoided |
|------|-------------|
| Rule file in wrong folder | Placed at repo root, not in `src/` or `docs/` |
| File grows into a stack guide | Stack detail deferred to later docs |
| AI invents FastAPI / pandas / cloud | No dependencies outside stdlib + ruff + pytest |

## Fallback
`_fallbacks/01-claude-md-fallback.md` — pre-written CLAUDE.md if sandbox
creation is blocked (no git, no write access).
