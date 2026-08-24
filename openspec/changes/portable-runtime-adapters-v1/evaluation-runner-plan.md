# P1 — Evaluation Runner Plan

## Status and Initial Boundary

Status: PR-G1 implemented and validated locally. The runner uses no network, model, provider, credentials, indexing, or payment access. It validates fixtures and contracts and does not answer the questions.

## Objectives

- Validate adapter declarations against the P0 contract.
- Load the frozen 25-question set and approved expected-result metadata.
- Validate normalized answer, citation, fallback, policy, evidence, usage, and cost fixtures.
- Produce deterministic machine-readable and human-readable verdicts.
- Prevent live execution until a separate PR-G2 authorization exists.

## Planned Lifecycle

```text
planned -> preflight_passed -> authorized -> running -> completed
                                   |           |
                                   |           -> stopped
                                   -> authorization_expired
```

The local runner may reach only `planned` and `preflight_passed`. `authorized` requires a signed/recorded PR-G2 gate external to this implementation. A changed configuration, adapter, corpus, question set, or ceiling creates a new deterministic dry-run identity.

## Planned Inputs

- approved release and corpus manifests;
- adapter declaration and mapping;
- frozen 25-question evaluation set;
- expected answer/fallback classification and allowed sources;
- synthetic normalized evidence fixtures;
- provider-native and normalized cost ceilings;
- explicit retry allowance.

## Planned Checks

1. Schema and immutable-version validation.
2. Exactly 25 primary question identifiers, with no duplicates.
3. At most five separately identified technical retries; never automatic or hidden.
4. Hebrew answer or approved Hebrew fallback classification.
5. Citation resolution to retrieved `source_id` and section evidence.
6. No citations on fallback responses unless the fallback itself is sourced by policy.
7. Empty `tool_calls` and no external-action evidence.
8. Provider-native usage preservation and traceable normalized cost estimate.
9. Stop before a ceiling breach; unknown cost is a blocking verdict.
10. Immutable evidence output tied to the exact configuration and run identity.

## Planned Evidence Record

Each attempt records `run_id`, `question_id`, `attempt`, timestamps, adapter/runtime identity, configuration hashes or immutable references, normalized request/response/evidence, rule verdicts, native usage, normalized cost, and stop reason. Raw provider evidence, in a future live gate, is referenced rather than copied when copying would expose sensitive content.

## Verdicts

- `pass`: all required behavior and evidence are present.
- `fail`: a requirement is violated.
- `blocked`: required evidence, capability, authorization, or cost control is absent.
- `not_run`: no execution occurred.

For PR-G1 all runtime cases remain `not_run`.

## Future Live-Run Stop Conditions

A future separately approved live runner stops immediately on authorization mismatch, configuration drift, non-synthetic data, non-empty tool calls, unresolved citation provenance, provider error that threatens retry limits, provider-native ceiling approach, normalized ceiling approach, or inability to read current usage.
