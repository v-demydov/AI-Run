---
kata: 5.D.4
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/02-spec.md · Artefacts/500-dev/03-implementation.md
sandbox: logsum-sandbox (local, ~/projects/logsum-sandbox)
deliverables: tests/test_logsum.py · test-notes.md
---

# 04 — Spec-First Tests

## Isolation method
Tests written from spec.md only — src/logsum.py not read.
This means test failures can reveal spec violations, not just implementation typos.

## Result
22 passed, 0 failed.

## Coverage map (spec section → test count)

| Spec section | Tests |
|-------------|-------|
| §Grouping rule | 3 (same group merge, different services, whitespace-service same group) |
| §Aggregation | 3 (count, first_seen min, last_seen max) |
| §Normalisation — level | 3 (lowercase, whitespace, nonstandard → UNKNOWN) |
| §Normalisation — service | 1 (strip + preserve case) |
| §Edge cases — level | 3 (empty, whitespace-only, nonstandard) |
| §Edge cases — timestamp | 3 (row skipped, warning on stderr, row number in warning) |
| §Edge cases — empty/missing | 3 (header-only, file not found, missing column) |
| §Outputs sort order | 2 (level asc, service asc) |
| §CLI | 2 (exit 0 valid, exit 1 bad file) |

## Decision record (from test-notes.md)
**Test:** `test_malformed_timestamp_warning_includes_row_number`

Spec says `WARN: row <N>`. N could be data-row count or CSV line number.
Decision: N = CSV file line number (header = 1) — matches what a text editor
shows. Test asserts `"3" in err` for a bad row at file line 3.
Outcome: implementation agreed; test passed. If `start=1` had been used
instead of `start=2`, the warning would say "row 2" and the test would fail —
the spec violation would have been caught.

## Failure modes avoided

| Risk | Outcome |
|------|---------|
| Test names helpers not in spec (peeked at code) | All test targets derived from spec text only |
| All tests pass but miss hardest edge case | Added row-number precision test and whitespace-service-grouping test |
| AI weakens a failing test | No failures to weaken; all passed first run |
