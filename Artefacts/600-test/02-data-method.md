---
kata: 6.W.3
consumes_from: 6.W.2
date: 2026-07-27
---

# Data Generation Method — Click & Collect Test Records

1. **Tool**: Claude Sonnet 4.6 (`claude-sonnet-4-6`), prompted inline in the kata session; no production database accessed; all values are the model's synthetic output.
2. **Fields obfuscated**: `customer_name` (locale-shaped fictional names — Italian for IT, Arabic script for AE, kanji+kana for JP), `customer_email` (fictional `@meridian-test.invalid` domain per RFC 2606), `payment_method.token` (last-4 masked, type preserved), `loyalty_number` (synthetic tier+numeric string matching real format).
3. **PII replacement strategy**: shape-preserving substitution — an Italian-pattern name replaces an Italian name, a German IBAN-style token replaces a German token; no field dropped; compliant with GDPR Art. 30 non-production data requirement per Asha Sundaram's office documentation obligation.
4. **Variety dimensions — country / market band**: 5 bands in realistic records (IT, DE, JP, GB, US); edge cases add ES, AE, SE, FR, NL — 10 distinct country codes across 15 records; no two realistic records share a store_id.
5. **Variety dimensions — payment method**: Postepay, Klarna installments, Klarna slice-it (3-instalment PSD2), JCB, Visa, Mastercard, CB-Visa (French), iDEAL, Giropay, Amex — 10 distinct payment types; `psd2_sca_required` flag set per card scheme and store country.
6. **Variety dimensions — identity state**: clean single identity (×12 records), merged / ambiguous identity (E6 — loyalty_number resolves to two customer_ids), anonymous non-member with empty loyalty_number (E7), expired loyalty card (E9).
7. **Variety dimensions — language script**: Latin-Basic (R1, R4, R5), Latin-Extended with accents and ß (R2 German, E2 Spanish, E4 German), CJK + hiragana/katakana (R3 Japanese), Arabic RTL (E3 UAE) — four scripts; three-script minimum per kata requirement met and exceeded.
8. **Variety dimensions — order structure**: single-item (×8 records), two-item (R2, E1, E5), three-item (R5), nine-line-item max-boundary (E10 — 11 units across 9 SKUs); no two records share an order_id.
9. **Edge case categories covered**: cross-region semantic violation (E1), max-length name boundary (E2, ~255 chars), RTL bidi script (E3), Latin-Extended special chars (E4), PSD2 split-pay (E5), merged identity (E6), empty loyalty field (E7), impossible store_id (E8), expired loyalty token (E9), max-items boundary (E10).
10. **Intentionally missing**: records from Phase 2 markets not yet onboarded (APAC ex-Japan, LATAM, CEE) — out of scope per `00-test-plan.md`; SAP count, OMS sync age, POS sell-through, and MAPE gate values are system-state stubs configured per TC preconditions, not customer-record fields, and are absent from this data set by design.
