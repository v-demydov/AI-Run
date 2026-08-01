---
kata: 10.W.6
date: 2026-08-01
consumes: 10.W.3, 10.W.4
inputs: 02-solution.md, 03-staffing.xlsx (Balanced variant)
---

# Implementation & Rollout Plan — Meridian UC1.1 Demand-Driven Inventory Allocation Pilot

---

## 1. Milestone Table

| # | Milestone | Date | Entry criterion | Exit criterion | Owner |
|---|-----------|------|-----------------|----------------|-------|
| M0 | Contract signed | 2026-09-12 | Bid accepted | MSA + SOW countersigned; Executive Sponsor named in writing; Prosci sub-vendor engaged | EPAM Bid Manager |
| M1 | Kick-off | 2026-09-22 | M0 complete | SAP credential request letter submitted by Meridian IT; Champion candidates nominated by Programme Director; EPAM dev environment provisioned | EPAM Engagement Lead |
| M2 | Phase 0 Gate — root-cause confirmed | 2026-10-06 | M1 complete | Root-cause ≥40% allocation-driven (reason-code methodology; arbiter: Meridian Head of Retail Planning; 2-day binding ruling); POS completeness ≥80% in ≥1 pilot country; written sign-off from Meridian Programme Director (deemed granted if not received within 3 business days) | EPAM Engagement Lead |
| M3 | Bronze dataset live | 2026-10-27 | M2 exit passed; SAP credentials provisioned to EPAM dev environment | Bronze dataset (SAP + POS, 5-year) loaded; data quality report signed off by Meridian Data team; model training baseline agreed; Champion onboarding sessions 1 completed | EPAM Data Engineer 1 |
| M4 | First recommendation | 2026-12-01 | M3 exit met; ≥5 named planners committed; Executive Sponsor written mandate to planners on file | Daily SKU-level recommendations running; dashboard live with accept/reject/reason capture; ≥5 planners completed onboarding; first-week accept rate ≥30% (dashboard audit log); both Prosci planner workshops complete | EPAM ML Engineer |
| M5 | Pilot close & handover | 2026-12-15 | M4 exit met; ≥4 weeks live recommendation data collected | Phantom stock measurement report (baseline vs. pilot-close, auditable); planner adoption ≥70% (% recommendations actioned ≤48 hrs); full-rollout recommendation pack delivered to Meridian steering committee; model artefacts + documentation handed to Meridian IT | EPAM PM |

---

## 2. Governance Cadence

### 2.1 Steering Committee — Monthly

| Attribute | Detail |
|-----------|--------|
| **Frequency** | Monthly; fixed dates: 2026-10-06 (Phase 0 gate), 2026-11-03, 2026-12-01 (Phase 2 exit), 2026-12-15 (pilot close) |
| **Attendees** | Meridian Programme Director · **Executive Sponsor (CSCO, mandatory Phase 2+)** · EPAM Engagement Lead · Prosci OCM Lead |
| **Decision rights** | Scope changes (written amendment required) · phase-gate pass/fail · budget adjustments · escalations that breach manager authority · Prosci right-to-cure trigger |
| **Standing agenda** | KPI dashboard (phantom stock rate, accept rate, adoption %) · risk register Δ · phase exit criteria status · blockers requiring executive unblock |
| **Executive Sponsor** | Meridian Chief Supply Chain Officer — named individual with written authority to mandate planner participation, resolve regional GM resistance, and authorise change orders. Authority documented in the SOW. First hard deadline: written planner mandate before 2026-10-24 (Phase 2 start − 3 business days; Phase 2 begins 2026-10-28). |

### 2.2 Sprint Review / Demo — Biweekly

| Attribute | Detail |
|-----------|--------|
| **Frequency** | Biweekly; Fridays at end of each 2-week sprint |
| **Attendees** | EPAM EL, SA (Phases 0–1), MLE, DE1, PM, QA (Phase 2+) · Meridian Data team lead · 1–2 named Champions |
| **Decision rights** | Accept/reject sprint deliverables · reprioritise next sprint backlog · flag blockers to steering (EL owns escalation within 24 hrs) |
| **Standing agenda** | Sprint demo (working software or analysis output — no slide decks without artefact) · metrics update · open blockers · next sprint goal |

