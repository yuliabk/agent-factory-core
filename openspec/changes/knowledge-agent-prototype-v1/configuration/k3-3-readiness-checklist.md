# K3.3 Readiness Checklist — Dify Cloud Sandbox

## Status

- `checklist_id`: `af-ka-01-k3-3-readiness`
- `version`: `3.6.0`
- `previous_version`: `3.5.0`
- `date`: `2026-08-20`
- `intended_runtime`: `Dify Cloud Sandbox`
- `overall_status`: `k4_0_capacity_plan_complete_k4_1c_not_granted`
- `provider_action_status`: `d3w_persisted_d3t_smoke_pass`
- `current_authorized_stage`: `none`
- `account_status`: `existing_owner_account_authenticated_by_owner`
- `indexing_status`: `all_six_documents_indexed_available`
- `runtime_status`: `one_request_citation_pass_36_remaining_full_evaluation_blocked_unpublished`
- `credentials_status`: `not_connected`
- `paid_execution_status`: `not_authorized`

## Purpose and Authorization Boundary

Checklist זה מרכז את הראיות שנאספו ואת גבולות ההרשאה לפני כל Stage נוסף של K3.3. הוא אינו מהווה הרשאה לשלב נוסף.

D3A בוצעה חלקית ונעצרה בבטחה. שישה ערכי metadata מסוג `source_id` נשמרו, וצומת `Citation Context` מחובר ל-`Knowledge Retrieval / result` השלם. Dify לא הציג נתיב nested של `source_id` או document metadata לבחירה, ולכן לא נוחש נתיב Jinja ולא בוצע חיבור ל-LLM. לא נצרכו Credits והיתרה נשארה 48.

D3B הושלמה מקומית בלבד. קוד המקור הרשמי של Dify מציב metadata מותאם תחת `metadata.doc_metadata`, בעוד שה-UI מציג `metadata` כאובייקט אטום. נבחר `M-DOCMETA-TEMPLATE` עם allow-list ו-fail-closed. לא בוצע שינוי נוסף ב-Dify, ו-D3S דורש אישור נפרד.

D3S נעצרה בבטחה. עורך הקוד לא קיבל את התבנית הרב-שורתית באופן אטומי; המצב השגוי זוהה, `{{ results }}` שוחזר ואומת לאחר Reload. לא בוצעו graph wiring או prompt editing, לא נצרכו Credits והיתרה נשארה 48. נדרשת הדבקה ידנית לפני D3SR לקריאה בלבד.

לפני D3SR ה-Owner אישרה שגם הפעילה Preview לאחר ההדבקה; הוא החזיר את תגובת חוסר-המידע הקנונית והוריד את היתרה מ-48 ל-42. לא בוצעה חזרה. D3SR עצמה אימתה את התבנית לקריאה בלבד. D3W חיברה את `Citation Context` בין Retrieval ל-LLM, שמרה את Retrieval Context לייחוס Dify והוסיפה `Citation Context / output` ל-System prompt. D3T הריצה את KA-E01 פעם אחת: העובדות, העברית ושני הציטוטים עברו; נצרכו 6 Credits ונשארו 36. האפליקציה נשארה Unpublished.

## Readiness Summary

