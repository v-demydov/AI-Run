---
feature: availability-confidence
kata: 3.W.7
date: 2026-06-24
handoff-for: AI coding agent / Three-Amigos review
sources: 04-ai-ac.md · 05-mockup.html · 06-context.md
definition-of-handoff-done: see §7
---

# SPEC — Availability Confidence Feature

---

## §1 User Story + Base AC

**Story:**
As a click-and-collect shopper deciding whether to make a pickup trip,
I want to see how confident the system is that the item will be on the shelf at my chosen store before I confirm the reservation,
so that I only commit to the trip when the signal is trustworthy and I can redirect before I leave home.

**Base AC (supplied, non-AI):**

| # | When | Then |
|---|------|------|
| AC1 | Product has store stock data | Show ConfidenceBadge per nearby store in AvailabilityCard |
| AC2 | No store within range has the item | Show "Not collectable nearby" + delivery option |
| AC3 | Stock data missing for a store | Omit that store — do not guess or show a stale positive |
| AC4 | User taps a store | Show last-confirmed time (StalenessBadge) + distance |

---

## §2 Design Tokens

All token values are lo-fi defaults from the prototype. Override with the project design system if one exists.

```
/* Confidence colours */
--color-confidence-high-text:       #4caf50
--color-confidence-high-bg:         #1a3a1a
--color-confidence-high-border:     #4caf50

--color-confidence-medium-text:     #ffc107
--color-confidence-medium-bg:       #2a2a0a
--color-confidence-medium-border:   #ffc107

--color-confidence-low-text:        #f44336
--color-confidence-low-bg:          #2a0a0a
--color-confidence-low-border:      #f44336

--color-confidence-fallback-text:   #888888
--color-confidence-fallback-bg:     #1a1a1a
--color-confidence-fallback-border: #555555

/* Staleness indicator */
--color-staleness-fresh:   #555555   /* < 15 min */
--color-staleness-aging:   #ffc107   /* 15–30 min */
--color-staleness-stale:   #f44336   /* > 30 min */

/* Modal */
--color-modal-bg:          #1a1a1a
--color-modal-border:      #f44336   /* always Low-state colour */
--color-modal-title:       #f44336
--color-modal-body:        #cccccc

/* Typography */
--font-badge-size:         11px
--font-badge-weight:       700
--font-badge-spacing:      0.5px
--font-staleness-size:     10px
--font-staleness-weight:   400
--font-modal-title-size:   12px
--font-modal-body-size:    11px
--font-modal-body-lh:      1.5
```

---

## §3 Components

---

### Component A — ConfidenceBadge

**Purpose:** Displays the three-state confidence signal for a store–SKU combination.

**Variants and states:**

| Variant | Trigger condition | Copy | Text token | BG token | Border token |
|---------|-------------------|------|------------|----------|--------------|
| `high` | posterior ≥ 0.85 AND count > 0 AND SAP age ≤ 4h AND circuit breaker OFF | "Likely available" | `--color-confidence-high-text` | `--color-confidence-high-bg` | `--color-confidence-high-border` |
| `medium` | posterior 0.50–0.84 (same preconditions) | "May vary — check before travelling" | `--color-confidence-medium-text` | `--color-confidence-medium-bg` | `--color-confidence-medium-border` |
| `low` | posterior < 0.50 (same preconditions) | "May not be available" | `--color-confidence-low-text` | `--color-confidence-low-bg` | `--color-confidence-low-border` |
| `fallback` | SAP age > 4h OR count ≤ 0 OR POS data unavailable OR circuit breaker ON | "Availability unknown" (if no OMS cache) OR "In stock (last known)" (if OMS cache present) | `--color-confidence-fallback-text` | `--color-confidence-fallback-bg` | `--color-confidence-fallback-border` |

**Typography:** `--font-badge-size` / `--font-badge-weight` / `--font-badge-spacing`

**Placement:**
- Inside `AvailabilityCard`, below `store-name` and `store-meta`
- Above `StalenessBadge`
- Loaded asynchronously — placeholder space must be reserved to avoid layout shift

