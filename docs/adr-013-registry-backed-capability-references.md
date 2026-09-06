# ADR-013: Registry-backed Capability References

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

Capability metadata could be duplicated inside every AgentManifest or centralized in Capability Registry. Duplicating provider, schema, risk, cost and routing metadata in every consumer would create drift and make capability replacement harder.

At the same time, an Agent needs a small amount of local declaration so its reusable definition can state what it provides/requires and, where explicitly supported, tune a bounded capability option.

## Decision

Capability Registry is the authoritative source of truth for capability contracts and metadata.

AgentManifest contains only lightweight capability references:

```yaml
ref: research.lookup
version: "1"
overrides: {}
```

Required capability references may also declare:

```yaml
optional: true
```

`overrides` is allowed only for keys explicitly marked overrideable by the resolved Registry record. The compiler rejects unknown, protected or out-of-range override values.

AgentManifest does not duplicate Registry-owned provider identity, schemas, risk class, cost class, permission metadata, health state or implementation details.

## Consequences

### Positive

- one source of truth for capability contracts;
- replacing an implementation does not require editing every consumer manifest;
- smaller reusable AgentManifest;
- less configuration drift;
- bounded local tuning remains possible;
- capability resolution stays policy/provider neutral.

### Tradeoffs

- compilation requires access to the relevant Registry contract/metadata;
- dynamic override validation cannot be expressed by AgentManifest JSON Schema alone and must also be enforced by the compiler/Registry resolver;
- Registry contract versioning becomes important infrastructure.

## Guardrails

- A manifest capability reference never grants runtime permission.
- `overrides` cannot weaken PlatformPolicy, security invariants or client restrictions.
- Unknown capability refs may degrade only under the accepted soft-strict development policy; critical production refs must resolve.
- New metadata belongs in the Registry unless it is demonstrably Agent-definition-specific.
