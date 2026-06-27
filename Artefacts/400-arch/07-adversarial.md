---
case: Meridian Retail Group
kata: 4.W.7
date: 2026-06-26
sources: 00-discovery-context.md · 01-context.mmd · 02-containers.mmd · 03-flow-instore-cart.mmd · 03-deps.mmd · 03-integrations.md · 04-adr-001.md · 04-adr-002.md · 04-adr-003.md · 05-patterns.md · 06-nfrs.md
adversarial-prompt: "You did not design this. Your job is to break it. Where does this architecture break first under: (a) 10× Black Friday peak load; (b) hostile inputs at EU checkout; (c) a partner outage — SAP ECC down 2 hours, or Stripe degraded? Top 3, most-likely-first. For each, name the specific container or relationship and the first symptom a user would see."
---

# 07 — Adversarial Pre-mortem: Meridian Phase 1

Nine findings across three stressors, each specifying the container or relationship that fails first and the symptom a user would see. Every finding is either patched (naming the artefact changed) or explicitly accepted (naming the owner).

---

## Stressor A — 10× Black Friday peak load
Normal: 8 000 RPS sustained. Stress: 80 000 RPS sustained, 120 000 RPS burst.

### A1 — Apollo GraphQL Gateway: HPA scale-out lag produces site-wide 503s before new pods are ready

**Container**: Apollo GraphQL Gateway

**First symptom**: HTTP 503 across ALL operations simultaneously — browse, cart, and checkout. Not just checkout. The customer sees a blank storefront with no meaningful error message.

**Why the design doesn't defend here**: Apollo Server (Node.js, single-threaded event loop) saturates within seconds of 10× load. EKS HPA triggers on CPU threshold but new pods take 60–120s to start (image pull + warm-up). During that window, the existing pod count is the only entry point for all 600 stores, web, mobile, and POS simultaneously. The design moves the 2024 Black Friday chokepoint from regional stacks into a shared gateway — a better architecture, but the same failure mode if HPA can't keep up.

**Disposition**: PATCH → `06-nfrs.md` NFR #2

---

### A2 — Order Event Bus + OMS consumer: Kafka lag turns the "reservation pending" window from <1s into minutes

**Container**: Checkout Service → Order Event Bus (Kafka) → OMS

**First symptom**: POS terminal shows "Payment confirmed — reservation completing" indefinitely. Store associate cannot complete the handover. The customer has paid; inventory has not moved.

**Why the design doesn't defend here**: The Outbox relay publishes `order.placed` events correctly. The break is on the consumer side: at 80 000 RPS, `order.placed` events arrive faster than the OMS consumer group can process reservations. Kafka consumer lag grows unboundedly if OMS is not scaled horizontally ahead of the spike. ADR-002 acknowledges the reservation window as "typically <1s under normal Kafka lag" — at 10× load, "typically <1s" becomes "possibly minutes," which is operationally indistinguishable from a stuck order for store staff.

**Disposition**: ACCEPTED RISK — **Owner: David Park (Store Operations)**

Acceptance rationale: OMS horizontal scaling before a scheduled flash sale is an operational pre-game task, not an architecture change. The "Payment confirmed — reservation completing" POS display is already specified in ADR-002 Consequences as the correct degraded state. If OMS is pre-scaled, the lag stays within the designed tolerance. David Park's team owns the flash-sale runbook that must include an OMS scale-out step.

---

### A3 — ML Scoring Engine: inference queue saturates, circuit breaker opens, C&C reverts to binary on peak day

**Container**: Confidence API → ML Scoring Engine

**First symptom**: All store product pages show binary stock status (In Stock / Out of Stock) instead of High/Medium/Low confidence signals. The Confidence API's circuit breaker has opened. Customers cannot trust click-and-collect availability on the highest-revenue day of the year.

**Why the design doesn't defend here**: The ML Scoring Engine (Python/scikit-learn, synchronous inference) has no horizontal auto-scaling specification in the design. At 10× product-page load, the inference queue saturates. Confidence API response times exceed the circuit-breaker calibration window; the rolling 24h High-correctness rate drops below 75% (because timeouts are logged as non-High). The circuit breaker opens correctly — but the business impact is that the €8M/year phantom-stock improvement is disabled precisely when it matters most.

**Disposition**: ACCEPTED RISK — **Owner: Asha Sundaram (Product — AI Availability)**

Acceptance rationale: The circuit breaker revert to binary is the documented degradation mode (ADR-001) — the Confidence API enhances, not gates, purchasing. Binary fallback does not break checkout. Pre-scaling the ML Scoring Engine for flash sales is a Phase 2 operational enhancement. Asha to communicate to store and ops staff that confidence signals may revert to binary during extreme-load events.

