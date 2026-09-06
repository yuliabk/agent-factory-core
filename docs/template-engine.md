# Template Engine

**Status:** Accepted direction after Owner Review

## Purpose

The Template Engine prevents every new Agent from being built from scratch while avoiding rigid one-template-fits-all behavior.

A template is a starting structure, not a cage.

## Composition model

```text
ClientIntent
 + Approved Spec
 + Base Template
 + Optional Capability Modules
 + AgentManifest
 + ClientInstanceConfig
 + PlatformPolicy
 + Agent-specific assets
 = Build Plan / Agent Repository + EffectiveReleaseConfig
```

## Hybrid principle

The Factory uses a **hybrid template + modular assembly** model:

1. choose the smallest suitable base template;
2. add only the capability modules required by the specification;
3. keep business-specific logic in the Agent repository;
4. compile client-specific configuration separately;
5. do not add complexity unless the business outcome requires it.

This implements progressive complexity: start simple, expand only when justified.

## Template classes

### Base templates

Small platform-maintained skeletons such as:

- `general-agent`;
- `knowledge-agent`;
- `workflow-agent`;
- `research-agent`.

They provide repository structure, manifest hooks, eval/test hooks, logging interfaces and policy integration points.

### Capability modules/templates

Composable additions may include:

- knowledge retrieval;
- conversational intake;
- external actions;
- research delegation;
- CRM integration;
- messaging channels;
- memory patterns;
- approval workflow hooks.

### Business templates

Larger domain templates may live in separate repositories/packages and register with the Core. The Core should not become a monorepo containing every business domain.

## Rules

- Templates are versioned and immutable after release.
- Every build records exact template/module versions.
- Templates contain no client secrets or production data.
- Template variables have schemas/defaults.
- Templates can declare requirements but cannot grant permissions.
- Client-specific values remain outside reusable template packages.
- Upgrades require policy-defined compatibility/regression evals.
- Business logic belongs to Agent repositories, not generic Core templates.

## Selection

The Spec Compiler recommends a composition from required capabilities, risk/trust profile, budget and expected complexity.

The Factory SHOULD prefer the simplest composition that can satisfy the approved business outcome.

Human override is available when policy or Owner review requires it, but routine low-risk composition can be policy-automated.

## Extension policy

Prefer composition over deep inheritance. A new need should first be represented as a capability, module or adapter. Add a new base template only when the structural difference cannot be expressed cleanly through composition.

## Template location strategy

The Engine and template contracts live in Core. Small platform base templates may live in Core. Large business/domain templates may live in separate repositories or a future package registry.

The exact registry/storage backend remains an implementation decision; the versioned contract is stable.