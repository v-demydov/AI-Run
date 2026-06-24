---
product: Meridian click-&-collect (product detail page)
date: 2026-06-24
sources: 02-workshop.md · 03-synthesis.xlsx
decision-owner: Sarah Chen, Head of CX
---

# Design Decision: AI Availability Assistant

---

## Chosen change

**A-i1 + A-i3 as a delivery package:** Replace the binary "In stock" label with a three-state confidence indicator (High / Medium / Low), derived from same-day POS sell-through rate and SAP inventory count. Pair it with a friction modal that intercepts the Reserve tap when the store's confidence is Low, presenting "Choose another store" as the default action and "Reserve anyway" as the opt-in escape.

These two ideas are a package, not two separate decisions. The modal (A-i3) has zero value without the label (A-i1) — it would fire against a binary signal that doesn't exist yet. The label (A-i1) without the modal leaves the shopper informed but unprotected at the commitment point (H5 violation persists). Together they close the heuristic gap at both intervention points identified in `01-heuristics.md`: the label (H1, H2) and the reservation gate (H5).

Combined score: Impact 5, Effort 4 (modal adds ~2pw to a 13pw ML build — marginal), Value 1.25.

---

## Rationale vs runner-up

**Runner-up: A-sup — Suppress reservation for uncertain stock** (Impact 3, Effort 2, Value 1.50)

Suppression scores higher on the value formula than the chosen package (1.50 vs 1.25) because it is simpler to build. It was not chosen for two reasons:

First, it fails the M2 guardrail. Suppressing the Reserve button for any store–SKU combination below a confidence threshold would prevent wasted trips (M1 ✅) but would also block reservations that shoppers would have made knowingly and successfully — converting legitimate intent into abandonment. The SAP sync window (15–30 min) means suppression would fire against real, available stock whenever the sync is stale. The feature metric guardrail (C&C reservation conversion rate ≥ baseline − 1 pp) would likely be breached at any threshold that meaningfully moves M1.

Second, suppression removes shopper agency. The JTBD — "only make the trip when the effort will be rewarded" — is a job the shopper wants to solve themselves with better information. Suppression solves it for them by removing the option. A shopper who would have reserved knowingly at a Medium-confidence store (local knowledge, proximity, low-value item) is blocked by a system that doesn't distinguish between their context and a high-stakes uncertain trip. The confidence signal respects that distinction; suppression cannot.

---

## Adversarial challenge (fresh session)

> *What would make the three-state label + modal fail?*

**Challenge 1:** The ML model does not achieve ≥ 85% High-correctness at launch. Shoppers see "High" and travel; the item isn't there. The feature produces the same outcome as today with a new label of authority — higher trust, same failure rate. The betrayal is worse because the system now made an explicit claim.

**Mitigation already in spec:** Circuit breaker in `04-stories-acs.md` S1: if rolling 24h High-correctness drops below 75%, the feature auto-reverts to binary fallback for all stores. Manual re-enable required after root-cause sign-off. The label cannot make a claim it cannot back — it falls back rather than lies.

**Challenge 2:** Shoppers don't understand "High / Medium / Low." The three states introduce a new vocabulary that the binary label doesn't require. A shopper who reads "Medium" and reserves unknowingly is in the same situation as today.

**Mitigation (label copy):** The label must use plain language, not the internal confidence class names. "Likely available" / "Check before you go" / "May not be available" communicates the same three states without requiring the shopper to learn a new scale. This is a copy decision, not an engineering decision — in scope for the prototype kata.

**Outcome of adversarial check:** The decision stands. The circuit breaker addresses Challenge 1; label copy addresses Challenge 2. Neither challenge is a reversal condition.

---

## Decision summary

| Field | Value |
|-------|-------|
| **Chosen** | Three-state confidence label (A-i1) + friction modal at Low (A-i3) |
| **Package rationale** | Label and modal are a single intervention; neither works without the other |
| **Runner-up** | Suppress reservation for uncertain stock (A-sup) |
| **Runner-up rejection** | Fails M2 guardrail; removes shopper agency; cannot distinguish context |
| **Adversarial risk 1** | Model miscalibration → circuit breaker (already in spec) |
| **Adversarial risk 2** | Label vocabulary → plain-language copy (prototype decision) |
| **Owner** | Sarah Chen, Head of CX |
| **Feeds** | Prototype (next kata) · `04-stories-acs.md` S1 + S4 (already in spec) |
