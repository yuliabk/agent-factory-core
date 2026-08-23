# Agent Factory V1 Spec Delta

## ADDED Requirements

### Requirement: AF-101 - Specification-derived configuration

The system SHALL derive each agent's configuration and implementation tasks from an approved OpenSpec change.

#### Scenario: Approved configuration

- GIVEN the Owner approved an agent change
- WHEN Codex prepares the client instance
- THEN every configured capability SHALL map to an approved requirement and task

#### Scenario: Unspecified capability

- GIVEN a requested capability is absent from the approved change
- WHEN implementation is attempted
- THEN the capability SHALL NOT be implemented until the specification is updated and approved

### Requirement: AF-102 - Composable agent profiles

The system SHALL support knowledge, customer-service, and action capabilities as composable profiles.

#### Scenario: Knowledge-only client

- GIVEN a client approves only knowledge requirements
- WHEN its instance is configured
- THEN service and action capabilities SHALL remain disabled

### Requirement: AF-103 - Grounded knowledge responses

The knowledge capability SHALL answer from approved sources and SHALL provide an insufficient-evidence fallback when grounding is inadequate.

#### Scenario: Supported answer

- GIVEN an approved source contains sufficient evidence
- WHEN the user asks a relevant question
- THEN the response SHALL identify the supporting source

#### Scenario: Unsupported answer

- GIVEN approved sources do not contain sufficient evidence
- WHEN the user asks a question
- THEN the agent SHALL state that it lacks sufficient information and SHALL NOT invent an answer

### Requirement: AF-104 - Controlled external actions

The action capability SHALL execute only allow-listed n8n workflows after authorization and required approval checks pass.

#### Scenario: Protected action without approval

- GIVEN an action requires human approval
- WHEN no valid approval exists
- THEN the workflow SHALL NOT execute and the request SHALL enter human review

#### Scenario: Duplicate action request

- GIVEN an action with the same idempotency key already succeeded
- WHEN the request is repeated
- THEN the system SHALL return the prior result without repeating the side effect

### Requirement: AF-105 - Client isolation

The system SHALL isolate every client's credentials, knowledge base, state, runtime configuration, and audit records.

#### Scenario: Cross-client retrieval attempt

- GIVEN a request belongs to Client A
- WHEN retrieval is executed
- THEN no source, credential, state, or audit record belonging to Client B SHALL be accessible

### Requirement: AF-106 - Channel abstraction and escalation

The system SHALL handle approved channels through a common request contract and SHALL support escalation to a human.

#### Scenario: Website escalation

- GIVEN a website user requests a human or the agent reaches a policy limit
- WHEN escalation occurs
- THEN the system SHALL transfer the minimum necessary context and record the handoff

#### Scenario: Unapproved channel

- GIVEN WhatsApp has not received separate approval
- WHEN a WhatsApp integration is requested
- THEN the system SHALL reject activation and require a dedicated OpenSpec change

### Requirement: AF-107 - Audit and observability

The system SHALL record minimized audit and operational events for consequential requests and tool actions.

#### Scenario: Tool execution audit

- GIVEN an allow-listed workflow executes
- WHEN it completes or fails
- THEN the audit record SHALL include tenant, actor, action, approval reference, tool, result, and timestamp without unnecessary sensitive content

### Requirement: AF-108 - Cost controls

The system SHALL enforce usage limits and expose monthly cost indicators for the pilot.

#### Scenario: Budget threshold

- GIVEN projected monthly usage reaches a configured threshold
- WHEN additional requests arrive
- THEN the system SHALL alert the Owner and apply the approved degrade or stop policy

### Requirement: AF-109 - Reproducible client cloning

The factory SHALL create a client package from versioned templates without copying another client's data or credentials.

#### Scenario: New client clone

- GIVEN an approved client intake and specification
- WHEN a new instance is prepared
- THEN it SHALL receive new identifiers, credentials, storage boundaries, evaluations, and delivery records

### Requirement: AF-110 - Data classification enforcement

The system SHALL associate each data source and workflow with a data classification and SHALL block unsupported classifications from the MVP.

#### Scenario: Sensitive source in MVP

