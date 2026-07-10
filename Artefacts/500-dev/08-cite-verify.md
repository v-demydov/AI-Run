---
kata: 5.D.8
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/07-async-feature.md
sandbox: logsum-sandbox (https://github.com/v-demydov/logsum-sandbox)
deliverable: questions.md
---

# 08 — Cite and Verify

## Three questions answered with file:line citations

| Question | Key citation | Verdict |
|----------|-------------|---------|
| Where is the grouping rule? | `src/logsum.py:57` (key construction), `14–16` (normalise_level), `19–20` (normalise_service) | ✅ all correct |
| How is missing level handled? | `src/logsum.py:15–16` (strip→upper→UNKNOWN), `9` (_KNOWN_LEVELS) | ✅ all correct |
| How do I run tests and CI locally? | `CLAUDE.md:16–17` (ruff/pytest), `ci.yml:19,22,25` (pip/ruff/pytest) | ✅ all correct |

## One imprecision found and corrected
Draft cited `_normalise_service` at "line 20 only".
Actual function spans lines 19–20 (def + body). Citation corrected to `19–20`.

## Unverifiable items documented
- `spec.md §Grouping rule`: prose section heading, no stable line number.
- `csv.DictReader` behaviour for empty fields: expected `""` but not traced to CPython source.
- `.venv/` requirement: present on disk but not documented in `CLAUDE.md`.

## Failure modes avoided
| Risk | Outcome |
|------|---------|
| Citation points near claim, not at it | Each citation opened with `sed -n '<line>p'` and content matched |
| Answer cites docs but not source | All claims trace to source file line numbers, not prose docs |
| Verification skipped because answer sounds plausible | All 11 citations spot-checked before verdict written |
