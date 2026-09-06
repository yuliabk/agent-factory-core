# Template Engine

**Status:** Proposed

## Purpose

The Template Engine prevents every new agent from being built from scratch. It composes a versioned agent skeleton from reusable platform contracts plus agent-specific configuration.

## Composition model

```text
ClientIntent
 + Approved Spec
 + Base Template
 + Optional Capability Templates
 + Agent Manifest
 + Policy Profiles
 + Agent-specific assets
 = Build Plan / Agent Repository
```

## Template classes

### Base templates

Small platform-maintained skeletons such as:

- `general-agent`
- `knowledge-agent`
- `workflow-agent`
- `research-agent`

They provide repository structure, manifest hooks, test hooks, logging interfaces and policy integration points.

### Capability templates

Composable additions such as:

- knowledge retrieval;
- conversational intake;
- external actions;
- research delegation;
- CRM integration;
- messaging channel.

### Business templates

Larger domain templates may live in separate repositories/packages and register with the Core. The Core should not become a monorepo of every domain.

## Rules

- Templates are versioned and immutable after release.
- A build records exact template versions.
- Templates contain no client secrets or production data.
- Template variables have schemas and defaults.
- A template cannot grant permissions; Manifest + Policy must authorize them.
- Template upgrades require compatibility checks and regression evals.
- Business logic belongs to the agent repository, not to the generic Core template.

## Selection

The Spec Compiler recommends templates from required capabilities and risk profile. The Owner may override the recommendation before build.

## Extension policy

Prefer composition over deep inheritance. A new need should first be represented as a capability or adapter. Add a new base template only when existing composition cannot express the structural difference cleanly.
