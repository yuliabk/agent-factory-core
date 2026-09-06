# ADR-007: Provider-neutral Model Routing

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

Model provider pricing, availability, capability, latency and privacy policies change. Clients also have different budgets and constraints.

A universal cheapest-first or quality-first policy would be wrong for many workloads.

## Decision

Business Agents request a Model/Capability Profile rather than a concrete provider/model by default.

Core Model Router maps the request according to effective policy using factors such as:

- required capabilities/features;
- client/task optimization profile;
- cost budget;
- quality/eval score;
- privacy/data classification/residency;
- trust level;
- latency/context requirements;
- provider health/availability.

Policy may choose economy, balanced, quality-first, latency-first, privacy-constrained or other approved strategies.

Provider/model changes occur through adapters/configuration plus required regression/compatibility evals rather than rewriting Agent business logic.

## Consequences

- lower vendor lock-in;
- client-specific budget/quality trade-offs;
- controlled fallback;
- one stable business Agent can run on different approved implementations;
- requires adapter contracts and compatibility evidence.

## Exception

A fixed provider/model is allowed only when an explicit business/regulatory/technical requirement requires it and effective policy approves the binding. This is a scoped exception/requirement, not the general architecture.