---

## Stressor B — Hostile inputs at EU checkout

### B1 — Checkout Service: Stripe webhook replay creates duplicate `order.placed` events and double reservations

**Container**: Checkout Service → Order Database → Order Event Bus

**First symptom**: No user-visible failure. The customer receives one confirmation email. The fulfilment team sees two pick-lists for the same order. Inventory is deducted twice. No error fires — the duplicate looks like two legitimate orders.

**Why the design doesn't defend here**: The Outbox pattern guarantees at-least-once delivery, which requires idempotency at the producer. ADR-002 does not require the Checkout Service to deduplicate on the Stripe event ID (`Stripe-Event-ID` header). Stripe retries failed webhooks for up to 72 hours on non-2xx responses; a transient Checkout Service error followed by a retry produces a second `order.placed` row in the Outbox, which the relay publishes to Kafka. OMS has no deduplication requirement either, so it creates a second reservation.

**Disposition**: PATCH → `04-adr-002.md` Agent-Readable Summary

---

### B2 — Apollo GraphQL Gateway: introspection enabled in production exposes full API surface to a compromised associate token

**Container**: Apollo GraphQL Gateway

**First symptom**: No immediate user-visible failure. An attacker with a stolen associate JWT (8h expiry window) issues an introspection query to the gateway, maps every query and mutation, and crafts targeted payloads against loyalty-QR lookup and cart operations. First observable symptom may be hours later: a `CART_NOT_FOUND` or `LOYALTY_QR_NOT_FOUND` spike in CloudWatch.

**Why the design doesn't defend here**: Apollo Server enables introspection by default. The design specifies "schema-level query-cost limits per client type" (05-patterns.md, BFF note) but never disables introspection. POS terminals issue RS256 JWTs — a stolen or cloned terminal has an 8-hour window. Introspection gives the attacker a complete schema map without any prior codebase knowledge.

**Disposition**: PATCH → `03-integrations.md` API security constraints

---

### B3 — Checkout Service: replayed Auth0 SCA callback completes a payment without fresh user authentication

**Container**: Checkout Service ↔ Auth0 (SCA step-up) ↔ Stripe

**First symptom**: A payment for an abandoned 3DS flow completes successfully without the customer re-confirming. The customer is charged for an order they did not complete. No fraud signal fires — from Stripe's perspective the `confirm` call was legitimate.

**Why the design doesn't defend here**: ADR-003 correctly delegates the SCA step-up challenge to Auth0. Auth0 redirects back to the Checkout Service with a signed `state` parameter after the 3DS challenge. If the Checkout Service does not validate: (1) that the `state` nonce is tied to the specific PaymentIntent and has not been used before, and (2) that the Stripe PaymentIntent is in `requires_confirmation` state, then a replayed Auth0 redirect from an abandoned 3DS flow can trigger a second Stripe `confirm` call. This is the standard OAuth CSRF / replay attack applied to the SCA redirect boundary — the design delegates SCA to Auth0 but leaves the callback validation responsibility unspecified.

**Disposition**: PATCH → `04-adr-003.md` Agent-Readable Summary

---

## Stressor C — Partner outage (SAP ECC down 2 hours; Stripe degraded)

### C1 — Inventory Read Cache: compound failure (SAP outage + Redis cold start) leaves all 600 stores unable to look up any inventory

**Container**: SAP Inventory Adapter → Inventory Read Cache (Redis) → Confidence API + POS cart lookup

**First symptom**: Every POS cart lookup for a cache-missed item returns `INVENTORY_DATA_UNAVAILABLE`. Every product page shows binary stock status. Store associates cannot confirm availability for any item not already warmed in Redis before the compound failure.

**Why the design doesn't defend here**: A single SAP outage is handled: the cache stays warm for ~30 minutes, then Confidence API circuit breaker opens at the 4-hour staleness threshold (ADR-001). The unhandled case is a compound failure: a Redis pod restart (ElastiCache maintenance window or capacity event) while SAP is simultaneously down. The cache is empty and SAP is unreachable — every SKU returns `INVENTORY_DATA_UNAVAILABLE`. The design does not specify Redis persistence (AOF/RDB) that would allow the cache to survive a pod restart with data intact.

**Disposition**: ACCEPTED RISK — **Owner: Tomás Reyes (Architecture)**

Acceptance rationale: The compound failure probability (ElastiCache maintenance + SAP outage simultaneously) is low. Two operational mitigations are sufficient for Phase 1: (1) align ElastiCache maintenance windows with SAP maintenance windows (the same overnight slot); (2) enable Redis AOF persistence on the ElastiCache cluster so data survives a pod restart without requiring SAP to be online. Both are infrastructure configuration, not architecture changes. Phase 2 mitigation: OMS as a secondary inventory fallback source for cache misses during SAP outage.

