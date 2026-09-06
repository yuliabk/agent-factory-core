# Capability Registry and Agent-to-Agent Routing

**Status:** Accepted direction after Owner Review; first external capability contract implemented

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

## 3. Registry is the source of truth

Capability Registry owns capability contract metadata. Agent manifests reference it; they do not duplicate it.

Registry-owned information includes, as applicable:

- canonical capability name and contract version;
- input/output schema references;
- provider implementation registrations;
- risk/side-effect class;
- permission requirements;
- cost/latency/quality metadata;
- supported environments/data classes;
- overrideable keys and their constraints;
- health/availability metadata used by resolution.

The canonical external record shape is `schemas/capability-registry-record.schema.json`. The Python `CapabilityRecord` is the internal projection. Resolved capabilities retain the authoritative schema/risk/cost/data-class metadata rather than reducing resolution to an implementation ID alone.

### Manifest reference shape

A provided capability is represented as a lightweight reference:

```yaml
ref: research.lookup
version: "1"
overrides: {}
```

A required capability may additionally be optional:

```yaml
ref: research.lookup
version: "1"
optional: true
overrides:
  qualityProfile: balanced
```

`overrides` is intentionally bounded. Only keys marked overrideable by the resolved Registry record are legal. Unknown or protected keys are rejected during compilation.

The manifest must not copy provider identity, risk class, schemas, cost class or other Registry-owned metadata into the reference.

## 4. Registry enforcement modes

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

## 5. Registry record

The first real external contract is checked in as `registry/capabilities/research.lookup.v1.json`:

```yaml
ref: research.lookup
version: "1"
inputSchemaRef: schemas/capabilities/research.lookup.input.v1.json
outputSchemaRef: schemas/capabilities/research.lookup.output.v1.json
riskClass: read_only
costClass: variable
allowedDataClassifications:
  - public
  - internal
environments:
  - sandbox
  - production
requiredPermissions:
  - research.lookup
overrideable:
  qualityProfile: [economy, balanced, high]
implementations: []
```

`implementations` is intentionally empty at C7.1. C7.2 registers the first compatible Research/Brain Agent release without changing the consumer contract.

### Permission boundary

A consumer that requires `research.lookup` receives only the consumer authority `research.lookup`.

Provider-internal authorities such as `web.search`, API access, model invocation, MCP access or internal-knowledge retrieval belong to the Research/Brain Agent's own compiled release. They MUST NOT be copied into Travel/Sales Agent manifests merely because the provider may use them internally.

This isolates consumer authority from provider implementation details.

## 6. `research.lookup` v1 public payload

Input is intentionally small and provider-neutral:

```json
{
  "query": "What changed in the rail schedule?",
  "purpose": "travel planning",
  "freshness": "current",
  "maxEvidenceItems": 6
}
```

`purpose` is semantic task intent only; it never grants runtime authority. The input schema rejects caller-selected provider, model, tool, web-search or credential fields.

Output is structured around answer + evidence-linked findings:

```json
{
  "status": "complete",
  "answer": "A schedule change was published.",
  "findings": [
    {
      "statement": "The published schedule changed.",
      "evidenceIds": ["e1"]
    }
  ],
  "evidence": [
    {
      "id": "e1",
      "sourceType": "web",
      "sourceRef": "https://example.test/schedule",
      "title": "Schedule update",
      "summary": "Official page reports the change.",
      "retrievedAt": "2026-09-06T13:00:00Z"
    }
  ],
  "limitations": []
}
```

Evidence is minimized provenance. Raw prompts, credentials and provider payloads are not part of the capability contract.

## 7. Resolution policy

The Core selects an implementation according to:

1. capability reference and contract compatibility;
2. validated manifest overrides;
3. environment and enforcement mode;
4. tenant permission and trust level;
5. data classification/privacy restrictions;
6. ClientInstanceConfig restrictions;
7. cost profile;
8. quality/eval profile;
9. provider health/availability;
10. latency target.

## 8. Hybrid orchestration

The Core Orchestrator owns boundaries, permissions, limits, routing and policy enforcement. A business Agent may autonomously decide which approved capability to request and how to decompose its task inside those boundaries.

Thus autonomy lives **inside** policy rather than being hard-coded either entirely in the central orchestrator or entirely in each Agent.

## 9. Agent hops and delegation

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

## 10. Failure and fallback

If a capability is unavailable:

- use a contract-compatible approved fallback when policy allows;
- otherwise return a typed degraded/partial result or escalate;
- never bypass the Registry by directly calling an unapproved peer implementation in production.

## 11. Contract versions

- backward-compatible changes may remain in the same major contract version;
- breaking changes require major version and compatibility/migration handling;
- consumers declare supported version/range through the manifest reference;
- provider replacement should not require consumer business-code changes when the capability contract remains compatible.

## 12. First reference capability status

`research.lookup@1` is now the first authoritative external capability contract.

Consumers are expected to include only a lightweight `research.lookup` reference and the corresponding consumer permission. The next implementation step is C7.2: create the Research/Brain Agent in a separate repository and register its first compatible implementation/release against this contract.
