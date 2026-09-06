# ארכיטקטורת Agent Factory Core

**Status:** Accepted and synchronized after Owner Review  
**Date:** 2026-09-06

## 1. מטרת המערכת

`Agent Factory Core` הוא שכבת הפלטפורמה המשותפת לכל Agent שנבנה במערכת. הוא אינו Agent עסקי ואינו מכיל לוגיקה ספציפית של Travel, Sales, CRM, Research או לקוח מסוים.

מטרת העל: לאפשר לבנות, להחליף, לתקן ולתחזק Agents במהירות כאשר Provider, Model, Tool, Runtime או דרישת לקוח משתנים.

> שינוי באחריות אחת צריך להיות מקומי ככל האפשר. לשאלה "איפה משנים את זה?" צריכה להיות בדרך כלל תשובה אחת ברורה.

## 2. העיקרון הקנוני: Spec first

ה-Specification וההיסטוריה שלה הם הארטיפקט הראשי של הפלטפורמה. Agent code, templates, configuration ו-deployment הם outputs שניתנים לשחזור מתוך contracts מאושרים.

```text
Business Intent
 -> Versioned Spec
 -> Agent Definition / Templates
 -> Client Instance Configuration
 -> PlatformPolicy / ExceptionPolicy
 -> EffectiveReleaseConfig
 -> Deployed Agent Instance
```

אין Feature מהותי ללא Spec. אין Runtime authority ללא Policy. אין Release שאינו ניתן לשחזור מה-artifacts הגרסאיים שלו.

## 3. חלוקת אחריות

### Core אחראי על

- Intent/Spec compilation.
- Template selection ו-composition.
- AgentManifest / ClientInstanceConfig validation.
- PlatformPolicy, ExceptionPolicy ו-effective configuration compilation.
- Orchestration ו-ExecutionContext.
- Capability Registry/routing.
- Model/Provider routing.
- Tool Gateway.
- Memory Gateway.
- Security, trust/risk profiles ו-tenant isolation.
- Budget, quotas, runtime limits ו-safety caps.
- Audit, traces, evidence ו-observability.
- Evals, release decisions/gates, rollback ו-drift detection.
- Runtime adapter contracts.

### Core אינו אחראי על

- Agent-specific business prompts/workflows.
- Client-specific business rules שאינם כלל פלטפורמה.
- Client knowledge/data/secrets.
- Business UI ייחודי ל-Agent.

### Agent repository אחראי על

- reusable Agent Definition;
- business intent/scope/behavior;
- provided/required capabilities;
- Agent-specific prompts/workflows/adapters;
- Agent-specific evals/acceptance tests;
- AgentManifest requirements.

Agent repository אינו מחזיק Secrets, raw PII או Client-specific business state.

## 4. שני Planes בתוך Core

בשלב הראשון Core נשאר Repository/Project אחד, אך נשמר contract boundary בין שני Planes כדי לאפשר פיצול עתידי.

### Build / Control Plane

אחראי על:

- conversational Client Intent;
- Spec Compiler;
- Template Engine;
- AgentManifest ו-ClientInstanceConfig validation;
- Policy/Exception compilation;
- eval/release planning;
- EffectiveReleaseConfig generation;
- release/version metadata;
- Registry metadata/contracts.

### Runtime Governance Plane

אחראי על:

- Orchestrator + trusted ExecutionContext;
- PlatformPolicy enforcement;
- trust/risk decisions;
- Capability routing;
- Model/Provider routing;
- Tool Gateway;
- Memory Gateway;
- Budget/safety/runtime guards;
- approvals/escalations according to policy;
- audit/traces/runtime evidence;
- drift detection.

### Client Data Plane

מחזיק בפועל tenant-scoped data, knowledge, state, secrets, channels ו-audit/storage partitions.

## 5. ארבעת ה-artifacts של Release

```text
AgentManifest
        +
ClientInstanceConfig
        +
PlatformPolicy / ExceptionPolicy
        =
EffectiveReleaseConfig
```

### AgentManifest

Reusable declaration of what the Agent is and requires. It requests capabilities/permissions; it does not grant them.

### ClientInstanceConfig

Tenant/environment-specific grants, budget, trust level, data/memory/retention, channels, provider restrictions, credential references and release preferences.

### PlatformPolicy / ExceptionPolicy

PlatformPolicy defines ceilings, defaults, risk/trust behavior and non-overridable invariants. ExceptionPolicy is a scoped, versioned, expiring overlay only for rules classified as overridable.

### EffectiveReleaseConfig

Immutable compiled authority for one `agent_release_id`. Runtime executes this object, not raw Manifest/client drafts.

## 6. ExecutionContext

Every invocation receives trusted context such as:

```text
request_id
trace_id
tenant_id
actor_id / actor_type
environment
agent_id
agent_release_id
trust_level
effective_permissions
data_classification
budget_context
model_policy
tool_policy
memory_policy
deadline
```

