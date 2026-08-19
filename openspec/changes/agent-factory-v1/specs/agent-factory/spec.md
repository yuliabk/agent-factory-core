# Agent Factory V1 Spec Delta

## ADDED Requirements

### Requirement AF-101 - Specification-derived configuration

The system SHALL derive each agent's configuration and implementation tasks from an approved OpenSpec change.

#### Scenario - Approved configuration

- GIVEN the Owner approved an agent change
- WHEN Codex prepares the client instance
- THEN every configured capability SHALL map to an approved requirement and task

#### Scenario - Unspecified capability

- GIVEN a requested capability is absent from the approved change
- WHEN implementation is attempted
- THEN the capability SHALL NOT be implemented until the specification is updated and approved

### Requirement AF-102 - Composable agent profiles

The system SHALL support knowledge, customer-service, and action capabilities as composable profiles.

#### Scenario - Knowledge-only client

- GIVEN a client approves only knowledge requirements
- WHEN its instance is configured
- THEN service and action capabilities SHALL remain disabled

### Requirement AF-103 - Grounded knowledge responses

The knowledge capability SHALL answer from approved sources and SHALL provide an insufficient-evidence fallback when grounding is inadequate.

#### Scenario - Supported answer

- GIVEN an approved source contains sufficient evidence
- WHEN the user asks a relevant question
- THEN the response SHALL identify the supporting source

#### Scenario - Unsupported answer

- GIVEN approved sources do not contain sufficient evidence
- WHEN the user asks a question
- THEN the agent SHALL state that it lacks sufficient information and SHALL NOT invent an answer

### Requirement AF-104 - Controlled external actions

The action capability SHALL execute only allow-listed n8n workflows after authorization and required approval checks pass.

#### Scenario - Protected action without approval

- GIVEN an action requires human approval
- WHEN no valid approval exists
- THEN the workflow SHALL NOT execute and the request SHALL enter human review

#### Scenario - Duplicate action request

- GIVEN an action with the same idempotency key already succeeded
- WHEN the request is repeated
- THEN the system SHALL return the prior result without repeating the side effect

### Requirement AF-105 - Client isolation

The system SHALL isolate every client's credentials, knowledge base, state, runtime configuration, and audit records.

#### Scenario - Cross-client retrieval attempt

- GIVEN a request belongs to Client A
- WHEN retrieval is executed
- THEN no source, credential, state, or audit record belonging to Client B SHALL be accessible

### Requirement AF-106 - Channel abstraction and escalation

The system SHALL handle approved channels through a common request contract and SHALL support escalation to a human.

#### Scenario - Website escalation

- GIVEN a website user requests a human or the agent reaches a policy limit
- WHEN escalation occurs
- THEN the system SHALL transfer the minimum necessary context and record the handoff

#### Scenario - Unapproved channel

- GIVEN WhatsApp has not received separate approval
- WHEN a WhatsApp integration is requested
- THEN the system SHALL reject activation and require a dedicated OpenSpec change

### Requirement AF-107 - Audit and observability

The system SHALL record minimized audit and operational events for consequential requests and tool actions.

#### Scenario - Tool execution audit

- GIVEN an allow-listed workflow executes
- WHEN it completes or fails
- THEN the audit record SHALL include tenant, actor, action, approval reference, tool, result, and timestamp without unnecessary sensitive content

### Requirement AF-108 - Cost controls

The system SHALL enforce usage limits and expose monthly cost indicators for the pilot.

#### Scenario - Budget threshold

- GIVEN projected monthly usage reaches a configured threshold
- WHEN additional requests arrive
- THEN the system SHALL alert the Owner and apply the approved degrade or stop policy

### Requirement AF-109 - Reproducible client cloning

The factory SHALL create a client package from versioned templates without copying another client's data or credentials.

#### Scenario - New client clone

- GIVEN an approved client intake and specification
- WHEN a new instance is prepared
- THEN it SHALL receive new identifiers, credentials, storage boundaries, evaluations, and delivery records

### Requirement AF-110 - Data classification enforcement

The system SHALL associate each data source and workflow with a data classification and SHALL block unsupported classifications from the MVP.

#### Scenario - Sensitive source in MVP

- GIVEN a proposed source is medical or financial
- WHEN it is submitted to the MVP
- THEN ingestion SHALL be blocked and a separate security, privacy, and legal approval path SHALL be required