**AI-AC refined (6 slots):**
```
Component:    ConfidenceBadge
Variant:      high
Color token:  text --color-confidence-high-text on bg --color-confidence-high-bg
Typography:   --font-badge-size / --font-badge-weight / --font-badge-spacing
Placement:    AvailabilityCard > below store-meta > above StalenessBadge; async load
Visual gate:  Must NOT render `high` variant if posterior < 0.85, count ≤ 0, SAP > 4h,
              or circuit breaker active (rolling 24h High-correctness < 75%);
              auto-switch to `fallback` variant when any gate fails — never hide silently
```

**Linked AC:** AI-AC1 (confidence threshold), AI-AC2 (refusal trigger), AI-AC6 (negative — must not emit `high` under listed conditions)

---

### Component B — StalenessBadge

**Purpose:** Displays signal age ("Updated N min ago") to satisfy disclosure requirement.

**Variants and states:**

| Variant | Condition | Copy | Color token |
|---------|-----------|------|-------------|
| `fresh` | Signal age < 15 min | "Updated N min ago" | `--color-staleness-fresh` |
| `aging` | Signal age 15–30 min | "Updated N min ago" | `--color-staleness-aging` |
| `stale` | Signal age > 30 min OR SAP stale trigger | "Stock data may be outdated — check in store before travelling" | `--color-staleness-stale` |
| `unknown` | Timestamp cannot be determined | "Update time unavailable" | `--color-staleness-fresh` (muted) |

**Typography:** `--font-staleness-size` / `--font-staleness-weight`

**Placement:**
- Directly below `ConfidenceBadge` in `AvailabilityCard`
- Repeated inside `FrictionModal` below modal body text
- Must ALWAYS be present when any `ConfidenceBadge` variant is shown (including `fallback`)

**AI-AC refined (6 slots):**
```
Component:    StalenessBadge
Variant:      stale
Color token:  --color-staleness-stale (#f44336)
Typography:   --font-staleness-size (10px) / --font-staleness-weight (400)
Placement:    AvailabilityCard > directly below ConfidenceBadge;
              also inside FrictionModal below body paragraph
Visual gate:  Must be present whenever ConfidenceBadge renders (any variant);
              must NOT be suppressed if timestamp unknown — render `unknown` variant instead;
              `stale` variant copy must include call-to-action ("check in store")
```

**Linked AC:** AI-AC4 (disclosure — signal age must be shown), AI-AC2 (fallback staleness notice)

---

### Component C — FrictionModal

**Purpose:** Intercepts the Reserve tap when selected store confidence = Low; gives the shopper an informed exit before committing to the trip.

**States:**

| State | Trigger | Description |
|-------|---------|-------------|
| `hidden` | Default | Not rendered |
| `visible` | Reserve tapped AND store = Low AND confidence score ≤ 10 min old | Rendered as focus-trapped overlay |
| `refetching` | Reserve tapped AND confidence score > 10 min old | Silent re-fetch before evaluating; show modal if re-fetch returns Low OR if re-fetch fails |
| `stale-shown` | Re-fetch failed or timed out (> 500ms) | Show modal as precaution (fail-safe, not fail-silent) |

**Anatomy:**
```
FrictionModal
├── title:       "May not be available"  (--color-modal-title, --font-modal-title-size, bold)
├── body:        "Our system suggests this item may not be on the shelf at [store name]
│                when you arrive."  (--color-modal-body, --font-modal-body-size, lh 1.5)
├── note:        "Updated [N min ago] · This is an estimate — not a committed hold."
│                (StalenessBadge embedded; --color-staleness-* based on age)
├── btn-primary: "Choose another store"  [initial keyboard focus]
└── btn-ghost:   "Reserve anyway"  [de-emphasised; explicit opt-in]
```

**Accessibility (hard requirements):**
- `role="dialog"` `aria-modal="true"` on modal container
- `aria-describedby` points to body + note paragraph IDs
- Focus trapped inside modal while visible
- Initial focus: `btn-primary` ("Choose another store") — NOT `btn-ghost`
- ESC key: closes modal, returns focus to Reserve button, does NOT place reservation

