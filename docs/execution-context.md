# ExecutionContext Contract

**Status:** Core Skeleton v1 implementation contract

## Purpose

Runtime receives trusted authority from `EffectiveReleaseConfig`, not from prompts, raw manifests or client drafts.

The first `ExecutionContext` is an immutable per-request projection containing:

- request and trace identifiers;
- actor identity/type;
- tenant and environment;
- Agent identity and exact `agentReleaseId`;
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

## Source boundary

- External JSON Schema: `schemas/execution-context.schema.json`
- Python model/builder: `agent_factory_core/contracts/execution_context.py`

This is the first thin Runtime Governance contract. Hop limits, runtime budget accounting and richer policy decisions are layered on top in later kernel tasks.
