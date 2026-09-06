# Design: Core Contracts v1

## Architecture direction

`Agent Factory Core` is a platform Core with two logical planes: Build / Control Plane and Runtime Governance Plane. Business Agents remain independently versioned repositories.

The versioned specification is the primary artifact.

```text
Business Intent
 -> Spec Compiler
 -> Template + modular composition
 -> AgentManifest
 + ClientInstanceConfig
 + PlatformPolicy / ExceptionPolicy
 -> EffectiveReleaseConfig
 -> Runtime Governance Plane
    -> bounded Agent planning
    -> Model Router
    -> Capability Registry
    -> Tool Gateway
    -> Memory Gateway
 -> Evals / Evidence / Release Decision
 -> Versioned Release
```

## Boundary decisions

### Build / Control Plane owns

- intent/spec compilation;
- template/module selection;
- AgentManifest and ClientInstanceConfig validation;
- PlatformPolicy/ExceptionPolicy compilation;
- EffectiveReleaseConfig generation;
- evaluation/release planning and evidence;
- registry/contract metadata.

### Runtime Governance Plane owns

- trusted ExecutionContext;
- policy/risk/trust enforcement;
- hybrid orchestration boundaries;
- capability/model/tool/memory routing;
- budget/runtime/hop/safety limits;
- approvals/escalations when effective policy requires them;
- runtime audit/traces/drift detection.

### Agent repository owns

- reusable domain/business behavior;
- domain prompts/workflows;
- provided/required capabilities;
- Agent-specific eval data;
- reusable AgentManifest requirements;
- domain-specific non-Core assets.

Agent repositories do not store client secrets, raw PII or client business state.

## Manifest / client / effective release model

```text
AgentManifest (reusable requirements)
 + ClientInstanceConfig (tenant grants/config)
 + PlatformPolicy / ExceptionPolicy
 = EffectiveReleaseConfig (immutable runtime authority)
```

Agents request authority; they do not grant it to themselves.

## Security and governance model

- default deny + least privilege + policy-before-execution;
- approvals are risk-based rather than mandatory for every low-risk action;
- trust profiles begin with `sandbox`, `internal`, `business`, `privileged`;
- Factory proposes trust; PlatformPolicy defines the ceiling; client can configure within it;
- rules are either non-overridable invariants or overridable through a scoped, expiring, audited ExceptionPolicy;
- untrusted content cannot grant permissions;
- persistent memory, tools, providers and Agent delegation remain governed outside model output.

## Release strategy

Release behavior is versioned and policy-bounded:

- `human-required`;
- `policy-auto`;
- `policy` (derive from risk/trust/environment/change class).

Automatic release still requires all blocking gates to pass and produces the same release evidence/decision record.

## Evaluation model

Functional/business, security/policy, cost/runtime and contract/portability evals are first-class. PlatformPolicy determines whether a result is blocking, warning or advisory.

Non-overridable security failures always block. A universal business-quality score is intentionally rejected.

## Provider model

Routing is provider-neutral and policy-driven. The system can optimize for economy, balance, quality, latency or privacy according to task/client constraints. Provider fallback must remain inside data/privacy/eval policy.

## Agent-to-Agent model

Consumers request versioned capabilities. Core resolves implementation and delegates minimum context/permissions/budget.

Registry enforcement is soft-strict:

- sandbox/dev may warn or use explicit mocks for optional/non-critical dependencies;
- production requires critical/consequential capabilities to resolve to registered, compatible and policy-approved implementations.

## Orchestration model

Core defines authority and limits. Business Agents autonomously decide how to plan/decompose and which approved capability to request inside those boundaries.

## Memory model

Memory classes are logically separated. Agents may identify useful information and request/write memory autonomously if effective policy permits. Policy decides class, purpose, retention, minimization/consent and tenant boundary.

## Template model

Templates are versioned starting points plus modular capability composition, not rigid complete architectures. Factory prefers the simplest composition that satisfies the approved outcome.

## Client intake

Client gives a plain-language business goal. The platform asks only critical missing questions, offers understandable budget options and uses `infer -> show assumptions -> confirm/correct` for non-critical ambiguity. Under-10-minute/5-6-question behavior is a UX target, not a hard contract limit.

## Implementation strategy

Move fast through a thin vertical slice instead of fully building each subsystem in isolation:

1. schemas/compiler -> EffectiveReleaseConfig;
2. trusted ExecutionContext + policy/budget kernel;
3. minimal provider/capability/tool/memory interfaces;
4. eval/release decision kernel;
5. one synthetic end-to-end reference Agent;
6. Research/Brain Agent as first real external Agent.

Do not wait for long-term database/service-mesh/registry choices before proving the contracts.