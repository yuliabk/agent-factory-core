# Change: Portable Runtime Adapters v1

## Purpose

Define a provider-neutral planning layer that preserves the Agent Factory's approved knowledge-agent behavior while allowing a future, separately approved runtime pilot outside Dify. Dify remains the current reference implementation; this change does not select, provision, or execute another runtime.

## Why

The current prototype is coupled to Dify-specific graph nodes, credit accounting, and evidence fields. That coupling makes cost comparison and runtime substitution difficult. A portable contract and normalized evaluation design let the Owner compare alternatives without duplicating the canonical specification or weakening security, citation, fallback, and cost controls.

## Scope

This change began with planning artifacts and later received bounded approvals for local validation and narrowly scoped external evidence gathering:

- **P0:** a versioned runtime-adapter contract.
- **P1:** a local, network-free evaluation-runner plan.
- **P2:** a Botpress capability and control mapping.
- **P3:** a Flowise capability and control mapping.
- **PR-G1:** a standard-library local validator and dry runner using synthetic fixtures only.
- **PR-G2-Flowise-Preflight:** read-only review of public official Flowise sources only.
- **PR-G2-Botpress-Preflight:** read-only review of public official Botpress sources only.
- **PR-G2-Botpress-A0:** Owner-performed Free-account registration in the official Botpress UI, with Codex limited to navigation and guidance.
- **PR-G2-Botpress-A1:** authenticated read-only inspection of the automatically available default workspace, Free-plan usage, and billing summary.
- **PR-G2-Botpress-A2:** authenticated read-only inspection of workspace controls for cost, membership, audit, deletion, and workspace-level export availability.
- **PR-G2-Botpress-A3:** authenticated read-only reconciliation of non-personal Bot inventory and available audit metadata without opening either Bot.
- **PR-G2-Botpress-IR-A0:** read-only incident triage after the Owner stated that she did not create the two observed Bots.
- **PR-G2-Botpress-IR-A1:** read-only incident re-verification of Bot count, usage, billing, storage, audit, and safely discoverable account-security routes.

## Out of Scope

- Provider adapter or live runner implementation code.
- Runtime execution, Preview, indexing, upload, publication, or migration.
- Creating additional accounts or workspaces, bots, flows, datasets, or credentials beyond the separately approved Botpress A0 registration.
- Payment, subscription, credit purchase, or provider configuration.
- Changing the approved Dify graph, prompt, corpus, or release.
- Production support or a claim of runtime equivalence.
- Commit, push, pull, fetch, merge, checkout, or branch creation.

## Proposed Capabilities

- A canonical, provider-neutral adapter contract with explicit capability declarations.
- Normalized request, answer, citation, evidence, policy, usage, and cost records.
- A deterministic local evaluation plan that fails closed when evidence or controls are missing.
- Documented Botpress and Flowise mappings, gaps, risks, and future approval gates.

## Security and Privacy Impact

The design retains synthetic-data-only operation, empty tool calls, per-client and per-runtime isolation, separate credentials, bounded logs, explicit deletion/export expectations, and fail-closed behavior. No secrets are stored in this change.

## Cost Impact

This planning change has no provider cost. A future pilot MUST use a provider-native hard cap, a normalized cost ceiling, and a separately approved stop condition before any billable action.

## Approval

- **Gate:** PR-G0
- **Status:** Approved
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Approved scope:** P0–P3 planning package only.

This approval accepts the local adapter contract, evaluation-runner plan, and Botpress and Flowise mappings as a planning baseline. It does not authorize implementation, Runtime, accounts, credentials, payment, Indexing, Publish, Commit, or Push.

The local validator/runner was implemented only after separate PR-G1 approval. PR-G2 external work was then split into narrow gates: public unauthenticated reviews, one Owner-operated Botpress Free-account registration, and separately approved authenticated read-only inspections. Every additional provider resource, configuration change, credential, data operation, cost control, or pilot still requires new explicit approval for exactly one maintained candidate runtime.

### PR-G1 Implementation Approval