| Gate | Current status | Decision |
|---|---|---|
| Scope and synthetic data | `pass_local` | הקורפוס, ה-tenant, ה-Owner והשפה קפואים ומאושרים |
| Runtime decision | `smoke_materialized_unpublished` | ADR-004 בחר Dify Cloud Sandbox; משאבי הסינתטי הוגדרו והאפליקציה נשארה Unpublished |
| Dify mapping | `smoke_validated_synthetic_only` | חמשת הצמתים, `gpt-4.1-mini`, Knowledge Context ו-Citation Context נשמרו ועברו KA-E01 |
| Region and data flow | `residual_risk_accepted_synthetic_only` | OpenAI נבחר ל-Generation/Embedding; Region מדויק נשאר לא ידוע ומתקבל לסינתטי בלבד |
| Export and restore | `pass_manual_reconstruction_planned` | DSL, Git corpus ו-Runbook שחזור מלאים מקומית; Restore בפועל נשאר פעולה מאושרת עתידית |
| Deletion and retention | `residual_risk_accepted_synthetic_only` | מחיקה ו-30 ימי Logs מתועדים; Backup/cache retention אינו ידוע ומתקבל רק לנתונים סינתטיים |
| Isolation and access | `partial_pass_owner_only_current_state` | Member יחיד; App ו-Knowledge ייעודיים לסינתטי; האפליקציה Unpublished וללא Tool או integration |
| Cost controls | `k4_0_planned_waiting_for_renewal` | 164/200 Credits בשימוש ו-36 זמינים; נדרשים 180 Credits עבור 25 שאלות ועד 5 retries. נבחרה המתנה לחידוש Sandbox ושער K4.1C לקריאה בלבד, שטרם אושר |
| Hebrew quality | `ka_e01_factual_and_citation_pass` | KA-E01 עברה עובדתית ובעברית עם שני ציטוטי `[SOURCE_ID § Section]` נכונים |
| K3.3 Owner approval | `d3c_consumed_no_current_stage` | D3SR, D3W, D3T ו-D3C הושלמו; כל Runtime נוסף ו-K4 דורשים Stage נפרד |

כל Gate המסומן `blocked_*`, `pending_*`, `not_tested` או `not_granted` מונע מעבר אוטומטי ל-K4.

## A. Scope, Identity and Data

- [x] Agent: `AF-KA-01 - Synthetic Knowledge Agent`.
- [x] Tenant קבוע: `af-demo-services`.
- [x] Actor type: `Owner` בלבד.
- [x] Corpus קבוע: `af-demo-services-he@1.0.0` בלבד.
- [x] Evaluation set קבוע: `ka-prototype-he-v1`, 25 שאלות.
- [x] Classification: `synthetic` בלבד.
- [x] Language: Hebrew בלבד.
- [x] External tools, browsing, channels, writes and side effects: disabled by policy.
- [ ] לפני כל פעולה עתידית, לבצע Hash verification מחדש מול Corpus manifest.
- [ ] לפני כל העלאה עתידית, לסרוק מחדש שאין PII, Secrets, URLs או מידע אמיתי.

## B. Local Mapping to Dify

המיפוי הנוכחי הוגדר חלקית ונבדק בשאלת Smoke אחת. אם Dify אינו תומך במיפוי מדויק, אין לבצע תחליף שקט; מעדכנים Configuration version ומבקשים Owner review.

| Factory artifact | Intended Dify mapping | Local status | External verification required |
|---|---|---|---|
| `AF-KA-01` | Owner-only five-node Chatflow with no tools | smoke validated | Verify sharing controls before any later release |
| Corpus manifest | One dedicated Knowledge Base for `af-demo-services` | mapped | Verify metadata and status filtering behavior |
| `AFD-001`–`AFD-006` | Only approved source documents from the frozen manifest | mapped | Verify upload preview before Indexing |
| Candidate `R-A` | Preserve stable Markdown sections, top 3, no reranking | mapped | Verify exact Dify chunking equivalent; mark unsupported fields explicitly |
| Request contract | Fixed tenant/actor/environment values; Owner question only | mapped | Verify which controls are enforced by UI versus prompt |
| Answer contract | Hebrew, grounded claims, `[SOURCE_ID § Section]`, fallback/refusal | mapped | Verify citation metadata exposed to the app |
| Access policy | Private Owner-only app and Knowledge Base | mapped | Verify public WebApp/API/share links are disabled |
| Evaluation set | 25 frozen questions, entered only during an approved run | mapped | Verify logs do not become the sole evidence store |
| Evaluation records | Local minimized evidence contract linked to Dify run metadata | mapped | Verify exportable usage, latency and retrieved-source indicators |
| Cost plan | Request ceilings plus 60/80/100 ₪ stop policy | mapped conceptually | Verify enforceable platform/model limits before first request |