### 2.3 Sprint Retrospective — Biweekly (internal EPAM)

| Attribute | Detail |
|-----------|--------|
| **Frequency** | Biweekly; immediately after sprint review (same Friday) |
| **Attendees** | EPAM delivery team only: EL, SA (Phases 0–1), DE1, DE2, MLE, PM, QA · Prosci OCM Lead (Phase 2 retros) |
| **Decision rights** | Process changes within EPAM delivery scope · escalation items that require client-side action routed to EL before Monday |
| **Format** | What worked / what didn't / one process change committed for next sprint. No client attendance — psychological safety requires a separate space |

---

## 3. Change-Management Plan

> Training is the small part. The 80% that fails silently is resistance handling, adoption tracking, and a named Champion network with protected time.

### 3.1 Resistance Handling

| Resistance scenario | Who | Response pattern |
|--------------------|-----|-----------------|
| **"The model doesn't understand our assortment"** (Sceptical planner) | Pilot planners, especially high-tenure planners who own their region | EPAM ML Engineer demos the SKU-level rationale panel at Sprint 3 review — each recommendation shows the 3 signals that drove it (stock level, lead time, historical cancellation rate). Week 1 runs in **advisory mode** (no mandate to act) to remove stakes. Champion runs a 60-min peer debrief with 2–3 sceptical planners: "what would you have done; what did the model recommend; what's the delta?" before the full pilot-group launch. |
| **"Our SAP data must not leave our systems"** (Anxious Meridian IT) | Meridian IT lead and their GDPR/InfoSec compliance officer | EPAM SA runs a 30-min technical walkthrough at Phase 0 kick-off: EPAM EU-region data residency, CLIENT_CONFIDENTIAL classification under EPAM Data Classification Matrix, DPA + data-sharing rider co-signature requirement, no third-country transfer. EPAM Data Engineer maintains a live data-residency log (shared read-only with Meridian IT) throughout Phase 1. No data flows until the rider is co-signed — this is a contractual hard stop, not a goodwill gesture. |
| **"HQ is imposing a new system on my team"** (Resistant regional GM) | Germany / France regional GM (not in pilot planner group but has influence over planner morale) | Executive Sponsor issues written mandate before Phase 2 start (hard dependency — Phase 2 cannot begin without it). Prosci OCM leads two co-design sessions in Phase 2 weeks 1 and 3 where the regional GM is named co-owner of acceptance criteria (not just an attendee). If GM remains resistant after workshop 2, EPAM EL escalates to Meridian Programme Director within 24 hours with a named remediation request; Meridian's steering committee decides the resolution — EPAM cannot manufacture participation. |

### 3.2 Adoption Tracking

| Behaviour | Why it signals real adoption | Measurement | Target | Owner |
|-----------|------------------------------|-------------|--------|-------|
| **Planners add rejection reasons** | Filling in `reason_code` on rejections shows planners are engaging with model logic, not just dismissing. A blank rejection is a single click; a labelled rejection requires cognitive engagement. | Dashboard audit log: % of reject events where `reason_code ≠ NULL` | ≥50% labelled rejections by Phase 2 week 3 | EPAM ML Engineer |
| **Champions log in without prompting** | An unprompted session (no scheduled demo, no workshop in prior 48 hrs) means the Champion has internalised the tool into their work routine. Prompted logins signal compliance; unprompted logins signal adoption. | Session log: unprompted login count per Champion per week (flag: session preceded by no meeting invite in 48 hrs) | ≥3 unprompted sessions/Champion/week by Phase 2 week 3 | EPAM Data Engineer 1 |
| **Accept rate weekly trend** | Week-over-week improvement from the Phase 2 exit floor (≥30%) toward the Phase 3 target (≥70%) shows planners are building trust, not just satisfying the measurement gate. A flat line after week 1 signals the minimum-viable behaviour, not real adoption. | Dashboard audit log: 7-day rolling accept rate | +5pp/week sustained improvement weeks 2–4 | Prosci OCM Lead, verified by EPAM EL |

