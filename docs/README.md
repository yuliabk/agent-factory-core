# Agent Factory Core - Architecture Documentation

This folder is the architectural entry point for `Agent Factory Core`.

## Canonical reading order

1. [`platform-vision.md`](platform-vision.md) - product/platform north star.
2. [`architecture.md`](architecture.md) - accepted Core architecture and artifact model.
3. [`agent-manifest.md`](agent-manifest.md) - reusable AgentManifest contract.
4. [`client-instance-config.md`](client-instance-config.md) - client/environment deployment configuration boundary.
5. [`platform-policy-contract.md`](platform-policy-contract.md) - typed PlatformPolicy and controlled ExceptionPolicy boundary.
6. [`effective-release-config.md`](effective-release-config.md) - compiler output and sole runtime-executable configuration artifact.
7. [`execution-context.md`](execution-context.md) - trusted per-request runtime authority projection.
8. [`runtime-governance-kernel.md`](runtime-governance-kernel.md) - request-time authority, limits, budget/safety and audit boundary.
9. [`agent-lifecycle.md`](agent-lifecycle.md) - lifecycle and policy-driven release strategy.
10. [`security-model.md`](security-model.md) - mandatory risk/trust security baseline and exception model.
11. [`governance.md`](governance.md) - policy hierarchy, approvals, exceptions and change governance.
12. [`orchestration.md`](orchestration.md) - hybrid bounded-autonomy execution contract.
13. [`capability-registry.md`](capability-registry.md) - authoritative capability contracts + soft-strict routing.
14. [`provider-and-cost-policy.md`](provider-and-cost-policy.md) - provider-neutral, policy-driven routing and budget controls.
15. [`tool-gateway.md`](tool-gateway.md) - governed Tool/API/MCP execution.
16. [`memory-contract.md`](memory-contract.md) - governed autonomous memory and storage-neutral rules.
17. [`template-engine.md`](template-engine.md) - hybrid template + modular composition.
18. [`client-experience.md`](client-experience.md) - non-technical, assumption-aware client intake.
19. [`evidence-and-evals.md`](evidence-and-evals.md) - policy-driven eval/release decisions, evidence and audit.
20. [`architecture-review-2026-09-06.md`](architecture-review-2026-09-06.md) - completed synchronization review, resolved inconsistencies and readiness assessment.
21. [`roadmap.md`](roadmap.md) - optimized implementation sequence and current next step.
22. [`decision-log.md`](decision-log.md) - concise accepted/open decision index.

## ADRs

- ADR-001 through ADR-004 - historical baseline/prototype decisions.
- ADR-005 - Core boundaries and two-plane architecture - **Accepted**.
- ADR-006 - capability-based Agent routing + soft-strict registry - **Accepted**.
- ADR-007 - provider-neutral, policy-driven model routing - **Accepted**.
- ADR-008 - business budget escalation + independent safety cap - **Accepted**.
- ADR-009 - risk-based Trust Profiles + controlled exceptions - **Accepted**.
- ADR-010 - policy-driven release strategy / auto-release when allowed - **Accepted**.
- ADR-011 - specification as primary platform artifact - **Accepted**.
- ADR-012 - JSON Schema as external contract, Pydantic as internal Python runtime model - **Accepted**.
- ADR-013 - Capability Registry as source of truth with lightweight manifest references - **Accepted**.

Historical ADRs remain evidence of previous prototype decisions and do not override newer accepted contracts.

## Source of truth

- Versioned approved/specification history is the primary design truth.
- JSON Schema is the canonical external machine-readable schema boundary for Core contracts.
- Pydantic is an internal Python runtime/validation representation and must remain aligned with the canonical schema.
- Capability Registry is authoritative for capability contract metadata; AgentManifest stores lightweight capability references only.
- `schemas/` - canonical external JSON Schemas for executable Core contracts.
- `agent_factory_core/contracts/` - internal Pydantic contract models for the Python Core runtime.
- `openspec/specs/` - accepted behavior when folded/archived into canonical specs.
- `openspec/changes/` - active/proposed implementation contract changes.
- `docs/` - architecture, policies and decision rationale.
- `templates/` - reusable machine-readable starting contracts.
- Agent-specific business logic - separate Agent repositories.

## Current architecture shorthand

```text
Spec
 + AgentManifest (lightweight capability refs)
 + Capability Registry (authoritative contracts/metadata)
 + ClientInstanceConfig
 + PlatformPolicy / ExceptionPolicy
 -> EffectiveReleaseConfig
 -> ExecutionContext
 -> bounded Runtime Governance
 -> Evals / Release Decision / Audit
```

No material feature without a spec. No runtime authority without compiled policy. Automatic release is allowed only where effective policy permits it and all blocking gates pass.
