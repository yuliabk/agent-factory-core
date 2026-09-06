# ADR-011: Specification as the Primary Platform Artifact

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

The platform is intended to remain maintainable while models, providers, tools, runtimes and client requirements change. Treating generated Agent code or a deployed runtime as the primary truth would make reconstruction and migration harder.

## Decision

The versioned specification and its decision history are the primary platform artifacts.

Agent code, templates, manifests, client configuration, EffectiveReleaseConfig and deployments are derived/reproducible outputs of approved contracts.

Material behavior changes begin as specification changes before implementation, except bounded emergency security actions which are documented retrospectively according to governance policy.

## Consequences

### Positive

- Agents can be rebuilt or migrated to new runtimes/providers;
- architecture does not depend on chat history;
- changes are reviewable and auditable;
- multiple implementations can satisfy the same business contract;
- support can answer what was intended versus what was deployed.

### Costs

- specification discipline is required;
- implementation drift must be detected;
- schema/version migration becomes a real platform responsibility.

## Guardrail

A deployed Agent instance that cannot be mapped back to an approved specification, effective release configuration and release evidence is considered unmanaged drift.