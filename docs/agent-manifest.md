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
- `capabilities` - lightweight references to capabilities the Agent provides or requires.
- `tools` - tool/capability requirements, not client credential bindings.
- `permissions` - permissions the Agent requires/requests, never grants to itself.
- `memoryProfile` - reference to the memory behavior/profile required by the Agent.
- `budgetProfile` - reference to the expected cost/budget behavior, not a concrete client amount.
- `evalProfile` - reference to the evaluation family/profile required before release.

This is the minimum skeleton, not the final forever-schema. New fields should be added only when a real use case proves they are needed.

## 3. Capability reference rule

`Capability Registry` is the source of truth for capability metadata and contracts. The AgentManifest does not duplicate registry-owned information such as provider identity, input/output schema, risk classification, cost class, health state or default routing metadata.

A capability entry in the manifest is deliberately small:

```yaml
ref: research.lookup
version: "1"
overrides: {}
```

A required capability may also declare whether it is optional:

```yaml
ref: web.search
version: "1"
optional: true
overrides: {}
```

Rules:

- `ref` identifies the registry capability.
- `version` declares the required/provided contract version or range representation supported by the current compiler.
- `optional` is allowed for `requires` entries only.
- `overrides` contains only keys explicitly declared overrideable by the resolved registry record.
- The compiler rejects unknown/non-overrideable keys.
- Registry-owned metadata is not copied into AgentManifest.
- A capability reference does not grant permission to use that capability.

This keeps Agent Definitions portable while allowing bounded per-Agent tuning without creating a second registry inside every manifest.

## 4. Canonical minimal example

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
      - ref: research.lookup
        version: "1"
        overrides: {}
    requires:
      - ref: web.search
        version: "1"
        optional: true
        overrides: {}

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

## 5. Important authority rule

Fields in `AgentManifest` are **requirements or profile references**, not runtime authority.

For example:

```text
AgentManifest says:      "I require web.search"
Capability Registry:     "This is the authoritative contract/metadata"
ClientInstanceConfig:    "This tenant enables web.search"
PlatformPolicy:          "web.search is allowed at this trust/data level"
ExceptionPolicy:         "optional scoped override, if valid"
Compiler result:         effective grant or denial
```

An Agent never authorizes itself by declaring a permission or capability in its manifest.

## 6. ClientInstanceConfig

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

## 7. EffectiveReleaseConfig compiler

The Build / Control Plane compiler combines:

```text
AgentManifest
+ Capability Registry contracts/metadata
+ ClientInstanceConfig
+ PlatformPolicy
+ valid ExceptionPolicy overlays
```

and produces one immutable `EffectiveReleaseConfig` for a specific `agent_release_id`.

The compiler resolves capability references and profile references into concrete effective values, including:

- capability contract resolution;
- validated capability overrides;
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

## 8. Schema implementation boundary

The accepted implementation model is hybrid:

```text
Approved contract/spec
      -> canonical JSON Schema
      -> Pydantic runtime models/validators
      -> compiler/runtime logic
```

Rules:

- JSON Schema is the canonical external machine-readable contract.
- Pydantic is the internal Python representation and validation layer.
- External consumers must be able to validate without importing Python/Pydantic.
- Pydantic must not define a second independent meaning for the contract.
- Schema/Pydantic alignment must be covered by automated tests so drift is detected early.
- If Core moves away from Python in the future, the external JSON Schema should remain stable while the internal type implementation can change.

Canonical files for the first skeleton:

- `schemas/agent-manifest.schema.json`
- `agent_factory_core/contracts/agent_manifest.py`
- `tests/contracts/test_agent_manifest_contract.py`

## 9. Validation rules for the first skeleton

The first validator/compiler must at minimum reject:

- missing `apiVersion`, `kind`, `metadata` or `spec`;
- missing `metadata.name`, `metadata.version` or `metadata.description`;
- unsupported template/profile reference;
- malformed capability reference;
- capability metadata duplicated into a reference when the schema forbids it;
- override key not declared overrideable by Capability Registry;
- requested permission not allowed by client/platform policy;
- secret values embedded in versioned configuration;
- invalid or expired ExceptionPolicy;
- compilation that cannot produce a complete EffectiveReleaseConfig for the selected environment.

Errors should identify the exact path, violated rule and a short remediation hint.

## 10. Expansion rule

Do not add fields to the AgentManifest simply because they may be useful someday.

A field moves into the reusable manifest only when it describes stable Agent Definition requirements shared across client instances. Capability-owned metadata stays in Capability Registry; client-specific values stay in `ClientInstanceConfig`; platform-wide rules stay in `PlatformPolicy`; resolved runtime authority stays only in `EffectiveReleaseConfig`.

## 11. Source of truth

The approved specification/history remains the primary design artifact. JSON Schema is the canonical external schema projection of the contract. Capability Registry is the source of truth for capability contract metadata. Pydantic models are internal runtime projections and must remain aligned with the canonical JSON Schema.
