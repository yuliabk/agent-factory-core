# PR-G2 Botpress Public and Authenticated Read-Only Preflight Evidence

## Authorization and Boundary

- **Gate:** `PR-G2-Botpress-Preflight`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Permitted action:** Read-only review of public official Botpress sources and local documentation.
- **Excluded:** Registration, login, account, credentials, upload, Indexing, Runtime, payment, Publish, Commit, and Push.
- **Provider-side changes:** None.

### A0 Registration Authorization

- **Gate:** `PR-G2-Botpress-A0`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Permitted action:** Open the official registration page and guide the Owner through one Free-account registration.
- **Data boundary:** The Owner entered all personal, authentication, and verification data. Codex did not enter or read those values.
- **Excluded:** Additional workspaces, Bots, Knowledge Bases, uploads, credentials, model configuration, AI Spend changes, payment, Indexing, Emulator, Runtime, Publish, Commit, and Push.
- **Result:** One Free account was created. Botpress exposed an automatically available default workspace and the `Create Bot` screen; no additional workspace or Bot was created.

### A1 Authenticated Read-Only Authorization

- **Gate:** `PR-G2-Botpress-A1`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Permitted action:** Read-only inspection of the existing default workspace, Usage page, and Billing summary.
- **Excluded:** Reading personal or authentication data; opening or changing plan management, payment, account identity, settings, integrations, tools, credentials, model configuration, Knowledge Base, Indexing, Emulator, Runtime, or Publish.
- **Provider-side changes:** None.

### A2 Authenticated Control-Inspection Authorization

- **Gate:** `PR-G2-Botpress-A2`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Permitted action:** Read-only inspection of workspace cost, membership, audit, deletion, and workspace-level export controls.
- **Excluded:** Activating Delete, Manage, Payment, Invite, Increase limits, Bot, export, or any change control; reading personal data or audit-event contents; creating or modifying provider resources.
- **Provider-side changes:** None by Codex during A2.

### A3 Authenticated Drift-Reconciliation Authorization

- **Gate:** `PR-G2-Botpress-A3`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Permitted action:** Read-only count of non-personal Bot inventory and inspection of available audit categories and timestamps.
- **Excluded:** Opening Bot or Studio; reading Bot names or identifiers, actor names, email addresses, or audit-event content; invoking Emulator, model, Runtime, or any change control.
- **Provider-side changes:** None by Codex during A3.

### IR-A0 Read-Only Incident-Triage Authorization

- **Gate:** `PR-G2-Botpress-IR-A0`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Trigger:** The Owner stated that she did not create the two observed Bots.
- **Permitted action:** Read-only recheck of Bot count, Usage, Billing, auto-recharge, and safely identifiable account-security routes.
- **Excluded:** Opening Bots or unknown identity-bearing menus; reading personal or authentication data; activating Manage, Payment, security, deletion, Emulator, model, Runtime, or any change control.
- **Provider-side changes:** None by Codex during IR-A0.

### IR-A1 Read-Only Re-verification Authorization

- **Gate:** `PR-G2-Botpress-IR-A1`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-22
- **Permitted action:** Read-only recheck of Bot count, Usage, Billing, storage, auto-recharge, Audits, and safely identifiable account-security routes.
- **Containment assumption:** Owner-controlled identity-provider containment was not confirmed and therefore remained `unknown`.
- **Excluded:** Opening Bots, Studio, identity-bearing menus, Manage, Payment, security, deletion, Emulator, model, Runtime, or any change control; reading personal or authentication data.
- **Provider-side changes:** None by Codex during IR-A1.

## Executive Decision

**Historical capability decision: `CONDITIONAL-GO`. Current operational decision: `INCIDENT-HOLD`; all provider preflight and pilot activity is blocked.**

