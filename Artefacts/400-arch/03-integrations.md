---
case: Meridian Retail Group
kata: 4.W.4
date: 2026-06-25
integration: POS Client → Apollo GraphQL Gateway — in-store cart hydration
contract-version: 1.0
consumer: POS Client (in-store terminal)
provider: Apollo GraphQL Gateway
---

# Integration Contract — cartLookupByQR

The single boundary that makes the in-store cart bridging moment work: a POS terminal presents a customer's loyalty QR code and receives a fully hydrated cart with per-line-item availability. This is the contract an engineer must implement on each side without asking a follow-up question.

---

## API style

GraphQL over HTTPS. Single endpoint — all operations through one URL.

| Field | Value |
|-------|-------|
| Endpoint | `POST https://api.meridian.internal/graphql` |
| Content-Type | `application/json` |
| Protocol | HTTPS/1.1 (TLS 1.2 minimum; TLS 1.3 preferred) |

---

## Authentication

Associate terminal sessions are JWT Bearer tokens issued by the Identity Service after the associate authenticates at terminal boot.

| Header | Format | Notes |
|--------|--------|-------|
| `Authorization` | `Bearer <associate-JWT>` | RS256, signed by Identity Service. Expires after 8h (shift length). |
| `X-Store-ID` | `<store-id>` | ISO store identifier. Validated server-side against the JWT's `store_id` claim. |

Token must include claims: `sub` (associate ID), `store_id`, `role: associate`, `exp`.

If `Authorization` is absent, malformed, or expired → `401 Unauthorized` — do not proceed to business logic.

---

## Request

```graphql
query CartLookupByQR($qrToken: String!, $storeId: ID!) {
  cartLookupByQR(qrToken: $qrToken, storeId: $storeId) {
    customer {
      id
      name
      loyaltyTier      # STANDARD | SILVER | GOLD
    }
    cart {
      id
      items {
        sku
        name
        qty
        unitPriceCents  # integer — no floating point in money
        availability {
          label         # HIGH | MEDIUM | LOW | UNKNOWN
          count         # integer; -1 if unknown
          dataSource    # CACHE | SAP_FALLBACK | UNAVAILABLE
          syncTs        # ISO-8601; null if UNAVAILABLE
        }
      }
      subtotalCents     # sum of unitPriceCents × qty across all items
      currency          # ISO-4217, e.g. "EUR"
    }
  }
}
```

**Variables (JSON body):**
```json
{
  "query": "...",
  "variables": {
    "qrToken": "eyJ...",
    "storeId": "DE-HAM-001"
  }
}
```

`qrToken`: base64url-encoded loyalty QR payload. Max 512 bytes. Tokens expire 60 seconds after generation (prevents replay).

---

## Response — success

HTTP `200 OK`. GraphQL errors use `errors[]` in the body even when HTTP is 200.

```json
{
  "data": {
    "cartLookupByQR": {
      "customer": {
        "id": "cust_a1b2c3",
        "name": "Maria Schneider",
        "loyaltyTier": "SILVER"
      },
      "cart": {
        "id": "cart_x9y8z7",
        "items": [
          {
            "sku": "MRD-JACKET-BLK-M",
            "name": "Meridian Wool Jacket — Black / M",
            "qty": 1,
            "unitPriceCents": 18900,
            "availability": {
              "label": "HIGH",
              "count": 4,
              "dataSource": "CACHE",
              "syncTs": "2026-06-25T10:14:02Z"
            }
          },
          {
            "sku": "MRD-SCARF-GRY-OS",
            "name": "Meridian Cashmere Scarf — Grey",
            "qty": 2,
            "unitPriceCents": 8900,
            "availability": {
              "label": "UNKNOWN",
              "count": -1,
              "dataSource": "UNAVAILABLE",
              "syncTs": null
            }
          }
        ],
        "subtotalCents": 36700,
        "currency": "EUR"
      }
    }
  }
}
```

