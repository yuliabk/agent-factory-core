# P0 — Runtime Adapter Contract

## Status and Boundary

Status: PR-G1 local validation contract implemented. The implementation validates declarations and synthetic fixtures only; it contains no provider adapter, credential, endpoint, account, or provider configuration.

## Contract Identity

Every adapter package MUST declare:

| Field | Meaning |
|---|---|
| `adapter_id` | Stable identifier, for example `botpress-v1` |
| `adapter_version` | SemVer version of the mapping contract |
| `runtime` | Provider/runtime name |
| `runtime_plan` | Intended plan or deployment class |
| `configuration_version` | Immutable provider-configuration reference |
| `agent_release_id` | Approved canonical Agent Factory release |
| `corpus_version` | Approved corpus manifest version |
| `question_set_version` | Frozen evaluation-set version |

An identity mismatch or mutable/unknown version blocks preflight.

## Capability Declaration

Each capability has `supported`, `evidence`, `limitations`, and `verified_at` fields. Required capabilities are:

- knowledge retrieval and metadata preservation;
- `source_id` and section provenance;
- Hebrew prompt and response handling;
- deterministic fallback routing;
- external-action/tool suppression;
- run-level logs and usage evidence;
- provider-native spend or usage stop;
- configuration export and reconstruction;
- data deletion and retention controls;
- client/runtime isolation.

`unknown` is not equivalent to `supported`; a required `unknown` value fails closed.

## Normalized Request

The adapter maps the canonical request without changing its meaning:

```yaml
request_id: string
agent_release_id: string
question_set_version: string
question_id: string
locale: he-IL
query_he: string
approved_corpus_version: string
max_retrieval_items: integer
tool_policy: deny_all
```

Provider-only optional settings remain in an isolated `provider_options` record and cannot override canonical policy.

## Normalized Evidence

```yaml
run_id: string
attempt: integer
adapter_id: string
provider_run_ref: string-or-redacted
retrieved_items:
  - source_id: string
    section_id: string
    provider_item_ref: string-or-redacted
    score: number-or-null
latency_ms: integer-or-null
usage:
  native_unit: string
  native_quantity: number
  native_cost: number-or-null
  native_currency: string-or-null
normalized_cost:
  amount_ils: number-or-null
  conversion_source: string-or-null
  conversion_timestamp: string-or-null
  confidence: verified-or-estimated-or-unknown
drift:
  detected: boolean
  details: array
```

Unknown data remains `null` or `unknown`; the adapter MUST NOT infer zero cost or fabricate retrieval evidence.

## Normalized Response

```yaml
response_type: answer-or-fallback-or-policy_block-or-runtime_error
answer_he: string
citations:
  - source_id: string
    section_id: string
    support: direct-or-partial
policy_result: allowed-or-blocked-or-unknown
tool_calls: []
```

Every answer citation MUST resolve to a retrieved item from the approved corpus version. Unsupported or unresolved citations cause the evaluation verdict to fail. Any non-empty `tool_calls` value is a policy failure.

## Contract Operations

| Operation | Responsibility |
|---|---|
| `validate_config` | Implemented locally for identity, schema, versions, and declared settings |
| `preflight` | Implemented locally for declared capabilities, isolation, fixtures, and ceilings; provider evidence remains PR-G2 |
| `map_request` | Contract validation implemented; provider translation remains PR-G2 |
| `map_evidence` | Synthetic fixture validation implemented; provider mapping remains PR-G2 |
| `map_response` | Normalized answer/citation validation implemented; generation is absent |
| `read_usage` | Synthetic usage/cost validation implemented; provider reading remains PR-G2 |
| `export_config` | Secret-field rejection implemented; provider export remains PR-G2 |

## Fail-Closed Conditions

Preflight or evaluation stops when any of the following is true:

- canonical or adapter versions are missing or drifted;
- a required capability is unsupported or unverified;
- credentials, storage, logs, indexes, or configuration are shared across clients;
- synthetic-data scope cannot be enforced;
- citation provenance cannot be resolved to `source_id` and section;
- external actions cannot be disabled;
- provider-native usage/spend limits cannot be enforced;
- cost or usage cannot be measured with an approved conservative fallback;
- configuration export, data deletion, or evidence retention is undefined.
