## ADDED Requirements

### Requirement: RP-101 Canonical Provider-Neutral Source of Truth

The system SHALL treat the approved Git/OpenSpec release, corpus manifest, request/answer contract, and evaluation set as the canonical source of truth, independent of any runtime provider.

#### Scenario: Provider configuration conflicts with the canonical release

GIVEN a provider configuration differs from the approved canonical release
WHEN portability preflight compares their immutable identities
THEN the system SHALL report configuration drift
AND SHALL block evaluation or runtime execution.

### Requirement: RP-102 Versioned Runtime Adapter Contract

The system SHALL require every runtime mapping to declare a stable adapter identifier, SemVer adapter version, runtime and plan, immutable configuration reference, agent release, corpus version, and question-set version.

#### Scenario: Adapter identity is complete

GIVEN all required adapter and canonical identities are immutable and present
WHEN the adapter declaration is validated
THEN the system SHALL accept the identity portion of preflight
AND SHALL preserve those identities in every evaluation record.

#### Scenario: Adapter identity is missing or mutable

GIVEN a required identity is missing, mutable, or inconsistent
WHEN the adapter declaration is validated
THEN the system SHALL fail preflight
AND SHALL identify the blocking field.

### Requirement: RP-103 Normalized Request and Response Mapping

The adapter SHALL map the canonical Hebrew request and normalized answer contract without weakening locale, corpus, policy, citation, or tool restrictions.

#### Scenario: Supported answer is normalized

GIVEN a runtime returns a Hebrew answer grounded in approved retrieved evidence
WHEN the adapter maps the result
THEN the normalized response SHALL contain the Hebrew answer and resolvable citations
AND `tool_calls` SHALL be an empty array.

#### Scenario: Provider option attempts to weaken policy

GIVEN a provider-specific option conflicts with the canonical deny-all tool policy or approved corpus boundary
WHEN the request is mapped
THEN the adapter SHALL reject the option
AND SHALL block the request.

### Requirement: RP-104 Local Evaluation Runner Plan

The system SHALL define a deterministic local evaluation runner that can validate adapter declarations and synthetic evidence fixtures without network, model, provider, credential, indexing, or payment access.

#### Scenario: Local dry validation is authorized

GIVEN a valid adapter declaration, frozen question set, and synthetic fixtures exist locally
WHEN the dry runner is invoked under approved PR-G1
THEN it SHALL validate schemas, identities, evidence, citations, policies, and ceilings without external calls
AND SHALL record all runtime questions as `not_run`.

#### Scenario: Live execution is requested without PR-G2

GIVEN PR-G2 has not been explicitly approved
WHEN a runner operation would call a model or provider
THEN the system SHALL block the operation
AND SHALL record missing authorization as the reason.

### Requirement: RP-105 Citation and Fallback Preservation

The adapter and evaluator SHALL preserve the approved citation and fallback rules and SHALL NOT fabricate provenance when a runtime omits evidence.

#### Scenario: Citation resolves to retrieved evidence

GIVEN an answer cites an approved `source_id` and section present in retrieved evidence
WHEN the evaluator validates the response
THEN it SHALL accept the citation relationship
AND SHALL retain the provider evidence reference.

#### Scenario: Citation provenance is absent

GIVEN an answer contains a citation that cannot be resolved to retrieved approved evidence
WHEN the evaluator validates the response
THEN it SHALL fail the citation verdict
AND SHALL NOT infer or generate missing provenance.

#### Scenario: Approved evidence is insufficient

GIVEN the retrieved approved evidence is insufficient to support an answer
WHEN the response is normalized
THEN the adapter SHALL return the approved Hebrew fallback classification
AND SHALL NOT present unsupported content as an answer.

### Requirement: RP-106 Runtime and Client Isolation

Every future runtime pilot SHALL isolate credentials, configuration, storage, knowledge, indexes, logs, and evidence by client and runtime and SHALL use synthetic data only during the prototype phase.

#### Scenario: Isolation evidence is complete

GIVEN a candidate runtime has dedicated scoped resources and credentials for one synthetic prototype
WHEN security preflight examines the declared boundaries
THEN it SHALL record the isolation evidence
AND MAY allow the security portion of preflight to pass.

#### Scenario: A resource is shared across clients

GIVEN any credential, knowledge store, index, log destination, or configuration is shared across client boundaries
WHEN security preflight runs
THEN it SHALL fail closed
AND SHALL block data upload and runtime execution.

### Requirement: RP-107 Normalized Cost and Hard Stops

Every future live evaluation SHALL preserve provider-native usage and cost units, calculate a traceable normalized estimate, and enforce both a provider-native limit and an Owner-approved normalized ceiling.

#### Scenario: Cost evidence and limits are available

