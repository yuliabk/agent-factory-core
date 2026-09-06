# Evidence, Evals, Human Approval and Audit

**Status:** Proposed

## Purpose

Every important agent release should be explainable and reproducible. The Core therefore treats evidence, evaluations, approvals and audit as first-class release/runtime artifacts.

## Build/Release Evidence Pack

A release evidence pack references at least:

- approved OpenSpec change;
- Manifest and template versions;
- permission and policy diff;
- model/provider profile;
- tool/capability contracts;
- functional eval result;
- security eval result;
- cost eval/estimate;
- known limitations;
- rollback target.

It stores references/hashes instead of secrets or unnecessary raw client data.

## Evaluation families

### Functional

Does the agent meet its approved business contract?

### Security

Includes prompt injection, permission bypass, data leakage, cross-tenant, unsafe tool use, approval replay and agent-hop abuse.

### Cost

Checks normal spend envelope, expensive-operation preflight, retries, loops and emergency safety cap behavior.

### Contract/portability

Used when changing provider/model/runtime/capability implementation to verify behavior remains within the contract.

## Human Approval Record

A protected decision records:

```text
approval_id
approver_id
approver_role
scope
action_or_release_reference
request_id / release_id
policy_version
decision
timestamp
expiry
comment
```

Approval is bound to the exact version/action. A changed release or material action requires fresh approval.

## Audit Bundle

For consequential runtime work, an Audit Bundle can reference:

- request/trace identifiers;
- release and policy versions;
- capability/tool decisions;
- evidence/provenance references;
- model profile and provider used;
- eval/approval references when applicable;
- cost/usage events;
- final result hash/status.

Raw prompts, secrets and full sensitive provider payloads are excluded by default.
