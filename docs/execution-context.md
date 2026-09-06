# ExecutionContext Contract

**Status:** Core Skeleton v1 implementation contract

## Purpose

Runtime receives trusted authority from `EffectiveReleaseConfig`, not from prompts, raw manifests or client drafts.

The first `ExecutionContext` is an immutable per-request projection containing:

- request and trace identifiers;
- actor identity/type;
- tenant and environment;
- Agent identity and exact `agentReleaseId`;
- compiled `trustProfile`;
- effective permissions;
- data classification;
- resolved capability bindings;
- provider profile;
- tool bindings;
- memory configuration;
- budget configuration;
- deadline.

## Construction rule

`ExecutionContext` is created from an already compiled `EffectiveReleaseConfig` plus request-scoped identity/trace/deadline values.

An Agent or model output cannot expand these fields. Changes to authority require a new compiled release or a separately governed runtime policy decision.

## Trust rule

`trustProfile` is copied from the compiled release. Runtime policy may require a minimum trust profile for an operation, but it cannot elevate the request above the compiled profile.

Trust order for Core Skeleton v1 is:

```text
sandbox < internal < business < privileged
```

Trust does not replace permission checks; both boundaries apply independently.

## Source boundary

- External JSON Schema: `schemas/execution-context.schema.json`
- Python model/builder: `agent_factory_core/contracts/execution_context.py`
- Shared trust order: `agent_factory_core/contracts/trust.py`

This is the first thin Runtime Governance contract. Hop limits, runtime budget accounting and policy decisions are layered on top by the Runtime Governance kernel.
