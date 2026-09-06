# Core Contracts v1 Spec Delta

## ADDED Requirements

### Requirement: CORE-201 - Core platform boundaries

The system SHALL keep platform-wide contracts and controls in Agent Factory Core, logically separating Build / Control Plane from Runtime Governance Plane, while keeping Agent-specific business behavior independently versioned outside Core.

#### Scenario: New domain Agent
- GIVEN a new Sales Agent requires platform security/model routing
- WHEN its repository is created
- THEN it SHALL consume Core contracts without copying Core policy logic into the Agent repository

### Requirement: CORE-202 - Minimal reusable AgentManifest and client-specific configuration

Every runnable Agent SHALL provide a versioned machine-readable `AgentManifest` that remains reusable across clients.

The first executable AgentManifest schema SHALL keep only these top-level fields:

- `apiVersion`
- `kind`
- `metadata`
- `spec`

For the first schema, `metadata` SHALL contain `name`, `version` and `description`.

For the first schema, `spec` SHALL contain only:

- `template`
- `capabilities`
- `tools`
- `permissions`
- `memoryProfile`
- `budgetProfile`
- `evalProfile`

Manifest permission/profile fields SHALL represent reusable Agent requirements or profile references, not concrete tenant authorization grants, client budget amounts, credentials or client-specific runtime bindings.

Client-specific grants, budget, retention, provider restrictions, credential references, tenant/environment identity and runtime bindings SHALL remain in `ClientInstanceConfig`.

New AgentManifest fields SHOULD be added only after a real use case demonstrates that the value belongs to the reusable Agent Definition rather than client configuration or PlatformPolicy.

#### Scenario: Same Agent for two clients
- GIVEN the same Research Agent version is deployed to two tenants
- WHEN each tenant has different budget/provider/tool policies
- THEN the Agent repository and AgentManifest SHALL remain reusable while ClientInstanceConfig differs per tenant

#### Scenario: Agent requests permission
- GIVEN AgentManifest requests `web.search`
- WHEN the client/platform policy does not grant it
- THEN the Agent SHALL NOT receive the permission simply because it requested it

#### Scenario: Minimal manifest validates
- GIVEN an AgentManifest contains the required top-level fields, `metadata.name/version/description`, and the seven required `spec` keys
- WHEN the first Core Skeleton validator runs
- THEN the manifest SHALL be eligible for compilation without requiring speculative future fields

### Requirement: CORE-203 - Effective Release compilation

The Build / Control Plane SHALL compile `AgentManifest + ClientInstanceConfig + PlatformPolicy + valid ExceptionPolicy overlays` into an immutable `EffectiveReleaseConfig` for each `agent_release_id`.

#### Scenario: Runtime receives drafts
- GIVEN an uncompiled client draft differs from the last EffectiveReleaseConfig
- WHEN Runtime execution begins
- THEN Runtime SHALL use the immutable EffectiveReleaseConfig rather than the draft

### Requirement: CORE-204 - Trusted ExecutionContext

Every Agent invocation SHALL receive a trusted ExecutionContext containing tenant, actor, environment, release, effective permission, trust, budget, model/tool/memory policy, trace and deadline information.

#### Scenario: Prompt tries to change authority
- GIVEN untrusted content instructs the Agent to change tenant/permission scope
- WHEN execution occurs
- THEN trusted ExecutionContext/EffectiveReleaseConfig SHALL remain authoritative and the escalation SHALL be denied

### Requirement: CORE-205 - Capability-based Agent routing

Agent-to-Agent delegation SHALL use versioned capabilities resolved by Core rather than direct repository/URL coupling by default.

#### Scenario: Research implementation replaced
- GIVEN Travel Agent requires `research.lookup`
- WHEN a contract-compatible Research implementation is replaced
- THEN Travel Agent SHALL continue to request the same capability without business-code changes

#### Scenario: Delegation exceeds hop limit
- GIVEN a delegation chain reaches its configured maximum hop count
- WHEN another delegation is requested
- THEN Core SHALL stop the delegation and record the event

### Requirement: CORE-206 - Soft-strict Capability Registry enforcement

Capability Registry enforcement SHALL permit policy-defined warnings/mocks/degraded optional resolution in sandbox/development while requiring critical/consequential production capabilities to resolve to registered, compatible and policy-approved implementations.

#### Scenario: Optional dev capability missing
- GIVEN an optional capability is missing in sandbox
- WHEN policy marks it non-critical
- THEN the system MAY warn/degrade without blocking the entire Agent

#### Scenario: Critical production capability missing
- GIVEN a required consequential capability is unresolved in production
- WHEN execution/release is attempted
- THEN the affected operation/release SHALL be blocked according to policy

### Requirement: CORE-207 - Provider-neutral policy-driven routing

Business Agents SHALL request model/capability profiles rather than hard-code a provider by default. Routing SHALL be policy-driven across cost, quality, privacy/data, trust, latency and availability constraints.

#### Scenario: Economy client
- GIVEN client policy prioritizes economy while preserving a minimum quality/privacy floor
- WHEN routing occurs
- THEN the Router SHALL select an allowed lower-cost implementation meeting that floor rather than always selecting the highest-quality model

#### Scenario: Provider fallback
- GIVEN selected provider is unavailable and policy allows fallback
- WHEN a compatible provider satisfies effective privacy, cost and quality constraints
- THEN Router MAY use it and SHALL record the implementation used

### Requirement: CORE-208 - Governed Tool/API/MCP execution

All governed Tool/API/MCP execution SHALL pass schema, permission, tenant, risk/side-effect, data-policy, budget and policy-defined approval checks before consequential side effects.

