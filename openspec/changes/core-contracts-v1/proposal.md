# Proposal: Core Contracts v1

## Status

Architecture direction reviewed and accepted by Owner on 2026-09-06. This change now serves as the implementation contract for a thin Core Skeleton. Material deviations from the accepted authority/security/data/cost architecture require renewed Owner review.

## Problem

The repository contains valuable prototype architecture, security controls, portability work and Agent experiments, but a scalable Factory needs one provider-neutral contract so every Agent does not reimplement security, cost, tools, memory, orchestration, release governance or provider logic.

## Goal

Define a maintainable Core that turns versioned specifications into reusable Agent Definitions and governed client deployments, while keeping Business Agents in separate repositories.

Canonical model:

```text
Business Intent -> Versioned Spec
AgentManifest + ClientInstanceConfig + PlatformPolicy/ExceptionPolicy
 -> EffectiveReleaseConfig
 -> bounded Runtime Governance
 -> Evidence/Evals/Release Decision
```

## Accepted platform decisions

The change formalizes:

- Build / Control Plane separated logically from Runtime Governance Plane;
- specification/history as primary artifact;
- reusable AgentManifest separated from ClientInstanceConfig;
- immutable EffectiveReleaseConfig as runtime authority;
- risk-based Trust Profiles and controlled ExceptionPolicy;
- configurable release strategy (`human-required`, `policy-auto`, `policy`);
- hybrid bounded-autonomy orchestration;
- soft-strict Capability Registry;
- provider-neutral policy-driven model routing;
- Tool Gateway and governed autonomous Memory Gateway;
- business budget + independent emergency safety cap;
- policy-driven evaluation thresholds and release gates;
- hybrid template-first modular composition;
- non-technical, assumption-aware client intake.

## Why now

Travel Agent and Knowledge Agent work already need shared governance/evidence/portability. Research/Brain Agent is the next reusable business Agent. Implementing it before the Core contract would duplicate platform concerns and create provider/capability coupling.

## Scope

### In scope for the next implementation slice

- schemas/validators for AgentManifest, ClientInstanceConfig, PlatformPolicy/ExceptionPolicy and EffectiveReleaseConfig;
- trusted ExecutionContext;
- minimal policy/trust/permission/budget runtime kernel;
- provider/capability/tool/memory adapter interfaces;
- minimal eval/release decision/evidence/audit contracts;
- one synthetic end-to-end vertical slice.

### Out of scope for this slice

- production customer data/secrets;
- full distributed registry/service mesh/Kubernetes;
- final long-term memory backend;
- full client-facing Factory UI;
- production Research/Brain or Travel migration before the Core slice passes its gate.

## Expected outcome

The repository provides one coherent source of truth and a fast implementation path: prove the thin Core vertical slice first, then build Research/Brain Agent as the first real reusable Agent and Travel Agent as its first consumer.