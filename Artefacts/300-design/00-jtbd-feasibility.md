---
product: Meridian click-&-collect (product detail page)
feature: AI availability assistant
date: 2026-06-24
role: series root — no upstream input
outputs: JTBD statement · two-branch feasibility checklist · verdict + approved-tools list
---

# JTBD + Feasibility Gate: AI Availability Assistant

---

## 1 — Job-to-be-Done

**User:** The click-and-collect shopper (not the store associate, not the ops team).

**Statement:**
> When I'm reserving a click-and-collect item for pickup at a nearby store,
> I want to be sure the item will actually be on the shelf when I arrive,
> so I only make the trip when the effort will be rewarded.

---

### Why this wording

**Situation** names the decision moment — the reservation, not the journey, not the
pickup. That's the last point where the shopper can act.

**Motivation** is "be sure the item will be there." *Not* "see a confidence widget."
The widget is one solution; a committed hold, RFID, or staff confirmation are others.
The JTBD stays neutral to all of them.

**Outcome** is behavioural: "only make the trip when the effort will be rewarded."
This is falsifiable — if the shopper still drives to an empty shelf at the same rate
after the feature ships, the job was not done.

---

### Hidden-assumption check

The first draft read: *"…I want **to know** whether the item will be available…"*

"To know" assumes the solution is informational — a signal, a label, a dashboard.
That is a solution-masquerade inside the motivation clause. A committed hold
(Apple Retail model) fulfils the same job without giving the shopper *any* information
at all — it just removes the risk. The outcome clause was tightened to remove the
information assumption; the job now admits both signal-based and hold-based solutions.

---

## 2 — Feasibility Checklist

### Branch 1 — AI in the Process (AI used to design and deliver this feature)

| Gate question | Evidence from brief | Verdict |
|---------------|---------------------|---------|
| Client permits AI tools for delivery? | "EPAM CodeMie pre-approved; third-party AI (Claude / GPT / Gemini) permitted for delivery with anonymised inputs." | **Yes** |
| Sensitive data kept out of AI inputs? | "non-PII stock + store metadata to the AI; customer identity / order history stay out of the AI path." | **Yes** |
| Approved toolset named? | EPAM CodeMie + Claude / GPT / Gemini, anonymised inputs only. | **Yes** |

**Branch 1 verdict: Yes.**
All three gates clear. Delivery team may use AI tools under the stated data constraints.
No additional permissions required before the next kata.

**Approved-tools list (carries through the entire series):**
- EPAM CodeMie (pre-approved, all uses)
- Claude / Anthropic (delivery; anonymised inputs: non-PII stock counts, store metadata, no customer identity, no order history)
- GPT / OpenAI (same constraints)
- Gemini / Google (same constraints)

---

### Branch 2 — AI in the Product (the availability assistant running in production)

| Gate question | Evidence from brief | Verdict |
|---------------|---------------------|---------|
| Stock data ready + fresh enough for the promise we'd make? | "SAP sync latency is 15–30 min (stock can be stale)." | **Conditional** |
| Regulatory framework clear (GDPR/CCPA; AI Act class)? | "GDPR/CCPA apply to any personalised surface." EU AI Act: "no high-risk classification expected, but unconfirmed." | **Conditional** |
| Worst-case understood (who's harmed if the estimate is wrong)? | Not addressed in brief. Inferable directionally: false positive = shopper drives to store, item not there — wasted trip, trust damage. Harm magnitude unquantified. | **Conditional** |

**Branch 2 verdict: Conditional.**
The assistant may be built and piloted, subject to three open conditions:

| # | Condition | Gate owner | Must be resolved before |
|---|-----------|------------|------------------------|
| C1 | **Promise calibrated to data freshness.** 15–30 min SAP latency means the product cannot promise binary "in stock now." The feature must be scoped as a probabilistic confidence signal with a visible staleness indicator — never a guarantee. | Product Lead | spec is finalised |
| C2 | **EU AI Act classification confirmed.** "No high-risk expected" is unconfirmed. If the assistant influences a consumer transaction, the classification must be formally verified before production launch. | Legal / Compliance | production go/no-go |
| C3 | **False-positive harm quantified.** Worst-case is understood directionally (wasted trip, trust damage) but the duty-of-care threshold — what rate of false positives is acceptable and what the remediation is — has not been stated. Required before circuit-breaker thresholds are set. | Product + Legal | circuit-breaker AC is finalised |

---

## 3 — Series Carry-Forward

Every downstream kata runs on these constraints:

```
Approved AI tools:     CodeMie, Claude, GPT, Gemini
Input constraint:      non-PII only (stock counts, store metadata)
Excluded from AI:      customer identity, order history, personalised surfaces
Promise ceiling:       probabilistic confidence signal — never a guarantee
Open conditions:       C1 (promise calibration) · C2 (AI Act class) · C3 (harm quantification)
Human gates:           scope · prioritisation · final spec acceptance · AI capability choices · kill decision
```