### 3.3 Champion Network — EPAM AI Champion Playbook Alignment

The L3 rollout names who **runs** adoption, not only who attends ceremonies. Champions are internal client advocates with protected time to test, relay, and model the new workflow for peers — not ceremonial sponsors.

| Role | Who | Protected time | Responsibilities | Backup |
|------|-----|---------------|-----------------|--------|
| **Champion — Germany Pilot** | Named planner; ≥2 years planning experience; nominated by Meridian Programme Director, confirmed in writing by Executive Sponsor before Phase 1 end | **20% (1 day/week)** during Phase 2 (weeks 6–10) | Tests recommendations before broader planner rollout · runs weekly 30-min peer review session with 2–3 non-Champion planners · relays model-quality feedback to EPAM ML Engineer via structured form · serves as first-line escalation for planner adoption concerns · co-facilitates Prosci workshop 2 | 1 named backup planner; receives same onboarding; activated if Champion is absent >3 consecutive days |
| **Champion — France Pilot** | Same criteria as Germany Champion; activated only if France POS completeness ≥80% at Phase 0 gate | 20% during Phase 2 (same as Germany) | Same as Germany Champion; operates independently for France planner cohort | 1 named backup; same criteria |
| **EPAM OCM Liaison (internal)** | EPAM Engagement Lead (point of contact for Prosci sub-vendor) | 10% during Phase 2 | Reviews all Prosci deliverables before presenting to Meridian · attends both Prosci planner workshops as EPAM observer · owns escalation from Prosci to EPAM Delivery Director if adoption KPIs are missed · signs off Prosci attendance lists and readiness survey results | EPAM PM (backup for OCM liaison if EL is travelling) |

**Champion onboarding:** 2 × half-day sessions — session 1 at Phase 1 end (dashboard walkthrough + model rationale), session 2 at Phase 2 week 1 (facilitated by Prosci). Champions are briefed on all three adoption-tracking metrics and asked to report on them weekly to the EPAM OCM Liaison.

---

## 4. Stakeholder Map

| Stakeholder | Interest | Influence | Key concerns | Engagement signal to monitor |
|-------------|----------|-----------|--------------|-------------------------------|
| **Meridian Programme Director** | Successful pilot delivery; on-time and within budget; credible handover to full-rollout business case | **H** | Scope creep adding cost; missed milestones creating reputational risk internally; Phase 3 measurement report used to challenge the full-rollout award | Attends every steering call · responds to weekly written status within 48 hrs · signs phase gates without requesting extensions · no escalations land at Executive Sponsor without passing through Programme Director first |
| **Executive Sponsor (Meridian CSCO)** | AI investment delivers measurable ROI; pilot becomes the reference case for 8-country expansion; Board-level optics on AI governance | **H** | Phantom stock rate doesn't move in 12 weeks (too short); regional GM resistance surfaces publicly; data privacy incident derails expansion narrative | Issues written planner mandate on schedule · attends Phase 3 steering · references pilot in internal comms (signal of advocacy, not just ownership) · asks for the Phase 3 measurement report ahead of the steering call (signals genuine interest in outcome) |
| **Pilot Planners (≥5, Germany)** | Tools that make daily work easier, not harder; model recommendations they can trust and override without bureaucracy | **M** | "Black box" decisions they can't explain to their manager · extra workflow step without visible benefit · job threat perception ("is this replacing me?") | Champion unprompted login rate · reject reason_code fill rate · accept rate week-over-week trend · planner NPS in Prosci readiness survey (pre/post) |
| **Meridian IT (SAP owner)** | No security incidents; no compliance exposure; predictable workload and no hidden SAP performance impact from batch extraction | **M** | SAP data exiting the ERP environment · DPA coverage gap between EPAM and Prosci · SAP extraction job conflicting with end-of-month batch windows | Provisions SAP credentials by Day 5 (hard dependency) · responds to EPAM data-residency log queries within 2 business days · raises no unresolved InfoSec queries after DPA co-signature · no SAP performance complaints during Phase 1 extraction runs |

---

## 5. Comms Plan

