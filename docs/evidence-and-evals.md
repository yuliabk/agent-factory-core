# Evidence, Evals, Release Decisions and Audit

**Status:** Accepted direction after Owner Review

## Purpose

Every important Agent release should be explainable and reproducible. Evidence, evaluations, release decisions/approvals and audit are first-class artifacts.

The system does not use one universal quality threshold or one universal human-approval rule. PlatformPolicy maps risk, trust level, environment, domain and change class to the required evals and blocking behavior.

## Build / Release Evidence Pack

A release evidence pack references at least:

- approved OpenSpec change;
- AgentManifest and ClientInstanceConfig versions;
- EffectiveReleaseConfig;
- PlatformPolicy and ExceptionPolicy references;
- template/module versions;
- permission/trust/data-policy diff;
- model/provider profile;
- tool/capability contracts;
- evaluation results;
- known limitations;
- release decision/approval record;
- rollback target.

It stores hashes/references instead of secrets or unnecessary raw client data.

## Evaluation families

### Functional / business quality

Does the Agent meet its approved business contract and success criteria?

Business-quality thresholds are policy-driven. A score such as 80% versus 90% is not inherently blocking unless the effective policy says so.

### Security / policy

Includes prompt injection, permission bypass, data leakage, cross-tenant access, unsafe tool use, approval replay, exception misuse and agent-hop abuse.

Failures of non-overridable security invariants are always blocking.

### Cost / runtime

Checks normal spend envelope, preflight behavior, retries, loops, agent hops and emergency safety cap behavior.

### Contract / portability

Used when changing provider/model/runtime/capability implementation to verify the business contract is preserved.

### Domain / client acceptance

Optional or mandatory according to the specification and risk profile. The first executable Core Skeleton keeps the canonical `EvalResult` family vocabulary to the four required CORE-212 families above; domain/client acceptance can later be represented by a dedicated approved check/family extension when a real use case requires it.

## Canonical EvalResult v1

The first executable `EvalResult` is a decision-neutral fact record. It contains:

- `evalId`;
- `releaseId`;
- `checkId` and `checkVersion`;
- one of the four required evaluation families;
- raw status `PASS`, `PASS_WITH_WARNINGS` or `FAIL`;
- a short summary;
- flat scalar metrics;
- unique evidence references;
- observation timestamp.

It intentionally does **not** contain `blocking`, `warning`, `advisory`, release eligibility, approval state or a release decision. Those meanings are applied later by PlatformPolicy and the release kernel.

Canonical sources:

- external contract: `schemas/eval-result.schema.json`;
- Python projection: `agent_factory_core/contracts/eval_result.py`;
- alignment/negative tests: `tests/contracts/test_eval_result_contract.py`.

## Eval decision model

Each check produces a raw status:

```text
PASS
PASS_WITH_WARNINGS
FAIL
```

PlatformPolicy then maps checks to:

- `blocking`;
- `warning`;
- `advisory`.

Therefore a lower business-quality score may still release under an approved policy, while a critical security failure remains blocked.

## Release strategies

Effective release strategy is compiled into EffectiveReleaseConfig:

- `human-required` - exact release requires a human approval;
- `policy-auto` - release may proceed automatically after all blocking gates pass;
- `policy` - PlatformPolicy selects the effective mode.

Automatic release produces the same evidence and release decision record as a human-approved release. It is not an unlogged bypass.

## Human Approval Record

When human approval is required, record:

```text
approval_id
approver_id
approver_role
scope
action_or_release_reference
request_id / release_id
policy_version
exception_refs[]
decision
timestamp
expiry
comment
```

Approval is bound to the exact version/action and scope.

## Automated Release Decision Record

For `policy-auto`, record at least:

```text
release_decision_id
release_id
policy_version
strategy
blocking_checks_passed
warnings[]
exception_refs[]
timestamp
result
```

## Audit Bundle

For consequential runtime work, an Audit Bundle can reference:

- request/trace identifiers;
- release and policy versions;
- trust level and exceptions used;
- capability/tool decisions;
- evidence/provenance references;
- model profile/provider used;
- eval/release-decision/approval references when applicable;
- cost/usage events;
- final result hash/status.

Raw prompts, secrets and full sensitive provider payloads are excluded by default.

## Fast paths

Compatible low-risk changes may use a regression fast path if policy allows. Fast path reduces process overhead, not safety invariants: required checks still run and the exact released configuration remains reconstructable.
