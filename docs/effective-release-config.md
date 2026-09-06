# EffectiveReleaseConfig Compiler Contract

**Status:** Core Skeleton v1 implementation contract  
**Date:** 2026-09-06

## Purpose

`EffectiveReleaseConfig` is the single runtime-executable configuration artifact for a released Agent instance.

It is generated, not hand-authored:

```text
AgentManifest
+ ClientInstanceConfig
+ PlatformPolicy
+ valid ExceptionPolicy overlays
+ Capability Registry resolution
-> compiler
-> EffectiveReleaseConfig
```

Runtime MUST execute the compiled Effective Release rather than raw Manifest, client configuration or conversational assumptions.

## Current compiler skeleton

The compiler now validates:

- `ClientInstanceConfig.spec.agentRef` matches the AgentManifest name/version;
- Agent-requested permissions are explicitly granted by the client and allowed by effective policy;
- PlatformPolicy `deniedPermissions` remain blocking;
- scoped, unexpired ExceptionPolicy overlays only expand dimensions declared overrideable by PlatformPolicy;
- provider profile is allowed by effective policy;
- every required tool has a concrete binding;
- budget and memory override keys are allowed by effective policy;
- required capability refs resolve through Capability Registry;
- capability override keys/values obey the Registry record;
- Registry-required permissions are declared by the Agent;
- exact PlatformPolicy and applied ExceptionPolicy references are recorded.

Validation failures expose `path`, `rule` and a short `remediation` hint.

## Output skeleton

The first `EffectiveReleaseConfig` records:

- release ID and environment;
- platform policy name/version and applied exception references;
- Agent reference and tenant;
- variables and declared capabilities;
- resolved `capabilityBindings` from capability ref to implementation ID;
- provider profile;
- secret references;
- memory and budget configuration;
- effective permissions;
- data classification;
- tool bindings;
- evaluation profile.

The Pydantic release model is frozen. Operationally, a released artifact is immutable: any material change produces a new `releaseId` instead of editing an existing release.

## Runtime handoff

The trusted per-request `ExecutionContext` is derived from this compiled object plus request identity/trace/deadline values. Runtime authority is never reconstructed from the raw inputs.

## Canonical implementation

- External contract: `schemas/effective-release-config.schema.json`
- Python model: `agent_factory_core/contracts/effective_release_config.py`
- Compiler: `agent_factory_core/compiler.py`
- Policy contracts: `schemas/platform-policy.schema.json`, `schemas/exception-policy.schema.json`
- Registry resolver: `agent_factory_core/registry.py`
- ExecutionContext: `schemas/execution-context.schema.json`, `agent_factory_core/contracts/execution_context.py`
