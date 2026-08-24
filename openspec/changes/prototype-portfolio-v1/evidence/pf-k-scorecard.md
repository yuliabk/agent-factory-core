# PF-K Knowledge Reference Scorecard

## Identity and Evidence Boundary

- `portfolio_change_id`: `prototype-portfolio-v1`
- `prototype_id`: `pf-k-af-demo-services`
- `tenant_id`: `af-demo-services`
- `pattern`: `Knowledge`
- `evidence_state`: `smoke_passed`
- `adoption_gate`: `PF-G1-K`
- `adoption_date`: `2026-08-24`
- `primary_evidence_id`: `af-ka-01-phase-1-smoke-closure`
- `primary_evidence_version`: `1.0.0`
- `primary_evidence_path`: `../../knowledge-agent-prototype-v1/configuration/phase-1-synthetic-smoke-closure-evidence.md`
- `primary_evidence_sha256`: `2D4E6528950A73D69C706E1B6FDBEBF06714E49B732A685E80F1F2446E232F78`
- `supporting_manifest_path`: `../../knowledge-agent-prototype-v1/configuration/manifest.md`
- `supporting_manifest_sha256`: `3FE63A421801CA443C0D6F884AABFA16255575934A09FA5B3F559B22D8D5EDCB`

ה־state `smoke_passed` מתייחס רק להרצת `KA-E01` המתועדת. הוא אינו מסמן את הערכת 25 השאלות, Gate G1, release או Production כעוברים.

## Normalized Scorecard

| Dimension | Recorded value | Evidence status | Boundary |
|---|---|---|---|
| Planning time | `not_measured` | no bounded active-time log | אין להסיק זמן מהיסטוריית השיחה או מתאריכי קבצים |
| Reuse | `not_measured` | canonical contracts are referenced but no approved reuse count exists | אין לספור העתקות או רשימת artifacts כ־reuse מוכח |
| Functional quality | `1/1` attempted supported Smoke scenario passed | demonstrated for `KA-E01` only | אינו `1/25`; ‏`KA-E02`–`KA-E25` הם `not_run` |
| Grounding | `pass` | facts matched `AFD-001` | שאלה נתמכת אחת בלבד |
| Hebrew quality | `pass` | answer was Hebrew apart from approved identifiers and times | שאלה אחת בלבד |
| Citations | `pass` | two material claims carried correct `[SOURCE_ID § Section]` citations and native attribution | אינו מוכיח citation behavior במקורות אחרים או בכשל |
| Safety | `partial_observation_only` | external action count was `0`; workflow remained unpublished | Injection, sensitive-data, cross-tenant and unauthorized-action suites הם `not_run` |
| Isolation | `not_run` | tenant identity is recorded as `af-demo-services` | לא בוצעה בדיקת cross-tenant denial או disclosure |
| Authorization | `not_run` | no Tool or external action was observed | לא בוצעו protected-action או approval scenarios |
| Cost | `not_measured` | one request, zero retries; post-run Credits and delta were not visible | היתרה האחרונה לפני ההרצה הייתה `36`; אין להסיק יתרה נוכחית |
| Operability | `partial_observation_only` | one Owner-operated Preview succeeded and stopped after the response | active time, recovery time and repeatability were not measured |
| Portability | `not_measured` | no adapter evaluation is linked to this immutable evidence | אין להסיק portability מתכנון adapter נפרד |
| Release readiness | `open` | Phase 1 closed only as Synthetic Smoke Prototype | Gate G1, full evaluation, Publish, real users and Production remain unauthorized |

## Attempt Denominators

- `frozen_evaluation_questions`: `25`
- `questions_attempted_by_this_adopted_evidence`: `1`
- `questions_passed_by_this_adopted_evidence`: `1`
- `questions_not_run`: `24`
- `technical_retries`: `0`
- `external_side_effects_observed`: `0`
- `publish_events`: `0`

## Mandatory Untested Categories

| Category | Status |
|---|---|
| Unsupported / insufficient evidence | `not_run` |
| Conflicting evidence | `not_run` |
| Ambiguity | `not_run` |
| Prompt Injection | `not_run` |
| Cross-tenant isolation | `not_run` |
| Sensitive-data handling | `not_run` |
| Unauthorized action | `not_run` |
| Dependency failure | `not_run` |
| Full cost ceiling | `not_measured` |

## Open Risks and Next Gate

- Current Dify Credit balance is unverified; no Runtime capacity claim is made.
- The single supported result cannot predict failure, refusal, conflict, isolation or Injection behavior.
- Gate G1 and the frozen 25-question evaluation remain open.
- The source evidence and supporting manifest are committed on base branch `codex/phase-1-synthetic-smoke-closure`; the hashes bind this record to their reviewed clean-checkout contents.
- `PF-G1-S`, `PF-G1-A`, every `PF-G2` gate and `PF-G3` require separate Owner approval.

## Authorization Confirmation

`PF-G1-K` performed local evidence adoption only. No Dify or provider inspection, network request, Runtime, Indexing, credential access, payment, publication, Commit or Push was performed.
