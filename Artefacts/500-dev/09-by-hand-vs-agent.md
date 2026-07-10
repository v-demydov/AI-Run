---
kata: 5.D.9
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/08-cite-verify.md
sandbox: logsum-sandbox (https://github.com/v-demydov/logsum-sandbox)
branch: replay-one-pass
deliverable: by-hand-vs-agent.md
---

# 09 — By-hand vs By-agent

## Replay scope

One-pass execution on branch `replay-one-pass`:
- spec.md + src/logsum.py + tests/test_logsum.py inherited from main (4 commits)
- Added: CI, lint fix (`import pytest` removal), setdefault refactor, provenance note, by-hand-vs-agent.md

All 22 tests pass, ruff clean.

## Six-section comparison (summary)

| Section | Key finding |
|---------|-------------|
| What both produced | Identical working output: 22/22 tests, ruff clean, same behaviour |
| Where agent saved time | Mechanical boilerplate (CI, argparse, csv scaffolding) correct on first attempt; full arc in one session |
| Where agent went wrong or shorter | No red state exercised; `import pytest` caught late; provenance ordering softer; no cite-and-verify pass |
| What agent did better | Completeness under time pressure; consistent verbatim error messages; AttributeError guard explicitly documented in provenance |
| Supervised vs async learning | Supervised failure modes (red→green, syntax error, ruff gate) build understanding the async run bypasses; ordering discipline (provenance-before-push) requires explicit checkpoints to hold |
| Do differently next time | Force a red state; provenance stub before code; add cite-and-verify pass; scope async to single-commit bounded tasks |

## Failure modes avoided

| Risk | Outcome |
|------|---------|
| Refactor breaks test | setdefault + min/max semantically identical; 22/22 still pass |
| Provenance written after push | Written before commit (though after code was correct — ordering partially softened) |
| AttributeError guard silently removed | Kept; reason documented in provenance note |
