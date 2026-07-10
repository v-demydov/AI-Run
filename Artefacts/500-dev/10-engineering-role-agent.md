---
kata: K5.3
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/09-by-hand-vs-agent.md
sandbox: logsum-sandbox (https://github.com/v-demydov/logsum-sandbox)
branch: replay-one-pass
deliverables: .claude/skills/engineering/SKILL.md · context/ · sessions/kata-5.3/ · reviews/replay-one-pass/
---

# K5.3 — Engineering Role-Agent

## What was built

A runnable Engineering Skill (`engineering-logsum`) that turns a spec into a PR
evidence chain — context bundle, independent tests (isolation tier recorded), seven-lens
review with adversarial pass, and PR provenance block.

## Skill structure (9 steps complete)

| Step | Content |
|------|---------|
| 1 — Name | `engineering-logsum` · Skill shape (team reaches for playbook) |
| 2 — Description | names input/output file paths; ends "NOT for architecture decisions, scope calls, or the merge button" |
| 3 — Role/goal/tools | stdlib + ruff + pytest; no external APIs; no prod data |
| 4 — Decision rules | 6 DO/DON'T rows (countable); 6 escalation conditions; 5 stop-and-ask triggers |
| 5 — Evals | 3 rows: AC coverage, guardrail refusal, ruff gate before verdict |
| 6 — Routing | 3/3 correct: context-bundle task ✓ · independent-tests task ✓ · architecture fork → escalated ✓ |
| 7 — Real run | spec.md → context/ + sessions/ + reviews/ + PR provenance block; all 9 ACs covered |
| 8 — Fix one thing | added stdlib escalation gate (missing in first draft — would let a numpy import through) |
| 9 — Run-log | embedded in SKILL.md §Run-log |

## Evidence chain produced

| File | Purpose |
|------|---------|
| `.claude/skills/engineering/SKILL.md` | The agent |
| `context/warm-reference.md` | Warm layer: repo layout, key invariants, test conventions |
| `context/cold-gaps.md` | Cold layer: 4 documented gaps (venv, min-count, CI, import note) |
| `sessions/kata-5.3/session-log.md` | Session: ruff clean, 22/22, tier B, 9 ACs covered, guardrail test |
| `reviews/replay-one-pass/review.md` | Seven-lens + adversarial: no blockers; 4 adversarial inputs tested |

## Seven-lens verdict

| Lens | Finding |
|------|---------|
| Correctness | none |
| Security | none applicable |
| Error handling | none |
| Performance | none applicable |
| Observability | none |
| Maintainability | minor: bare `dict` type hint (not a blocker) |
| Spec compliance | G-2 gap noted (--min-count absent from main); not a branch violation |

Adversarial pass: 4 inputs (all-empty row, short row, misspelled header column, whitespace-only service) — all handled per spec.

## Failure modes avoided

| Risk | Outcome |
|------|---------|
| Description too generic → wrong routing | Named exact file paths in description; 3/3 routing correct |
| Eval criteria not countable | Every row has a number (≥1 per AC, 0 uncovered, 7 lenses) |
| Guardrail fires but no log entry | Session log explicitly records escalation of hard input |
| Fix not recorded | Step 8 before/after: added stdlib escalation gate |
| Run-log absent | Embedded in SKILL.md; reproduced in this artefact |
