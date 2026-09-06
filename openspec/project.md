# Project Context

## Vision

`Agent Factory Core` enables a small platform team/Owner to specify, compose, evaluate and maintain many client Agents while keeping the client experience short and non-technical.

The versioned specification and decision history are the primary artifacts. Agents/deployments are reproducible outputs.

## Core architecture

Core is logically split into:

- **Build / Control Plane** - Intent/Spec Compiler, Template Engine, Manifest/client config validation, policy compilation, eval/release artifacts.
- **Runtime Governance Plane** - trusted ExecutionContext, policy/trust/risk enforcement, orchestration, capability/model/tool/memory routing, budget/runtime limits and audit.

Business Agents live in separate repositories.

Canonical release model:

```text
AgentManifest
 + ClientInstanceConfig
 + PlatformPolicy / ExceptionPolicy
 -> EffectiveReleaseConfig
 -> Deployed Agent Instance
```

## Platform principles

- provider-neutral and adapter-based;
- specification first;
- one Core, many independent Agent repositories;
- Agent requests authority but does not grant it;
- security/tenant/budget/audit/runtime controls are platform-level;
- approvals are risk/policy driven rather than mandatory for every low-risk operation;
- Trust Profiles simplify configuration while preserving ceilings;
- controlled ExceptionPolicy handles overridable rules without modifying global architecture;
- Agents communicate through versioned capabilities, not direct peer coupling;
- Capability Registry is soft-strict: flexible development, strict critical production resolution;
- orchestration is hybrid: Core sets boundaries, Agents plan autonomously inside them;
- memory is governed and separated by class/tenant; Agents may write within effective policy;
- routing optimizes according to client/task policy across cost, quality, privacy, latency and availability;
- templates are starting points plus modular composition;
- eval thresholds and release strategy are policy-driven;
- progressive complexity: start with the simplest architecture that satisfies the outcome.

## Client experience constraints

- clients describe business intent, not technology;
- initial intake target is usually under 10 minutes and typically 5-6 critical follow-up questions, not a hard limit;
- ambiguous requests use `infer -> show assumptions -> confirm/correct`;
- technical black box remains business-transparent regarding scope, material assumptions, data use, cost, limitations and approvals.

## Data/security constraints

- MVP/prototype uses synthetic/non-sensitive data unless a dedicated privacy/security gate is approved;
- client data/secrets/state remain tenant-scoped and outside reusable Agent Definition;
- untrusted Web/Email/file/retrieval/MCP/Tool/Agent output cannot grant authority;
- production will finalize the explicit catalog of non-overridable Platform Invariants;
- emergency safety cap is independent from business-budget approval.

## Roles

- Platform Owner: material product/architecture decisions and platform governance.
- Builder/Coding Agent: specs, synchronization, implementation of accepted task groups and evidence collection.
- Client Process Owner/authorized client approver: client scope, business permissions/acceptance and policy-defined runtime approvals.
- Security/Privacy/Domain Owner: elevated data/risk path approval when effective policy requires it.
- PlatformPolicy: deterministic authority for low-risk auto decisions and mandatory gates.

## Source of Truth

- versioned approved specification/history: primary behavior intent;
- `openspec/specs/`: accepted/folded behavior;
- `openspec/changes/`: active bounded implementation contracts;
- `docs/`: architecture, policies, ADRs and decision history;
- `templates/`: reusable machine-readable starting contracts;
- Agent repositories: Agent-specific behavior/domain assets;
- `EffectiveReleaseConfig`: immutable runtime authority for a specific release.

## Current implementation strategy

Prove a thin vertical Core slice before deep infrastructure: schemas/compiler, trusted policy/runtime kernel, minimal adapters/registry/gateways, eval/release kernel and one synthetic end-to-end Agent. Then build Research/Brain Agent as the first real reusable Agent.