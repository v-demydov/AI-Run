---
fallback-for: 02-spec.md
use-when: planning session cannot be opened before implementation starts; paste
          this into the session and ask the AI to verify it matches the repo.
---

# Fallback — spec.md for logsum-sandbox

If the AI has already written code, stop. Open a fresh session, paste this
file, and say: "Treat this as the signed-off spec. Do not change it."

The spec lives at `logsum-sandbox/spec.md`. Its key decisions:

- Group key: `(normalised_level, normalised_service)`
- level normalisation: strip + uppercase → `UNKNOWN` if not INFO/WARN/ERROR/DEBUG
- service normalisation: strip whitespace, preserve case
- Output columns: level, service, count, first_seen, last_seen
- Malformed timestamp: skip row + stderr warning
- Empty input: header-only output, exit 0
- CLI: `python -m logsum <input> [--output <path>]`
- Exit codes: 0 success / 1 input error / 2 output error
- Out of scope: filtering, message parsing, streaming, non-CSV
