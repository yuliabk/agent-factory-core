# Design: Agent Factory V1

## Context

The Owner needs a low-code system that can be reused for multiple agent types and cloned for organizations. The system may later handle confidential, personal, medical, or financial information, so isolation and approval controls must exist before those data classes are introduced.

## Goals

- Keep the first prototype understandable and operable by one Owner.
- Separate reusable factory assets from client runtime data.
- Support knowledge, service, and action capabilities through composable modules.
- Make every consequential action auditable and reversible where possible.
- Keep the pilot inside the agreed time and cost constraints.

## Non-Goals

- Build a universal autonomous agent.
- Optimize for large enterprise scale in V1.
- Replace human judgment in regulated or high-impact decisions.

## Proposed Architecture

### Control Plane

- GitHub repository with OpenSpec changes and version history.
- Repo-scoped Skills for repeatable specification workflows.
- Templates for client intake, agent specification, and acceptance tests.
- Evaluation and release-gate definitions.
- Versioned release manifests that reference approved specifications, configuration versions, evidence, and rollback targets without containing secrets or client data.

### Client Data Plane

- Dify project for agent prompts, RAG, workflow, and chat UI.
- n8n project or credential boundary for integrations and actions.
- Dedicated knowledge base and storage namespace.
- Dedicated secrets and audit destination.
- Identity and policy enforcement that executes before retrieval and before every external action.

## Key Decisions

### D1 - Spec-first gate

Implementation begins only after the Owner approves the relevant OpenSpec change.

### D2 - Dify for low-code agent runtime

Dify is proposed because it combines chat, knowledge retrieval, workflow configuration, and model access with limited custom code. This decision remains reversible until prototype approval.

### D3 - n8n for side-effecting actions

All external actions run through named n8n workflows instead of arbitrary model-generated tool calls. Each workflow declares input schema, authorization rule, idempotency strategy, timeout, and audit event.

### D4 - Per-client isolation

Each client receives separate credentials, knowledge, state, logs, and configuration. Reuse occurs through templates and specifications, not through a shared client-data store.

### D5 - Channel sequence

Website chat and internal/email-draft workflows precede WhatsApp. WhatsApp receives a separate change because it adds consent, template, retention, and provider considerations.

### D6 - Policy authority outside the model

The runtime SHALL treat model output as untrusted input. Tenant resolution, authorization, approval validation, data-classification enforcement, and tool allow-list checks execute in deterministic controls outside the prompt.

### D7 - Risk-based isolation

Templates are reusable, but credentials, knowledge indexes, state, audit records, evaluations, and runtime identifiers are new for each client. Logical project isolation is acceptable for non-sensitive prototypes only after negative isolation tests. Higher data classifications require an explicit hosting and isolation decision.

### D8 - Versioned client releases

Every deployment receives an `agent_release_id` linked to the approved OpenSpec change, commit, prompt and workflow versions, policy version, evaluation evidence, approvers, environment, and rollback target. The manifest excludes secrets and customer content. Unrecorded runtime changes are configuration drift and block promotion.

## Accepted Architecture Decisions

- ADR-001: Managed Cloud for a synthetic or approved non-sensitive Prototype; no approval for sensitive data or Production.
- ADR-002: Risk-based client isolation with new credentials, indexes, state, audit, evaluations, and runtime identifiers for every client.
- ADR-003: A versioned `agent_release_id` and release manifest with evidence, approvals, and rollback target, excluding secrets and client content.

## Trust Boundaries

1. Channel to policy boundary: input is untrusted, schema-validated, size-limited, and associated with a tenant and actor.
2. Policy to agent boundary: the agent receives only the minimum authorized context.
3. Agent to knowledge boundary: retrieval is filtered by tenant, source approval, and data classification.
4. Agent to tool boundary: structured output is validated against an allow-listed tool schema and current approval.
5. Client to provider boundary: provider processing, region, retention, deletion, and export capabilities are recorded before data use.
6. Control plane to client boundary: only versioned configuration artifacts flow into the client data plane; client data and secrets do not flow back into Git.

## Common Request Contract

Every channel normalizes requests into a contract containing `request_id`, `tenant_id`, `actor_id`, `actor_type`, `channel`, `environment`, `agent_release_id`, `data_classification`, `intent`, and a schema-validated `payload`. The contract is propagated to retrieval, policy, tools, and minimized audit events.

## Client Lifecycle

1. Intake and risk classification.
2. Approved client-specific OpenSpec change and acceptance set.
3. Provisioning of unique runtime, identity, storage, credential, knowledge, and audit boundaries.
4. Synthetic evaluation and owner-only pilot.
5. Client acceptance and controlled Production promotion when authorized.
6. Suspension that blocks side effects without destroying evidence.
7. Decommissioning that revokes access, exports or returns approved records, removes data and indexes, handles backups according to policy, and records completion evidence.

## Data and Audit Lifecycle

Every data category declares purpose, owner, classification, storage, access, retention, deletion method, and backup behavior. Audit events contain references and decisions rather than full prompts or documents by default. A deletion request covers primary storage, retrieval indexes, caches, exports, and backups within a documented window.

## Release and Drift Control

The promotion sequence is `Draft Spec → Owner Approval → Synthetic Evaluation → Security Checks → Client Acceptance → Release Manifest → Controlled Deployment`. A provider, major model version, prompt, workflow, policy, tool schema, channel, or isolation-boundary change requires a versioned change and proportionate regression evaluation.

## Resilience and Recovery

- External actions fail closed when authorization, approval, policy, or a dependency cannot be verified.
- Retries are bounded and restricted to safe idempotent operations.
- Each client defines an incident owner, degraded mode, rollback target, backup owner, and risk-based RPO/RTO before Production.
- Rollback restores a known configuration version; compensating a completed business action requires its own approved procedure.

## Request Flow

1. Receive a request from an approved channel and assign or validate `request_id`.
2. Resolve tenant, actor, environment, agent release, and data classification.
3. Validate the common request schema and user authorization.
4. Classify the request as knowledge, service, or action.
5. Retrieve tenant-scoped approved knowledge when required.
6. Apply deterministic policy and approval gates outside the model.
7. Validate structured tool input and execute only an allow-listed workflow.
8. Return a result or escalate to a human with minimum necessary context.
9. Write a minimized audit event and usage metrics linked to `agent_release_id`.

## Failure Handling

- Retrieval uncertainty: respond with insufficient-information fallback.
- Tool timeout: stop, record failure, and offer human follow-up.
- Duplicate request: use idempotency key and avoid repeated side effects.
- Authorization failure: deny without revealing protected information.
- Provider outage: fail closed for actions and provide a service-status fallback.

## Evaluation Strategy

- Grounded-answer accuracy and citation coverage.
- Refusal when evidence is insufficient.
- Prompt-injection resistance.
- Authorization and tenant-isolation tests.
- Correct escalation and human-approval behavior.
- Action idempotency and rollback behavior.
- Cost per completed request and monthly cap alerts.

## Rollout

1. Synthetic local or sandbox evaluation.
2. Owner-only website prototype.
3. Limited internal pilot with non-sensitive information.
4. Security and privacy review.
5. Client-specific pilot under a separate approved change.

## Open Decisions

- Dify Cloud versus self-hosted.
- n8n Cloud versus self-hosted.
- Storage and vector-store provider.
- Log destination and retention duration.
- First reversible business action.
- First document collection and acceptance dataset.
- Isolation tier required for each data classification.
- Default retention windows and deletion evidence format.
- Prototype release-manifest template and drift-detection method.
- Risk-based RPO/RTO defaults for future client tiers.

