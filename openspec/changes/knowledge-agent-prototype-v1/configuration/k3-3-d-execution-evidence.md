# K3.3-D Execution Evidence

## Scope and Stop Result

- `stage`: `K3.3-D`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of the exact bounded K3.3-D wording presented immediately before approval`
- `authorized_questions`: `KA-E01, KA-E16, KA-E18, KA-E22, KA-E24`
- `result`: `stopped_after_first_question_on_cost_and_citation_drift`
- `model_requests_completed`: `1`
- `technical_retries_consuming_credits`: `0`
- `questions_not_run`: `KA-E16, KA-E18, KA-E22, KA-E24`
- `credits_before`: `60`
- `credits_after`: `54`
- `measured_credit_delta`: `6`
- `forecast_credit_delta_per_question`: `1`
- `minimum_required_remaining`: `50`

## Pre-run Drift Check

- Workspace remained Sandbox with no visible Paid quota.
- App remained Unpublished.
- The four-node graph and `gpt-4.1-mini-2025-04-14` remained present.
- After a full reload and explicit node selection, `af-demo-services-he-1-0-0` was confirmed linked to Knowledge Retrieval.

## KA-E01 Result

- Question: `באילו ימים ושעות הארגון פעיל?`
- Result summary: correctly answered Sunday through Thursday, 09:00–17:00, and also stated the supported Friday/Saturday closure.
- Grounding: Dify displayed `AFD-001.md` as the citation source.
- `factual_verdict`: `pass`
- `citation_presence_verdict`: `pass_provider_visible`
- `citation_contract_verdict`: `fail`
- Observed citation text: `[AFD-001.md § 1][AFD-001.md § 3]`
- Required citation form: `[AFD-001 § שעות פעילות]`
- Overall smoke verdict: `fail_requires_versioned_remediation`

One UI submission attempt failed before dispatch. Dify produced no Log and no Credit delta for that attempt, so it was not counted as a Model request. The successful Enter submission produced the single measured response.

## Stop Decision

The first successful question consumed 6 Credits rather than the forecast 1. Only 4 Credits remained above the approved 50-Credit reserve, so another comparable question could have violated the reserve. Execution stopped before KA-E16. No retry, further question, Publish, Tool, Credential, Payment or Workspace change occurred.