- **Status:** Approved and completed locally
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Scope:** Standard-library Validator and Dry Evaluation Runner using synthetic fixtures only.

PR-G1 did not expand the PR-G0 boundary to any external system. Provider work remained separately gated; the later A0–A3 approvals authorized only the Botpress registration and read-only inspections recorded below and did not authorize a runtime pilot.

### PR-G2 Flowise Public Preflight

- **Status:** Approved read-only review completed; `NO-GO`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Scope:** Public official-source review of Flowise capabilities, limits, costs, isolation, citations, export, and deletion.
- **Result:** Flowise Cloud and the official upstream are blocked from a pilot because the product is being sunset, the repository is archived, and EOL is scheduled for 2026-08-31.

No registration, account, credentials, upload, Indexing, Runtime, payment, or publication was authorized or performed. A Flowise community fork would be a new candidate, not a continuation of this approval.

### PR-G2 Botpress Public Preflight

- **Status:** Approved read-only review completed; `CONDITIONAL-GO`, currently blocked
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Scope:** Public official-source review of Botpress continuity, capabilities, limits, costs, isolation, citations, export, deletion, security, and privacy.
- **Result:** No public vendor-continuity blocker was found, but authenticated inspection and Runtime remain blocked pending exact citation, deny-all, isolation, export/reconstruction, deletion, Hebrew, and cost-control evidence.

No registration, login, account, credentials, upload, Indexing, Runtime, payment, or publication was authorized or performed.

### PR-G2 Botpress A0 Registration

- **Status:** Approved and completed 2026-08-21
- **Approved by:** Owner (Yulush)
- **Scope:** Open the official Botpress registration page and guide the Owner while the Owner entered all personal, authentication, and verification data.
- **Result:** One Free account was created. Botpress presented its automatically available default workspace and the `Create Bot` screen; no additional workspace or Bot was created.

Codex did not enter or read personal data, passwords, or verification codes. A0 did not authorize Knowledge Base creation, data upload, credentials, model configuration, AI Spend changes, payment, Indexing, Emulator, Runtime, Publish, Commit, or Push.

### PR-G2 Botpress A1 Authenticated Read-Only Inspection

- **Status:** Approved and completed 2026-08-21; `CONDITIONAL-GO` remains blocked
- **Approved by:** Owner (Yulush)
- **Scope:** Read-only inspection of the existing default workspace, Free-plan identity, usage counters, and billing summary.
- **Observed:** Free plan; 0/100 conversations; 0/1,000 table rows; 0/100 MB vector storage; 0/100 MB file storage; and USD 0.00/USD 10.00 AI usage shown as included plan allowance.
- **Result:** No Bot existed or was created. The AI-usage allowance is not evidence of an enforceable provider-native hard stop.

A1 did not inspect or change `Manage plan`, payment, account identity, personal data, settings, tools, integrations, credentials, model configuration, Knowledge Base, Runtime, Indexing, Emulator, or publication. Exact citation provenance, deterministic deny-all behavior, client isolation, export/reconstruction, deletion, Hebrew behavior, and an enforceable cost stop remain unverified and blocking.

### PR-G2 Botpress A2 Authenticated Control Inspection

- **Status:** Approved and completed 2026-08-21; `CONDITIONAL-GO` remains blocked and prior workspace-state evidence is drifted
- **Approved by:** Owner (Yulush)
- **Scope:** Read-only inspection of workspace settings, billing and usage controls, membership and audit surfaces, workspace deletion control, and workspace-level export availability.
- **Observed:** AI-spend auto-recharge displayed `Disabled`; the Usage page exposed `Increase limits` but no visible hard-cap control; `Delete Workspace`, Members, Invite member, and Audits surfaces were present; no workspace-level export control was found.
- **Drift:** Two distinct Bot routes were observed after A1 even though A1 recorded the `Create Bot` state. A2 did not open the Bots, determine their origin, or inspect their configuration.
- **Result:** Disabled auto-recharge reduces accidental top-up risk but does not prove an enforceable provider-native hard stop. Bot-level export, deletion, deny-all, citation, Hebrew, isolation, and Runtime controls remain unverified.

