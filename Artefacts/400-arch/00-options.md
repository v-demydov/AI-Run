---
case: Meridian Retail Group
kata: 4.W.2
date: 2026-06-25
decision: How does the Confidence API access a consistent, low-latency snapshot of inventory state (SAP count · POS velocity · OMS sync age) for a given store-SKU pair at product page load time, given that all source systems are batch-sync'd?
status: options open — do not choose here; scoring is kata 4.W.5
---

# 00 — Options: Confidence API Inventory Read Model

## The load-bearing dimension

The three options differ on **where and when inventory state is materialised for the Confidence API to read**:

| Option | When materialised | By whom |
|--------|-------------------|---------|
| A — Scheduled batch import | Every 15–30 min by a background job | The Confidence service itself |
| B — Pull-through cache | On first request for a store-SKU pair | The Confidence API, on the hot path |
| C — Event-driven projection | On every inventory mutation event | A dedicated projection service |

They are not three microservice variants. They differ in coupling, operational surface, and what "fresh" means at inference time.

---

## Option A — Scheduled batch import into a local read store

*The deliberately boring option.*

**Core idea:**
- A background import job runs every 15–30 min, pulling SAP inventory snapshots and OMS/POS velocity exports into the Confidence service's own Redis store (keyed by `{storeId, sku}`).
- The Confidence API reads only from this local store at inference time — zero live calls to SAP, OMS, or POS during scoring.
- Staleness is deterministic and bounded: worst-case lag = import interval. The import timestamp is written with every record, so the "SAP sync > 4h stale" refusal trigger reads the import timestamp directly — no mystery.

**Optimises for:** Team operability — one background job + one Redis store; entirely testable in isolation; a junior team can operate it; failure modes are predictable (job misses → stale data, not outage).

**Sacrifices:** Freshness. A store that sells out between import cycles will show stale "High" confidence until the next run. For a 30-min import cadence this is a smaller phantom window than today's 4h SAP lag — but it is still a window.

**Meridian constraint that pressures it hardest:** POS granularity gap (Assumption A2). If the OMS POS export is daily (not sub-hour), the import job has nothing to pull for velocity. The velocity signal degrades to the daily snapshot regardless of import frequency. Pressures the model's MAPE improvement case.

---

## Option B — Pull-through cache with live SAP adapter

**Core idea:**
- Each confidence request checks Redis for a valid cache entry (`TTL = 30 min`). On a cache hit, return immediately.
- On a cache miss, the Confidence API calls a thin SAP adapter service for the current inventory count + OMS sync age, and a POS snapshot endpoint for velocity. The result is written to cache before returning.
- The "live" call's response timestamp drives the staleness evaluation; the 4h refusal trigger is evaluated from the SAP adapter's own sync metadata.

**Optimises for:** Freshness on the first request for a store-SKU pair — useful for high-velocity SKUs during flash sales where the 30-min cached value is already wrong. Also simplest to reason about consistency: the cache is a performance layer, not a data layer.

**Sacrifices:** Availability under source-system load. Every cache miss puts SAP and OMS on the hot path. During a SAP maintenance window or OMS brownout, all cache misses fall back — potentially forcing most of a peak-day's product-page loads into binary fallback simultaneously. Also: if SAP exposes no real-time query API (Assumption A1), the adapter is reading the same batch-refreshed query view Option A would have imported — delivering Option A's freshness with Option B's latency risk.

**Meridian constraint that pressures it hardest:** SAP batch-update reality (Assumption A1). "Live" SAP queries likely read a batch-refreshed snapshot, not a transaction-consistent count. The architectural complexity of a live-call model delivers no freshness improvement over a scheduled import; the cache miss latency is spent for nothing.

---

## Option C — Event-driven materialised projection

**Core idea:**
- SAP stock movements, OMS reservation events, and POS sales transactions are published to an event bus (Kafka or AWS EventBridge) as they occur.
- A dedicated projection service consumes these events and maintains a materialised view: `(storeId, sku) → {count, velocity_4h, oms_sync_ts, last_event_ts}`. Velocity windows are pre-computed by the projection.
- The Confidence API reads only the projection store at inference time. No source-system calls at query time; P95 is bounded by the projection store's read latency, not SAP or OMS.

**Optimises for:** Inference latency and scalability. The read model is always warm; the scoring path has no external dependency at runtime. Pre-computed velocity windows also unlock the store-map (S8) and alternative-stores (S2) batch scoring without sequential SAP round-trips.

**Sacrifices:** Operational complexity. Requires event bus, projection service, schema versioning, dead-letter queue handling, and guaranteed-delivery semantics — typically 2–3 additional services the junior team must operate. If SAP emits no native domain events (batch-only, Assumption A1), a synthetic event poller must simulate events from batch snapshots, adding infrastructure that behaves identically to Option A's import job but with an event bus in front of it.

**Meridian constraint that pressures it hardest:** SAP batch-update reality + junior team operability. SAP's batch architecture means the event bus receives batch-triggered synthetic events anyway; the projection service adds operational surface without improving the freshness ceiling over Option A. The complexity budget is spent without a freshness return.

---

## What each option silently assumes

| Option | Hidden assumption | Breaks if… |
|--------|-------------------|------------|
| A | OMS exports sub-day POS velocity snapshots | POS data is daily-only → velocity input unavailable |
| B | SAP exposes a queryable inventory count per store-SKU on demand | SAP is batch-only → live calls read batch data at hot-path latency |
| C | SAP emits inventory change events natively | SAP is batch-only → event bus is populated by a polling job = Option A + overhead |

All three options share Assumption A1 as a risk. Option A is the only one that doesn't pretend the assumption is resolved.

---

## Do not choose here

Scoring against Meridian constraints (SAP batch reality, junior team, PSD2 SCA latency, strangler-fig coexistence) is kata 4.W.5. All three options remain on the table.