GIVEN provider-native usage is observable, conversion metadata is current, and both limits are approved
WHEN cost preflight runs
THEN it SHALL record native and normalized ceilings with their stop thresholds
AND MAY allow the cost portion of preflight to pass.

#### Scenario: Cost is unknown

GIVEN native usage, price, conversion, or an enforceable limit is unknown
WHEN cost preflight runs
THEN the system SHALL treat the condition as blocking rather than zero cost
AND SHALL prohibit live execution.

#### Scenario: A run approaches a ceiling

GIVEN an authorized future live run reaches its configured stop threshold
WHEN usage is evaluated
THEN the runner SHALL stop before the approved ceiling is exceeded
AND SHALL prohibit automatic retry.

### Requirement: RP-108 Capability Gaps and Drift Fail Closed

The system SHALL represent required runtime capabilities as supported, unsupported, or unknown and SHALL block a pilot when a required capability is unsupported, unknown, or drifted.

#### Scenario: Required capability is unknown

GIVEN citation provenance, isolation, external-action suppression, usage limits, export, deletion, or retention is marked unknown
WHEN candidate preflight runs
THEN it SHALL fail closed
AND SHALL list the evidence required to continue.

#### Scenario: Provider configuration changes after approval

GIVEN an approved mapping or provider configuration changes
WHEN its immutable reference is compared before execution
THEN the system SHALL invalidate the prior preflight
AND SHALL require a new run identity and approval.

### Requirement: RP-109 Botpress Candidate Mapping

The system SHALL maintain a planning-only Botpress mapping that covers canonical release, prompt/policy, knowledge, retrieval evidence, response, evaluation, cost, export, deletion, and isolation concepts without claiming equivalence.

#### Scenario: Botpress mapping is reviewed

GIVEN the local Botpress mapping documents known capabilities, gaps, assumptions, and dated cost inputs
WHEN the planning package is reviewed
THEN the Owner SHALL be able to distinguish verified evidence from future preflight work
AND no Botpress account or runtime authorization SHALL be implied.

#### Scenario: Botpress citation or spend control is unproven

GIVEN exact citation provenance or enforceable AI-spend and event stops are unproven
WHEN Botpress is considered for PR-G2
THEN the candidate SHALL remain blocked.

#### Scenario: Botpress passes public continuity review but controls remain partial

GIVEN public evidence shows an active vendor and documented knowledge, usage, export, privacy, and deletion capabilities
AND exact section provenance, deny-all behavior, complete deletion, Hebrew fallback, or plan-specific isolation remains unverified
WHEN the Botpress public preflight is completed
THEN the candidate MAY be marked `CONDITIONAL-GO` for later synthetic evaluation
AND account creation, authenticated inspection, data upload, Indexing, Runtime, and payment SHALL remain blocked.

#### Scenario: Botpress account registration is separately authorized

GIVEN the Owner separately approves A0 for one Botpress Free account
WHEN the official registration flow requires personal or authentication data
THEN the Owner SHALL enter that data directly
AND Codex SHALL NOT enter or read personal data, passwords, or verification codes
AND no additional workspace, Bot, Knowledge Base, credential, model, payment, Indexing, Emulator, Runtime, or publication SHALL be created or configured.

#### Scenario: Botpress authenticated read-only inspection is separately authorized

GIVEN A0 is complete and the Owner separately approves A1 read-only inspection
WHEN the existing default workspace, usage page, and billing summary are inspected
THEN the evidence SHALL record only non-personal plan identity, allowances, and current counters
AND SHALL NOT open or change plan management, payment, account identity, settings, tools, integrations, credentials, model configuration, knowledge, or Runtime controls.

#### Scenario: Botpress Free allowance is visible but a hard stop is unproven

GIVEN the authenticated Free workspace displays plan allowances and current usage
AND the UI displays an AI-usage allowance without verified enforcement behavior
WHEN cost preflight evaluates the authenticated evidence
THEN the allowance SHALL NOT be treated as an enforceable provider-native hard stop
AND the candidate SHALL remain blocked from Runtime until a separately approved inspection proves an Owner-approved stop without payment or billable execution.

#### Scenario: Botpress workspace controls are inspected read-only

GIVEN the Owner separately approves A2 read-only inspection
WHEN workspace cost, membership, audit, deletion, and export surfaces are inspected
THEN the evidence SHALL distinguish a disabled auto-recharge setting from an enforceable hard cap
AND SHALL record only the presence or absence of controls without activating Delete, Manage, Payment, Invite, Increase limits, export, or Bot controls
AND SHALL NOT read personal data or audit-event contents.

#### Scenario: Botpress state drifts after authenticated evidence

GIVEN A1 records a workspace with no Bot
AND a later read-only inspection observes one or more Bot routes
WHEN the candidate evidence is reviewed
THEN the system SHALL preserve A1 as a historical observation
AND SHALL mark the current provider configuration as drifted without inferring who created or changed it
AND SHALL require a fresh bounded identity, evidence snapshot, and Owner approval before any further provider preflight or Runtime activity.

