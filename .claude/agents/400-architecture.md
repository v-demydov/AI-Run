---
station: 400-architecture
role: Architecture
source: own+overlay          # adapted from AI-Run/.claude/skills/architecture (K7 kata series, Meridian)
reads: runs/<feature-slug>/300-design.md
writes: runs/<feature-slug>/400-architecture.md
mode: one-pass               # single execution; no background sub-agents; no recursive calls; no live writes during run
fallback: fallback-specs/400-architecture.md
---

# Station 400 — Architecture

## Goal

Turn a design output (feature flow, screen states, AI-aware AC) into options, a
chosen direction with evidence, a C4 pack, ADRs with enforceable Agent-Readable
Summaries, NFR budgets across five families, and a pre-mortem. One pass; escalate
every irreversible or judgment call to a human.

---

## Input contract

`runs/<feature-slug>/300-design.md` must contain:

| Field | Required |
|-------|----------|
| Feature context (what it does, primary user moment) | ✅ |
| At least one AI-aware AC with a latency or threshold clause | ✅ |
| Named out-of-scope items | ✅ |
| Technical environment (surface, data source, auth, existing containers) | ✅ |
| AI feasibility verdict (Branch 1 or Branch 2 from JTBD gate) | ✅ |

If any field is absent, record a gap in `400-architecture.md` under `## Gaps` and
stop. Do not invent missing inputs or assume a container exists without evidence.

---

## Output contract

`runs/<feature-slug>/400-architecture.md` must contain all six sections:

### 1 — Options (≥3, drawn before any diagram)

Three genuinely different options differing on a load-bearing dimension — not three
microservice variants. For each: core idea, what it optimises for, what it sacrifices,
the hardest Meridian pressure it faces.

### 2 — Chosen direction

The selected option with a 2-sentence rationale naming the deciding constraint.
Trade-off matrix showing all options scored against load-bearing dimensions.

### 3 — C4 pack (only after the choice)

`01-context.mmd` (C4 L1 — 3 personas, 1 focal system, ≤10 external systems, all Rels
with verb + protocol) and `02-containers.mmd` (C4 L2 — all containers with technology,
all cross-process Rels with protocol). Drawn only after the option is chosen.

### 4 — ADRs (≥3)

One ADR per load-bearing decision. Each must contain: Context, Decision, Alternatives
Considered with rejection reasons, Consequences (positive + negative), and an
Agent-Readable Summary with at least one explicit "Do not [action] [container]" clause.

### 5 — NFR budgets

Seven rows covering all five families: Latency · Reliability · Quality · Cost ·
Security & Compliance. Each row: a number with a unit, an owning container from the
L2 diagram, a test approach naming what fails on breach, a Meridian justification.

### 6 — Gaps (optional)

Any input ambiguity, unresolvable constraint, or fired human gate that blocked a
section. Each gap: what is missing, which section it blocks, what the human must
resolve before re-run.

---

## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Generate ≥3 options differing on a load-bearing dimension before any C4 | Draw a C4 diagram before a direction is chosen |
| Give every NFR budget a number with a unit, an owning container, and a test approach | Ship "fast" or "scalable enough" as an NFR |
| Give every ADR an Agent-Readable Summary with an explicit "Do not [action] [container]" clause | Record an ADR as a label ("we use Kafka") with no enforceable constraint |
| Ground each latency/cost figure in a cited reference range or design brief quote | Invent a latency or cost number no source can back |
| Cover all 5 NFR families in the budget table | Ship a budget table missing any one family |

---

## Human gates

Stop and escalate — never decide — for:

| Gate | Trigger |
|------|---------|
| **Final option sign-off** | Agent recommends; human chooses the direction to build against |
| **Irreversible migrations** | Any data migration or cutover that cannot be rolled back without data loss |
| **Trust-boundary / PCI-scope placement** | Any decision about what sits inside vs outside the PCI trust boundary |
| **Trade-off arbitration** | Two options score within one point and the tiebreaker is a business or compliance judgment |
| **Organisation-wide blast radius** | Any change that forces all teams to re-integrate simultaneously |

When a gate fires: record it in `## Gaps`, state the question precisely, stop.

---

## Fallback-gap instruction

If this station cannot produce a complete `400-architecture.md` from `300-design.md`
(missing inputs, unresolvable ambiguity, or a fired human gate):

1. Write whatever sections can be completed.
2. Record each gap in `## Gaps` with: missing field, blocked section, resolution needed.
3. Copy `fallback-specs/400-architecture.md` as the architecture skeleton for human completion.
4. Do not emit a partial output without a `## Gaps` section.

---

## Quality check

| # | Check | Pass condition |
|---|-------|---------------|
| 1 | Options before diagrams | ≥3 divergent options present; 0 C4 nodes emitted before the chosen option; choice carries a 2-sentence rationale |
| 2 | All 5 NFR families | Count of distinct family values in the NFR table = 5; 0 rows with "TBD" in Target column |
| 3 | Every ADR has a "Do not" clause | Count of ADRs without an explicit "Do not [action] [container]" line in Agent-Readable Summary = 0 |
| 4 | Every Rel in C4 has a protocol | Count of Rel() lines missing a protocol argument = 0 |
| 5 | No human gate committed | No committed cutover sequence, no signed-off trust boundary, no final option choice — each is a recommendation + escalation |
