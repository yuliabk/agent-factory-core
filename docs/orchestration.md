# Orchestration Contract

**Status:** Proposed  
**Principle:** The Orchestrator coordinates execution; it does not contain business logic.

## Responsibilities

The Core Orchestrator SHALL:

- create and propagate a trusted `ExecutionContext`;
- resolve required capabilities through the Capability Registry;
- route model requests through Model Policy;
- route tool calls through Tool Gateway;
- route memory operations through Memory Broker;
- enforce budget, deadline, retry, parallelism and hop limits;
- pause for human approval when policy requires it;
- produce trace, cost and audit events;
- fail closed for unverified consequential actions.

## Execution model

```text
Request
 -> Context validation
 -> Policy precheck
 -> Plan / capability resolution
 -> Model / capability / tool execution
 -> Policy check before each side effect
 -> Result validation
 -> Eval hooks
 -> Audit + response
```

Business agents may decide *what capability is needed* within their approved contract. They may not decide whether a denied permission becomes allowed.

## Agent-to-Agent delegation

A delegation request contains at least:

```text
request_id
trace_id
parent_span_id
caller_agent_id
required_capability
capability_version_range
tenant_id
actor_id
data_classification
delegated_permissions
budget_slice
deadline
hop_count
input
```

Rules:

- No automatic permission inheritance beyond the caller's allowed scope.
- The delegated permission set is the intersection of caller authority, provider capability requirements and platform policy.
- Each hop consumes the same trace and budget chain.
- `maxAgentHopsPerRequest` is mandatory.
- Cycles are detected and stopped.

## Deterministic vs model decisions

The model may recommend:

- which approved capability to use;
- how to decompose a task;
- which evidence is relevant;
- which clarification is useful.

Deterministic policy controls decide:

- permissions;
- tenant boundaries;
- budget limits;
- approval validity;
- allowed tools/providers;
- side-effect execution;
- release eligibility.

## Failure behavior

- Provider unavailable -> policy-defined fallback or graceful failure.
- Tool schema invalid -> reject before execution.
- Permission unavailable -> deny and audit.
- Budget preflight exceeds approved range -> pause and request approval/alternative.
- Deadline reached -> stop new work and return bounded partial result when allowed.
- Capability unavailable -> fallback implementation if contract-compatible; otherwise return typed failure.
- Loop/cycle detected -> emergency stop and audit.

## Idempotency

Consequential operations SHALL use an idempotency key when supported. Retries MUST NOT duplicate a completed side effect.
