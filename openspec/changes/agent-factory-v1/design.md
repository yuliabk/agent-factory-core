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

### Client Data Plane

- Dify project for agent prompts, RAG, workflow, and chat UI.
- n8n project or credential boundary for integrations and actions.
- Dedicated knowledge base and storage namespace.
- Dedicated secrets and audit destination.

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

## Request Flow

1. Receive a request from an approved channel.
2. Resolve tenant and user authorization.
3. Classify the request as knowledge, service, or action.
4. Retrieve approved knowledge when required.
5. Apply policy and approval gates.
6. Execute only an allow-listed workflow.
7. Return a result or escalate to a human.
8. Write a minimized audit event and usage metrics.

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

