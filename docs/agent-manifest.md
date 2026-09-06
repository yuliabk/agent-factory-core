# Agent Manifest, Client Instance and Effective Release Contracts

**Status:** Accepted minimal Core Skeleton direction  
**Date:** 2026-09-06

## 1. Purpose

For the first executable Core Skeleton, the reusable `AgentManifest` must stay intentionally small. It describes the Agent Definition, not a concrete client deployment.

```text
AgentManifest
        +
ClientInstanceConfig
        +
PlatformPolicy / ExceptionPolicy
        =
EffectiveReleaseConfig
        -> Deployed Agent Instance
```

The first implementation should prove this chain end-to-end before the manifest grows additional fields.

## 2. Minimal AgentManifest shape

The MVP manifest has only four top-level elements:

- `apiVersion`
- `kind`
- `metadata`
- `spec`

### `metadata`

For the first schema, metadata contains only:

- `name`
- `version`
- `description`

### `spec`

For the first schema, `spec` contains only:

- `template` - reference to the starting template/version.
- `capabilities` - capabilities the Agent provides or requires.
- `tools` - tool/capability requirements, not client credential bindings.
- `permissions` - permissions the Agent requires/requests, never grants to itself.
- `memoryProfile` - reference to the memory behavior/profile required by the Agent.
- `budgetProfile` - reference to the expected cost/budget behavior, not a concrete client amount.
- `evalProfile` - reference to the evaluation family/profile required before release.

This is the minimum skeleton, not the final forever-schema. New fields should be added only when a real use case proves they are needed.

## 3. Canonical minimal example

```yaml
apiVersion: agentfactory.io/v1alpha1
kind: AgentManifest

metadata:
  name: research-agent
  version: 0.1.0
  description: "Reusable policy-bounded research capability"

spec:
  template:
    name: general-agent
    version: 1

  capabilities:
    provides:
      - research.lookup@v1
    requires:
      - web.search@v1

  tools:
    required:
      - web.search

  permissions:
    requested:
      - web.search

  memoryProfile: session-plus-client-knowledge
  budgetProfile: balanced
  evalProfile: standard-agent
```

## 4. Important authority rule

Fields in `AgentManifest` are **requirements or profile references**, not runtime authority.

For example:

```text
AgentManifest says:      "I require web.search"
ClientInstanceConfig:    "This tenant enables web.search"
PlatformPolicy:          "web.search is allowed at this trust/data level"
ExceptionPolicy:         "optional scoped override, if valid"
Compiler result:         effective grant or denial
```

An Agent never authorizes itself by declaring a permission in its manifest.

## 5. ClientInstanceConfig

`ClientInstanceConfig` adds values belonging to a specific client/environment without modifying the reusable Agent Definition.

Typical client-specific values include:

- tenant/environment identity;
- actual permission grants;
- enabled tools/capabilities and bindings;
- concrete budget and runtime approver;
- trust/data classification;
- provider restrictions;
- memory/retention choices;
- channels/integrations;
- credential references;
- release strategy and approved exception references.

The same AgentManifest can therefore be deployed to many clients without repository forks.

## 6. EffectiveReleaseConfig compiler

The Build / Control Plane compiler combines:

```text
AgentManifest
+ ClientInstanceConfig
+ PlatformPolicy
+ valid ExceptionPolicy overlays
```

and produces one immutable `EffectiveReleaseConfig` for a specific `agent_release_id`.

The compiler resolves profile references into concrete effective values, including:

- effective permissions;
- enabled tools/capabilities;
- memory policy;
- concrete business budget and safety controls;
- model/provider routing policy where applicable;
- runtime limits;
- eval requirements;
- release strategy/approval route;
- credential references;
- policy/exception versions.

Runtime executes the compiled Effective Release, never the raw manifest or conversational assumptions.

## 7. Validation rules for the first skeleton

The first validator/compiler must at minimum reject:

- missing `apiVersion`, `kind`, `metadata` or `spec`;
- missing `metadata.name`, `metadata.version` or `metadata.description`;
- unsupported template/profile reference;
- requested permission not allowed by client/platform policy;
- secret values embedded in versioned configuration;
- invalid or expired ExceptionPolicy;
- compilation that cannot produce a complete EffectiveReleaseConfig for the selected environment.

Errors should identify the exact path, violated rule and a short remediation hint.

## 8. Expansion rule

Do not add fields to the AgentManifest simply because they may be useful someday.

A field moves into the reusable manifest only when it describes stable Agent Definition requirements shared across client instances. Client-specific values stay in `ClientInstanceConfig`; platform-wide rules stay in `PlatformPolicy`; resolved runtime authority stays only in `EffectiveReleaseConfig`.

## 9. Source of truth

The approved specification/history remains the primary artifact. The manifest is a machine-readable projection of the Agent Definition used by the Core compiler.