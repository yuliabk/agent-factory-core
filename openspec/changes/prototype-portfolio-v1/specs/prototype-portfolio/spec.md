# Prototype Portfolio V1 Spec Delta

## ADDED Requirements

### Requirement: PP-101 - Versioned portfolio identity

The portfolio SHALL assign a stable prototype identifier, synthetic tenant, capability pattern, release identity, evaluation-set version and evidence status to every member.

#### Scenario: Complete prototype identity

- GIVEN a portfolio member declares all required immutable identities
- WHEN its planning package is validated
- THEN the member SHALL be traceable to one tenant, one capability pattern and one evidence status

#### Scenario: Ambiguous or shared identity

- GIVEN two portfolio members share an identifier, tenant-bound release or mutable evaluation reference
- WHEN portfolio preflight runs
- THEN validation SHALL fail and Materialization SHALL remain blocked

### Requirement: PP-102 - Isolated synthetic data planes

Each portfolio member SHALL use only synthetic data and SHALL have logically separate corpus or fixtures, configuration, evaluation records, logs, storage, indexes and future credentials.

#### Scenario: Correct tenant isolation

- GIVEN a request is evaluated for one synthetic tenant
- WHEN evidence, fixtures or audit records are selected
- THEN only assets assigned to that exact tenant SHALL be eligible

#### Scenario: Cross-tenant request

- GIVEN a request, fixture or retrieved item references another portfolio tenant
- WHEN the prototype evaluates the request
- THEN it SHALL deny processing, disclose no foreign content or metadata and record a cross-tenant policy failure

#### Scenario: Shared provider resource proposed

- GIVEN a future provider mapping proposes one shared corpus, index, credential, log or storage scope for multiple tenants
- WHEN the mapping is reviewed
- THEN the provider gate SHALL fail until separate tenant scopes are defined

### Requirement: PP-103 - Reusable factory contracts

Each new portfolio member SHALL reuse approved Factory contracts by reference and SHALL document behavior-specific differences as explicit deltas rather than copied divergent policy.

#### Scenario: Shared contracts reused

- GIVEN a Service or Controlled Action prototype is planned
- WHEN its artifact map is reviewed
- THEN it SHALL reference at least Intake, release identity, cost gate, minimized audit schema and evaluation contract

#### Scenario: Copied policy drifts

- GIVEN a copied contract weakens an approved isolation, authorization, audit or cost rule
- WHEN portfolio validation compares it with the canonical Factory contract
- THEN validation SHALL fail and identify the conflicting rule

### Requirement: PP-104 - Knowledge reference evidence boundary

The portfolio SHALL treat the existing `af-demo-services` Knowledge result as bounded reference evidence only and SHALL NOT represent it as completion of the frozen 25-question evaluation or Gate G1.

#### Scenario: Knowledge smoke evidence adopted

- GIVEN the approved Phase 1 smoke evidence is referenced by immutable change and evidence identifiers
- WHEN the Portfolio scorecard records the Knowledge pattern
- THEN it SHALL record the demonstrated grounding and citation checks and SHALL preserve all untested categories as `not_run`

#### Scenario: PF-G1-K reference adoption is approved

- GIVEN the Owner explicitly approves `PF-G1-K` after `PF-G0`
- WHEN the existing Phase 1 Knowledge evidence is linked to the Portfolio scorecard
- THEN only locally recorded, hash-bound evidence SHALL be adopted
- AND the latest supported `KA-E01` result MAY be recorded as `smoke_passed`
- AND Gate G1, the frozen 25-question evaluation, provider access, Runtime, Indexing, Publish and all untested categories SHALL remain open, unauthorized or `not_run` as applicable

#### Scenario: Knowledge release claim attempted

- GIVEN only the bounded `KA-E01` evidence is available
- WHEN a Portfolio report attempts to label Knowledge as `release_approved`
- THEN the report SHALL fail validation and keep Gate G1 open

### Requirement: PP-105 - Customer Service triage and escalation

The `af-demo-retail` Customer Service prototype SHALL classify synthetic requests, answer only from approved policy fixtures, ask focused clarification when required and escalate unresolved or protected cases to the Owner without sending an external message.

#### Scenario: PF-G1-S local materialization is approved

- GIVEN the Owner explicitly approves `PF-G1-S` for synthetic local artifacts only
- WHEN the Service Intake, policies, cases, contracts and evaluation set are materialized
- THEN every artifact SHALL be bound to tenant `af-demo-retail`, classification `synthetic` and an immutable local version
- AND validation SHALL use no network, model, provider, credential, Runtime, Indexing, payment, external message or Ticket connector

#### Scenario: Supported service request

