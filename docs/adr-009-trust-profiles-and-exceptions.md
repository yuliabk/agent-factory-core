# ADR-009: Risk-based Trust Profiles and Controlled Exceptions

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

Security controls must protect every Agent, but requiring manual approval for every low-risk configuration/action would make the platform slow and difficult to scale.

At the same time, real systems need documented exceptions without forcing a redesign of the global architecture.

## Decision

Platform security uses risk-based Trust Profiles and a controlled ExceptionPolicy mechanism.

Initial trust-profile direction:

- `sandbox`;
- `internal`;
- `business`;
- `privileged`.

Factory recommends a trust level from the specification. PlatformPolicy defines the maximum permitted level. Client configuration may remain within or below that ceiling.

Rules are classified as:

1. non-overridable Platform Invariants;
2. overridable policy rules.

An overridable rule may be changed only by a scoped, versioned, auditable ExceptionPolicy with reason, approver, compensating controls and expiration/review date.

The exact final list of non-overridable production invariants will be finalized before Production hardening.

## Consequences

### Positive

- fewer unnecessary manual approvals;
- easier client-specific configuration;
- consistent security vocabulary;
- exceptions remain visible and reversible;
- platform can scale without turning every configuration into bespoke permissions work.

### Costs

- policy engine must resolve trust levels and exception overlays;
- expired/out-of-scope exceptions require deterministic handling;
- production needs a clearly maintained invariant catalog.

## Guardrail

No Prompt, Agent, ClientInstanceConfig or ExceptionPolicy can create authority beyond a non-overridable invariant.