Prompt/model output cannot modify authority.

## 7. Template-first, modular composition

A new Agent is not built from zero and is not forced into one rigid template.

```text
Spec
 + smallest suitable Base Template
 + required Capability Modules
 + Agent-specific assets
 = reusable Agent Definition
```

The Factory follows progressive complexity: choose the simplest composition that satisfies the business outcome and add autonomy/integrations/premium capabilities only when justified.

## 8. Hybrid orchestration and Agent autonomy

The Runtime Governance Plane sets boundaries. The business Agent can autonomously plan inside them.

The Agent may decide how to decompose a task, which approved capability to request, when more evidence is needed and how to replan after failure.

The Agent may not grant itself permission, widen tenant/data scope, disable safety/audit/budget controls or bypass a blocking policy decision.

## 9. Capability-based Agent-to-Agent routing

Agents request versioned capabilities, not peer URLs/repositories.

```text
Travel Agent requires: research.lookup
Core resolves: compatible Research Agent release
```

Registry behavior is soft-strict:

- sandbox/dev may warn or use mocks for optional/non-critical unresolved capabilities;
- production requires critical/consequential capabilities to be registered, compatible and policy-approved;
- security invariants remain blocking in all environments.

## 10. Provider/model independence

Agents request Model/Capability Profiles. Routing is policy-driven, not universally cheapest-first or quality-first.

Inputs include capability, privacy/data classification, trust level, budget, quality evals, latency, availability and client restrictions.

Provider/model change with compatible contract is a configuration + regression-eval change, not business-Agent rewrite.

## 11. Tool Gateway

Every governed Tool/API/MCP request passes typed schema, authorization, tenant binding, risk/side-effect classification, budget/preflight, approval when policy requires, timeout/retry/idempotency and audit.

External content is untrusted data, not authority.

## 12. Memory Gateway

Memory classes remain logically separated: session, task working state, user/client persistent memory, client knowledge, operational state and platform knowledge.

Agents may autonomously request/write useful memory when EffectiveReleaseConfig permits it. Policy decides whether the write is allowed, minimized/transformed, denied or requires consent/approval.

Client information is never silently promoted into platform knowledge.

## 13. Security and trust

Security is a platform invariant but approvals are risk-based, not universal.

PlatformPolicy defines Trust Profiles such as `sandbox`, `internal`, `business`, `privileged` and maps them to ceilings/defaults/evals/approvals.

Factory recommends a trust level from the Spec. Client may configure within the permitted ceiling. ExceptionPolicy can override only explicitly overridable rules. A future production gate will finalize the small set of non-overridable invariants.

## 14. Budget

Business budget and emergency safety cap are separate.

- business budget: warn/project/offer alternatives/approve overage according to policy;
- emergency safety cap: stops runaway loops/anomalies regardless of business overage approval.

Routing can optimize for economy, balance, quality, latency or privacy according to client/task policy.

## 15. Evals and Release

Evaluation families include functional/business, security/policy, cost/runtime and contract/portability.

Thresholds are policy-driven. Business score below a target may be blocking/warning/advisory depending on risk. Failure of a non-overridable security invariant blocks release.

Release strategy is versioned:

- `human-required`;
- `policy-auto`;
- `policy` (derive effective strategy from risk/trust/environment/change class).

Automatic release still generates the same evidence and release decision record.

## 16. Client experience

The client sees a technical black box but a transparent business contract. They see scope, assumptions, material services/data use, expected cost, limitations and required approvals.

Normal intake target: under 10 minutes, typically 5-6 critical questions. For ambiguous requests use `infer -> show assumptions -> confirm/correct`.

## 17. Release and drift

Every `agent_release_id` links to exact Spec, Manifest, ClientInstanceConfig, PlatformPolicy/ExceptionPolicy, EffectiveReleaseConfig, templates, contracts, eval evidence, release decision and rollback target.

Runtime drift from EffectiveReleaseConfig is detected and can block promotion or trigger remediation/suspension.

## 18. Core MVP boundary

First implementation proves only critical contracts:

- AgentManifest + ClientInstanceConfig schemas;
- compiler to EffectiveReleaseConfig;
- trusted ExecutionContext;
- PlatformPolicy/ExceptionPolicy evaluation;
- risk/trust + permission gate;
- budget precheck/safety cap;
- provider-neutral model adapter interface;
- soft-strict capability registration/resolution;
- Memory/Tool gateway interfaces;
- minimal audit/evidence/release decision schema;
- policy-driven eval/release gate.

No Kubernetes, service mesh, multi-region or distributed bus is required for MVP.

## 19. First reference Agent

After Core Skeleton, build Research/Brain Agent in a separate repository providing `research.lookup`. It selects among internal knowledge, Web, API, MCP, model knowledge and approved capabilities under policy, budget and provenance requirements.

Travel Agent is the first consumer to prove reusability and provider independence.