---

### C2 — SAP Inventory Adapter: import job fails silently for up to 4 hours before the ADR-001 staleness trigger fires

**Container**: SAP Inventory Adapter → Inventory Read Cache (Redis)

**First symptom**: No visible failure for the first 30–60 minutes (cache still warm from last successful import). Between 30 minutes and 4 hours: Confidence API silently serves increasingly stale signals. At 4 hours: circuit breaker opens, all C&C reverts to binary. The team's first notification is the circuit breaker event — by which time 4 hours of phantom-stock risk has already been served to customers.

**Why the design doesn't defend here**: The design names the 4-hour staleness trigger as the circuit-breaker threshold (ADR-001) but specifies no import-job health metric or alerting. A BAPI schema change, a network partition, or an expired SAP service account can silently fail every import invocation for 4 hours with no alert. The circuit breaker is the last line of defence — there is nothing between "job fails" and "circuit breaker opens 4 hours later."

**Disposition**: PATCH → `06-nfrs.md` NFR #3

---

### C3 — Apollo Gateway → Stripe circuit breaker: open state has no auto-probe, silently blocks all EU checkout until manual re-arm

**Container**: Apollo GraphQL Gateway → Stripe (circuit breaker)

**First symptom**: All EU checkout attempts return "payment unavailable." The circuit breaker opened correctly on Stripe degradation. Stripe recovers. The circuit breaker stays open — there is no automated half-open probe — and checkout remains blocked until an on-call engineer manually re-arms it "after root-cause sign-off" (05-patterns.md). A 2 AM EU circuit-breaker open event is blocked until morning standup.

**Why the design doesn't defend here**: 05-patterns.md explicitly calls out "A circuit that opens and is never re-armed silently degrades the feature forever." The design acknowledges this risk in prose but specifies no SLO alert, no half-open probe schedule, and no runbook step. At the 99.95% availability target (NFR #4), 2 hours of checkout downtime during business hours exhausts the monthly budget in a single incident.

**Disposition**: ACCEPTED RISK — **Owner: Tomás Reyes (Architecture)**

Acceptance rationale: Stripe's contractual SLA (99.99%) makes multi-hour degradations rare. The mitigation is operational: NFR #4's 99.92% SLO alert (synthetic probe every 60s) fires within 5 minutes of the circuit breaker opening. The on-call runbook must include a manual circuit re-arm step with a 30-minute Stripe health check as the gate condition. A half-open auto-probe is a Phase 2 enhancement — the synthetic probe + runbook is sufficient for Phase 1. Tomás to add circuit re-arm procedure to the Phase 1 incident runbook before launch.

---

## Patch register

All patches applied to the named artefacts at the time this document was created.

| Finding | Artefact patched | Change applied |
|---------|-----------------|----------------|
| A1 — Gateway HPA lag | `06-nfrs.md` NFR #2 | Added cold-start load-test scenario and pre-warm deployment hook to test approach |
| B1 — Stripe webhook replay | `04-adr-002.md` Agent-Readable Summary | Added Stripe event ID deduplication requirement (`stripe_event_id` unique constraint in Order Database) |
| B2 — GraphQL introspection | `03-integrations.md` | Added API security constraints section: introspection disabled in production, CI enforcement |
| B3 — Auth0 SCA replay | `04-adr-003.md` Agent-Readable Summary | Added one-time `state` nonce + PaymentIntent status check before Stripe `confirm` |
| C2 — Import job silent failure | `06-nfrs.md` NFR #3 | Added `last_successful_import_ts` CloudWatch alarm at 60-minute staleness to test approach |

---

## Risk register

| Finding | Accepted risk summary | Owner |
|---------|----------------------|-------|
| A2 — Kafka consumer lag at 10× | OMS reservation lag extends beyond 1s at extreme load — acceptable if OMS is pre-scaled in the Black Friday runbook | David Park (Store Operations) |
| A3 — ML inference capacity at 10× | Circuit breaker opens and C&C reverts to binary on peak day — designed degradation; binary fallback does not block checkout | Asha Sundaram (Product — AI Availability) |
| C1 — Compound SAP + Redis cold start | Empty cache + SAP down leaves stores unable to look up inventory — low probability; mitigated by AOF persistence and maintenance-window alignment | Tomás Reyes (Architecture) |
| C3 — Circuit breaker unmonitored open state | Manual re-arm leaves checkout blocked until on-call response — mitigated by 5-minute NFR #4 SLO alert and Phase 1 incident runbook | Tomás Reyes (Architecture) |
