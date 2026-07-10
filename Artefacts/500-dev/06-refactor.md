---
kata: 5.D.6
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/03-implementation.md · Artefacts/500-dev/04-tests.md
sandbox: logsum-sandbox (local + https://github.com/v-demydov/logsum-sandbox)
deliverables: src/logsum.py (refactored) · refactor-notes.md
---

# 06 — Refactor Review

## What was refactored
Group accumulation block in `summarise()` — the messiest section.
6 lines → 4 lines using `setdefault` + `min/max`.

## Every removed line examined

| Removed | Safe? | Reason |
|---------|-------|--------|
| `if key not in groups:` init guard | ✅ keep removed | `setdefault` handles first-occurrence initialisation identically |
| `groups[key] = {"count": 0, ...}` | ✅ keep removed | Folded into `setdefault` |
| `if ts < g["first_seen"]:` | ✅ keep removed | `min(g["first_seen"], ts)` is equivalent; datetime supports `<` |
| `if ts > g["last_seen"]:` | ✅ keep removed | `max(g["last_seen"], ts)` is equivalent |

## Line that was NOT removed (key finding)
`except (ValueError, AttributeError)` in `_parse_ts`.

A narrowing to `except ValueError` would break the spec's "timestamp field
absent from row" edge case: `csv.DictReader` fills short rows with `None`, so
`_parse_ts(None)` raises `AttributeError` on `None.strip()`. Without the catch,
a short row crashes instead of triggering skip+warn. Documented in refactor-notes.md.

## Test result after refactor
22 passed, 0 failed — identical to pre-refactor.

## Failure modes avoided

| Risk | Outcome |
|------|---------|
| "No behaviour change" accepted without tests | Ran full suite; all 22 passed |
| Removed guard treated as cleanup | Each removed line traced to spec requirement before approval |
| Notes skipped | refactor-notes.md records every removed line + decision |
