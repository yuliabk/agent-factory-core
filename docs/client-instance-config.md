# ClientInstanceConfig Contract

**Status:** Accepted  
**Date:** 2026-09-06

## Purpose

`ClientInstanceConfig` describes one concrete client/environment deployment of a reusable Agent Definition. It does not contain reusable Agent business logic.

```text
AgentManifest
+ ClientInstanceConfig
+ PlatformPolicy / ExceptionPolicy
-> EffectiveReleaseConfig
```

## Minimal shape

Top level:

- `apiVersion`
- `kind: ClientInstanceConfig`
- `metadata`
- `spec`

`metadata` contains only:

- `name`
- `environment`

`spec` contains:

- `agentRef` - reusable Agent name/version.
- `tenant` - tenant identity.
- `variables` - client/environment values that do not redefine Agent behavior.
- `providerProfile` - requested provider/model policy profile.
- `secretsRef` - references only; never secret values.
- `memoryConfig` - client memory settings/overrides.
- `budgetOverrides` - client budget settings/overrides.
- `permissionOverrides` - explicit allow/deny values within policy.
- `toolBindings` - concrete approved tool bindings.

## Boundary rule

`ClientInstanceConfig` MUST NOT contain prompts, reusable workflows, domain rules or other Agent business logic. Those remain in the Agent Definition/AgentManifest/specification.

All overrides are requests/configuration bounded by `PlatformPolicy` and valid `ExceptionPolicy`. They do not independently create runtime authority.

## Runtime rule

Runtime does not execute `ClientInstanceConfig` directly. The Core compiler validates and combines it with the AgentManifest and policy inputs to produce an immutable, versioned `EffectiveReleaseConfig`.

## Canonical implementation

- External contract: `schemas/client-instance-config.schema.json`
- Python runtime model: `agent_factory_core/contracts/client_instance_config.py`
- Example: `templates/client-instance-config.yaml`
- Alignment tests: `tests/contracts/test_client_instance_config_contract.py`
