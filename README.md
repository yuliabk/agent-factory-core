# Agent Factory Core

A spec-driven control plane for building, testing, releasing and governing reusable AI agents.

The repository is currently in architecture/contract hardening. It does not contain a production agent runtime or real customer data.

## Platform goal

A non-technical client should be able to describe a business need in plain language, answer a small number of critical questions, confirm assumptions/budget and receive an agent built from approved templates and policies.

Behind that simple experience, Core standardizes:

- Agent Manifest and lifecycle.
- Security, tenant isolation and approvals.
- Orchestration and `ExecutionContext`.
- Capability-based agent-to-agent routing.
- Provider-neutral model routing.
- Tool/API/MCP access through policy.
- Memory/retrieval contracts.
- Budget and cost guardrails.
- Evals, evidence, audit and release controls.
- Template-first agent composition.

## Repository boundaries

`Agent Factory Core` is not a business agent. Travel, Research, Sales, CRM and future agents should live in separate repositories and consume Core contracts.

Specific providers such as OpenAI, Dify, n8n, Gemini, DeepSeek or others are adapters/options rather than architectural dependencies unless an approved requirement explicitly fixes one.

## Repository structure

```text
AGENTS.md                         repository governance for coding agents
docs/                             architecture, security, contracts, ADRs, roadmap
openspec/                         accepted specs and proposed changes
templates/                        reusable manifest/intake/spec/test templates
.agents/skills/                   repo-scoped authoring/build skills
tools/                            bounded validation/portability tooling
tests/                            deterministic repository tests
```

Start with [`docs/README.md`](docs/README.md).

## Current state

- `main` is the canonical branch.
- Travel Agent Instance Contract v1 is included as architecture/spec work.
- The historical Knowledge Agent synthetic smoke closure evidence is consolidated into `main`.
- Current architectural focus: `Core Contracts v1` before new runtime implementation.
- Next intended specialized repository after Core contracts are stable: a Research/Brain Agent exposing a reusable `research.lookup` capability.

## Working rule

`Intent -> OpenSpec -> Architecture/ADR -> Tasks -> Owner approval -> Implementation -> Evals -> Release evidence -> Merge`

No production implementation is implied by documentation being present in `main`.