A2 did not activate Delete, Manage, Payment, Invite, Increase limits, Bot, export, or any other change control. It did not read personal data or audit entries and did not create or modify provider resources. The observed Bot routes constitute configuration drift under RP-108; any future preflight requires a fresh bounded identity, evidence snapshot, and approval.

### PR-G2 Botpress A3 Drift Reconciliation

- **Status:** Approved and completed 2026-08-21; drift confirmed but not attributable
- **Approved by:** Owner (Yulush)
- **Scope:** Read-only count of distinct Bot routes plus non-personal audit categories and timestamps, without opening Bot or Studio.
- **Observed:** Two distinct Bot routes were consistently visible after the workspace page finished loading. The Audits surface exposed no event rows, timestamps, or create/update/delete categories that could establish origin or time.
- **Weak signal:** The workspace home page contained three generic occurrences of `8 hours ago`; they could not be safely associated with either Bot or with creation and are not accepted as provenance evidence.
- **Result:** Bot count is verified as two at A3 observation time. Creator, creation method, creation timestamp, configuration, and approval status remain `unknown`; configuration drift remains unresolved and blocking.

A3 did not open either Bot or Studio, inspect Bot names or identifiers, read actor names or email addresses, or invoke Emulator, model, Runtime, or change controls. No inference about who created the Bots is permitted from absent audit evidence or ambiguous relative-time text.

### PR-G2 Botpress IR-A0 Incident Triage

- **Severity:** Provisional internal `SEV3`
- **Status:** `Investigating`; operational decision `INCIDENT-HOLD`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Trigger:** The Owner stated that she did not create the two Bots observed in A2 and A3.
- **Scope:** Read-only recheck of Bot count, Usage, Billing, auto-recharge, and safely discoverable account-security routes without opening Bots or identity-bearing menus.
- **Observed:** Two Bot routes persisted; conversations remained 0/100; AI spend remained USD 0.00/USD 10.00; table rows and vector storage remained zero; file storage increased from 0 MB in A1 to 1 MB; the plan remained Free; auto-recharge remained `Disabled`.
- **Account-security surface:** No safely identifiable Security, Session, MFA, Account, or Profile route or labeled control was exposed. Unknown user-menu controls were not opened because they could reveal personal data.
- **Impact:** No evidence of conversation execution, AI spend, vector indexing, payment, model use, or Runtime was found. The unexplained Bots and 1 MB file-storage increase remain unauthorized configuration and storage drift.

The public `CONDITIONAL-GO` decision remains a historical capability assessment only. `INCIDENT-HOLD` supersedes it operationally until account access is secured by the Owner, the provider state is re-verified, and a separately approved incident decision resolves containment. IR-A0 did not open, modify, or delete Bots; activate Manage, Payment, or security controls; or create provider resources.

### PR-G2 Botpress IR-A1 Read-Only Re-verification

- **Status:** Approved and completed 2026-08-22; `SEV3 / Investigating / INCIDENT-HOLD`
- **Approved by:** Owner (Yulush)
- **Scope:** Read-only recheck of Bot inventory, Usage, Billing, file and vector storage, auto-recharge, Audits, and safely identifiable account-security routes.
- **Observed:** Two Bot routes persisted; file storage remained 1 MB; conversations, AI spend, table rows, and vector storage remained zero; the plan remained Free; auto-recharge remained `Disabled`.
- **Audit and security:** No event rows, timestamps, or Bot create/update/delete categories appeared. No safely labeled Security, Session, MFA, Account, or Profile route was exposed.
- **Result:** No additional provider drift was observed relative to IR-A0, but origin and configuration remain unknown. Stability does not establish containment or authorization.

IR-A1 did not open Bots, Studio, identity-bearing menus, Manage, Payment, or any change control. Owner-controlled identity-provider containment has not been confirmed as complete, so the incident remains `Investigating`; it is not downgraded, moved to `Monitoring`, or resolved.