Botpress passes the public vendor-continuity check: its official documentation is current, its public status page is operational, and the company announced a USD 25 million Series B in June 2025. PAYG exposes useful cost controls and the product documents Knowledge Base citations, logs, workspace separation, export, retention, deletion APIs, privacy terms, and security controls.

The public evidence and completed A1–A3 read-only inspections are not sufficient for Runtime approval. A1 narrowed plan and quota uncertainty; A2 confirmed that auto-recharge was disabled but did not find a visible hard-cap control and detected provider-configuration drift. A3 confirmed a count of two Bot routes but found no attributable audit evidence and could not reconcile their origin, time, or configuration. The Owner then stated that she did not create the Bots. IR-A0 confirmed persistent routes and additional file-storage drift, so incident containment now supersedes candidate evaluation. Exact citation, deny-all, isolation, export, deletion, Hebrew, and cost controls remain unproven.

## Incident Update: Unrecognized Botpress Resources

**Severity:** Provisional `SEV3` | **Status:** `Investigating` | **Operational gate:** `INCIDENT-HOLD` | **Last updated:** 2026-08-22

**Impact:** One Free, non-production workspace. No client data, conversations, AI spend, vector indexing, payment, model use, or Runtime activity is known. Account integrity is affected by two unrecognized Bot routes and unexplained file-storage growth.

### IR-A0 Current Status

| Read-only surface | Observed value | Incident interpretation |
|---|---|---|
| Bot inventory | Two distinct routes persisted | Owner disclaimed creation; origin and configuration remain unknown |
| Conversations | 0 / 100 | No conversation execution observed |
| AI spend | USD 0.00 / USD 10.00 | No AI spend observed; displayed allowance is not a hard-stop proof |
| Table rows | 0 / 1,000 | No table-row use observed |
| Vector storage | 0 MB / 100 MB | No vector indexing observed |
| File storage | 1 MB / 100 MB, up from 0 MB in A1 | Additional state drift; cause and contents were not inspected |
| Plan and recharge | Free; auto-recharge `Disabled` | Accidental top-up risk reduced; no payment surface was opened |
| Account security routes | No safely labeled Security, Session, MFA, Account, or Profile route found | Unknown user-menu controls were not opened to avoid personal-data exposure |

### IR-A0 Actions Taken

- Stopped provider evaluation and placed Botpress on `INCIDENT-HOLD`.
- Preserved minimized non-personal evidence only.
- Did not open, modify, execute, export, publish, or delete either Bot.
- Recommended Owner-controlled identity-provider security and session review without sharing credentials or personal data.

### IR-A0 Next Steps

- Owner secures the identity provider and reviews or revokes unknown sessions.
- A separately approved read-only re-verification checks whether state changes continue.
- The incident remains open until configuration identity and containment are resolved or the account is decommissioned through an explicitly approved destructive gate.

### IR-A1 Re-verification Update

| Read-only surface | IR-A1 observation | Change from IR-A0 |
|---|---|---|
| Bot inventory | Two distinct routes | No change |
| Conversations | 0 / 100 | No change |
| AI spend | USD 0.00 / USD 10.00 | No change |
| Table rows | 0 / 1,000 | No change |
| Vector storage | 0 MB / 100 MB | No change |
| File storage | 1 MB / 100 MB | No change |
| Plan and recharge | Free; auto-recharge `Disabled` | No change |
| Audits | No visible event rows, timestamps, or Bot create/update/delete categories | No new evidence |
| Account security routes | No safely labeled Security, Session, MFA, Account, or Profile route | No new safe surface |

**IR-A1 verdict:** Stable relative to IR-A0, but unresolved. Stability does not prove that the Bots are authorized, that their internal state is inactive, or that account access is contained. With Owner-controlled identity-provider containment unconfirmed, status remains `Investigating / INCIDENT-HOLD`; no transition to `Monitoring` or `Resolved` is allowed.

## Authenticated A1 Findings