`availability.dataSource` tells the POS exactly what to trust:
- `CACHE` — read from Redis within TTL; reliable within 30-min window
- `SAP_FALLBACK` — live RFC/BAPI call succeeded but added ~400ms latency
- `UNAVAILABLE` — cache miss AND SAP call failed or skipped; count is -1

---

## Response — errors

GraphQL errors are returned in `errors[]` alongside `data: null`. Each error object contains `message` and `extensions.code`.

| Scenario | `extensions.code` | HTTP status | POS terminal state |
|----------|-------------------|-------------|-------------------|
| QR token not in Identity Service (expired, unknown, replayed) | `LOYALTY_QR_NOT_FOUND` | 200 | Show "Customer not found — ask for email or loyalty card number" |
| Customer has no active online cart | `CART_NOT_FOUND` | 200 | Show "No online cart — start new in-store cart" |
| All line-item availability unknown (full cache miss + SAP timeout) | `INVENTORY_DATA_UNAVAILABLE` | 200 | Show cart items but label each as "Check with floor staff before ringing up" |
| Identity Service timed out resolving QR | `IDENTITY_SERVICE_TIMEOUT` | 200 | Show "Customer lookup timed out — scan again or enter loyalty number" |
| Associate JWT expired or invalid | `UNAUTHORIZED` | 401 | Trigger terminal re-authentication flow; do not show error to customer |
| Gateway internal error | `INTERNAL_ERROR` | 500 | Show "System error — try again in 30 s; if persistent, contact support" |

**Error body example (`LOYALTY_QR_NOT_FOUND`):**
```json
{
  "data": null,
  "errors": [
    {
      "message": "QR token not found or expired",
      "extensions": {
        "code": "LOYALTY_QR_NOT_FOUND",
        "qrTokenPrefix": "eyJ...[truncated]"
      }
    }
  ]
}
```

`qrTokenPrefix`: first 8 characters of the token for logging. Never log the full token.

---

## SLO

| Path | p95 target | Hard timeout |
|------|-----------|--------------|
| Happy path (all cache hits) | ≤ 200ms | — |
| Degraded path (≥1 cache miss → SAP fallback) | ≤ 700ms | — |
| Gateway hard timeout (any path) | — | 1000ms; returns `INTERNAL_ERROR` after this |

If the Gateway does not respond within 1000ms, POS Client renders the cart from the last cached local state (if available) and shows a staleness warning. POS Client must never block the associate workflow waiting indefinitely.

---

## Idempotency and side-effects

`cartLookupByQR` is a **read-only query**. It has no side-effects:
- Does not modify cart state
- Does not create a reservation
- Does not log the lookup event (that is the Confidence Event Log's responsibility, on reservation only)

Safe to retry on timeout or transient error. Retry budget: 2 attempts, 200ms backoff.

---

## API security constraints

| Constraint | Requirement | Enforcement |
|-----------|-------------|-------------|
| GraphQL introspection | Disabled in all production and staging environments (`introspection: false` in Apollo Server config). Introspection may be enabled in local development via `APOLLO_INTROSPECTION=true` environment flag only. | CI step on every PR — Apollo Server config must be validated before deploy. An enabled introspection flag in a production build must fail the pipeline. |
| Associate JWT scope | POS terminals receive 8h RS256 tokens. A compromised terminal provides an 8h attack window on all gateway operations — introspection disabled above limits blast radius. Token revocation (mid-shift) requires an explicit invalidation call to Identity Service. | `store_id` claim in JWT must be validated server-side against `X-Store-ID` header on every request (see Authentication section above). |

---

## PII and compliance notes

- `qrToken` must be treated as a session secret — never logged in full, never cached in browser storage
- `customer.id` is a Meridian internal opaque identifier, not an email or national ID — safe to log for operational purposes
- Loyalty tier (`SILVER`, `GOLD`) is personal data under GDPR Article 4(1) — must not be stored on the POS terminal beyond the current session
- `X-Store-ID` must match the `store_id` claim in the JWT; a mismatch indicates a token used outside its authorised store → treat as `UNAUTHORIZED`
