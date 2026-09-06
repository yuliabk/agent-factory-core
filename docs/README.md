# Agent Factory Core - Architecture Documentation

This folder is the architectural entry point for `Agent Factory Core`.

## Recommended reading order

1. [`platform-vision.md`](platform-vision.md) - product/platform north star and non-goals.
2. [`architecture.md`](architecture.md) - Core boundaries and shared platform modules.
3. [`agent-manifest.md`](agent-manifest.md) - declarative contract every agent must provide.
4. [`agent-lifecycle.md`](agent-lifecycle.md) - lifecycle from client intent to release and decommission.
5. [`security-model.md`](security-model.md) - mandatory security baseline inherited by every agent.
6. [`governance.md`](governance.md) - policy hierarchy, approvals and change governance.
7. [`orchestration.md`](orchestration.md) - execution and delegation contract.
8. [`capability-registry.md`](capability-registry.md) - agent-to-agent routing without direct coupling.
9. [`provider-and-cost-policy.md`](provider-and-cost-policy.md) - model/provider portability, budget and cost controls.
10. [`tool-gateway.md`](tool-gateway.md) - governed tool/API/MCP execution.
11. [`memory-contract.md`](memory-contract.md) - storage-neutral memory and retrieval rules.
12. [`template-engine.md`](template-engine.md) - template-first agent composition.
13. [`client-experience.md`](client-experience.md) - non-technical client intake and black-box UX.
14. [`evidence-and-evals.md`](evidence-and-evals.md) - evidence packs, evals, approvals and audit bundles.
15. [`roadmap.md`](roadmap.md) - implementation sequence and current stop point.
16. [`decision-log.md`](decision-log.md) - concise history of decisions and open items.

## ADRs

- ADR-001 through ADR-004 - historical baseline/prototype decisions.
- ADR-005 - Core as platform control plane.
- ADR-006 - capability-based agent routing.
- ADR-007 - provider-neutral model routing.
- ADR-008 - budget warning, approval and safety cap.

Historical ADRs remain useful evidence of earlier prototype decisions. They do not override a newer accepted ADR or current OpenSpec contract.

## Source of truth

- `openspec/specs/` - currently accepted behavior.
- `openspec/changes/` - proposed changes not yet folded into accepted specs.
- `docs/` - architecture, policy, design rationale and decision history.
- `templates/` - reusable contracts/templates.
- Agent-specific business logic - lives in the agent repository, not in Core.

No material feature without a spec. No runtime permission without policy. No production release without evaluation, evidence and the required approval.
