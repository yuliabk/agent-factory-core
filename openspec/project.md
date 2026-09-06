# Project Context

## Vision

`Agent Factory Core` enables a small platform team/Owner to specify, compose, evaluate and maintain many client agents through Spec-Driven Development and OpenSpec while keeping the client experience short and non-technical.

The platform is designed for modular maintenance: models, providers, runtimes, tools and agent implementations can change without rewriting unrelated business logic.

## Platform principles

- Core is a provider-neutral control plane, not a business agent.
- Business agents live in separate repositories.
- Agents communicate through versioned capabilities resolved by Core, not direct coupling by repository/URL.
- Security, tenant isolation, permissions, budget, audit and runtime limits are inherited mandatory controls.
- New agents are composed from templates + manifest + approved spec rather than built from zero.
- Client intake asks for business intent, constraints and budget rather than technology choices.
- Material behavior is specified before implementation and evaluated before release.

## Constraints

- Owner maintenance burden must stay low: changes should be localized and configuration-driven where practical.
- Prefer simple components and bounded interfaces over infrastructure complexity.
- Initial client intake target: usually under 10 minutes with no more than 5-6 critical follow-up questions after free-form description.
- Budget is first-class for both build-time planning and runtime operations.
- Future channels may include Website, Email, WhatsApp, CRM and internal automation.
- Future data may include public, internal, confidential, personal and sensitive classes; sensitive paths require dedicated approval.
- MVP/prototype work uses synthetic or non-sensitive data unless a separate privacy/security gate is approved.

## Roles

- Owner / Platform Owner: product decisions, architecture approval, permissions/budget approval, QA and release authorization.
- Builder/Coding Agent: analysis, specs, implementation of approved tasks and evidence collection.
- Client Process Owner: business-process scope, client permissions, acceptance and runtime business approvals.
- Security/Privacy Owner: approval for elevated data classes and higher-risk production paths.

## Source of Truth

- `openspec/specs/`: accepted behavior.
- `openspec/changes/`: proposed bounded changes.
- `docs/`: architecture, policies, ADRs and decision history.
- `templates/`: reusable contracts and intake/spec/eval templates.
- Agent repositories: agent-specific behavior and domain assets.
