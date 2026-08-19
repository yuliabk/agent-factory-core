---
name: build-openspec-agent
description: Turn an agent idea or client request into an approval-ready OpenSpec proposal, design, capability spec delta, and task plan. Use for new knowledge agents, customer-service agents, action agents, client-specific clones, integrations, channel additions, or material changes to agent behavior. Do not implement code before Owner approval.
---

# Build OpenSpec Agent

## Objective

Convert a business request into a testable, secure, cost-aware OpenSpec change that another Codex session can implement without relying on conversation history.

## Workflow

1. Read `AGENTS.md`, `openspec/project.md`, the current specifications, and active changes.
2. Collect missing information with `templates/client-intake.md`. Ask only questions that materially change scope, data handling, architecture, cost, or acceptance.
3. Classify the requested capabilities as knowledge, service, action, or a combination.
4. Assign a kebab-case change ID and create `openspec/changes/<change-id>/`.
5. Draft `proposal.md` with why, scope, exclusions, impact, success criteria, and approval meaning.
6. Draft `design.md` with boundaries, components, data flow, permissions, failures, observability, rollout, rollback, alternatives, and open decisions.
7. Draft capability deltas under `specs/<capability>/spec.md` using stable requirement IDs and normative `SHALL` language.
8. Add `GIVEN / WHEN / THEN` scenarios for success, insufficient evidence, failure, authorization, tenant isolation, privacy, cost, and escalation as applicable.
9. Draft `tasks.md` in dependency order. Map every task to requirement IDs and place approval gates before implementation or Production work.
10. Compare the change against `docs/security-model.md`, `docs/tooling-and-costs.md`, and `docs/skill-registry.md`.
11. Report contradictions, unresolved decisions, risks, and the smallest safe next step to the Owner in Hebrew.
12. Stop for explicit Owner approval. Do not create implementation files.

## Design Rules

- Separate reusable factory assets from client data planes.
- Create new credentials, storage, logs, retrieval indexes, and evaluations for every client.
- Use only synthetic or approved non-sensitive data in an MVP.
- Route side-effecting actions through named, allow-listed workflows.
- Require human approval for irreversible, regulated, financial, permission-changing, or externally binding actions.
- Prefer reversible and idempotent operations.
- Define an insufficient-evidence response for every knowledge capability.
- Defer WhatsApp to a dedicated change unless it is already explicitly approved.
- Keep the design operable by one Owner within the documented time and cost limits.

## Skill Import Rules

- Treat external skills as candidates until the registry contains source, pinned revision, license, scan result, access profile, and Owner approval.
- Never execute or copy a candidate skill merely because it appears in a catalog or fork.
- Adapt one approved workflow at a time instead of importing a complete collection.

## Required Output

Produce a coherent change folder containing:

- `proposal.md`
- `design.md`
- `tasks.md`
- at least one `specs/<capability>/spec.md`

End with a short Owner decision list and an explicit implementation stop.