#### Scenario: Indirect prompt injection requests a tool
- GIVEN an external document instructs the Agent to call a protected tool
- WHEN tool request is evaluated
- THEN the document SHALL be treated as untrusted data and the tool SHALL execute only if independent policy authorizes it

### Requirement: CORE-209 - Governed autonomous memory

Memory SHALL be mediated by a storage-neutral Memory Gateway enforcing tenant, permission, purpose, memory class, classification and retention controls. An Agent MAY autonomously request/write memory when effective policy permits.

#### Scenario: Useful persistent memory
- GIVEN an Agent identifies information useful for future work
- WHEN it requests a persistent write
- THEN policy SHALL decide whether to allow, minimize/transform, deny or require consent/approval

#### Scenario: Cross-tenant retrieval
- GIVEN a request belongs to Tenant A
- WHEN memory/knowledge retrieval occurs
- THEN records belonging to Tenant B SHALL NOT be returned

### Requirement: CORE-210 - Risk-based Trust Profiles and controlled exceptions

PlatformPolicy SHALL support trust/risk profiles and distinguish non-overridable invariants from rules that MAY be overridden through a valid scoped ExceptionPolicy.

#### Scenario: Client asks for higher authority
- GIVEN Factory recommends `internal` and PlatformPolicy ceiling is `business`
- WHEN client config requests `privileged`
- THEN compilation SHALL reject the request unless an applicable overridable rule and valid ExceptionPolicy permit it

#### Scenario: Non-overridable invariant
- GIVEN an ExceptionPolicy attempts to override a non-overridable rule
- WHEN configuration is compiled
- THEN the exception SHALL be rejected

### Requirement: CORE-211 - Budget approval and independent safety cap

The system SHALL distinguish client/business budget from an independent emergency safety cap.

#### Scenario: Business budget would be exceeded
- GIVEN a new operation would cross the approved business limit
- WHEN policy requires preflight handling
- THEN the system SHALL offer an allowed cheaper alternative or pause the new spend for authorized overage approval

#### Scenario: Runaway loop
- GIVEN abnormal recursion or repeated use reaches the safety cap
- WHEN the cap triggers
- THEN execution SHALL stop regardless of business-budget overage approval

### Requirement: CORE-212 - Policy-driven evaluation gates

The system SHALL support functional/business, security/policy, cost/runtime and contract/portability evaluations and SHALL let PlatformPolicy classify checks/thresholds as blocking, warning or advisory.

#### Scenario: Business quality below preferred target
- GIVEN business-quality score is below a preferred target but above policy minimum
- WHEN release eligibility is evaluated
- THEN policy MAY allow release with warnings rather than universally blocking it

#### Scenario: Non-overridable security failure
- GIVEN a release candidate fails a non-overridable security check
- WHEN promotion is attempted
- THEN promotion SHALL be blocked

### Requirement: CORE-213 - Policy-driven release strategy

Every release SHALL use a versioned effective release strategy of `human-required`, `policy-auto` or `policy`, with PlatformPolicy allowed to require a stricter strategy than requested.

#### Scenario: Low-risk auto release
- GIVEN a compatible low-risk change and policy permits `policy-auto`
- WHEN all blocking gates pass
- THEN release MAY proceed automatically and SHALL create a release decision/evidence record

#### Scenario: Permission expansion
- GIVEN a change expands permissions and policy requires human approval
- WHEN Agent/client requests auto release
- THEN the effective strategy SHALL require human approval

### Requirement: CORE-214 - Hybrid bounded-autonomy orchestration

Core SHALL enforce trusted boundaries while allowing Business Agents to autonomously plan, decompose work and request approved capabilities inside those boundaries.

#### Scenario: Agent replans after provider failure
- GIVEN an approved provider/capability fails
- WHEN another allowed capability/fallback exists
- THEN the Agent MAY replan/request it without gaining additional authority

### Requirement: CORE-215 - Hybrid template-first composition

Factory SHALL use a smallest-suitable base template plus modular capability composition and SHALL prefer progressive complexity over building every Agent from zero or forcing a rigid template.

#### Scenario: New integration becomes necessary
- GIVEN an Agent initially needs only knowledge retrieval
- WHEN later spec adds CRM write capability
- THEN Factory SHOULD add the approved module/capability rather than rebuild unrelated platform scaffolding

### Requirement: CORE-216 - Non-technical client intake

Factory SHALL collect business intent, critical constraints, consequential-action boundaries and budget without requiring clients to choose technical providers.

#### Scenario: Ambiguous request
- GIVEN client describes a broad business outcome without technical details
- WHEN intake runs
- THEN the platform SHALL infer a reasonable configuration, show material assumptions, and ask the client to confirm/correct them

#### Scenario: Intake duration
- GIVEN a normal uncomplicated client request
- WHEN intake is performed
- THEN the product SHOULD target under ten minutes and typically 5-6 critical follow-up questions, without treating that target as a hard technical limit

### Requirement: CORE-217 - Minimized audit and release traceability

Consequential operations and releases SHALL record enough minimized evidence to reconstruct decisions, effective authority, versions, policy/exception use, costs and results without storing secrets or unnecessary sensitive content.

#### Scenario: Consequential tool call completes
- GIVEN a protected tool action is allowed and executes
- WHEN it completes/fails
- THEN audit SHALL include tenant, request/trace, actor, release, policy/exception/approval reference, tool/capability, cost event, result and timestamp

### Requirement: CORE-218 - Specification as primary artifact

Material platform/Agent behavior SHALL be traceable to a versioned approved specification, and deployed instances SHALL be treated as reproducible outputs rather than the sole source of truth.

#### Scenario: Runtime drift
- GIVEN a deployed configuration cannot be mapped to the approved spec and EffectiveReleaseConfig
- WHEN drift detection runs
- THEN the deployment SHALL be flagged as unmanaged drift and handled according to policy
