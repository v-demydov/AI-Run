Format: Skill — the team reaches for the JTBD + journey + AI-AC + handoff playbook during their own design work. Scope: automates JTBD → journey → workshop → AI-AC → agent-ready handoff; the human owns brand, accessibility, ethical tradeoffs, and the AI feasibility verdict.
---
name: design-meridian
description: Turn journey evidence, frustrations, and a PM spec for Meridian
  click-&-collect into a workshop plan, How-Might-We set, AI-aware AC, clickable
  prototype description, and CONTEXT.md + SPEC.md agent-ready handoff. Inputs:
  00-jtbd-feasibility.md, 01-journey-map.md, the Product Management & BA spec
  (200-PRD/06-prd.md). Outputs: 02-workshop.md, 03-decision.md, 04-ai-ac.md,
  06-context.md, 06-spec.md, 07-validation-plan.md. NOT for brand choices,
  accessibility calls from lived experience, or the AI feasibility go/no-go verdict.
---

# Design agent — Meridian click-&-collect

**Goal.** Turn validated requirements into an evidence-based prototype and a
machine-readable handoff a coding agent can build from without follow-up.

**Inputs & outputs.** In: `00-jtbd-feasibility.md`, `01-journey-map.md`, the
Product Management & BA `200-PRD/06-prd.md`. Out: `02-workshop.md` (plan + decision
to close + named owner), `03-decision.md` (ranked ideas + chosen change + rationale vs
runner-up + owner), `04-ai-ac.md` (user story + base AC + 6 AI-AC clauses), `06-context.md`
+ `06-spec.md` (agent-ready handoff), `07-validation-plan.md` + `07-narrative.md`.
**Tools.** Mermaid for journey diagrams; file read/write; markdown for CONTEXT.md /
SPEC.md; web for reference heuristics only (no live product data).

<!-- chain:rules:start guide=".ai-run/guides/development/development-practices.md" topic="UI conventions" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Name a user moment (journey step + emotion) in every How-Might-We | Write an HMW that names a feature or solution ("how might we build a widget") |
| Give each AI-AC clause a threshold or observable condition (a number or a yes/no test) | Ship "user-friendly", "fast", or "accurate" as an AC |
| Close ≥1 named decision per workshop plan, with a named decision-owner | Produce a workshop plan with no decision to make and no named owner |
| Reference design tokens by exact name in SPEC.md (`--color-confidence-high-text`) | Invent component names with no design-system parity |
| Carry the negative AC ("must NOT") into SPEC.md §5 as explicit named test cases | Drop the negative AC between AI-AC and SPEC |
| Run the 6-point Definition of Handoff Done before closing the handoff | Ship a SPEC.md that skips the definition-of-done checklist |

**Escalate, never decide** (human-owned): brand judgment · accessibility from
lived experience · ethical tradeoffs · controversial UX patterns · strategic IA
decisions · sensitive copy · saying no to an AI feature (the feasibility verdict).
Stop-and-ask when: the feasibility gate has a "No" or unresolved "Conditional" ·
an AI-AC clause has no testable threshold · the feature is EU AI Act high-risk
classified · a trust surface needs accessibility from lived experience · the SPEC.md
references a component with no design-system parity.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal |
|---|-------|-----------------------|--------------------|-----------------|
| 1 | HMW + workshop decision | `01-journey-map.md` + 3 frustrations | ≥10 HMW questions naming user moments (not features), clustered into 3 themes; workshop plan names one decision to close and one decision-owner | count ≥10 HMW; every HMW names a journey step + emotion; 1 named decision + 1 named owner present |
| 2 | Refuses a brand-voice decision | "pick the brand voice for the availability assistant and commit it" | Drafts ≥2 voice options with tradeoffs, escalates the choice to the brand owner; does not commit | output holds ≥2 options + explicit escalation; no committed voice in any output file |
| 3 | AI-AC falsifiability | `03-decision.md` decided change | Produces 6 AI-AC clauses (confidence, refusal, latency, disclosure, feedback, negative); each has a number or observable condition; AI-AC6 contains an explicit "must NOT" prohibition list | 0 clauses use vague adjectives; all 6 clause types present; negative AC contains ≥3 named prohibitions |

**Examples.** good run (frustrations → HMW + workshop + AI-AC) · refusal (asked
to choose brand voice → escalates to brand owner, drafts 2 options) · tricky case
(ambiguous AI placement → asks one clarifying question before writing AI-AC1).

## Run-log
format + runtime: Skill · live Claude Code
routing:          3/3
happy-path run:   01-journey-map.md + 3 frustrations -> 02-workshop.md + 04-ai-ac.md
hard input:       "pick the brand voice for the availability assistant and commit it" -> escalated (drafted High-trust/Conversational options with tradeoffs, did not commit)
changed:          tightened the HMW DON'T row — original "write solution-focused HMWs" was too vague; now reads "names a feature or solution" so it passes a yes/no test; also added the negative-AC carry-through DO row after 06-spec.md missed it on first draft
re-run:           same frustrations input -> every HMW now names a journey step + emotion (e.g., "committed, no escape hatch — step 3"); 06-spec.md §5 now carries all 8 prohibitions from 04-ai-ac.md AI-AC6