| Read-only surface | Observed value | Interpretation |
|---|---|---|
| Current plan | Free; 100 conversations | Plan identity and displayed conversation allowance verified for this workspace |
| Table rows | 0 / 1,000 | Zero current use; 1,000 rows displayed as included in the Free plan |
| Vector DB storage | 0 MB / 100 MB | Zero current use; 100 MB displayed as included in the Free plan |
| File storage | 0 MB / 100 MB | Zero current use; 100 MB displayed as included in the Free plan |
| AI usage | USD 0.00 / USD 10.00 | Zero current use; USD 10 displayed as plan allowance, not verified as an enforceable hard stop |
| Bot state | `Create Bot` landing screen; no Bot created | Citation, deny-all, Hebrew, export, deletion, Runtime, and bot-level isolation evidence remain unavailable |

The authenticated Free-plan UI differs from the earlier public pricing snapshot, which described PAYG using events and a USD 5 monthly AI credit. This may reflect a product or plan change, terminology change, account-specific presentation, or public-page drift. A1 records the authenticated values without treating either surface as proof of billable behavior or enforcement.

## Authenticated A2 Findings

| Read-only surface | Observed value | Interpretation |
|---|---|---|
| AI-spend auto-recharge | Disabled | Reduces accidental top-up risk but is not an enforceable hard cap |
| Usage controls | `Increase limits`; no visible hard-cap label or control | RP-107 remains blocking; absence was recorded without opening plan or payment management |
| Billing controls | Manage plan, AI-spend management, Payment & billing, and Invoice History surfaces present | Financial and plan controls were not activated or opened |
| Workspace deletion | `Delete Workspace` control present | Deletion capability is visible, but execution scope, retention, backups, and completion evidence remain unverified |
| Membership | Members and Invite member surfaces present | No invitation was opened or sent; role enforcement and plan-specific RBAC remain unverified |
| Audit | Audits surface present | Audit entries and personal data were not read; coverage and retention remain unverified |
| Workspace-level export | No export control found | Public Bot-level `.bpz` evidence remains unverified in this authenticated workspace |
| Provider state | Two distinct Bot routes observed after A1 | Configuration drift; routes were not opened, their origin was not inferred, and neither Bot is approved evidence |

A1 remains a valid historical observation that no Bot was present at its inspection time. A2's later observation invalidates only the assumption that the A1 workspace state is still current. Any future preflight must establish a new bounded provider-configuration identity before relying on Bot-level evidence.

## Authenticated A3 Findings

| Read-only surface | Observed value | Interpretation |
|---|---|---|
| Bot inventory | Two distinct Bot routes after page load | Count verified for the A3 observation date; neither route was opened and no identifier or name was recorded |
| Audits surface | No visible event rows, timestamps, or create/update/delete categories | No attributable evidence for creator, creation method, or creation time |
| Relative-time text | Three generic occurrences of `8 hours ago` on the workspace home page | Could not be safely associated with either Bot or a creation event; rejected as provenance evidence |
| Reconciliation verdict | Unresolved | Creator, creation method, creation timestamp, configuration, and approval status remain `unknown` |

A3 confirms the count but does not resolve the configuration identity. Absence of visible audit evidence is not evidence that no creation event occurred, and ambiguous UI text cannot be used to infer an actor or timestamp.

## Capability Findings

