# K3.3-D3T Execution Evidence

## Status

- `evidence_id`: `af-ka-01-k3-3-d3t`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `result`: `smoke_pass_citation_contract_pass`
- `question_id`: `KA-E01`
- `model_requests`: `1`
- `technical_retries`: `0`
- `credits_before`: `42`
- `credits_after`: `36`
- `credit_delta`: `6`
- `publication_status`: `Unpublished`

## Authorization

The Owner authorized exactly one Preview request for KA-E01 under a six-Credit ceiling, with an immediate stop after the response and no retry, Indexing or Publish.

## Pre-run Drift Check

- Workspace tier: `Sandbox`.
- Model: `gpt-4.1-mini-2025-04-14`.
- Corpus: `af-demo-services-he@1.0.0`.
- Graph: `User Input → Knowledge Retrieval → Citation Context → LLM 2 → Answer 2`.
- Direct `Knowledge Retrieval → LLM 2` graph edge: absent.
- App: `Unpublished`.
- Available Credits: `42`.

## Frozen Request and Response

Question:

> באילו ימים ושעות הארגון פעיל?

Response:

> הארגון פעיל בימים ראשון עד חמישי, בין השעות 09:00 ל-17:00. הארגון סגור בימי שישי ושבת. ימים אלה אינם נחשבים לימי עסקים במדיניות הסינתטית [AFD-001 § שעות פעילות] [AFD-001 § ימי סגירה].

Dify also displayed native attribution to `AFD-001.md`.

## Verdicts

| Check | Verdict | Evidence |
|---|---|---|
| Hebrew-only answer | Pass | Response is entirely in Hebrew apart from approved identifiers and times |
| Factual grounding | Pass | Operating days, hours and closed days match `AFD-001.md` |
| Citation presence | Pass | Both material claims contain inline citations |
| Citation format | Pass | Both citations use `[SOURCE_ID § Section]` |
| Citation correctness | Pass | `שעות פעילות` and `ימי סגירה` are exact stable headings in `AFD-001.md` |
| External action safety | Pass | No Tool or external action was invoked |
| Request ceiling | Pass | Exactly one request and zero retries |
| Credit ceiling | Pass | Six-Credit delta, matching the approved ceiling |

This is a bounded smoke result only. It does not satisfy the frozen 25-question evaluation or authorize K4. At the measured six Credits per response, 25 questions would require approximately 150 Credits before technical retries; only 36 Sandbox Credits remain.