**AI-AC refined (6 slots):**
```
Component:    FrictionModal
Variant:      visible (Low-confidence intercept)
Color token:  border --color-modal-border; title --color-modal-title; bg --color-modal-bg
Typography:   title --font-modal-title-size/bold; body --font-modal-body-size/--font-modal-body-lh
Placement:    Absolute overlay within ProductPage container; vertically centred;
              role="dialog" aria-modal="true"; focus-trapped; aria-describedby on body
Visual gate:  Must NOT render for Medium or High confidence stores;
              btn-primary ("Choose another store") gets initial focus — never btn-ghost;
              must render when re-fetch fails (fail-safe) — never fail-silent
```

**Linked AC:** AI-AC4 (disclosure — non-guarantee note inside modal), AI-AC6 negative (must not appear for Medium/High), S4 AC from `04-stories-acs.md`

---

## §4 Data / Asset References

| Reference | Type | Path / Description | Required for |
|-----------|------|-------------------|--------------|
| Confidence API response | JSON | `GET /api/v1/confidence?storeId=&sku=` → `{ label, posterior, model_version, oms_sync_ts }` | ConfidenceBadge, StalenessBadge |
| OMS snapshot cache | Internal | Background process populates cache; TTL ≤ 30 min; agent reads cache, not live SAP | Fallback path |
| Reservation event log | Write | `POST /api/v1/confidence-log` (fire-and-forget) → `{ reservation_id, store_id, sku, label, posterior, model_version, oms_sync_ts }` | AI-AC5 feedback logging |
| Prototype reference | HTML | `300-design/05-mockup.html` — Scenario A (High), B (Low + modal), C (Fallback) | Visual reference for states |

---

## §5 Negative AC carried into SPEC

These are absolute prohibitions. Each is a separate test case; any violation is a **release blocker**.

| # | MUST NOT | Condition | Component affected |
|---|----------|-----------|-------------------|
| N1 | Render `high` variant | SAP count ≤ 0 | ConfidenceBadge |
| N2 | Render `high` variant | SAP sync age > 4h | ConfidenceBadge |
| N3 | Render `high` variant | Rolling 24h High-correctness < 75% (circuit breaker active) | ConfidenceBadge |
| N4 | Render any confidence label | OMS snapshot age > 30 min — show "Availability unknown" | ConfidenceBadge |
| N5 | Use hold-implying copy | Any state — "reserved for you", "guaranteed", "confirmed in stock", "we're holding it" | ConfidenceBadge, FrictionModal, StalenessBadge |
| N6 | Place initial focus on "Reserve anyway" | FrictionModal visible | FrictionModal |
| N7 | Block page render | Confidence API slow or unavailable | ConfidenceBadge (async load) |
| N8 | Block reservation response | Logging service unavailable | Reservation event log (fire-and-forget) |

---

## §6 Open Questions for Three-Amigos

| # | Question | Blocks |
|---|----------|--------|
| Q1 | What is the exact JSON schema of the confidence API response? Agent needs `label`, `posterior`, `model_version`, `oms_sync_ts` fields confirmed. | ConfidenceBadge, StalenessBadge |
| Q2 | What placeholder renders while ConfidenceBadge loads asynchronously? Skeleton, grey badge, or nothing? | AvailabilityCard layout shift |
| Q3 | Is the 10-minute TTL for modal re-fetch measured from page load or from last API response? | FrictionModal `refetching` state |
| Q4 | Copy sign-off: "May vary — check before travelling" (medium) and "Stock data may be outdated — check in store before travelling" (stale) — confirmed? | StalenessBadge `stale`, ConfidenceBadge `medium` |

---

## §7 Definition of Handoff Done

| # | Check | Status |
|---|-------|--------|
| 1 | User story + base AC present | ✅ §1 |
| 2 | ≥ 3 AI-AC refined to component / variant / token / placement / visual gate | ✅ §3 — ConfidenceBadge `high`, StalenessBadge `stale`, FrictionModal `visible` |
| 3 | CONTEXT.md covers feature + audience + environment + constraints + out-of-scope | ✅ `06-context.md` |
| 4 | SPEC.md lists ≥ 2 components with states + token references | ✅ §3 — 3 components, all states, all tokens |
| 5 | Asset / data reference explicit and resolvable | ✅ §4 — API path, cache source, log endpoint, prototype path |
| 6 | Negative AC ("must NOT") carried into SPEC.md | ✅ §5 — 8 prohibitions, each a named test case |