- [x] `R-A` is the first mapping candidate, not a proven final configuration.
- [x] `R-B` and `R-C` remain inactive alternatives.
- [x] Generation `gpt-4.1-mini-2025-04-14` is verified in the App; the approved Embedding mapping is `text-embedding-3-small`; Rerank and Score threshold are off.
- [x] The repository remains the source of truth; Dify configuration drift blocks evaluation.

## C. Region and Data Flow Gate

Required evidence record:

| Field | Required value | Current value |
|---|---|---|
| Dify Cloud storage region | Exact named region and legal entity | `unknown`; managed region בלבד |
| Knowledge document path | Storage and processing locations | `partial`; primary processing in US, exact storage region unknown |
| Index/vector path | Provider, region and retention | `partial`; Qdrant/TiDB listed as subprocessors, exact use/region unknown |
| Embedding provider | Name, model, region and data-use terms | OpenAI via Dify-managed Credits; `text-embedding-3-small`; exact region unknown |
| Generation provider | Name, model, region and data-use terms | OpenAI via Dify-managed Credits; `gpt-4.1-mini`; exact region unknown |
| Logs/analytics path | Data types, region, access and retention | `partial`; content and 30-day Sandbox retention documented, region unknown |
| Support/subprocessor access | Who can access and under what control | `partial`; official DPA list recorded, exact prototype path unknown |

- [x] Record authoritative public Dify sources for the fields currently documented. Evidence: `dify-official-evidence.md`.
- [x] Draw a high-level data flow from Owner question through Knowledge, providers and Logs; it remains explicitly non-final.
- [x] Draw the final bounded data flow with Dify-managed OpenAI Generation and Embedding; exact provider region remains within the accepted synthetic-only risk.
- [x] Confirm that only the frozen synthetic corpus is allowed even if the provider offers stronger controls.
- [x] Unknown exact Region and retention paths are accepted only as a bounded residual risk for this frozen synthetic corpus; they remain a hard `no-go` for real data, clients or Production.

### Owner residual-risk decision

- `accepted_on`: `2026-08-20`
- `accepted_scope`: אי-ודאות ב-Region המדויק וב-Backup/cache retention עבור `af-demo-services-he@1.0.0` הסינתטי בלבד.
- `not_accepted`: מידע אמיתי או רגיש, לקוח, Production, Provider/Model שלא נבחר, Cross-tenant use או ויתור על מחיקה כאשר היא זמינה.
- `effect`: החלטה זו מסירה את Region/Retention כחסם מוחלט לאב-טיפוס הסינתטי בלבד; UI, reconstruction ו-zero-spend controls הושלמו מאוחר יותר, אך שום Stage של K3.3 אינו מאושר אוטומטית.

## D. Isolation and Access Gate

Unauthenticated UI evidence on `2026-08-20`: `https://cloud.dify.ai/` redirected to `/signin`; available methods were GitHub OAuth, Google OAuth or Email verification code. No identifier was entered and no OAuth flow was started.

The initial authenticated UI snapshot on `2026-08-20` is minimized in `dify-ui-inspection-evidence.md`. It confirmed a 1/1 Owner-only Sandbox with zero Apps, Documents, usage and visible external connections before materialization. Later staged evidence records one dedicated App and one dedicated Knowledge Base; no personal account field was retained locally.

- [x] Confirm one Sandbox Workspace with one dedicated Unpublished App and one dedicated six-document Knowledge Base for the synthetic tenant.
- [x] Confirm the current Workspace has one of one Members and that Member is the Owner.
- [x] Confirm no public WebApp exists because the dedicated App remains Unpublished. Official docs warn that a published Web App is public by default; therefore do not publish.
- [x] Confirm no Data Source, Trigger, Extension, MCP, Custom Endpoint, Workflow-as-Tool or Swagger Tool is configured; built-in Tools remain available at Workspace level and SHALL NOT be attached to the App.
- [ ] Confirm no other Knowledge Base can be attached or searched.
- [ ] Confirm request input cannot choose a tenant, corpus or actor.
- [ ] Define and later execute negative checks for unknown actor, foreign tenant, foreign source and unapproved source status.
- [ ] Record screenshots or exported settings without email address, token, account identifier or other unnecessary personal data.

