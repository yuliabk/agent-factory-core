# PF-S Local Dry Validation Evidence

## Status

- `validation_id`: `pf-s-local-dry-2026-08-24`
- `release_id`: `pf-s-af-demo-retail@0.1.0-dry`
- `evaluation_set_version`: `pf-s-service-he@1.0.0`
- `result`: `pass`
- `evidence_state`: `dry_validated`
- `validation_mode`: `local_json_schema_and_deterministic_invariants`
- `network_calls`: `0`
- `provider_requests`: `0`
- `model_requests`: `0`
- `authorized_cost_ils`: `0`
- `external_messages`: `0`
- `tickets_created`: `0`

## Validated Inputs

- five JSON Schemas for request, response, audit, cases and evaluation set;
- six versioned synthetic Service cases;
- thirteen frozen `CS-*` scenarios;
- three minimized audit fixtures;
- four approved synthetic policy sources with stable identifiers;
- tenant, classification, locale, request ceiling and cost invariants.

## Results

| Check | Result |
|---|---|
| JSON parsing and Schema validation | Pass |
| Unique scenario identifiers | Pass — `13/13` unique |
| Minimum scenario count | Pass — `13 >= 10` |
| Functional success coverage | Pass — `3` scenarios |
| Missing-information coverage | Pass |
| Conflict/ambiguity coverage | Pass |
| Prompt Injection coverage | Pass |
| Cross-tenant coverage | Pass |
| Unauthorized-action coverage | Pass |
| Dependency-failure coverage | Pass |
| Cost-stop coverage | Pass |
| Sensitive-data coverage | Pass |
| Tenant consistency | Pass — all envelopes and expected outputs use `af-demo-retail` |
| External actions empty | Pass — `13/13` |
| Messages not sent | Pass — `13/13` |
| Tickets not created | Pass — `13/13` |
| Provider request ceiling | Pass — `0` |
| Authorized cost | Pass — `0 ILS` |

## Validation Notes

Two setup attempts stopped before fixture validation: the first used a relative path that could not become a file URI, and the second exposed a relative `$ref` under a URN schema identifier. The schema references were corrected to their full contract URNs. A subsequent shell interpolation issue was corrected in the validation command. The final deterministic validation then passed all schemas and invariants. None of these attempts accessed a network or provider.

The local environment emitted a deprecation warning for `jsonschema.RefResolver`; this does not invalidate the result, but a future reusable validator should migrate to the `referencing` registry API before the deprecated interface is removed.

## Evidence Boundary

This result proves the local artifact structure and deterministic expected decisions only. It does not execute classification, Retrieval, generation, escalation, messaging or Ticket behavior. `PF-G2-S`, provider mapping, Runtime, model quality and release approval remain unauthorized and unproven.
