# ADR-006: Capability-based Agent Routing

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

Future Agents need to use capabilities of other Agents. Direct calls by name/URL create coupling and make replacement, policy, cost control and audit harder.

A fully strict Registry in every environment would also slow experimentation and future scale-up.

## Decision

Agents declare versioned capabilities they `provide` and `require`. Agent-to-Agent invocation uses Core Orchestrator + Capability Registry rather than direct peer coupling by default.

The consumer does not know the concrete provider implementation.

Registry enforcement is **soft-strict**:

- development/sandbox may warn, degrade or use explicit mocks for optional/non-critical unresolved capabilities;
- production requires critical/consequential capabilities to resolve to registered, compatible and policy-approved implementations;
- security/tenant invariants remain blocking in all environments.

The business Agent may decide autonomously which approved capability to request; Core controls resolution, authority, budget, hops and audit.

## Consequences

### Positive

- Research Agent can be replaced without changing Travel Agent business code.
- Contract-compatible fallback implementations are possible.
- Delegation is observable and budgeted.
- Development is not blocked by unnecessary registry bureaucracy.

### Costs

- capability contracts need versioning;
- Registry resolution adds a platform dependency;
- production needs health/compatibility metadata;
- hop/cycle limits are required.

## Rejected default

Direct Agent-to-Agent URLs are not the production default. A bounded direct integration requires an explicit approved exception/design decision.