- GIVEN a proposed source is medical or financial
- WHEN it is submitted to the MVP
- THEN ingestion SHALL be blocked and a separate security, privacy, and legal approval path SHALL be required

### Requirement: AF-111 - Identity, authorization, and approval integrity

The system SHALL resolve tenant, actor, environment, and agent release before retrieval or tool use, and SHALL enforce authorization and approval through deterministic policy controls outside the language model.

#### Scenario: Model requests an unauthorized tool

- GIVEN the model emits a structurally valid request for a tool the actor is not authorized to use
- WHEN the policy control evaluates the request
- THEN execution SHALL be denied and the denial SHALL be recorded without exposing protected data

#### Scenario: Approval replay

- GIVEN an approval belongs to a different request, action, target, tenant, or expired time window
- WHEN an action attempts to use that approval
- THEN the approval SHALL be rejected and the action SHALL NOT execute

#### Scenario: Unknown tenant or actor

- GIVEN a request cannot be associated with a known tenant and authorized actor
- WHEN the request reaches the runtime
- THEN retrieval and external actions SHALL be denied and the request SHALL follow the approved fallback path

### Requirement: AF-112 - Controlled client lifecycle

The system SHALL manage each client instance through documented intake, specification, provisioning, pilot, promotion, suspension, and decommissioning states.

#### Scenario: Client provisioning

- GIVEN a client specification is approved
- WHEN its instance is provisioned
- THEN new runtime identifiers, credentials, storage, knowledge indexes, audit boundaries, and evaluation records SHALL be created without copying another client's data or secrets

#### Scenario: Client suspension

- GIVEN a client instance is suspended
- WHEN a request attempts an external action
- THEN the action SHALL be blocked while required audit evidence remains available according to policy

#### Scenario: Client decommissioning

- GIVEN decommissioning is approved
- WHEN the process completes
- THEN access SHALL be revoked and data, indexes, caches, credentials, exports, and backups SHALL be returned or removed according to the documented policy with completion evidence

### Requirement: AF-113 - Versioned releases and drift control

The system SHALL assign every deployed client configuration an `agent_release_id` linked to an approved specification, versioned configuration, evaluation evidence, approvers, environment, and rollback target without storing secrets or client content in the release manifest.

#### Scenario: Approved release

- GIVEN all required release gates passed
- WHEN a client configuration is promoted
- THEN the deployed `agent_release_id` SHALL resolve to the exact approved evidence and configuration versions

#### Scenario: Unrecorded runtime change

- GIVEN runtime configuration differs from its release manifest
- WHEN promotion or verification runs
- THEN the difference SHALL be reported as drift and further promotion SHALL be blocked until reviewed

#### Scenario: Rollback

- GIVEN a release fails its approved health or quality threshold
- WHEN rollback is authorized
- THEN configuration SHALL return to a known approved `agent_release_id` and the rollback result SHALL be audited

### Requirement: AF-114 - Resilience and recoverability

The system SHALL fail closed for consequential actions and SHALL define bounded retry, degraded mode, backup ownership, rollback, and risk-based RPO/RTO before Production.

#### Scenario: Policy or dependency unavailable

- GIVEN authorization, approval, policy, or an action dependency cannot be verified
- WHEN a consequential action is requested
- THEN the action SHALL NOT execute and the system SHALL provide the approved retry or human-escalation path

#### Scenario: Restore rehearsal

- GIVEN a client tier has approved RPO and RTO targets
- WHEN a restore rehearsal is executed
- THEN recovery evidence SHALL show whether both targets were met without crossing client boundaries

### Requirement: AF-115 - Data and audit lifecycle

The system SHALL define purpose, owner, classification, access, retention, deletion, and backup behavior for each stored data category and SHALL minimize audit content.

#### Scenario: Minimized audit event

- GIVEN a consequential request or tool action completes or fails
- WHEN its audit event is written
- THEN the event SHALL contain correlation, actor, release, decision, approval, tool, result, environment, and timestamp fields without full prompts, documents, or secrets by default

#### Scenario: Verified deletion

- GIVEN an authorized deletion request reaches its due date
- WHEN deletion is executed
- THEN primary storage, retrieval indexes, caches, exports, and backups SHALL be handled within the documented window and evidence SHALL be recorded