#### Scenario: Botpress drift reconciliation lacks attributable audit evidence

GIVEN the Owner separately approves A3 read-only reconciliation
AND two distinct Bot routes are counted without opening either Bot
WHEN the available Audits surface exposes no event rows, timestamps, or create/update/delete categories
THEN the evidence SHALL record the Bot count and observation date only
AND SHALL keep creator, creation method, creation timestamp, configuration, and approval status as `unknown`
AND SHALL NOT treat ambiguous relative-time text as creation provenance
AND the configuration drift SHALL remain unresolved and blocking.

#### Scenario: Botpress drift is disclaimed by the Owner

GIVEN the Owner states that she did not create the observed Bots
AND read-only incident triage confirms that the Bot routes persist
AND file storage has increased while conversations, AI spend, table rows, and vector storage remain zero
WHEN incident preflight evaluates the workspace
THEN the system SHALL place Botpress on `INCIDENT-HOLD`
AND SHALL preserve only minimized non-personal evidence
AND SHALL prohibit opening, executing, modifying, or deleting either Bot
AND SHALL require Owner-controlled account containment and a separately approved re-verification before any provider preflight or pilot can resume.

#### Scenario: Botpress incident state is stable but containment is unverified

GIVEN a separately approved read-only re-verification observes no change in Bot count, file storage, usage, billing, or audit evidence
AND Owner-controlled identity-provider containment has not been confirmed
WHEN incident status is reviewed
THEN the system SHALL record the provider state as stable relative to the prior incident snapshot
AND SHALL NOT infer that the Bots are authorized or that account access is contained
AND SHALL keep the incident `Investigating` and the candidate on `INCIDENT-HOLD`
AND SHALL prohibit transition to `Monitoring`, resolution, or provider preflight.

### Requirement: RP-110 Flowise Candidate Mapping

The system SHALL maintain a planning-only Flowise mapping that covers canonical release, prompt/policy, document and vector stores, retrieval evidence, response, evaluation, cost, export, deletion, and isolation concepts without claiming equivalence.

#### Scenario: Flowise mapping is reviewed

GIVEN the local Flowise mapping documents known capabilities, gaps, assumptions, and dated cost inputs
WHEN the planning package is reviewed
THEN the Owner SHALL be able to distinguish verified evidence from future preflight work
AND no Flowise account or runtime authorization SHALL be implied.

#### Scenario: Flowise metadata or combined cost stop is unproven

GIVEN exact metadata propagation or enforceable combined Flowise and model-provider cost stops are unproven
WHEN Flowise is considered for PR-G2
THEN the candidate SHALL remain blocked.

#### Scenario: Flowise upstream reaches end of life

GIVEN the official Flowise vendor has announced wind-down, archived the upstream repository, and scheduled End of Life
WHEN Flowise Cloud or the official upstream is considered for a new pilot
THEN the candidate SHALL fail the vendor-continuity preflight
AND published pricing or technical features SHALL NOT override the block.

### Requirement: RP-111 One-Runtime-at-a-Time Approval

The system SHALL require separate Owner approval for local implementation and for exactly one candidate provider's external preflight or pilot, with explicit authorization for every external action and cost-bearing resource.

#### Scenario: Planning package is approved

GIVEN the Owner approves P0 through P3 planning
WHEN the change is recorded
THEN only the local planning package SHALL be authorized
AND implementation, accounts, credentials, data operations, runtime, payment, and publication SHALL remain unauthorized.

#### Scenario: Multiple candidate pilots are proposed

GIVEN more than one external runtime candidate is included in a proposed pilot authorization
WHEN PR-G2 is evaluated
THEN the gate SHALL fail
AND SHALL require selection of exactly one candidate.

### Requirement: RP-112 Export, Deletion, and Reconstruction

A future candidate pilot SHALL prove that canonical assets remain in Git, secrets are excluded from exports, provider-side prototype data can be deleted, and the runtime configuration can be reconstructed from an approved release and sanitized provider references.

#### Scenario: Reconstruction evidence is complete

GIVEN a sanitized export or immutable configuration reference and the canonical release are available
WHEN reconstruction is assessed
THEN the evaluator SHALL verify that required behavior and control settings can be reproduced
AND SHALL record any provider-managed state that remains non-portable.

#### Scenario: Secrets appear in an export

GIVEN a provider export contains a credential, token, or secret value
WHEN export validation runs
THEN the artifact SHALL be rejected from Git and evidence bundles
AND the security gate SHALL fail.

#### Scenario: Deletion scope is undefined

GIVEN deletion or retention behavior for documents, chunks, vectors, conversations, logs, runs, or backups is undefined
WHEN exit preflight runs
THEN the candidate SHALL remain blocked from a pilot.