| Contract area | Official public evidence | Status | Preflight consequence |
|---|---|---|---|
| Vendor continuity | Current docs, operational public status, 2025 Series B | Supported | No continuity blocker found publicly |
| Knowledge/RAG | Documents, websites, tables, rich text, integrations, web search | Supported | Approved corpus must disable broad web search and integrations |
| Citation output | Knowledge Agent exposes `answer` and `citations`; logs expose source name, preview, token use, and table metadata | Partial | Exact stable `source_id` and section schema remains unverified |
| Hebrew behavior | General model-based generation and translation capabilities | Unknown | Hebrew-only answer and canonical fallback require a bounded test |
| External-action suppression | Studio supports integrations, webhooks, Execute Code, web search, tools, and autonomous behavior | Partial | A dedicated no-tool bot and negative graph inspection are mandatory |
| Logs and usage | Per-action AI Spend/token details, production logs, debugger, usage quotas | Supported in design | Requires authenticated evidence for the intended plan |
| Hard cost stop | Public custom-cap documentation; A2 observed disabled auto-recharge but no visible hard-cap control | Partial | Forecasting is officially described as unreliable; all quota dimensions need verified stops and disabled auto-recharge is insufficient |
| Export/reconstruction | Whole-bot `.bpz` export/import documented | Partial | Proprietary archive must not be modified; knowledge files remain server-linked; integrations require manual restoration |
| Deletion | Public deletion APIs; A2 observed `Delete Workspace` without activating it | Partial | Execution scope, logs, retention windows, files, backups, and completion evidence remain unverified |
| Tenant isolation | Workspace-level billing/usage plus A2 membership and audit surfaces | Partial | Role enforcement, audit coverage, shared administration, and lower-plan permissions remain unverified |
| Security/compliance | SOC 2 claim, GDPR/DPA, TLS and logical separation commitments, audit records on supported plans | Partial-positive | Plan-specific controls and evidence require authenticated or contractual review |
| Sensitive data | DPA states the service is not designed for sensitive data | Unsupported for sensitive-data scope | Synthetic data only; no medical, financial, or other sensitive data pilot |

## Published Cost Snapshot

Pricing was reviewed on the official public page on 2026-08-21. All amounts are USD and exclude taxes, additional quotas, implementation labor, and exit work.

| Option | Published base price | Indicative annual base | Selected published allowances | Additional cost exposure |
|---|---:|---:|---|---|
| PAYG | USD 0/month + AI Spend | USD 0 | 1 bot, 1 collaborator, 500 events/month, 100 MB vector DB, 100 MB files, USD 5 monthly AI credit | AI Spend above credit after raising limit; add-ons |
| Plus, annual billing | USD 79/month + AI Spend | USD 948 | 2 bots, 2 collaborators, 5,000 events, 1 GB vector DB, 10 GB files | AI Spend and add-ons |
| Plus, monthly billing | USD 89/month + AI Spend | USD 1,068 | Same published Plus allowance | AI Spend and add-ons |
| Team, annual billing | USD 445/month + AI Spend | USD 5,340 | RBAC, 3 bots, 3 collaborators, 50,000 events, 2 GB vector DB | AI Spend and add-ons |
| Team, monthly billing | USD 495/month + AI Spend | USD 5,940 | Same published Team allowance | AI Spend and add-ons |

Published add-ons include USD 20/month per additional 5,000 events, USD 10/month per bot, USD 25/month per collaborator, USD 20/month per additional 1 GB vector storage, and USD 10/month per additional 10 GB file storage. PAYG/Plus AI Spend has a published USD 100 monthly maximum and Team has USD 500; the workspace can set a lower custom cap. The provider states that reliable AI Spend forecasting is not currently available.

For the synthetic 25-question prototype, PAYG is the only plan that fits the current cost objective for a future pilot. Public evidence cannot prove that the USD 5 credit covers corpus ingestion plus the full test, so no zero-cost claim is made.

## Total-Cost and Exit Assessment

| Component | Assessment |
|---|---|
| Platform license | Potentially USD 0 for PAYG prototype |
| Model/AI usage | Provider-cost passthrough; variable and not reliably forecastable |
| Build/migration labor | Manual mapping of prompt, flow, corpus metadata, citations, fallbacks, and policies |
| Security/tenant controls | Stronger RBAC requires Team, far above the prototype budget |
| Export | `.bpz` is Botpress-specific and not a portable, editable source artifact |
| Knowledge exit | Export links source files hosted on Botpress rather than embedding them |
| Deletion/retention | Requires multiple APIs and waiting for retention windows; backup timing remains contractual |

