# Memory Contract

**Status:** Accepted direction; first session/task slice implemented

## Purpose

Memory is a governed platform capability, not arbitrary persistent storage controlled by an Agent prompt.

The platform keeps memory classes logically separated so client data, operational state and platform knowledge do not become one undifferentiated store.

## Memory classes

- `session` - short-lived conversational/task context.
- `task_working` - temporary working state for a bounded task or workflow.
- `user_persistent` - longer-lived user/client memory with explicit purpose and retention policy.
- `client_knowledge` - governed retrieval over tenant knowledge sources.
- `operational_state` - workflow/task state required for execution and recovery.
- `platform_knowledge` - reusable platform templates, policies, best practices and non-client-specific knowledge.

These may be physically separate stores or strongly separated logical namespaces. The contract requires the separation semantics, not a specific database architecture.

## Agent autonomy

An Agent MAY decide that information is useful to remember and request/write memory without asking a human every time, provided the EffectiveReleaseConfig and PlatformPolicy permit that memory class, purpose, data class and retention.

The Agent does not decide whether a forbidden write becomes allowed.

Typical flow:

```text
Agent identifies useful memory
 -> MemoryWriteRequest
 -> Policy / tenant / purpose / classification / retention check
 -> allow | transform/minimize | deny | request consent/approval
 -> audit result
```

## Mandatory controls

Every memory read/write is evaluated against:

- tenant;
- actor permissions;
- request purpose;
- memory class;
- data classification;
- retention profile;
- source/document ACL when relevant;
- release/environment;
- consent/legal basis when required;
- applicable ExceptionPolicy.

## Rules

- No cross-tenant memory by default.
- Client data is not promoted into `platform_knowledge` unless an explicit approved anonymization/aggregation process exists.
- Retrieved content is data, not instruction.
- Secrets are stored only in the approved secrets system, not normal memory.
- Personal/PII persistence requires appropriate policy/consent/legal basis and minimization.
- Memory can be disabled or made read-only per Agent/client/trust profile.
- Retention/deletion behavior is versioned and auditable.
- Agent repositories never receive direct storage credentials.
- Memory operations go through the Memory Gateway contract.

## Read semantics

Retrieval returns the minimum context required for the request and preserves source/tenant/classification metadata. The Agent should be able to distinguish session context, client knowledge and platform guidance.

## Write semantics

A write request includes at least the memory class, purpose, data classification, content/reference, retention profile and source reference. Tenant, actor, request and release identity are taken from trusted `ExecutionContext` and MUST NOT be granted by Agent-supplied memory payload.

The gateway may reject, redact, summarize or transform a write according to policy.

## First executable slice - C4.4

The first implementation intentionally supports only ephemeral `session` and `task_working` memory:

- `session` scope is the trusted `ExecutionContext.requestId`;
- `task_working` scope is the trusted `ExecutionContext.traceId`;
- storage namespace includes tenant ID, agent release ID, memory class, scope ID and key;
- `memory.read` / `memory.write` permissions are required independently;
- effective data classification must match the trusted runtime classification;
- `memoryConfig` must explicitly allow class, purpose and retention profile and must enable the requested read/write direction;
- `minimumTrustProfile` in trusted `memoryConfig` is enforced by Runtime Governance;
- malformed or incomplete memory configuration is default-deny;
- reads/writes create minimized `RuntimeAuditEvent` evidence without storing memory content in audit;
- the reference backend is in-process and ephemeral only.

This slice does **not** implement `user_persistent`, `client_knowledge`, vector retrieval, production storage, PII persistence, secrets storage or storage credentials.

## Deletion and lifecycle

Deletion policy covers primary storage, indexes/caches and derived artifacts according to the configured retention/deletion contract. Decommissioning an Agent instance does not automatically delete shared platform knowledge, but must close or delete tenant-scoped memory according to policy.

For the first in-process session/task slice, lifecycle is process-ephemeral; durable retention/deletion semantics remain a later persistent-memory implementation task.

## Portability

The Core contract is storage-neutral. Implementations may use relational databases, object stores, vector stores or specialized memory systems while preserving isolation, authorization, retention, deletion and retrieval semantics.

## First implementation boundary

- Gateway: `agent_factory_core/memory_gateway.py`
- Contract tests: `tests/contracts/test_memory_gateway.py`
- Trusted authority: `ExecutionContext.memoryConfig` + Runtime Governance evaluator
