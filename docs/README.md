# Agent Factory Core - Architecture Documentation

This folder is the architectural entry point for `Agent Factory Core`.

## Canonical reading order

1. [`platform-vision.md`](platform-vision.md) - product/platform north star.
2. [`architecture.md`](architecture.md) - accepted Core architecture and artifact model.
3. [`agent-manifest.md`](agent-manifest.md) - AgentManifest, ClientInstanceConfig and EffectiveReleaseConfig contracts.
4. [`agent-lifecycle.md`](agent-lifecycle.md) - lifecycle and policy-driven release strategy.
5. [`security-model.md`](security-model.md) - mandatory risk/trust security baseline and exception model.
6. [`governance.md`](governance.md) - policy hierarchy, approvals, exceptions and change governance.
7. [`orchestration.md`](orchestration.md) - hybrid bounded-autonomy execution contract.
8. [`capability-registry.md`](capability-registry.md) - soft-strict capability routing without direct coupling.
9. [`provider-and-cost-policy.md`](provider-and-cost-policy.md) - provider-neutral, policy-driven routing and budget controls.
10. [`tool-gateway.md`](tool-gateway.md) - governed Tool/API/MCP execution.
11. [`memory-contract.md`](memory-contract.md) - governed autonomous memory and storage-neutral rules.
12. [`template-engine.md`](template-engine.md) - hybrid template + modular composition.
13. [`client-experience.md`](client-experience.md) - non-technical, assumption-aware client intake.
14. [`evidence-and-evals.md`](evidence-and-evals.md) - policy-driven eval/release decisions, evidence and audit.
15. [`architecture-review-2026-09-06.md`](architecture-review-2026-09-06.md) - completed synchronization review, resolved inconsistencies and readiness assessment.
16. [`roadmap.md`](roadmap.md) - optimized implementation sequence and current next step.
17. [`decision-log.md`](decision-log.md) - concise accepted/open decision index.

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

Historical ADRs remain evidence of previous prototype decisions and do not override newer accepted contracts.

## Source of truth

- Versioned approved/specification history is the primary design truth.
- JSON Schema is the canonical external machine-readable schema boundary for Core contracts.
- Pydantic is an internal Python runtime/validation representation and must remain aligned with the canonical schema.
- `openspec/specs/` - accepted behavior when folded/archived into canonical specs.
- `openspec/changes/` - active/proposed implementation contract changes.
- `docs/` - architecture, policies and decision rationale.
- `templates/` - reusable machine-readable starting contracts.
- Agent-specific business logic - separate Agent repositories.

## Current architecture shorthand

```text
Spec
 + AgentManifest
 + ClientInstanceConfig
 + PlatformPolicy / ExceptionPolicy
 -> EffectiveReleaseConfig
 -> bounded Runtime Governance
 -> Evals / Release Decision / Audit
```

No material feature without a spec. No runtime authority without compiled policy. Automatic release is allowed only where effective policy permits it and all blocking gates pass.