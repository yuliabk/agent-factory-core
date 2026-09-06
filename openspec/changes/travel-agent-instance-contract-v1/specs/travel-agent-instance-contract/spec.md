# Travel Agent Instance Contract v1 - Spec Delta

## ADDED Requirements

### Requirement: TAIC-101 - Canonical versioned TripRequest

The Travel Agent Instance SHALL accept customer-originated and agent-originated travel requests through one versioned `TripRequest` contract that is independent of Web, Email, or WhatsApp.

#### Scenario: Customer creates a valid request

- GIVEN a customer submits origin, destination, dates, traveler counts, currency, and available preferences
- WHEN intake validation succeeds
- THEN the system SHALL create a unique `request_id`
- AND SHALL set `created_by_type=customer`
- AND SHALL preserve the source channel only as metadata, not as a separate business schema

#### Scenario: Agent creates a request for a customer

- GIVEN an authorized travel agent creates a request on behalf of a customer
- WHEN intake validation succeeds
- THEN the same `TripRequest` schema SHALL be used
- AND `created_by_type=agent` SHALL be recorded

#### Scenario: Required information is missing

- GIVEN destination, dates, traveler count, or currency is missing or invalid
- WHEN intake validation runs
- THEN the request SHALL enter `NEEDS_INFORMATION`
- AND the system SHALL return focused `clarification_questions`
- AND provider search SHALL NOT fabricate or infer the missing material value

#### Scenario: IATA resolution fails

- GIVEN a destination label cannot be mapped confidently to an IATA code
- WHEN a provider adapter requires an IATA code
- THEN the request SHALL remain unresolved for that search
- AND the system SHALL NOT substitute the origin or a default airport code

### Requirement: TAIC-102 - Data classification and PII gate

The contract SHALL support `synthetic`, `public`, and `personal` classifications, but processing of `personal` data SHALL remain disabled until an explicit Privacy/Security and Implementation gate authorizes it for the target runtime.

#### Scenario: Current synthetic MVP request

- GIVEN the current repository policy limits MVP execution to synthetic or non-sensitive data
- WHEN a request is processed before a PII gate is approved
- THEN `data_classification=synthetic` or `public` MAY proceed under existing gates
- AND `personal` SHALL fail closed or be redirected to an approved non-production-safe path

#### Scenario: Future PII processing is proposed

- GIVEN the Owner product decision allows real customer contact and trip data in the target product
- WHEN PII processing is proposed for implementation
- THEN a separate change SHALL define retention, purpose/consent, encryption, access control, deletion, audit minimization, incident handling, and environment boundaries
- AND this contract approval alone SHALL NOT authorize PII execution

### Requirement: TAIC-103 - Canonical EvidencePack and verified-price provenance

Every material priced option presented as verified SHALL be traceable to immutable canonical evidence.

#### Scenario: Verified price is displayed

- GIVEN a flight or hotel price is presented as verified
- WHEN the proposal is rendered
- THEN the selected item SHALL reference at least one `evidence_id`
- AND the evidence SHALL include provider, provider reference, search time, currency, amount, environment/source classification, and content hash

#### Scenario: Price lacks required provenance

- GIVEN an amount lacks provider identity, provider reference, search timestamp, currency, amount, or valid source classification
- WHEN normalization or rendering runs
- THEN the amount SHALL NOT be labeled verified
- AND it MAY appear only as `ESTIMATE` or `UNVERIFIED` with a visible label

#### Scenario: Evidence becomes stale or invalid

- GIVEN the evidence expires, becomes stale, fails schema validation, or no longer matches the request
- WHEN a new proposal version is generated
- THEN the stale evidence SHALL NOT silently retain `VERIFIED` status
- AND a new search or visible warning SHALL be required

### Requirement: TAIC-104 - Evidence-bound ProposalDraft with partial-result behavior

The system SHALL create versioned Proposal drafts that distinguish verified facts, estimates, assumptions, warnings, and missing information.

#### Scenario: Complete AI draft

- GIVEN sufficient eligible evidence and request data are available
- WHEN planning completes
- THEN the system SHALL create a Proposal with `status=AI_DRAFT` or `READY_FOR_REVIEW`
- AND every selected priced flight or hotel item SHALL reference supporting evidence

#### Scenario: Information is incomplete but useful work exists

- GIVEN the system has enough evidence to prepare part of the trip but material request information is still missing
- WHEN planning completes
- THEN the system SHALL preserve available work in `PARTIAL_DRAFT`
- AND SHALL populate `missing_information[]` and `clarification_questions[]`
- AND SHALL NOT invent the missing value

#### Scenario: No evidence supports a material recommendation

- GIVEN no eligible evidence supports a material flight, hotel, or price claim
- WHEN planning runs
- THEN the system SHALL omit that claim or mark the corresponding section incomplete
- AND SHALL NOT present model memory as verified provider fact

### Requirement: TAIC-105 - Proposal versioning and immutable approval target

Every material Proposal change SHALL create a new version and hash, and approvals SHALL bind to exactly one version and hash.

#### Scenario: Draft is revised before approval

- GIVEN `proposal_version=3` exists
- WHEN material content changes
- THEN the system SHALL create `proposal_version=4`
- AND SHALL calculate a new `proposal_hash`
- AND version 3 SHALL remain immutable

#### Scenario: Approved proposal is changed

