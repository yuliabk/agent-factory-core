# Agent Factory Core - Platform Vision

**Status:** Proposed  
**Date:** 2026-09-06

## Vision

Agent Factory Core is a reusable platform for turning a short business request into a governed, testable, maintainable AI agent without requiring the client to understand models, APIs, MCP, runtimes or infrastructure.

The client experience should feel like a black box:

`Business need -> short clarification -> transparent assumptions/budget -> agent ready for acceptance`

The internal platform should remain modular and repairable:

`Intent -> Spec -> Template -> Manifest -> Policies -> Build -> Evals -> Approval -> Release -> Monitor`

## Product principles

1. **Simple for the client.** Most initial intake should complete in under 10 minutes and normally require no more than 5-6 critical follow-up questions.
2. **Simple to maintain.** Each responsibility has one clear owner/module; a provider, model or tool change should not require rewriting business agents.
3. **Provider neutral.** Models, search, runtimes and integrations are adapters selected by policy, not hard-coded platform dependencies.
4. **Security by default.** Security, tenant isolation, budget, permissions, audit and runtime limits are inherited platform controls.
5. **Template first.** Agents are composed from versioned templates and manifests rather than built from zero.
6. **Spec driven.** Material behavior starts as an approved contract before implementation.
7. **Evidence before release.** Evals, approvals and release evidence are required for consequential production changes.
8. **Capability based.** Agents consume capabilities rather than specific peer repositories or URLs.
9. **Human control where it matters.** Financial, permission-expanding, irreversible or externally consequential actions require explicit approval according to policy.
10. **One Core, many Agent repos.** The Core contains platform contracts and shared controls; business agents remain independently versioned repositories.

## What success looks like

- A new client can describe a business outcome in plain language and receive a draft solution profile without choosing technology.
- A new agent reuses security, cost, memory, tools, orchestration and evaluation contracts from Core.
- A model/provider can be replaced through policy and adapter configuration plus regression evaluation.
- An agent can delegate research or another capability without direct coupling.
- The Owner can answer "where do I change this?" with one clear location for most changes.
- A production release can be reconstructed from its spec, manifest, policies, evaluations, approvals and commit references.

## Non-goals for the first Core MVP

- Kubernetes, service mesh or multi-region control plane.
- A complex distributed agent bus.
- A universal autonomous agent that can access arbitrary tools.
- Client-facing technical configuration screens.
- Production handling of sensitive data before dedicated privacy/security approval.
