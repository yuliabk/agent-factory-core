# Core Contracts v1 Spec Delta

## ADDED Requirements

### Requirement: CORE-201 - Core platform boundaries

The system SHALL keep platform-wide control-plane contracts in Agent Factory Core and SHALL keep agent-specific business behavior independently versioned outside the Core.

#### Scenario: New domain agent
- GIVEN a new Sales Agent requires platform security and model routing
- WHEN its repository is created
- THEN it SHALL consume Core contracts without copying Core policy logic into the agent repository

### Requirement: CORE-202 - Mandatory Agent Manifest

Every runnable agent SHALL provide a versioned machine-readable manifest and the Core SHALL reject manifests that are invalid or request permissions outside approved policy.

#### Scenario: Missing permission declaration
- GIVEN an agent requests a tool not allowed by its manifest/policy
- WHEN execution is attempted
- THEN the request SHALL be denied and audited

### Requirement: CORE-203 - Trusted ExecutionContext

Every agent invocation SHALL receive a trusted ExecutionContext containing tenant, actor, environment, release, permission, budget, model/tool/memory policy, trace and deadline information.

#### Scenario: Prompt tries to change authority
- GIVEN untrusted content instructs the agent to change tenant or permission scope
- WHEN the agent executes
- THEN the trusted ExecutionContext SHALL remain authoritative and the requested escalation SHALL be denied

### Requirement: CORE-204 - Capability-based agent routing

Agent-to-agent delegation SHALL use versioned capabilities resolved by the Core rather than direct repository/URL coupling by default.

#### Scenario: Research implementation replaced
- GIVEN Travel Agent requires `research.lookup`
- WHEN a contract-compatible Research Agent implementation is replaced
- THEN Travel Agent SHALL continue to request the same capability without code changes for the provider identity

#### Scenario: Delegation exceeds hop limit
- GIVEN a delegation chain reaches its configured maximum hop count
- WHEN another agent delegation is requested
- THEN the Core SHALL stop the delegation and record the event

### Requirement: CORE-205 - Provider-neutral model routing

Business agents SHALL request model profiles/capabilities rather than hard-coding a model provider unless an approved requirement explicitly fixes one.

#### Scenario: Provider fallback
- GIVEN the selected provider is unavailable and policy allows fallback
- WHEN a compatible provider satisfies privacy, cost and quality constraints
- THEN the Model Router MAY use the fallback and SHALL record the provider/model used

### Requirement: CORE-206 - Governed tool execution

All governed tool/API/MCP execution SHALL pass schema, permission, tenant, data-policy, budget and approval checks before consequential side effects.

#### Scenario: Indirect prompt injection requests a tool
- GIVEN an external document instructs the agent to call a protected tool
- WHEN the tool request is evaluated
- THEN the document SHALL be treated as untrusted data and the tool SHALL execute only if independent policy authorizes it

### Requirement: CORE-207 - Governed memory access

Persistent memory and client knowledge access SHALL be mediated by a storage-neutral contract that enforces tenant, permission, purpose, classification and retention controls.

#### Scenario: Cross-tenant retrieval
- GIVEN a request belongs to Tenant A
- WHEN memory/knowledge retrieval occurs
- THEN records belonging to Tenant B SHALL NOT be returned

### Requirement: CORE-208 - Budget approval and safety cap

The system SHALL distinguish client/business budget from an independent emergency safety cap.

#### Scenario: Business budget would be exceeded
- GIVEN a new operation would cross the approved business limit
- WHEN preflight or request accounting detects the crossing
- THEN the operation SHALL pause before the new spend and request authorization or a cheaper approved alternative

#### Scenario: Runaway loop
- GIVEN abnormal recursion or repeated tool/model use reaches the safety cap
- WHEN the cap is triggered
- THEN execution SHALL stop without requiring additional business-budget approval

### Requirement: CORE-209 - Evidence, evaluation and approval gates

A production release SHALL be linked to functional, security and cost evaluation evidence plus required human approvals and a rollback target.

#### Scenario: Security eval fails
- GIVEN a release candidate fails a mandatory security evaluation
- WHEN promotion is attempted
- THEN promotion SHALL be blocked

#### Scenario: Release changed after approval
- GIVEN an approval references an earlier manifest/release version
- WHEN a material version change occurs
- THEN the earlier approval SHALL NOT automatically authorize the new version

### Requirement: CORE-210 - Template-first composition

The factory SHALL compose new agents from versioned templates, manifests, policy profiles and agent-specific assets rather than rebuilding platform scaffolding from zero.

#### Scenario: Template upgrade
- GIVEN an existing agent adopts a newer template version
- WHEN the build plan changes
- THEN the exact template version SHALL be recorded and required regression evaluations SHALL run before release

### Requirement: CORE-211 - Non-technical client intake

The factory SHALL collect business intent, critical constraints, consequential-action boundaries and budget without requiring the client to choose technical providers.

#### Scenario: Client does not know technology
- GIVEN a client describes a business outcome but does not know which API/model/runtime is needed
- WHEN intake runs
- THEN the platform SHALL infer/recommend technical options and ask only critical clarifications rather than requiring technical configuration

#### Scenario: Client budget is unknown
- GIVEN the client cannot state an exact budget
- WHEN intake reaches budget planning
- THEN the platform SHALL offer understandable solution tiers or a recommended range before finalizing the build plan

### Requirement: CORE-212 - Minimized audit and release traceability

Consequential operations and releases SHALL record enough minimized evidence to reconstruct decisions, versions, policies, costs and results without storing secrets or unnecessary sensitive content.

#### Scenario: Consequential tool call completes
- GIVEN a protected tool action is allowed and executes
- WHEN it completes or fails
- THEN the audit event SHALL include tenant, request/trace, actor, release, policy/approval reference, tool/capability, cost event, result and timestamp
