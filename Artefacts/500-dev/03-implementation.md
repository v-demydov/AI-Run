---
kata: 5.D.3
date: 2026-07-10
role: developer
consumes_from: Artefacts/500-dev/02-spec.md
sandbox: logsum-sandbox (local, ~/projects/logsum-sandbox)
deliverables: src/logsum.py · data/sample_events.csv · data/summary.csv
---

# 03 — Implementation (src/logsum.py)

## What was built
`src/logsum.py` — stdlib-only CLI, implements every spec section.
Run: `python -m src.logsum <input> [--output <path>]`

## Diff-against-spec check (before run)

| Spec requirement | Verified in code |
|-----------------|-----------------|
| stdlib only | No third-party imports |
| level: strip + upper → UNKNOWN if not in set | `_normalise_level` |
| service: strip, preserve case | `_normalise_service` |
| Empty level → UNKNOWN | `"".strip().upper()` not in set → UNKNOWN |
| Malformed timestamp → skip + stderr warn with row N | `_parse_ts` returns None → WARN message |
| Missing required column → exit 1 | fieldnames check before loop |
| File not found → exit 1 | pre-check + OSError catch |
| Output not writable → exit 2 | OSError on write → return 2 |
| Sort: level asc, service asc | `sorted(groups.items())` on tuple key |
| Header always in output | `writerow(["level", ...])` unconditional |

## Sample run output
```
stderr: WARN: row 6 skipped — unparseable timestamp: "not-a-timestamp"
exit: 0
```

`summary.csv`:
```
level,service,count,first_seen,last_seen
DEBUG,order-service,1,2024-01-15T10:20:00,2024-01-15T10:20:00
ERROR,payment-service,1,2024-01-15T10:10:00,2024-01-15T10:10:00
INFO,auth-service,2,2024-01-15T10:00:00,2024-01-15T10:05:00
UNKNOWN,billing-service,1,2024-01-15T09:00:00,2024-01-15T09:00:00
WARN,auth-service,1,2024-01-15T10:15:00,2024-01-15T10:15:00
```

Sample exercises: duplicate group (INFO/auth-service ×2), empty level → UNKNOWN,
whitespace-padded level ("  WARN  "), malformed timestamp skipped.

## Implementation notes (from spec.md §Implementation notes)
- Row numbering: `enumerate(reader, start=2)` gives the correct CSV line number
  because DictReader consumes the header before the loop.
- Read-all-into-memory: streaming is out of scope; a single `groups` dict holds
  all state.
- CLI deviation: challenge run-command used two positional args; signed-off spec
  uses `--output` flag; spec took precedence.

## Failure modes avoided

| Risk | Outcome |
|------|---------|
| AI adds pandas | No third-party imports; stdlib only |
| Missing-level rows disappear | UNKNOWN group present in output |
| Sample data has no duplicate rows | INFO/auth-service appears twice in input |