- GIVEN version 3 has an `APPROVED` decision
- WHEN any material content is changed to create version 4
- THEN the approval for version 3 SHALL remain historical only
- AND version 4 SHALL require a new Eval and a new Approval before final delivery

### Requirement: TAIC-106 - Eval gate before human approval

A Proposal SHALL pass a versioned Eval suite before it can receive a valid final Agent approval.

#### Scenario: Eval passes

- GIVEN a Proposal has completed mandatory checks
- WHEN `overall_status=PASS`
- THEN the Proposal MAY enter Agent Review

#### Scenario: Eval passes with warnings

- GIVEN mandatory blocking checks pass but non-blocking issues remain
- WHEN `overall_status=PASS_WITH_WARNINGS`
- THEN the Proposal MAY enter Agent Review
- AND all warnings SHALL be visible to the approving agent and recorded in Audit

#### Scenario: Eval fails

- GIVEN any blocking check returns `FAIL`
- WHEN approval is requested
- THEN the system SHALL deny approval
- AND SHALL return the failed check identifiers and remediation hints

#### Scenario: Mandatory MVP checks execute

- GIVEN an AI draft is evaluated
- WHEN the MVP Eval suite runs
- THEN it SHALL check price provenance, currency presence, date/traveler consistency, hard constraints, routing/stops, selected-item evidence coverage, itinerary/evidence contradictions, unsupported facts, secret leakage, unnecessary PII exposure, prohibited actions, and delivery-without-approval

### Requirement: TAIC-107 - Human approval for final proposal and external delivery

An AI Draft MAY be shown to the customer with a clear draft label, but only an authorized travel agent MAY approve a final Proposal version.

#### Scenario: Customer views AI Draft

- GIVEN a draft has not been approved by an agent
- WHEN it is displayed to a customer
- THEN it SHALL be visibly labeled `AI Draft` or equivalent
- AND SHALL NOT be represented as an Agent-approved final proposal

#### Scenario: Agent approves final Proposal

- GIVEN the Proposal version and hash match the current immutable version
- AND the linked Eval is not `FAIL`
- WHEN an authorized agent records `decision=APPROVED`
- THEN an `ApprovalRecord` SHALL capture agent identifier, decision time, proposal version, proposal hash, Eval reference, and approval scope

#### Scenario: Final PDF or external message is requested without valid approval

- GIVEN a user requests final PDF delivery, Email, WhatsApp, publication, or another official external delivery
- WHEN no valid Approval exists for the exact current Proposal version and hash
- THEN the delivery SHALL fail closed
- AND the denial SHALL be recorded in Audit

#### Scenario: Future financial or booking action is requested

- GIVEN a future workflow requests Booking, Hold, Payment, Ticketing, Cancel, Refund, or PNR mutation
- WHEN authorization is evaluated
- THEN a separate action-specific gate SHALL be required in addition to Proposal approval
- AND this contract SHALL NOT authorize the action by itself

### Requirement: TAIC-108 - AuditBundle reconstructs the decision path without secret duplication

Every Proposal workflow SHALL produce a minimized `AuditBundle` that can reconstruct the request-to-output decision chain without embedding secrets or unnecessary personal data.

#### Scenario: Audit bundle is finalized

- GIVEN a Proposal generation reaches review, approval, rejection, or terminal failure
- WHEN the AuditBundle is assembled
- THEN it SHALL reference request snapshot, evidence manifest, ranking record, model/configuration versions, Eval, Approval when present, policy events, usage/cost metadata, and output hash when present

#### Scenario: Sensitive value is encountered

- GIVEN a secret, credential, access token, full provider payload, full prompt, or unnecessary personal value is available to the workflow
- WHEN Audit is written
- THEN the sensitive value SHALL NOT be copied into the AuditBundle by default
- AND only an approved reference, redacted summary, hash, or category SHALL be recorded when needed

#### Scenario: Proposal can be traced

- GIVEN an authorized reviewer has `request_id`, `proposal_id`, and `proposal_version`
- WHEN traceability is inspected
- THEN the reviewer SHALL be able to identify the EvidencePack, EvalResult, ApprovalRecord, system release, and final output hash associated with that exact version

### Requirement: TAIC-109 - One runtime contract for all channels

Web, Email, and WhatsApp SHALL use the same Travel Agent Runtime business contract and SHALL NOT maintain independent planning engines that can produce conflicting Proposals.

#### Scenario: Web request generates a Proposal

- GIVEN the Next.js Web App submits a request
- WHEN generation is invoked
- THEN the Web layer SHALL call the shared Runtime contract
- AND SHALL NOT independently call an LLM or travel provider to create a competing authoritative Proposal

#### Scenario: Email or WhatsApp continues the same request

- GIVEN an existing `request_id` is continued through Email or WhatsApp
- WHEN the channel sends updated information
- THEN the shared Runtime SHALL update or version the same canonical request/proposal chain
- AND channel-specific state SHALL NOT become a second source of truth

### Requirement: TAIC-110 - Contract approval does not authorize implementation

This OpenSpec change SHALL define architecture and contracts only.

#### Scenario: Owner approves Contract v1

- GIVEN the Owner approves this specification package
- WHEN the change is ready for implementation planning
- THEN application code, Provider calls, Runtime migration, PII processing, Production database changes, Billing, and external delivery SHALL remain blocked
- AND a separate bounded implementation gate SHALL be required according to `AGENTS.md`
