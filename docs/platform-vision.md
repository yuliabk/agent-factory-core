# Agent Factory Core - Platform Vision

**Status:** Accepted  
**Date:** 2026-09-06

## Vision

Agent Factory Core is a reusable platform for turning a short business request into a governed, testable, maintainable AI agent without requiring the client to understand models, APIs, MCP, runtimes or infrastructure.

The client experience should feel like a black box from a technical perspective, while remaining transparent about business consequences:

`Business need -> short clarification -> visible assumptions/budget/approvals -> agent ready for acceptance`

The internal platform should remain modular and repairable:

`Intent -> Spec -> Template -> Manifest -> Policies -> Build -> Evals -> Approval -> Release -> Monitor`

## Product principles

1. **Simple for the client.** Initial intake targets completion in under 10 minutes and will typically require no more than 5-6 critical follow-up questions. This is a UX target, not a hard limit: the platform may ask additional questions when required for safety, correctness, legal/privacy constraints or material business ambiguity.
2. **Simple to maintain.** Each responsibility has one clear owner/module; a provider, model or tool change should not require rewriting business agents.
3. **Provider neutral.** Models, search, runtimes and integrations are adapters selected by policy, not hard-coded platform dependencies.
4. **Security by default.** Security, tenant isolation, budget, permissions, audit and runtime limits are inherited platform controls.
5. **Template first.** Agents are composed from versioned templates and manifests rather than built from zero.
6. **Spec driven.** Material behavior starts as an approved contract before implementation.
7. **Evidence before release.** Evals, approvals and release evidence are required for consequential production changes.
8. **Capability based.** Agents consume capabilities rather than specific peer repositories or URLs.
9. **Human control where it matters.** Financial, permission-expanding, irreversible or externally consequential actions require explicit approval according to policy.
10. **One Core, many Agent repos.** The Core contains platform contracts and shared controls; business agents remain independently versioned repositories.
11. **Progressive complexity.** Start with the simplest viable agent that satisfies the approved business outcome. Add integrations, persistent memory, autonomy, premium models or additional capabilities only when they provide justified value.
12. **Transparent black box.** The client is not asked to choose technical implementation details, but must be able to understand the agent's business scope, important assumptions, connected external services, expected operating-cost profile and actions requiring approval.
13. **Infer, then confirm.** When a client's request is underspecified but a safe likely configuration can be inferred, the Factory should propose that configuration with explicit assumptions and ask the client to confirm or correct it instead of extending intake unnecessarily. Material uncertainty must still be clarified before build or protected actions.

## Client-intake decision rule

For vague requests such as "I want an agent that sells for me":

1. Infer the most likely business capability profile from available context.
2. Ask only the minimum critical questions needed to avoid a materially wrong or unsafe design.
3. Present the inferred scope and assumptions in plain language.
4. Present the relevant budget/cost profile and approval boundaries.
5. Ask the client to confirm or correct the proposed interpretation.
6. Convert the confirmed interpretation into the formal specification and Manifest.

The client should not need to decide whether the implementation uses a particular model, API, MCP server, search provider, orchestration runtime or storage engine unless a business, privacy, compliance or contractual constraint makes that choice material.

## What success looks like

- A new client can describe a business outcome in plain language and receive a draft solution profile without choosing technology.
- A new agent reuses security, cost, memory, tools, orchestration and evaluation contracts from Core.
- A model/provider can be replaced through policy and adapter configuration plus regression evaluation.
- An agent can delegate research or another capability without direct coupling.
- The Owner can answer "where do I change this?" with one clear location for most changes.
- A production release can be reconstructed from its spec, manifest, policies, evaluations, approvals and commit references.
- A vague client request can be converted into a proposed agent configuration through inference plus confirmation without forcing a long technical questionnaire.

## Non-goals for the first Core MVP

- Kubernetes, service mesh or multi-region control plane.
- A complex distributed agent bus.
- A universal autonomous agent that can access arbitrary tools.
- Client-facing technical configuration screens.
- Production handling of sensitive data before dedicated privacy/security approval.
- Maximizing autonomy before a simpler governed workflow has proven insufficient.
