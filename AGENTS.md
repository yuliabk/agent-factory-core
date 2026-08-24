# Repository Instructions

## Mission

Build a reusable, low-code Agent Factory through Spec-Driven Development and OpenSpec. Keep the factory reusable across clients while isolating every client's data, credentials, runtime, and audit trail.

## Current Phase

- Work on architecture and specifications only.
- Do not implement application code, infrastructure, integrations, or production configuration until the Owner explicitly approves implementation.
- Treat `openspec/specs/` as current truth and `openspec/changes/` as proposed deltas.

## Required Workflow

1. Read this file, `openspec/project.md`, and the active change folder.
2. Resolve ambiguity in specifications before proposing implementation.
3. Update `proposal.md`, capability specs, `design.md`, and `tasks.md` in that order.
4. Present material decisions and tradeoffs to the Owner in Hebrew.
5. Stop for explicit Owner approval before starting implementation tasks.
6. Implement one approved task group at a time on a dedicated branch.
7. Run the stated validation and review the diff before declaring work complete.

## Non-Negotiable Constraints

- Never commit secrets, tokens, credentials, private keys, real customer exports, or production data.
- Use synthetic or non-sensitive data in the MVP.
- Never mix data, credentials, storage, logs, or retrieval indexes between clients.
- Require human approval before irreversible, financial, medical, legal, account-changing, or external-message actions.
- Log consequential agent actions with tenant, actor, request, decision, tool, result, and timestamp while minimizing personal data.
- Keep imported third-party skills unchanged until their source, pinned revision, license, scan result, and approval status are recorded.
- Do not execute an unapproved external skill or script.
- Prefer reversible and idempotent automations.

## Architecture Boundaries

- GitHub and OpenSpec are the control-plane source of truth.
- Dify is the proposed low-code agent, workflow, and knowledge runtime.
- n8n is the proposed integration and action orchestrator.
- OpenAI API is the proposed model provider behind an abstraction layer.
- Each client receives a logically isolated deployment configuration and data plane.
- WhatsApp is a later channel and must not block the website-chat and internal-automation MVP.

## Definition of Done

A specification change is complete only when requirements are testable, acceptance scenarios cover failure and authorization, security and cost impacts are documented, tasks map to requirements, and the Owner approves it.

An implementation change is complete only when its approved checks pass and no secrets or client data appear in the diff.

## Language

- Write Owner-facing summaries and business documentation in Hebrew.
- Keep code identifiers, configuration keys, requirement IDs, and product names in English.

