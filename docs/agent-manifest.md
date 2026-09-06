# Agent Manifest, Client Instance and Effective Release Contracts

**Status:** Accepted direction after Owner Review  
**Owner approval:** Required for implementation of the contract schemas

## 1. Purpose

The platform separates reusable agent definition from client-specific authorization and runtime configuration.

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

This separation prevents client budgets, credentials, retention rules and permissions from being embedded in a reusable Agent repository.

## 2. AgentManifest

`AgentManifest` lives with the Agent Definition and describes what the Agent is and what it requires. It is machine-readable, versioned and reusable across clients.

It MUST NOT contain secrets, raw PII, client credentials, client-specific business state or concrete authorization grants.

### Required MVP sections

| Section | Purpose |
|---|---|
| `apiVersion` | Contract schema version |
| `kind` | `AgentManifest` |
| `metadata` | Stable identity, version and owner |
| `intent` | Business purpose and success outcome |
| `template` | Base/template lineage |
| `capabilities` | Capabilities provided and required |
| `requirements` | Requested tools, memory, data classes and runtime needs |
| `modelRequirements` | Model profile requirements, not hard-coded provider |
| `evaluationRequirements` | Functional/security/cost/domain eval families |
| `releaseRequirements` | Default release strategy and rollback expectations |

### Example

```yaml
apiVersion: agentfactory.io/v1alpha1
kind: AgentManifest
metadata:
  id: research-agent
  version: 0.1.0
  owner: platform-owner
intent:
  businessGoal: "Provide policy-bounded research to other agents"
  successOutcome: "Return structured evidence with provenance"
template:
  id: general-agent
  version: 1
capabilities:
  provides:
    - name: research.lookup
      contractVersion: 1
  requires:
    - name: web.search
      optional: true
requirements:
  requestedPermissions:
    - capability: web.search
  memoryClasses:
    - session
    - client_knowledge
  dataClasses:
    - public
    - internal
  runtimeProfile: bounded-standard
modelRequirements:
  profile: balanced
  allowFallback: true
evaluationRequirements:
  requiredFamilies:
    - functional
    - security
    - cost
releaseRequirements:
  strategy: policy
  rollbackRequired: true
```

The Agent asks for permissions and capabilities. It never grants them to itself.

## 3. ClientInstanceConfig

`ClientInstanceConfig` is tenant/environment specific. It binds the reusable Agent Definition to one client deployment.

It includes, as applicable:

- `tenant_id` and environment;
- enabled capabilities and tools;
- concrete permission grants within Platform Policy;
- client data classification and source references;
- budget envelope and runtime approver;
- model/provider restrictions;
- memory and retention configuration;
- channels and integration bindings;
- trust level;
- release strategy override if permitted;
- approved policy exceptions by reference;
- credential references, never credential values.

A client may make configuration stricter. It may not exceed the maximum authority permitted by Platform Policy or a valid ExceptionPolicy.

## 4. PlatformPolicy and ExceptionPolicy

PlatformPolicy defines mandatory limits, risk rules, trust-level ceilings, security invariants, cost guardrails and release governance.

ExceptionPolicy is a controlled, explicit override mechanism for rules that are declared overridable. An exception includes scope, reason, approver, expiration/review date and audit reference.

Non-overridable platform invariants cannot be bypassed by Manifest, client configuration, prompt, model output or exception.

## 5. EffectiveReleaseConfig

The Build / Control Plane compiles the three inputs into an immutable `EffectiveReleaseConfig` for a specific `agent_release_id`.

```text
EffectiveReleaseConfig
- agent_release_id
- agent_manifest_version
- client_instance_config_version
- platform_policy_version
- exception_policy_refs[]
- effective_permissions[]
- enabled_capabilities[]
- tool_bindings[]
- model_routing_profile
- memory_policy
- data_classification
- trust_level
- business_budget
- emergency_safety_cap
- runtime_limits
- release_strategy
- required_evals[]
- approval_routes[]
- credential_refs[]
- rollback_target
```

Runtime executes the Effective Release, not raw drafts or conversational assumptions.

## 6. Validation invariants

The compiler/validator rejects a release when:

- a requested permission is not granted by ClientInstanceConfig + PlatformPolicy;
- a grant exceeds the trust-level ceiling;
- a non-overridable invariant would be weakened;
- a required capability has no acceptable resolution for the target environment;
- a secret value appears in a versioned config;
- required budget/runtime controls are absent;
- a protected side effect lacks a valid approval route;
- release strategy conflicts with Platform Policy;
- an ExceptionPolicy is expired, out of scope or invalid;
- required evals or rollback requirements are missing.

## 7. Change and re-approval rules

A new Effective Release is required when any material input changes. Fresh approval is required when policy classifies the change as material, including permission expansion, higher data class, new consequential tool, increased trust level, material budget expansion, retention change, major capability contract change or release-policy change.

Provider/model substitutions that preserve the approved profile may use a regression fast path when Platform Policy permits.

## 8. Source of truth

The specification and its version history are the primary design artifact. Agent code and deployed instances are reproducible outputs of approved specs, manifests, client configuration and policy versions.