Failure of any isolation check is a hard `no-go` and does not trigger an automatic switch to another provider.

## E. Export, Restore and Drift Gate

- [x] Confirm a documented DSL export method for the App or Workflow configuration.
- [x] Define minimized local recording of Knowledge metadata, source mapping, Chunk counts and Retrieval settings when native export is incomplete.
- [x] Confirm original source files remain recoverable from the Git corpus, independent of Dify.
- [x] Record that DSL excludes API keys and Knowledge data; Secret environment variables SHALL be explicitly excluded during export.
- [x] Define local naming convention: `AF-KA-01_<agent_release_id>_config-<version>_<yyyy-mm-dd>.yaml` and matching Knowledge archive prefix.
- [x] Define a restore/reconstruction test into a disposable synthetic-only target; do not execute without later approval.
- [ ] Compare restored configuration to the local manifest and record Drift.
- [x] Document the manual reconstruction runbook in `dify-reconstruction-runbook.md` before Runtime.

Minimum pass condition: the local corpus is always recoverable, and the approved App/Knowledge configuration can be reconstructed without relying on conversation history or hidden settings.

## F. Deletion and Retention Gate

The future deletion sequence SHALL cover, in order:

1. Disable all access and Runtime paths.
2. Delete or detach the App from the Knowledge Base.
3. Delete documents and Chunks.
4. Delete the Knowledge Base and vector Index.
5. Delete evaluation conversations and application Logs when supported.
6. Delete the App and, when in scope, Workspace/account resources.
7. Revoke and delete Credentials from the provider Credential store.
8. Record provider Retention windows for caches, backups, analytics and support systems.
9. Preserve only the approved local synthetic corpus and minimized non-secret evidence in Git.

- [x] Record official documentation for App, Document + Chunks, and Knowledge Base + Documents deletion operations.
- [x] Record Sandbox Log retention as 30 days and that deleting conversations does not delete uploaded files.
- [ ] Record what remains after deletion and for how long.
- [ ] Define proof of deletion without capturing Secrets or unnecessary account data.
- [x] Unknown Backup/cache retention is accepted only for the frozen synthetic corpus; supported App/Document/Knowledge deletion remains mandatory after any future authorized test.

## G. Cost and Hard-Stop Gate

### Required pre-authorization forecast

- [x] Verify current Dify Sandbox price, credits and quotas on the decision date; overage/payment behavior remains pending UI verification.
- [x] Verify current UI shows Sandbox, zero paid usage, disabled Billing management and a separate manual Upgrade action; no Payment method or paid quota is visible. Reverify before every authorized run.
- [x] Select `gpt-4.1-mini` and `text-embedding-3-small` after documenting their current Credit rates; no BYOK path is permitted.
- [x] Define a staged Indexing forecast: one-document pilot with 25-Credit ceiling, then extrapolate the remaining five and preserve at least 50 Credits.
- [x] Supersede the original 30-Credit forecast with the measured six-Credit response rate: approximately 150 Credits for 25 questions before retries.
- [x] Record current monthly committed spend as 0 ₪ because no account, subscription, key or provider action exists.
- [x] Record committed monetary spend as 0 ₪; currency conversion is not applicable while paid paths remain disabled.

### Enforced thresholds

| Threshold | Required control | Current status |
|---|---|---|
| Forecast > 60 ₪ | Do not start; reduce scope or request review | policy defined; enforcement unverified |
| Actual/committed 60 ₪ | Warn Owner; no new candidate | policy defined; enforcement unverified |
| Actual/committed 80 ₪ | Freeze all new experiments | policy defined; enforcement unverified |
| Actual/committed 100 ₪ | Hard stop Runtime and Indexing | policy defined; enforcement unverified |
| Cost cannot be measured | Block before first billable request | `blocking_default` |

