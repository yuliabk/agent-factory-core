# ADR-012: JSON Schema as external contract, Pydantic as internal runtime model

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

The first Core Skeleton needs machine-readable contracts that are portable across languages/tools while remaining convenient to validate and manipulate inside a Python implementation.

Using only Python/Pydantic would make the external contract too implementation-specific. Using only JSON Schema would make the runtime implementation more verbose and less ergonomic for typed Python code.

## Decision

Agent Factory Core will use a hybrid contract boundary:

1. **JSON Schema is the canonical external schema contract** for versioned machine-readable objects such as `AgentManifest`, `ClientInstanceConfig`, `PlatformPolicy`, `ExceptionPolicy` and `EffectiveReleaseConfig`.
2. **Pydantic models are the internal Python representation and validation/runtime layer** when the Core implementation is Python.
3. Pydantic models must remain semantically aligned with the canonical JSON Schema. They do not define a second independent contract.
4. External consumers may validate against JSON Schema without depending on Python or Pydantic.
5. If the implementation language changes later, the external JSON Schema contracts remain stable and the internal type system can be replaced.

## Direction of authority

```text
Approved Spec
    -> Canonical JSON Schema
    -> Pydantic runtime models / validators
    -> compiler and runtime logic
```

When generated schemas/types are used, drift between JSON Schema and Pydantic must be detected by tests/CI.

## Consequences

### Positive

- Provider/language/runtime neutrality is preserved.
- Python implementation remains strongly typed and ergonomic.
- JSON Schema can be used by CLI, UI, CI, external agent repos and non-Python tooling.
- Future migration away from Python does not require changing the public contract.
- Validation errors can still be normalized into the platform error format: path, rule, remediation hint.

### Negative

- Two representations must stay synchronized.
- Schema generation/round-trip tests are required to prevent drift.
- Pydantic-specific behavior must not leak into the public contract unless represented in JSON Schema.

## Guardrails

- Do not add Pydantic-only fields or coercions that change the meaning of the external contract without updating the canonical schema/spec.
- Prefer deterministic schema validation at the boundary before business/runtime logic.
- The first implementation should cover only the accepted minimal AgentManifest shape before expanding other contracts.
