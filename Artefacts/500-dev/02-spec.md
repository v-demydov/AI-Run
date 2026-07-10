---
kata: 5.D.2
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/01-claude-md.md
sandbox: logsum-sandbox (local, ~/projects/logsum-sandbox)
deliverable: spec.md (120 lines, signed off)
---

# 02 — Implementation Contract (spec.md)

## Challenge summary
If the first durable file is code, the team has no contract to check.
Write spec.md before any implementation exists.

## Eight spec questions answered

| # | Question | Decision |
|---|----------|----------|
| 1 | Exact group key | `(normalised_level, normalised_service)` — two-tuple after normalisation |
| 2 | Normalisation rules | `level`: strip + uppercase → `UNKNOWN` if not in known set; `service`: strip whitespace, preserve case |
| 3 | Count only, or first/last too? | `count` + `first_seen` + `last_seen` — time distribution is the point of log summarisation |
| 4 | Missing level | Normalise to `UNKNOWN`; keep row |
| 5 | Malformed timestamp | Skip row; warn to stderr with row number and raw value |
| 6 | Empty input | Header-only output; exit 0 |
| 7 | CLI flags + exit codes | `python -m logsum <input> [--output <path>]`; exit 0/1/2 |
| 8 | Out of scope | Date filtering, message parsing, streaming, non-CSV I/O |

## Failure modes avoided

| Risk | How avoided |
|------|-------------|
| "Group similar events" (vague key) | Exact two-tuple key named with normalisation steps |
| Edge cases absent | 8 rows in edge-case table; each maps to a specific exit or behaviour |
| Spec follows generated code | CLAUDE.md rule + explicit "no code" constraint in session |

## Fallback
`_fallbacks/02-spec-fallback.md` — pre-written spec.md if planning session
cannot be opened before implementation starts.
