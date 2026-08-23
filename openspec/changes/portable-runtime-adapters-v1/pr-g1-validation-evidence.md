# PR-G1 Local Validation Evidence

## Authorization

- **Gate:** PR-G1
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Scope:** Local Validator and Dry Evaluation Runner using synthetic data only.
- **Excluded:** Network, models, providers, Runtime, credentials, Indexing, payment, Publish, Commit, and Push.

## Implemented Artifacts

- `tools/runtime_portability/validator.py`: deterministic adapter, question-set, evidence, citation, policy, isolation, secret-field, drift, usage, and cost validation.
- `tools/runtime_portability/cli.py`: local-path-only JSON CLI with no live mode.
- `tests/fixtures/runtime_portability/`: one offline adapter declaration, the frozen 25-question set, and three synthetic evidence fixtures.
- `tests/runtime_portability/test_validator.py`: success and fail-closed tests.

## Verification Result

Date: 2026-08-21

```text
python -B -m unittest discover -s tests -v
Ran 13 tests
OK
```

The valid CLI fixture run returned:

| Field | Result |
|---|---:|
| `overall_verdict` | `pass` |
| `lifecycle_state` | `preflight_passed` |
| `external_calls` | `0` |
| `runtime_questions_executed` | `0` |
| question records | `25`, all `not_run` |
| fixture results | `3` passed |
| native synthetic quantity | `3` |
| normalized synthetic cost | `0 ILS` |

The tests cover duplicate questions, malformed drift, non-empty tool calls, provider-option policy override, deterministic output, canonical release drift, secret-bearing fields, unknown capabilities, unknown cost, unresolved citations, ceiling breach, and successful validation while sockets are disabled.

## Decision

PR-G1 local implementation and validation are complete. This evidence does not authorize PR-G2, a provider preflight, a provider account, credentials, data upload, Indexing, Runtime, payment, or publication.
