# Orchestration Contract

**Status:** Accepted direction after Owner Review  
**Principle:** Core sets boundaries; Agents may plan autonomously inside those boundaries.

## 1. Hybrid orchestration model

The platform avoids both extremes:

- a central orchestrator that contains all business planning;
- completely autonomous Agents that can bypass shared controls.

Instead:

```text
Runtime Governance Plane
  defines trusted context, permissions, limits, routing and policy
        ↓
Business Agent
  decides how to solve the task and which approved capabilities to request
        ↓
Core gateways/registry
  validate and execute each governed operation
```

The Agent is therefore genuinely agentic, but its autonomy is bounded by EffectiveReleaseConfig and PlatformPolicy.

## 2. Core Orchestrator responsibilities

The Core Orchestrator SHALL:

- create and propagate trusted `ExecutionContext`;
- load the immutable EffectiveReleaseConfig;
- enforce PlatformPolicy and applicable ExceptionPolicy;
- resolve capabilities through Capability Registry;
- route model requests through Model/Provider Policy;
- route tool calls through Tool Gateway;
- route memory operations through Memory Gateway;
- enforce trust/risk, budget, deadline, retry, parallelism and hop limits;
- invoke approval/escalation only when policy requires it;
- produce trace, cost and minimized audit events;
- detect loops/cycles and abnormal spend;
- fail closed for prohibited or unverified consequential actions.

The Core Orchestrator does not contain Travel/Sales/Research-specific business logic.

## 3. Agent planning responsibilities

Within its approved contract, a business Agent MAY:

- decide whether a task needs another capability;
- decompose work into subtasks;
- choose among capabilities/options exposed by policy;
- decide when more evidence or clarification is useful;
- request memory reads/writes;
- choose a bounded plan and revise it after failures.

It MAY NOT:

- grant itself permissions;
- widen tenant/data scope;
- disable audit/security/budget limits;
- use unregistered/unapproved production capabilities when policy blocks them;
- approve its own protected action unless policy explicitly defines a non-human automated authority.

## 4. Execution model

```text
Request
 -> ExecutionContext + EffectiveReleaseConfig validation
 -> Policy/risk/trust precheck
 -> Agent planning
 -> capability/model/tool/memory request
 -> gateway/registry policy check
 -> execute
 -> observe result/evidence
 -> Agent may continue/replan within limits
 -> result validation/eval hooks
 -> audit + response
```

A policy check occurs before each consequential side effect and at other policy-defined control points.

## 5. Delegation contract

A delegation request includes at least:

```text
request_id
trace_id
parent_span_id
caller_agent_id
caller_release_id
required_capability
capability_version_range
tenant_id
actor_id
data_classification
delegated_permissions
budget_slice
deadline
hop_count
input
```

Rules:

- no automatic full permission inheritance;
- delegated authority is the intersection of caller authority, provider scope, ClientInstanceConfig and PlatformPolicy;
- each hop shares the trace/budget chain;
- `maxAgentHopsPerRequest` is mandatory;
- cycles are detected/stopped;
- context is minimized to task need.

## 6. Deterministic vs model/agent decisions

Agents/models may decide/recommend:

- task decomposition;
- which allowed capability to call;
- evidence relevance;
- clarification strategy;
- plan adaptation.

Deterministic platform controls decide:

- permissions and tenant boundaries;
- trust-level ceilings;
- blocking security rules;
- effective budget/safety cap;
- approval validity;
- allowed tools/providers/capabilities;
- exception validity;
- side-effect authorization;
- release eligibility.

## 7. Failure behavior

- Provider unavailable -> policy-defined fallback or graceful failure.
- Tool schema invalid -> reject before execution.
- Permission unavailable -> deny + audit; Agent may choose an allowed alternative.
- Budget preflight exceeds range -> offer cheaper alternative or request approval according to policy.
- Deadline reached -> stop new work and return bounded partial result when allowed.
- Capability unavailable -> compatible fallback, degraded result or escalation.
- Loop/cycle/safety cap -> emergency stop + audit.

## 8. Idempotency and retries

Consequential operations use idempotency when supported. Retry policy is risk-aware and bounded; retries must not duplicate a completed side effect.

## 9. Development flexibility

Sandbox/dev may use warnings, mocks and unresolved optional capabilities where policy permits. Production uses stricter resolution for critical dependencies. Security invariants remain enforced in every environment.