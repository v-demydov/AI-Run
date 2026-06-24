---
product: Meridian click-&-collect (product detail page)
date: 2026-06-24
sources: 04-ai-ac.md · 05-mockup.html · 03-decision.md
prototype: 300-design/05-mockup.html (Scenarios A, B, C)
---

# Validation Plan: Availability Confidence Feature

---

## Method

**Moderated usability test** on the clickable prototype (`05-mockup.html`).
5 task-based questions — no preference questions, no leading cues.
Recommended: 5–8 participants, C&C shoppers who have made a pickup in the last 90 days.

**Session structure:** 45 min · 5 min intro + consent · 30 min tasks · 10 min debrief
**Observer rule:** facilitator does not explain the feature before tasks begin.
**Pass threshold per task:** ≥ 7 of 10 participants complete without facilitator intervention.

---

## Task Questions

---

### Task 1 — Confidence signal (happy path / Scenario A)

> "You're looking to pick up this item today at a store near you. Show me how you'd figure out whether it's worth making the trip before you reserve."

**What we're testing:**
- Does the shopper notice the confidence label unprompted?
- Do they read "Likely available" as an estimate rather than a guarantee?
- Do they notice the "Updated N min ago" staleness badge?

**Success condition:** Participant references or interacts with the ConfidenceBadge before tapping Reserve, without facilitator pointing to it.

**Pass threshold:** ≥ 7 / 10

**Linked AC:** AI-AC1 (confidence visible before commit), AI-AC4 (disclosure)

---

### Task 2 — Signal recency (staleness comprehension)

> "The product page is showing you some availability information for a store. Show me how you'd decide whether that information reflects what's on the shelf right now."

**What we're testing:**
- Does the shopper find and interpret the staleness badge?
- Do they understand that the signal is an estimate from N minutes ago, not a live count?
- Does "May vary — check before travelling" (Medium badge) communicate uncertainty?

**Success condition:** Participant can state the signal age (or describe it as "not live") without facilitator prompting.

**Pass threshold:** ≥ 7 / 10

**Linked AC:** AI-AC4 (disclosure — signal age shown), StalenessBadge `aging` variant

---

### Task 3 — Low-confidence friction modal (Scenario B)

> "You want to reserve this item at Oxford Street. Go ahead and try to reserve it."

*[Prototype starts at Scenario B — store shows Low confidence.]*

**What we're testing:**
- Does the modal stop the shopper before the trip commitment?
- Do they understand the modal as a warning, not an error?
- Does "Choose another store" (primary) vs "Reserve anyway" (secondary) communicate the intended hierarchy?
- Does the shopper feel in control, not blocked?

**Success condition:** Participant reads the modal body before taking an action; they can say unprompted which action the system recommends.

**Pass threshold:** ≥ 7 / 10 read and acknowledge modal content before choosing.

**Failure signal to watch for:** Shopper taps "Reserve anyway" immediately without reading — modal is not friction-effective.

**Linked AC:** AI-AC4 (non-guarantee copy), AI-AC6 (modal must not appear for High/Medium), S4 AC

---

### Task 4 — Fallback state comprehension (Scenario C)

> "You open the product page and see this. Show me what you'd do next."

*[Prototype starts at Scenario C — "Availability unknown" / SAP stale.]*

**What we're testing:**
- Does the shopper understand "Availability unknown" means the system cannot give an estimate?
- Do they know to verify before travelling (call the store or not reserve)?
- Does "Stock data may be outdated — check in store before travelling" communicate action?

**Success condition:** Participant does NOT tap Reserve without first noting the uncertainty; they mention calling the store, choosing another store, or waiting.

**Pass threshold:** ≥ 7 / 10 do not proceed directly to reservation under fallback state.

**Failure signal to watch for:** Shopper reads "In stock (last known)" as a guarantee and reserves without hesitation — this is the AI-AC6 N4 violation in user perception.

**Linked AC:** AI-AC2 (refusal/fallback), AI-AC4 (disclosure), N4 (must not show clean positive)

---

### Task 5 — Store comparison under uncertainty

> "You need this item today and you're not sure which store is best. Show me how you'd choose between Oxford Street and Westfield using this page."

*[Prototype at Scenario B — Oxford Street = Low, Westfield = High.]*

**What we're testing:**
- Does the shopper use confidence labels to choose between stores (not just distance)?
- Does the inline alternatives layout surface the better store without navigation?
- Does "Likely available" at Westfield make the choice feel resolved, not reluctant?

**Success condition:** Participant selects the higher-confidence store (Westfield) OR explicitly weighs confidence against distance as a stated factor.

**Pass threshold:** ≥ 7 / 10

**Linked AC:** B-i1 (inline alternatives), AI-AC4 (comparative labels legible)

---

## Risk list

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Shoppers don't distinguish "Likely available" from "confirmed in stock" | High | Task 1 + Task 2 directly test this; if >3/10 fail, copy must be revised before shipping |
| Modal is ignored (tapped through immediately) | High | Task 3 measures this; if >3/10 tap "Reserve anyway" without reading, increase friction (e.g., timed delay on secondary button) |
| "Availability unknown" read as "In stock" | High | Task 4 measures this; any failure here is a release blocker — AI-AC6 N4 |
| Staleness badge not noticed | Medium | Task 2 measures this; if >3/10 miss it, increase typographic contrast or move badge above ConfidenceBadge |
| Shopper feels blocked rather than informed at Low | Medium | Task 3 debrief; ask "how did that feel?" — frustration without understanding is a redesign signal |