Cadence is derived from the stakeholder map quadrant, not from politeness. High-influence stakeholders need early warning before surprises; medium-influence high-interest stakeholders need frequent lightweight touchpoints to build trust in the tool.

### Audience A — Meridian Programme Director (High influence / High interest → manage closely)

| Item | Detail |
|------|--------|
| **What they get** | Weekly written 3-bullet status pack (progress since last week · current blockers · next week plan) + monthly steering deck (KPI dashboard, risk register delta, phase gate status, decisions needed) |
| **Channel** | Email (weekly status) · MS Teams call (monthly steering) · direct message (same-day if a blocker is unresolved >2 business days) |
| **Cadence** | Weekly written + monthly live; escalation message same-day on unresolved blockers — **not** deferred to next weekly email |
| **Owner** | EPAM Engagement Lead |
| **Why this cadence** | High influence means a surprise at steering destroys trust faster than anywhere else. Weekly written status removes surprises by providing a paper trail of what was flagged and when. The same-day escalation rule means no blocker sits in silence over a weekend. |

### Audience B — Pilot Planners (Medium influence / High interest in daily tool → keep informed, build pull)

| Item | Detail |
|------|--------|
| **What they get** | Biweekly sprint demo (Champion-facilitated, 30 min, showing new dashboard features and model improvements); in-dashboard adoption nudge at login (weekly recommendation summary: "last week you accepted 4 of 10 recommendations — here is what happened to the 6 you rejected"); weekly 30-min Champion-led peer session (no EPAM presence — Champion owns this space) |
| **Channel** | In-dashboard notification · Champion-led in-person session · Prosci workshop (Phase 2 weeks 1 and 3) · **no large group emails** |
| **Cadence** | Biweekly demo + weekly Champion session — **no monthly all-hands** for this audience |
| **Owner** | Prosci OCM Lead (workshop design) · Champion (peer sessions) · EPAM ML Engineer (sprint demo) |
| **Why this cadence** | Planners need frequent low-stakes exposure to build trust in model recommendations before the adoption target kicks in. A monthly briefing creates a 3-week gap where adoption drifts and the Champion network goes cold. The in-dashboard nudge provides a continuous signal between sessions without requiring planners to attend anything. The weekly Champion session has no EPAM presence because peer trust transfers faster than vendor trust. |

**Why the two cadences differ:** Programme Director needs early-warning authority (weekly written + same-day escalation for blockers). Pilot Planners need repetition and peer-to-peer trust (frequent lightweight, Champion-owned, no vendor in the room). One cadence serving both audiences would produce either over-communication to the Director or under-communication to the planners.

---

## 6. Quality and Risk Gates — Governance Alignment

The governance cadence enforces the same gates named in the QA test report (M600) and security evidence pack (M900) so milestones match the real delivery shape:

| Gate | Governance event | Who decides | Escalation if not met |
|------|-----------------|-------------|----------------------|
| Phase 0 root-cause ≥40% | Steering committee 2026-10-06 | EPAM EL + Meridian Programme Director (arbiter: Head of Retail Planning for disputed codes) | EPAM invoices Phase 0 only; SOW amendment required for Phase 1 restart |
| POS completeness ≥80% | Steering committee 2026-10-06 | Meridian Data team (EPAM EL observes) | Pilot restricted to higher-quality country; if both fail, Phase 1 paused pending Meridian data remediation |
| Bronze data quality sign-off | Sprint review at M3 | Meridian Data team lead | Phase 2 start deferred; SAP buffer contingency activated |
| Dashboard acceptance | Sprint review preceding M4 | EPAM QA + Meridian Data team lead | MLE holds sprint; fixes before Phase 2 exit clock starts |
| Accept rate ≥30% (week 1) | Steering committee 2026-12-01 | EPAM EL + Prosci OCM Lead | Prosci right-to-cure: facilitation repeated with Executive Sponsor involvement; if ≥70% adoption not achieved by week 8, Phase 3 report states this explicitly and full-rollout recommendation is conditional |
| Model artefact handover | Steering committee 2026-12-15 | Meridian IT + EPAM PM | PM holds pilot-close until documentation complete; no final invoice until Meridian IT countersigns handover checklist |
