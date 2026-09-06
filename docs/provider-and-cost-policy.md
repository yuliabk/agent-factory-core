# Provider, Model and Cost Policy

**Status:** Accepted direction after Owner Review

## 1. Goals

- avoid dependency on one provider/model;
- adapt to client budget without rebuilding the Agent;
- allow fast switching when price, quality or availability changes;
- select the best allowed option for the task rather than always prioritizing price or always prioritizing quality;
- make cost a first-class runtime control.

## 2. Policy-driven optimization

The platform does **not** use a universal `cheapest-first` or `quality-first` strategy.

Routing is selected by policy according to the client, task and risk context.

Example optimization profiles:

- `economy` - lowest acceptable cost for the required quality/risk floor;
- `balanced` - default trade-off among quality, cost and latency;
- `quality-first` - maximize validated quality within budget/policy;
- `latency-first` - prioritize response time within quality/privacy floor;
- `private-data-compatible` - provider/runtime constrained by data policy;
- `high-reasoning` - stronger reasoning capability when justified.

The client chooses outcomes/budget preferences in plain language. The Core maps them to technical routing policy.

## 3. No provider hard-code in business logic

An Agent requests a model/capability profile, not a concrete provider/model, unless an explicit approved exception or domain requirement fixes one.

Provider/model mapping belongs to Runtime Governance configuration and is versioned separately from Agent business logic.

## 4. Router inputs

The Model/Provider Router considers at least:

- required capability/features;
- data classification and trust level;
- ClientInstanceConfig restrictions;
- region/privacy/residency requirements;
- approved budget and projected cost;
- latency/SLA target;
- context length;
- eval quality/compatibility score;
- current provider health/rate limits;
- portability/fallback eligibility.

## 5. Fallback

Fallback is allowed only to implementations that satisfy the effective policy and passed required compatibility/regression evals.

Provider outage never authorizes sending data to an unapproved provider.

Fallback decisions are recorded in trace/audit.

## 6. Budget model

### Build budget

The Factory estimates build/evaluation cost and can offer business-readable alternatives. Human approval is required only when PlatformPolicy classifies the build spend/change as requiring approval.

### Client runtime budget

Business budget belongs to the client/Agent instance and is stored in ClientInstanceConfig / EffectiveReleaseConfig.

Default behavior is `warn-and-approve` rather than silent overrun or a rigid business kill switch.

### Emergency safety cap

Emergency safety cap is separate from business budget and exists to stop abnormal loops, recursion or anomalous spend. Business overage approval does not override it.

## 7. Budget checks

Every request receives a lightweight budget check. Expensive/composite operations receive preflight estimation where feasible.

Typical expensive operations include large web research, batch document processing, long-context work, multi-agent plans and high-cost media generation.

Thresholds are policy profiles, not universal constants. A default profile may use informational/warning/high-warning/preflight bands, but clients/workloads can use approved alternatives.

## 8. Overage flow

When an operation would cross an approved business limit:

1. estimate/project cost;
2. offer a cheaper approved alternative when available;
3. pause the new spend if policy requires;
4. request authorization from the effective runtime approver;
5. record amount/new limit, period, approver, timestamp, reason and expiry/review date.

## 9. Cost events

Cost/accounting event contains as available:

```text
request_id
trace_id
agent_id
agent_release_id
provider
model_or_implementation
operation_type
input_units
output_units
estimated_cost
actual_cost
currency
budget_bucket
policy_decision
approval_reference
```

Raw prompt content is not stored merely for cost accounting.

## 10. Client options

The Factory can present 2-3 understandable business options such as:

- economical;
- balanced/recommended;
- advanced/premium.

These are dynamic solution profiles, not permanent bindings to provider brands.

## 11. Provider/model change

A provider/model change requires the policy-defined combination of:

- compatibility/regression eval;
- quality comparison;
- cost comparison;
- privacy/data-policy check;
- tool/function compatibility;
- rollback target.

If the approved contract/profile is preserved, provider replacement should not require rewriting Agent business logic.