---
kata: 5.D.7
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/06-refactor.md
sandbox: logsum-sandbox (https://github.com/v-demydov/logsum-sandbox)
deliverables: src/logsum.py · spec.md · tests/test_logsum.py · provenance-min-count.md
pr: https://github.com/v-demydov/logsum-sandbox/pull/2
---

# 07 — Bounded Async Feature (--min-count)

## Plan (approved before execution)
1. Update spec.md §CLI + §Outputs
2. Add `min_count: int = 1` to `summarise()` and filter output
3. Add `--min-count` to `main()` argparse
4. Add 4 tests (threshold filter, explicit 1, regression no-arg, header-always)
5. Run pytest

## Changes
| File | Change |
|------|--------|
| `spec.md` | `--min-count N` in §CLI table; filter note in §Outputs |
| `src/logsum.py` | `summarise(min_count=1)` param + generator filter; `--min-count` in argparse |
| `tests/test_logsum.py` | 4 new tests; 26 total, all pass |
| `provenance-min-count.md` | Written before push; reviewed against diff |

## Provenance note check
All source files in diff matched note claims.
Only omission: `.pyc` build artefacts — acceptable.

## Plan deviation documented
Syntax error on first code attempt (`for X in Y if cond` is not loop syntax).
Corrected to generator expression before any tests ran; noted in provenance.

## Untested items (from provenance note)
- `--min-count 0` and negative values: not in spec; behaviour is defined by
  `count >= 0` always true — harmless but undocumented.
- CLI-level `--min-count` invocation: not tested; wiring is argparse pass-through
  covered by the direct `summarise()` tests.

## Failure modes avoided
| Risk | Outcome |
|------|---------|
| Task too broad | Scoped to one flag, three files, one behaviour |
| Provenance note written after review | Written before `git push`; diff checked against it |
| Default behaviour changes | Two explicit regression tests (`min_count=1` and no-arg) |
