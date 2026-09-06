# Capability Registry and Agent-to-Agent Routing

**Status:** Accepted direction after Owner Review

## 1. Purpose

Allow an Agent to use another Agent or implementation without knowing its repository, URL, provider or internal runtime.

## 2. Capability-first contract

Agents request capabilities such as:

```text
research.lookup
crm.customer.read
message.draft
travel.inventory.search
```

The Runtime Governance Plane resolves a compatible implementation.

Direct peer coupling is not the default architecture.

## 3. Registry enforcement modes

The Registry is intentionally **soft-strict** so development stays flexible while production stays reproducible.

### Development / sandbox

- Missing non-critical registrations MAY produce warnings instead of blocking the entire Agent.
- Local/mock implementations may be used when explicitly marked as development-only.
- Unknown optional capability can degrade gracefully.
- Security invariants, tenant isolation and prohibited side effects remain blocking even in development.

### Production / elevated environments

- Critical capabilities MUST resolve to a registered, version-compatible and policy-approved implementation.
- Consequential capabilities MUST have risk classification, schemas, effective permission and audit configuration.
- A required capability without valid resolution blocks the affected execution/release according to policy.

This prevents the Registry from becoming a development bottleneck without allowing production dependencies to become invisible.

## 4. Registry record

A production-capable registration contains at least:

```yaml
name: research.lookup
contractVersion: 1
providerAgent: research-agent
release: research-agent@1.3.2
risk: read-only
costClass: variable
environments:
  - sandbox
  - production
supports:
  - public-web
  - client-knowledge
```

## 5. Resolution policy

The Core selects an implementation according to:

1. contract compatibility;
2. environment and enforcement mode;
3. tenant permission and trust level;
4. data classification/privacy restrictions;
5. ClientInstanceConfig restrictions;
6. cost profile;
7. quality/eval profile;
8. provider health/availability;
9. latency target.

## 6. Hybrid orchestration

The Core Orchestrator owns boundaries, permissions, limits, routing and policy enforcement. A business Agent may autonomously decide which approved capability to request and how to decompose its task inside those boundaries.

Thus autonomy lives **inside** policy rather than being hard-coded either entirely in the central orchestrator or entirely in each Agent.

## 7. Agent hops and delegation

Every Agent hop:

- inherits `request_id` and `trace_id`;
- receives only task-required context;
- does not inherit all caller permissions automatically;
- is recorded as a child span;
- consumes request budget/deadline;
- increments hop count.

Effective delegated authority is bounded by:

`Caller authority ∩ Provider allowed scope ∩ Client policy ∩ PlatformPolicy ∩ Request purpose`

`maxAgentHopsPerRequest` and cycle detection prevent recursion/cost explosion.

## 8. Failure and fallback

If a capability is unavailable:

- use a contract-compatible approved fallback when policy allows;
- otherwise return a typed degraded/partial result or escalate;
- never bypass the Registry by directly calling an unapproved peer implementation in production.

## 9. Contract versions

- backward-compatible changes may remain in the same major contract version;
- breaking changes require major version and compatibility/migration handling;
- consumers declare supported version/range;
- provider replacement should not require consumer business-code changes when the capability contract remains compatible.

## 10. First reference capability

The planned Research/Brain Agent will provide:

```text
Capability: research.lookup
Consumers: Travel Agent, Sales Agent, future agents
```

It is the first portability test for reusable Agent-to-Agent capabilities.