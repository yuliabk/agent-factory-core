# Agent Factory Core

A spec-driven platform Core for building, testing, releasing and governing reusable AI agents.

The repository now has an accepted architectural foundation and is preparing the first thin executable Core Skeleton. It does not contain a production customer runtime or real customer data.

## Platform goal

A non-technical client describes a business need in plain language, answers only critical questions, confirms material assumptions/budget and receives an Agent built from approved specifications, templates and policies.

Behind that experience, Core standardizes:

- Spec compilation and reproducible releases.
- Reusable `AgentManifest` separated from `ClientInstanceConfig`.
- Immutable `EffectiveReleaseConfig` as runtime authority.
- Risk/trust-based security and controlled exceptions.
- Hybrid orchestration and trusted `ExecutionContext`.
- Capability-based Agent-to-Agent routing.
- Provider-neutral, policy-driven model routing.
- Tool/API/MCP access through policy.
- Governed autonomous memory contracts.
- Budget and emergency safety guardrails.
- Policy-driven eval/release decisions, evidence and audit.
- Hybrid template-first modular composition.

## Core architecture

```text
Business Intent -> Versioned Spec

AgentManifest
 + ClientInstanceConfig
 + PlatformPolicy / ExceptionPolicy
 -> EffectiveReleaseConfig
 -> Runtime Governance
 -> Evidence / Evals / Release Decision / Audit
```

Core is logically divided into:

- **Build / Control Plane** - intent/spec, templates, manifests/configs, policy compilation, eval/release build artifacts.
- **Runtime Governance Plane** - orchestration, policy, routing, tools, memory, cost/runtime limits and audit.

These can initially live in one repository/project while preserving a contract boundary for future physical separation.

## Repository boundaries

`Agent Factory Core` is not a business Agent. Travel, Research, Sales, CRM and future Agents live in separate repositories and consume Core contracts.

Specific providers such as OpenAI, Dify, n8n, Gemini, DeepSeek or others are adapters/options rather than architectural dependencies unless an approved bounded requirement fixes one.

## Repository structure

```text
AGENTS.md                         repository governance for coding agents
docs/                             architecture, security, contracts, ADRs, roadmap
openspec/                         accepted specs and active change contracts
templates/                        reusable machine-readable starting contracts
.agents/skills/                   repo-scoped authoring/build skills
tools/                            bounded validation/portability tooling
tests/                            deterministic repository tests
```

Start with [`docs/README.md`](docs/README.md).

## Current state

- `main` is the canonical branch.
- Platform Vision and Core architecture have completed Owner review.
- Core Contracts v1 has been synchronized to the accepted decisions from 2026-09-06.
- Travel Agent Instance Contract v1 remains part of the architecture/spec history.
- Knowledge Agent synthetic smoke evidence remains historical reference material.
- Next executable milestone: the thin Core Skeleton vertical slice in `docs/roadmap.md`.
- First real reusable Agent after that gate: Research/Brain Agent exposing `research.lookup`.
- Travel Agent will be the first external consumer to prove reuse/provider independence.

## Working rule

The specification/history is the primary artifact.

`Intent -> Spec -> Architecture/ADR -> Tasks -> approved task group -> Implementation -> Evals -> Release decision/evidence -> Merge`

Routine low-risk decisions may be policy-automated. Material changes to authority, security, data handling, cost or external side effects return to the appropriate approval path.