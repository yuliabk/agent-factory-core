# Runtime Governance Kernel

**Status:** Core Skeleton v1 implementation contract

## Purpose

The Runtime Governance kernel applies trusted request-time boundaries on top of `ExecutionContext` before adapters, tools, memory or orchestration are allowed to act.

It does not contain Agent business logic and it does not treat prompts, retrieved content, tool output or model output as authority.

## Current thin kernel

### Request-time authority

`agent_factory_core/runtime/policy.py` evaluates only trusted `ExecutionContext` fields.

The first conservative rules are:

- the request deadline must still be valid;
- request tenant must exactly match `ExecutionContext.tenantId`;
- requested permission must already exist in `ExecutionContext.permissions`;
- when a data classification is supplied, it must exactly match the trusted context classification.

The classification rule intentionally uses exact matching until a classification hierarchy/lattice is explicitly approved. Runtime does not infer a broader authority relationship.

### Runtime limits

`agent_factory_core/runtime/limits.py` provides a small deterministic boundary for:

- maximum delegation hops;
- maximum repeats of the same capability inside a capability path.

Reaching either limit blocks the next delegation. The kernel does not attempt to plan or replan work itself.

### Budget and safety cap

`agent_factory_core/runtime/budget.py` keeps two independent boundaries:

- business budget - may produce `pause` for a separately governed overage decision;
- emergency safety cap - produces `stop` and is evaluated independently before business-budget handling.

Business overage approval cannot convert a safety-cap stop into an allow decision.

### Runtime audit event

Runtime evidence uses the canonical external JSON Schema:

- `schemas/runtime-audit-event.schema.json`

and the aligned Python model:

- `agent_factory_core/contracts/runtime_audit_event.py`

`agent_factory_core/runtime/audit.py` builds the event from trusted `ExecutionContext` plus explicit policy/operation/result/cost evidence.

The event records minimized reconstructable evidence including tenant, request/trace, actor, release, policy/exception/approval references, operation/target, decision, result, timestamp and optional cost.

Prompts, payload bodies, secrets and arbitrary retrieved content are intentionally not fields in this contract.

## Remaining C3 boundary

The current `ExecutionContext` does not yet carry an implemented `trustProfile`/risk-ceiling contract. Therefore full trust/risk request-time enforcement remains open under C3.1 and must not be invented implicitly inside the runtime evaluator.

C3.2-C3.5 can be implemented and tested independently from that remaining trust-profile decision.

## Next architectural boundary

The Hybrid Orchestrator remains later work. It may consume these governance decisions, but it must not bypass or redefine them.
