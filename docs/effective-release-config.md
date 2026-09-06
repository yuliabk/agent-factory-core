# EffectiveReleaseConfig Compiler Contract

**Status:** Accepted skeleton direction  
**Date:** 2026-09-06

## Purpose

`EffectiveReleaseConfig` is the single runtime-executable configuration artifact for a released Agent instance.

It is generated, not hand-authored:

```text
AgentManifest
+ ClientInstanceConfig
+ PlatformPolicy
+ valid ExceptionPolicy overlays
-> compiler
-> EffectiveReleaseConfig
```

Runtime MUST execute the compiled Effective Release rather than raw Manifest, client configuration or conversational assumptions.

## First compiler skeleton

The first compiler validates already-accepted rules only:

- `ClientInstanceConfig.spec.agentRef` matches the AgentManifest name/version;
- Agent-requested permissions are explicitly granted by the client and allowed by PlatformPolicy;
- explicit client/platform denies win;
- provider profile is allowed by policy;
- every required tool has a concrete binding;
- budget and memory override keys are policy-allowed;
- the PlatformPolicy version is recorded;
- ExceptionPolicy references are recorded for the release.

Validation failures expose `path`, `rule` and a short `remediation` hint.

## Output skeleton

The first `EffectiveReleaseConfig` records:

- release ID and environment;
- platform/exception policy references;
- Agent reference and tenant;
- resolved variables and capabilities;
- provider profile;
- secret references;
- memory and budget configuration;
- effective permissions;
- tool bindings;
- evaluation profile.

The Pydantic release model is frozen. Operationally, a released artifact is immutable: any material change produces a new `releaseId` instead of editing an existing release.

## Current limitation

The first compiler temporarily receives PlatformPolicy through a narrow mapping interface. The dedicated `PlatformPolicy` and `ExceptionPolicy` JSON Schema/Pydantic contracts remain the next policy-contract task and will replace that temporary boundary without changing the compiler's role.

## Canonical implementation

- External contract: `schemas/effective-release-config.schema.json`
- Python model: `agent_factory_core/contracts/effective_release_config.py`
- Compiler: `agent_factory_core/compiler.py`
- Example: `templates/effective-release-config.yaml`
- Tests: `tests/contracts/test_effective_release_compiler.py`
