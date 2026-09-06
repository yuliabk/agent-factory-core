# Memory Contract

**Status:** Accepted direction after Owner Review

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

A write request includes at least:

```text
request_id
agent_release_id
tenant_id
actor_id
memory_class
purpose
data_classification
content_or_reference
retention_profile
source_reference
```

The gateway may reject, redact, summarize or transform a write according to policy.

## Deletion and lifecycle

Deletion policy covers primary storage, indexes/caches and derived artifacts according to the configured retention/deletion contract. Decommissioning an Agent instance does not automatically delete shared platform knowledge, but must close or delete tenant-scoped memory according to policy.

## Portability

The Core contract is storage-neutral. Implementations may use relational databases, object stores, vector stores or specialized memory systems while preserving isolation, authorization, retention, deletion and retrieval semantics.