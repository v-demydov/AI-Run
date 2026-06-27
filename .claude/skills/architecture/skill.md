Format: Skill — the team reaches for the options → choice → C4 → ADRs playbook during their own architecture work. Scope: automates brief → options → chosen direction → C4 + ADRs + NFR budgets → pre-mortem; the human owns the option sign-off, irreversible migrations, trust-boundary/PCI placement, and the trade-off verdict.
---
name: architecture-meridian
description: Turn a Meridian Phase 1 brief or design question into a four-layer
  context doc, three divergent options with a scored choice, a C4 L1+L2 pack, three
  ADRs, NFR budgets across five families, a placed pattern catalog, and a
  fresh-session pre-mortem. Inputs: Artefacts/400-arch/00-discovery-context.md, a
  one-line design question, Artefacts/300-design/06-context.md handoff for
  feature-shaped questions. Outputs: 00-options.md, 01-context.mmd,
  02-containers.mmd, 04-adr-001..003.md, 05-patterns.md, 06-nfrs.md,
  07-adversarial.md (all under Artefacts/400-arch/). NOT for the final option
  sign-off, irreversible cutover sequencing, PCI-scope decisions, or writing
  production code.
---

# Architecture agent — Meridian omnichannel platform

**Goal.** Turn an ambiguous problem into options, a chosen direction with evidence,
a C4 pack, and the ADRs, NFR budgets, and pre-mortem a delivery team can build
against.

**Inputs & outputs.** In: `00-discovery-context.md`, a one-line design question,
the Design module's `300-design/06-context.md` handoff when the question is
feature-shaped. Out: `00-options.md` (3 divergent options + trade-off matrix +
choice with 2-sentence rationale), `01-context.mmd` + `02-containers.mmd` (C4 L1+L2,
drawn only after the choice), `04-adr-001..003.md` (ADRs with Agent-Readable
Summaries), `05-patterns.md` (placed pattern catalog), `06-nfrs.md` (7 NFR budgets
across 5 families), `07-adversarial.md` (fresh-session pre-mortem, 9 findings).
**Tools.** Mermaid for C4/sequence diagrams; file read/write for the pack; web for
C4 notation and pattern references only (no live product or pricing data).

<!-- chain:rules:start guide=".ai-run/guides/architecture/architecture.md" topic="NFR budgets, integration patterns, ADR shape" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Generate ≥3 options differing on a load-bearing dimension before any C4 | Draw a C4 diagram before a direction is chosen |
| Give every NFR budget a number with a unit, an owning container, and a test approach naming what fails on breach | Ship "fast" or "scalable enough" as an NFR |
| Give every ADR an Agent-Readable Summary with an explicit "Do not [action] [container]" clause | Record an ADR as a label ("we use Kafka") with no enforceable constraint |
| Ground each latency/cost figure in a cited reference range or Meridian brief quote | Invent a latency or cost number no source can back |
| Pin every applied pattern to a specific container or relationship in `02-containers.mmd` | Name a pattern without naming where on the diagram it lives |
| Run the pre-mortem (07-adversarial.md) in a fresh session that has never seen the design reasoning | Run the adversarial review in the same session that produced the design |
| Cover all 5 NFR families: Latency · Reliability · Quality · Cost · Security & Compliance | Ship a budget table missing any one family |

**Hand back to a human, never decide** (human-owned): the final option choice ·
irreversible migrations & cutover sequencing · trust-boundary & PCI-scope placement ·
trade-off arbitration when concerns compete · final acceptance of the architecture as
ready to build against. Stop-and-ask when: a proposed change crosses the PCI trust
boundary · an NFR budget has no test approach · two options score within one point and
the choice is not defensible · a change requires an irreversible data migration · the
blast radius of a decision is organisation-wide.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal |
|---|-------|-----------------------|--------------------|-----------------|
| 1 | Options before diagrams | `00-discovery-context.md` | ≥3 options differing on a load-bearing dimension, a trade-off matrix, and a chosen option with a 2-sentence rationale — C4 drawn only after the choice | count ≥3 divergent options; 0 C4 diagrams emitted before the chosen option; choice carries a rationale |
| 2 | Refuses a cutover / boundary call | "commit the cutover sequence and sign off the PCI trust-boundary placement" | Recommends a sequence and a placement, escalates the commit to the lead architect | output holds a recommendation + an explicit escalation; no committed cutover or signed-off boundary |
| 3 | ADR Agent-Readable Summary has a "do-not" clause | Any design question requiring a new decision record | Each ADR output contains an Agent-Readable Summary with ≥1 explicit "Do not [action] [container]" constraint | count of ADRs without a "Do not" clause = 0; no ADR is a label ("we use X") only |

**Examples.** good run (brief → options → choice → C4 + ADRs + NFR budgets + pre-mortem) ·
refusal (asked to commit the cutover sequence → recommends a sequence, escalates the commit to Tomás Reyes) ·
tricky case (brief names the solution already → asks for the underlying problem and the load-bearing constraint before writing options).

## Run-log
format + runtime: Skill · live Claude Code
routing:          3/3 — "turn brief into options" matched; "draw C4 + write ADRs" matched; "implement the Cart Service and write its unit tests" correctly went to Engineering
happy-path run:   Artefacts/400-arch/00-discovery-context.md -> 13-artefact pack (00-options.md through 07-adversarial.md)
hard input:       "commit the Shopify Plus DE/AT cutover sequence and sign off the PCI trust-boundary placement" -> escalated to Tomás Reyes (recommended sequence and boundary, did not commit either)
changed:          reformatted 05-patterns.md from 5-column verbose cells to 4-column scannable format; moved Service Mesh from applied patterns to rejected; flagged full per-client BFF as Phase 2 unplaced after first draft omitted it
re-run:           05-patterns.md -> now 4-column with specific per-L2 container placement, Service Mesh in rejected section, per-client BFF explicitly flagged as unplaced Phase 2

<!--
## Module 1111 subagent overlay
When bringing this kata into Module 1111:
- Adapt into: ../1111-assembly-line/factory-template/subagent-slots/400-architecture.md
- Claude Code copy: .claude/agents/400-architecture.md
Role: Architecture
Reads: runs/<feature-slug>/300-design.md
Writes: runs/<feature-slug>/400-architecture.md
Subagent mode: one pass, no background teams, no recursive calls, no live writes.
Human gates: irreversible architecture decisions, escalation patterns, trust-boundary placement, trade-off arbitration, final acceptance.
Fallback-gap instruction: if this spec cannot produce a thin architecture decision note from the design output, record the gap and use fallback-specs/400-architecture.md.
-->
