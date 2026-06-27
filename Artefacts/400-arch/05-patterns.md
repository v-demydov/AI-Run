---
case: Meridian Retail Group
kata: 4.W.6
date: 2026-06-26
sources: 02-containers.mmd · 04-adr-001.md · 04-adr-002.md · 04-adr-003.md
---

# 05 — Placed Pattern Catalog: Meridian Phase 1

Each row pins a pattern to a specific container or relationship in `02-containers.mmd`, names the Meridian constraint that forces it, and names the trade-off it introduces.

| Pattern | Where on L2 | Meridian constraint it addresses | Trade-off |
|---------|-------------|----------------------------------|-----------|
| **Strangler Fig** | Apollo GraphQL Gateway routes `/v2/*` to new platform containers; anything not yet migrated falls through to legacy stacks (Shopify Plus DE/AT first, then custom .NET IT, then Magento 2 FR/ES). | "22 regional stacks in 18 months — no Big Bang." Shopify Plus DE/AT is the first target: largest revenue share, most standardised, clearest rollback boundary. | Routing split layer becomes a deployment dependency; parity tests must run continuously, not once. Cannot retire the routing layer until the last region migrates in Phase 3. |
| **Outbox** | Checkout Service writes `order.placed` as a row in Order Database within the same checkout transaction; a relay process polls and publishes to the Order Event Bus (Kafka). Containers: Checkout Service + Order Database + Order Event Bus. | ADR-002: a Checkout Service restart between Stripe webhook receipt and the OMS call silently loses the reservation event without a durable write. | Relay process adds ~100–500ms publication lag between checkout commit and Kafka availability. OMS reservation lags payment confirmation by this window — POS cart lookup must tolerate a brief "paid, reservation pending" state. |
| **Saga (choreography)** | Checkout Service → Order Event Bus → OMS (reservation). Compensating transaction: `reservation.failed` event → Checkout Service triggers Stripe refund. Containers: Checkout Service, Order Event Bus, OMS, Stripe. | PSD2 SCA and PCI-DSS require payment and reservation to be consistent from the shopper's perspective; synchronous two-phase commit across Stripe and OMS is not feasible. | Every failure branch needs a compensating transaction coded and tested explicitly. A `reservation.failed` arriving after a confirmation email has been sent requires manual resolution — the Saga has no automated rollback for that state. |
| **Bulkhead** | Checkout Service maintains separate connection pools per payment-method route: Stripe card, Stripe + Postepay (IT), Stripe + Giropay (DE), Stripe + Sofort (DE/AT). Container: Checkout Service (internal pool config). | BaFin + Italian regulators mandate local payment methods per country; each has independent failure modes. Without bulkheads, a Postepay degradation exhausts the shared pool and cascades to DE card checkout — the same failure topology as the 2024 Black Friday outage. | More pools to configure, monitor, and capacity-plan. Under low traffic, pools are underutilised. Mis-sizing a pool (too small) produces timeouts that look like payment processor failures, not capacity errors. |
| **Circuit Breaker** | Two placements: (1) Confidence API → ML Scoring Engine — opens when rolling 24h High-correctness < 75%, reverts all stores to binary fallback (ADR-001). (2) Apollo Gateway → Stripe — opens on repeated 5xx, returns "payment unavailable" before the connection pool is exhausted. | ADR-001 circuit breaker prevents the model emitting misleading "High" signals at scale. Gateway circuit breaker prevents a Stripe degradation from taking down browse and cart operations through shared pool exhaustion (2024 Black Friday root cause). | Open state must be observable and manually re-closable after root-cause sign-off. A circuit that opens and is never re-armed silently degrades the feature forever — worse than having no circuit. |
| **CQRS (implicit — inventory read model)** | Inventory Read Cache (Redis, written by SAP Inventory Adapter) is the read side; SAP S/4HANA is the write side. Confidence API reads from Redis only — it has no write path to inventory. Containers: Confidence API, Inventory Read Cache, SAP Inventory Adapter. | ADR-001: read latency requirement (p95 ≤ 800ms async) and write cadence (SAP batch, 2–4h) are incompatible in a single storage tier. *Note: this is read/write segregation by another name — the Redis cache IS the CQRS read model.* | Read model is eventually consistent with SAP (30-min import lag). Any Phase 2 feature requiring transactional consistency between inventory write and confidence read (e.g., committed item hold) would require dismantling this separation. |

---

## Not yet placed on L2 — open question for Phase 2

| Pattern | Status | Why deferred |
|---------|--------|--------------|
| **BFF (per-client gateway instances)** | Not placed in Phase 1 | Phase 1 uses Apollo Gateway with per-client GraphQL query shaping as a lightweight proxy. Separate Web BFF, Mobile BFF, and POS BFF instances are not on `02-containers.mmd`. The full BFF pattern (three separate deployments, each with client-specific schemas and response shaping) is a Phase 2 milestone once traffic patterns from the strangler-fig migration are understood. *Risk to note:* POS Client and Web App share one gateway instance; a runaway POS query affects web checkout. Mitigated by schema-level query-cost limits per client type. |

---

## Rejected patterns

| Pattern | Decision | Meridian-specific reason |
|---------|----------|--------------------------|
| **Event Sourcing** | Rejected | Kafka already provides durable event replay for the order domain (the only Phase 1 use case). Full Event Sourcing across all services requires event schema governance, projection rebuild capability, and distributed-systems expertise the predominantly junior Phase 1 team does not have. Cost: 3–6 months of Phase 1 budget for Phase 3 requirements. |
| **Pipe & Filter (system-level)** | Not applicable | The SAP Inventory Adapter's internal import pipeline (RFC/BAPI pull → transform → enrich → write Redis) could be designed as Pipe & Filter internally, but this is a single batch job, not a system-level pattern. Naming it adds vocabulary without adding architectural constraints. |
| **Service mesh (Istio / Linkerd)** | Rejected | A service mesh is a deployment-level concern, not a design pattern, and its operational overhead (mTLS rotation, sidecar lifecycle, traffic policy debugging) is disproportionate for a junior Phase 1 team migrating 22 stacks simultaneously. Circuit Breaker and Bulkhead implemented at the application level cover the resilience requirements. Revisit in Phase 3. |