- GIVEN an approved synthetic policy directly supports the request and routing category
- WHEN the Service prototype prepares a response
- THEN it SHALL return a Hebrew draft response, the category, supporting source identifiers and the next permitted step

#### Scenario: Missing service information

- GIVEN a required field is absent and materially changes the routing or answer
- WHEN the request is evaluated
- THEN the prototype SHALL ask only for the missing synthetic field and SHALL NOT invent a value

#### Scenario: Insufficient policy evidence

- GIVEN no approved tenant policy supports the requested answer
- WHEN the Service prototype prepares a response
- THEN it SHALL use the approved insufficient-evidence response and route the case to Owner review

#### Scenario: Protected or out-of-scope request

- GIVEN a request concerns payment, legal commitment, sensitive data, account change, refund execution or an external message
- WHEN triage runs
- THEN the prototype SHALL mark the case `human_review_required` and SHALL perform no action

#### Scenario: Escalation unavailable

- GIVEN the escalation target or required Owner role is missing
- WHEN a case requires escalation
- THEN the case SHALL fail closed with status `blocked_missing_escalation_owner`

### Requirement: PP-106 - Controlled Action draft-only behavior

The `af-demo-operations` Controlled Action prototype SHALL produce only a normalized synthetic office-supply request Draft and SHALL have no executable external action path in V1.

#### Scenario: Valid draft proposed

- GIVEN an authorized synthetic Owner request contains the required item, quantity, purpose and cost-band fields
- WHEN the prototype prepares the action
- THEN it SHALL emit a versioned Draft with `execution_status = not_executed` and a human-readable summary

#### Scenario: Required draft field missing

- GIVEN a required action field is missing or ambiguous
- WHEN Draft preparation runs
- THEN the prototype SHALL request clarification and SHALL NOT create an approvable Draft

#### Scenario: Execution requested

- GIVEN a user instructs the prototype to submit, purchase, send, update or otherwise execute the Draft
- WHEN the request is processed
- THEN the prototype SHALL refuse execution and SHALL record `execution_blocked_v1`

### Requirement: PP-107 - Approval and idempotency boundary

Every Controlled Action Draft SHALL require a separate, expiring approval reference before any future execution gate and SHALL carry an idempotency key derived from immutable request identity rather than model text.

#### Scenario: Draft has no approval

- GIVEN a valid Draft exists without an approval reference
- WHEN a later component requests execution
- THEN execution SHALL remain blocked and the audit result SHALL state `approval_missing`

#### Scenario: Approval is expired or mismatched

- GIVEN an approval references another tenant, action, Draft version, request or expiry window
- WHEN authorization is checked
- THEN the approval SHALL be rejected and no side effect SHALL occur

#### Scenario: Duplicate action request

- GIVEN the same immutable request identity is submitted more than once
- WHEN the idempotency contract is evaluated
- THEN all copies SHALL resolve to one idempotency key and SHALL NOT authorize duplicate execution

#### Scenario: Synthetic approval is present in V1

- GIVEN a synthetic approval fixture is valid
- WHEN the V1 prototype evaluates it
- THEN the prototype MAY mark the Draft `approval_validated_dry_only` but SHALL keep `execution_status = not_executed`

### Requirement: PP-108 - Minimized portfolio audit evidence

Every consequential portfolio decision SHALL record minimized structured evidence without secrets, personal data, full hidden prompts or real customer content.

#### Scenario: Service decision recorded

- GIVEN a Service request is classified, answered, clarified, refused or escalated
- WHEN the evaluation record is written
- THEN it SHALL include tenant, actor, request, release, category, evidence references, policy decision, escalation result and timestamp

#### Scenario: Controlled Action decision recorded

- GIVEN a Draft is created, blocked or dry-approved
- WHEN the evaluation record is written
- THEN it SHALL include tenant, actor, request, Draft version, proposed action, approval reference status, idempotency key, execution result and timestamp

#### Scenario: Sensitive or real data appears

- GIVEN a fixture or proposed record contains personal, confidential, medical, financial, credential or real customer information
- WHEN local validation runs
- THEN the artifact SHALL be rejected and SHALL NOT enter the portfolio evidence set

### Requirement: PP-109 - Comparable evaluation scorecard

The portfolio SHALL use one normalized scorecard that preserves pattern-specific tests while comparing planning time, reuse, functional quality, safety, isolation, cost and unresolved risk.

#### Scenario: Smoke plan is complete

- GIVEN a portfolio member has at least ten frozen scenarios, mandatory safety cases, request ceiling, cost indicator and stop conditions
- WHEN its Smoke plan is reviewed
- THEN the member MAY advance to a separately approved provider or dry-validation gate

#### Scenario: Mandatory safety failure

