---
fallback-for: 01-claude-md.md
use-when: sandbox repo cannot be created (no git, no write access to ~/projects/)
---

# Fallback — CLAUDE.md content

Copy this text verbatim to `CLAUDE.md` at the root of any Python CLI project
to establish baseline rules before the first AI coding session.

```markdown
# <project-name>

## Project context
Tiny CLI that reads `data/events.csv` and prints a statistical summary to stdout.
Synthetic data only — no real events, no PII.

## Conventions
- Source code: `src/`
- Tests: `tests/`
- Synthetic data: `data/`
- One module per responsibility; no circular imports.
- Test files mirror `src/` names: `src/summarise.py` → `tests/test_summarise.py`.

## Utilities to prefer
- Python 3.11 standard library: `csv`, `statistics`, `argparse`, `pathlib`, `collections`.
- `ruff` for linting and formatting (replaces flake8 + isort).
- `pytest` for tests; no test framework beyond pytest.

## Escalation gates
- Stop and ask before adding any dependency outside the standard library.
- Synthetic data only; never load or reference real log files.
- Never overwrite `spec.md` after sign-off without asking first.
```
