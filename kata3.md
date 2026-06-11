# Maturity Gap Analysis

**Date:** 2026-06-11
**Author:** Vsevolod Demydov — Architect
**Project:** bench
**Committed location:** /Users/vsevolod_demydov/projects/AI-Run/kata3.md

---

## Scorecard

| Dimension | Level (L1 / L2 / L3) | Score (1.0 / 2.0 / 3.0) | Evidence (2–3 sentences) |
|---|---|---|---|
| AI Capabilities | L2 | 2.0 | Part of the team uses AI tools regularly for coding and analysis tasks. Usage is uneven across roles and seniority levels; no standardized workflows exist yet. |
| Reusability | L1 | 1.0 | Each team member builds prompts independently from scratch with no shared repository or template library. Reuse happens informally via copy-paste in chats, not through a structured asset store. |
| AI Champions | L1 | 1.0 | No formally designated AI champions exist on the team. Interest in AI is driven by individual initiative without coordination, mentoring, or a mandate to spread knowledge. |
| Performance Tracking | L1 | 1.0 | No metrics are collected on the impact of AI usage. Time savings and quality improvements are anecdotal and not tied to any baseline or success criteria. |
| DAU | L3 | 3.0 | More than 60% of team members use AI tools on a daily basis. Strong adoption signals high willingness to integrate AI into daily work across the team. |
| **Average** | | **1.6** | |
| **Overall Level** | **L1** | | L1 = 1.0–1.9 / L2 = 2.0–2.9 / L3 = 3.0 |

---

## Gap Analysis

### Gap 1

**Dimension:** Performance Tracking
**Current level:** L1
**Why this gap is most damaging:** Without measurable data, the team cannot prioritize AI improvements, justify investment, or demonstrate ROI to stakeholders.
**Root cause:** No one owns measurement — there is no agreed baseline, success criteria, or lightweight process for logging AI impact.

---
### Gap 2

**Dimension:** Reusability
**Current level:** L1
**Why this gap is most damaging:** High DAU with zero shared assets means every team member duplicates effort daily, slowing onboarding and compounding inconsistency in outputs.
**Root cause:** No designated owner for shared assets; prompts remain trapped in individual notebooks and chat histories and are never extracted into a common library.

---

## 30-Day Improvement Plan

### Step 1 — addresses Gap 1

| Field | Value |
|---|---|
| **Action** | Define 3 core metrics (time per task, rework rate, prompt reuse count) and start weekly logging in a shared spreadsheet accessible to the whole team. |
| **Owner** | Vsevolod Demydov |
| **Timeline** | 2026-07-11 |
| **Success metric** | ≥ 3 consecutive weeks of logged data collected from ≥ 5 team members by day 30. |

---

### Step 2 — addresses Gap 2

| Field | Value |
|---|---|
| **Action** | Create a `/prompts` directory in the repo and collect at least 10 validated prompts from current daily users, each with a one-line description and example output. |
| **Owner** | Vsevolod Demydov |
| **Timeline** | 2026-07-11 |
| **Success metric** | ≥ 10 prompts committed to `/prompts`, referenced or reused by ≥ 3 team members within 30 days. |

---

## Peer Review

**Reviewer:** [Name — Role]
**Date reviewed:** YYYY-MM-DD

| Review question | Reviewer answer |
|---|---|
| Is the evidence for each dimension specific and observable — not aspirational? | [One sentence] |
| Which score do you challenge, and why? | [At least one — dimension, proposed alternative score, reason] |
| Is each root cause a structural/behavioural cause — not a symptom? | Yes / No — [one sentence] |
| Are the success metrics measurable without asking the author? | Yes / No — [one sentence] |
| Would you sign off on this plan as a teammate? | Yes / No — [one sentence] |

---


## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-06-11 | Initial commit | Vsevolod Demydov |