- [x] Identify the current zero-spend boundary: Sandbox credits only, no BYOK, no paid quota and no Upgrade; exhaustion stops included capacity. This is state-based and SHALL be drift-checked before use.
- [ ] Disable paid add-ons and auto-renewing subscriptions unless separately approved.
- [x] Define request/Credit ceilings for every staged authorization before any Indexing or model call.
- [x] Propose smaller request-scoped authorizations in `k3-3-staged-authorization.md`; each requires explicit Owner approval.
- [x] The current account has no visible paid quota, BYOK or enabled Billing management; the permitted committed spend is therefore 0 ₪ and any Drift from this state blocks execution before a request.

Authenticated UI evidence initially confirmed 0/200 Credits used. The current post-D3T state is 164/200 used and 36 available, with no visible BYOK or paid quota, disabled Billing management and a separate manual Upgrade action. All four observed generation responses consumed six Credits: D, D2, the Owner-invoked pre-D3SR Preview, and D3T. The citation contract now passes for KA-E01, but the full 25-question evaluation is blocked because its measured pre-retry forecast is approximately 150 Credits.

## H. Security, Logging and Failure Gate

- [x] Require the five-node `User Input → Knowledge Retrieval → Citation Context → LLM → Answer` Chatflow with zero Tool attachments; retrieved documents cannot activate Plugins, Triggers or external calls.
- [x] Require System instructions and retrieved text to remain separated by the approved request/answer contract.
- [x] Confirm full prompts, Credentials and unnecessary document content are excluded from local evidence.
- [x] Confirm the evaluation record contract records source IDs, verdicts, latency and cost indicators.
- [x] Define behavior for Retrieval unavailable, missing citation, budget reached and configuration drift.
- [x] Define immediate stop conditions for unexpected publication, cross-source retrieval, secret exposure or spending in the staged authorization record.

## I. K3.3 Owner Decision Record

Each additional K3.3 Stage can be proposed only when the preceding Stage evidence is complete and the overall status names that next decision. Approval must name exactly one Stage and state its actions, Credit/request ceiling, permitted data, forbidden actions and expiry. The current status is `stage_d3c_local_closure_complete_full_evaluation_blocked`.

An eventual approval SHALL NOT be interpreted as authorization for Production, real data, external users, n8n, Tools, public channels or Gate G1.

### Current decision

- `decision`: `k4_0_capacity_plan_complete_k4_1c_not_granted`
- `reason`: deterministic citation enrichment passed KA-E01, but only 36 Credits remain; the scored set requires 150 Credits and the safe envelope with five technical retries requires 180.
- `selected_capacity_strategy`: wait for the monthly Sandbox allowance, then verify at least 180 Credits and frozen configuration under a separately approved read-only K4.1C gate.
- `next_safe_step`: no provider action. The Owner may later approve K4.1C only; a passing check still does not authorize the separately gated K4.3E scored run.

## Traceability

- ADR: `docs/adr-004-dify-cloud-sandbox-runtime.md`
- Proposal: `openspec/changes/knowledge-agent-prototype-v1/proposal.md`
- Spec: KA-101, KA-107, KA-108, KA-109, KA-110, KA-111
- Cost policy: `configuration/cost-control-plan.md`
- Retrieval plan: `configuration/retrieval-experiment-matrix.md`
- Access policy: `configuration/access-policy.md`
- Evaluation record: `configuration/evaluation-record-contract.md`
- Official Dify evidence: `configuration/dify-official-evidence.md`
- Authenticated UI evidence: `configuration/dify-ui-inspection-evidence.md`
- Closure package: `configuration/k3-2d-closure-package.md`
- Reconstruction runbook: `configuration/dify-reconstruction-runbook.md`
- Staged authorization: `configuration/k3-3-staged-authorization.md`
- D3W evidence: `configuration/k3-3-d3w-execution-evidence.md`
- D3T evidence: `configuration/k3-3-d3t-execution-evidence.md`
- K4.0 capacity plan: `configuration/k4-0-capacity-evaluation-plan.md`
