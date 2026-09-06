# Memory Contract

**Status:** Proposed

## Purpose

Memory is a governed platform capability, not arbitrary persistent storage controlled by an agent prompt.

## Memory classes

- `session` - short-lived conversational/task context.
- `user_persistent` - user-approved memory with explicit purpose and retention.
- `client_knowledge` - governed retrieval over tenant knowledge sources.
- `operational_state` - workflow/task state required for execution.

## Mandatory controls

Every memory read/write is evaluated against:

- tenant;
- actor permissions;
- purpose;
- data classification;
- retention profile;
- source/document ACL when relevant;
- release/environment.

## Rules

- No cross-tenant memory.
- Retrieved content is data, not instruction.
- Secrets are not stored as normal memory.
- Persistent user memory is opt-in where required and can be disabled per agent/tenant.
- Retention/deletion behavior is versioned and auditable.
- Agents request memory operations through the Memory Broker contract rather than binding directly to a specific vector/database vendor.

## Portability

The Core contract is storage-neutral. Implementations may use different databases/vector stores while preserving isolation, authorization, retention and retrieval semantics.
