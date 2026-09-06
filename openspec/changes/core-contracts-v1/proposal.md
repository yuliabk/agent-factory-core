# Proposal: Core Contracts v1

## Problem

The repository already contains useful prototype architecture, security controls, runtime portability work and agent-specific experiments, but several platform-wide decisions are still implicit or tied too closely to specific providers/runtimes. The next generation of agents needs a stable Core contract so each agent does not reimplement security, cost controls, tools, memory, orchestration or provider logic.

## Goal

Define a provider-neutral Core contract that every future agent can inherit while keeping business agents in separate repositories.

The change formalizes:

- Agent Manifest and ExecutionContext;
- template-first composition;
- mandatory security and tenant isolation;
- capability-based agent-to-agent routing;
- provider-neutral model selection;
- Tool Gateway and Memory Broker contracts;
- budget warnings, approval and emergency safety caps;
- evidence, eval, approval and release lifecycle;
- conversational non-technical client intake.

## Why now

The Travel Agent contract and Knowledge Agent prototype demonstrate that agent-specific work already needs shared governance, evidence and portability. A reusable Research/Brain Agent is planned next. Without Core contracts, that work would create direct coupling and duplicate platform concerns.

## Scope

### In scope

- Architecture/specification/documentation only.
- Contract definitions and proposed schemas/templates.
- Provider/runtime neutrality rules.
- Security, cost, orchestration, memory, tooling and evaluation requirements.
- Transition guidance from earlier provider-specific prototype assumptions.

### Out of scope

- Production runtime implementation.
- New provider accounts or billing changes.
- Production secrets or customer data.
- Deployment of Research/Brain Agent.
- Production migration of Travel Agent.

## Expected outcome

After approval, the repository has one clear architectural direction and a bounded implementation sequence for a small Core skeleton before the Research/Brain Agent repository is built.
