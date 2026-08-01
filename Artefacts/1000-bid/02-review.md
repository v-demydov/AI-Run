---
kata: 10.W.3
date: 2026-07-31
source: 02-solution.md
reviewer: adversarial fresh-session (bid-review director persona)
---

# Adversarial Review — Solution Outline

_Prompt used: "You are a sceptical bid-review director. Attack this solution outline. Name the 3 sharpest concerns — phase boundaries with hidden scope, governance the sub-vendor will exploit, assumptions the client will dispute. No praise."_

---

## Critique 1 — The root-cause gate methodology is stated but not owned

**Concern.** The Phase 0 exit criterion requires that "methodology is agreed at kick-off, assessed by both parties against agreed reason-code classification." That is a process description, not a criterion. Two parties assessing the same data can produce different answers: EPAM classifies a cancellation as "allocation-driven" using reason-code logic; Meridian's retail planning team classifies the same cancellation as "store execution failure." There is no stated arbiter when they disagree. The gate will be disputed at the exact moment EPAM needs it to pass to move €220K+ of budget into Phase 1. A Meridian procurement manager who is cold on the engagement can simply not agree on methodology and the engagement stalls at Phase 0 while EPAM has already mobilised.

**Verdict.** This is the sharpest risk in the document. The gate is precise on the threshold (40%) but silent on who classifies ambiguous cases and what happens when classification is disputed.

---

## Critique 2 — The Prosci sub-vendor governance creates a liability gap at Phase 2 exit

**Concern.** The Phase 2 exit criterion requires a ≥30% first-week recommendation accept rate. The solution document assigns this to the "sub-vendor OCM track, verified by EPAM dashboard audit." If the accept rate is 18%, EPAM is contractually responsible to Meridian but contractually dependent on Prosci to fix it. The sub-contractor MSA is mentioned but the remedy is not: does EPAM have a right-to-cure clause against Prosci with a time-box? Can EPAM terminate Prosci and staff the OCM track internally mid-flight without a Meridian change order? If not, the governance chain (Meridian → EPAM → Prosci) means Prosci's underperformance becomes EPAM's delay. The escalation path (sub-vendor lead → EPAM Engagement Lead → EPAM Delivery Director) is internal to EPAM — it does not resolve the adoption shortfall; it just names who finds out about it in what order.

**Verdict.** Naming the sub-vendor does not constitute a governance plan. The remediation clause is vague: "sub-vendor repeats facilitation" is not a bounded commitment. Meridian's legal team will ask what EPAM's contractual remedy against Prosci is before they sign a proposal that ties Phase 3 outcomes to Prosci's performance.

---

## Critique 3 — Assumption A4 (executive sponsor) is unfalsifiable and load-bearing

**Concern.** A4 states "CxO executive sponsor named and available at kick-off meeting." Named and available at a single meeting is the weakest possible definition of sponsorship. The opportunity brief (Gate 6) explicitly warns that "regional GM resistance will not be resolved by the pilot team alone; CxO must mandate minimum participation." If the executive sponsor attends the kick-off and then is unavailable for weeks 3–8 (realistic for a CxO), EPAM has no contractual lever. The adoption workstream collapses and the Phase 2 exit criterion (≥30% accept rate) fails, but the consequence is just a note in the Phase 3 measurement report — not a contractual event. EPAM bears the reputational cost of a missed adoption target caused by a client-side dependency that was stated as an assumption, not a hard deliverable.

**Verdict.** Reframe A4 as a client-side dependency with a named individual and a defined engagement commitment (e.g., minimum 1-hour steering call per fortnight + authority to mandate planner participation in writing before Phase 2 start). Without this, A4 is a hope, not an assumption.

---

## Patch Applied — Critique 1 (weakest part)

Root-cause gate methodology ambiguity is the highest-risk gap because it controls whether €220K+ of Phase 1–3 scope is triggered at all. The following change was applied to `02-solution.md` Phase 0 exit criteria:

**Before patch:**
> Root-cause diagnostic confirms ≥40% of phantom stock is allocation/visibility-driven (methodology agreed at kick-off, assessed by both parties against agreed reason-code classification)

**After patch (applied in 02-solution.md):**
> Root-cause diagnostic confirms ≥40% of phantom stock is allocation/visibility-driven. Methodology: EPAM classifies each POS cancellation reason code from the most recent 12-month period in the pilot country into two buckets — (A) allocation/visibility-driven (reason codes: out-of-stock at source warehouse, incorrect inventory position, inter-store transfer lag) and (B) operational/other (reason codes: store execution failure, returns processing error, shrinkage, customer cancellation). Classification logic is documented and submitted to Meridian Data team at Phase 0 kick-off. If Meridian disputes any specific reason-code classification, the disputed codes are escalated to Meridian's Head of Retail Planning for a binding ruling within 2 business days. Final gate assessment uses the agreed classification; no further dispute mechanism. The 40% threshold is assessed against the agreed (and optionally patched) classification only.

**Why this patch closes the gap.** The arbiter (Head of Retail Planning) is named by role. The dispute window is bounded (2 business days). The final assessment is non-re-openable after the ruling. Meridian can no longer stall Phase 1 by withholding classification agreement — the process has a time-box and a named decision-maker.

---

## Critiques 2 and 3 — Status

**Critique 2 (Prosci liability gap):** Deferred to contract negotiation phase. The solution outline correctly names the escalation path; the right-to-cure clause against Prosci must appear in the sub-contractor MSA, not the client-facing solution outline. Action: flag for EPAM Legal before contract draft.

**Critique 3 (unfalsifiable executive sponsor):** Assumption A4 in `02-solution.md` updated from "named and available at kick-off meeting" to: "named individual with authority to mandate planner participation; commits to ≥1 fortnightly 60-minute steering call throughout Phase 2; written mandate to pilot planners issued before Phase 2 start — this is a client-side dependency, not an assumption." Moved from the Assumptions table to Client-Side Dependencies.