- GIVEN any Injection, cross-tenant, unauthorized-action or sensitive-data scenario fails
- WHEN the scorecard is calculated
- THEN the member SHALL remain blocked regardless of its aggregate functional score

#### Scenario: Failure is preserved

- GIVEN a test fails and a contract, fixture or configuration changes
- WHEN evaluation resumes
- THEN a new version and run identity SHALL be created and the original failure SHALL remain recorded

#### Scenario: Portfolio comparison is incomplete

- GIVEN one member lacks comparable time, reuse, safety, isolation or cost evidence
- WHEN Portfolio proof is considered
- THEN the missing dimension SHALL be reported as `not_measured` and SHALL NOT be inferred

### Requirement: PP-110 - Measurable time and reuse proof

The portfolio SHALL measure Factory efficiency using explicit start and stop events and artifact references rather than subjective estimates.

#### Scenario: Planning time measured

- GIVEN an approved planning task begins and completes
- WHEN efficiency evidence is written
- THEN it SHALL record active Owner/Codex hours separately from provider waiting time

#### Scenario: Reuse measured

- GIVEN a prototype references shared and prototype-specific artifacts
- WHEN reuse is calculated
- THEN the scorecard SHALL count canonical references separately from copied or modified files and SHALL require at least five shared Factory contracts

### Requirement: PP-111 - Cost and request gates

No portfolio Runtime SHALL execute until the exact member, provider, model, data scope, request ceiling, measurable cost indicator, hard stop and Owner-approved cap are recorded in a separately approved gate.

#### Scenario: Planning-only work

- GIVEN only `PF-G0` planning scope is approved
- WHEN a task would access a provider, model, network, credential, index or paid resource
- THEN the task SHALL stop before access and report missing authorization

#### Scenario: Cost balance is unknown

- GIVEN provider Credits, price, hard-stop behavior or combined provider cost is unknown or unverified
- WHEN a Runtime gate is proposed
- THEN Runtime SHALL remain blocked

#### Scenario: Request or budget ceiling reached

- GIVEN an authorized future Smoke reaches its request or cost ceiling
- WHEN another attempt is requested
- THEN execution SHALL stop without automatic retry and SHALL record the stop event

### Requirement: PP-112 - Explicit evidence states and approval gates

Each portfolio member SHALL use only the evidence states `planned`, `dry_validated`, `smoke_passed` and `release_approved`, and every transition SHALL require the named Owner gate defined by this change.

#### Scenario: Planning draft completed

- GIVEN the four OpenSpec planning artifacts validate strictly
- WHEN the current authorized work completes
- THEN the change SHALL remain `planning_draft_complete_waiting_for_PF-G0`

#### Scenario: PF-G0 planning baseline approved

- GIVEN the Owner explicitly approves `PF-G0` for the Portfolio plan only
- WHEN the approval is recorded
- THEN the change SHALL become `PF-G0_approved_planning_baseline_only`
- AND Materialization, provider access, Runtime, credentials, payment, Indexing, publication and every later gate SHALL remain unauthorized

#### Scenario: PF-G1-K completes without expanding evidence

- GIVEN `PF-G1-K` is approved for local reference adoption only
- WHEN the PF-K scorecard is completed and strictly validated
- THEN the change SHALL become `PF-G1-K_complete_reference_evidence_only`
- AND `PF-G1-S`, `PF-G1-A`, every `PF-G2` gate, `PF-G3` and Gate G1 SHALL remain unauthorized

#### Scenario: PF-G1-S dry validation completes locally

- GIVEN the approved `PF-G1-S` artifacts contain only synthetic data and all mandatory Service safety scenarios pass deterministic local validation
- WHEN the validation evidence is recorded
- THEN the PF-S member MAY become `dry_validated`
- AND provider mapping, model quality, Runtime, message delivery, Ticket creation, `PF-G2-S` and release approval SHALL remain unauthorized and unproven

#### Scenario: Gate approval is ambiguous

- GIVEN an Owner message does not name one gate, member, permitted actions and exclusions
- WHEN authorization is interpreted
- THEN no provider, Runtime or Materialization action SHALL be authorized

#### Scenario: Botpress proposed during incident hold

- GIVEN Botpress remains on `INCIDENT-HOLD`
- WHEN it is proposed for a portfolio Materialization or Runtime gate
- THEN the gate SHALL fail until a separately approved incident process resolves the hold

#### Scenario: Portfolio proof reviewed

- GIVEN all selected members have comparable evidence and mandatory safety outcomes
- WHEN `PF-G3` is reviewed
- THEN the Owner MAY accept the bounded Factory proof without implying Gate G1, G2, G4 or Production approval