## Risk Assessment

| Risk | Likelihood | Impact | Control or disposition |
|---|---|---|---|
| Citation schema lacks stable section provenance | Medium | High | Block until an authenticated schema inspection or one bounded synthetic test proves mapping |
| Proprietary `.bpz` creates lock-in | High | High | Keep Git/OpenSpec canonical; treat export only as disaster-recovery aid |
| Hosted knowledge files are linked, not embedded in export | High | High | Retain canonical corpus locally; verify deletion separately |
| External tools/web search can be enabled | Medium | High | Use a dedicated bot with no integrations/tools and inspect graph before any run |
| AI Spend cannot be reliably forecast | High | Medium | Use the lowest custom cap, disable Auto Recharge, and stop before threshold |
| Multiple independent quotas can stop the bot | Medium | Medium | Track events, AI Spend, vector storage, files, rows, and bots independently |
| PAYG lacks RBAC and SLA | High | Medium | Single Owner only; synthetic non-production pilot; no client users |
| Long or indefinite retention for some data | High | High | Synthetic data only and explicit deletion evidence before closing a pilot |
| Service not designed for sensitive data | High | High | Prohibit sensitive and real client data |
| Provider state changed after A1 | High | High | Treat as configuration drift; do not inspect or execute either Bot without a fresh bounded gate and identity |
| Owner disclaims observed Bots and file storage increased | Medium | High | Treat as an account-integrity incident; maintain `INCIDENT-HOLD`, secure identity, preserve minimized evidence, and require re-verification |

## Official Sources Reviewed

- Pricing, quotas, add-ons, AI Spend, and caps: https://botpress.com/en/pricing
- Workspace, quota, Auto Recharge, roles, and audit controls: https://botpress.com/docs/studio/get-started/configure-your-workspace/
- Knowledge Bases and retrieval logs: https://botpress.com/docs/studio/concepts/knowledge-base/introduction/
- Knowledge Agent citation variable: https://botpress.com/docs/studio/concepts/agents/knowledge-agent/
- Import/Export and `.bpz` limitations: https://botpress.com/docs/studio/concepts/import-export-bots/
- Retention periods: https://botpress.com/docs/learn/guides/advanced/retention-period
- Workspace deletion API: https://botpress.com/docs/api-reference/admin-api/openapi/deleteWorkspace/
- Privacy Statement: https://botpress.com/legal/privacy-statement
- Data Processing Agreement: https://botpress.com/legal/data-processing-agreement
- Legal portal and compliance claims: https://botpress.com/en/legal
- Enterprise-only SLA: https://botpress.com/legal/service-level-agreement
- Public service status: https://status.botpress.com/
- Series B continuity signal: https://botpress.com/blog/series-b

## Stop Record

The public preflight, A0 registration, A1–A3 inspections, IR-A0 triage, and IR-A1 re-verification are complete. One Free account was created by the Owner, and Botpress exposed one automatically available default workspace. A0 and A1 recorded no Bot; A2 through IR-A1 later observed two distinct Bot routes. The Owner stated that she did not create them. IR-A0 observed file storage at 1 MB after A1 had recorded 0 MB; IR-A1 found no additional change. Codex did not create, open, inspect, modify, or delete the Bots or storage and did not attribute their origin. No additional workspace, credential, payment method, Knowledge Base, model, Indexing, Emulator, Runtime, or publication was created or configured by Codex. No personal data, password, verification code, Bot name or identifier, actor identity, session data, or audit-event content was read or recorded by Codex.

Botpress is on `INCIDENT-HOLD` and blocked from every additional provider action. The historical `CONDITIONAL-GO` is not operational authorization. IR-A1 showed a stable but unresolved state; Owner-controlled account containment remains unconfirmed. Resumption requires confirmed containment, a separately approved post-containment re-verification, a bounded current configuration identity, and an explicit incident disposition.
