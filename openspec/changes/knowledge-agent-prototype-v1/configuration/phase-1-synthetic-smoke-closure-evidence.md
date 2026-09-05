# Phase 1 Synthetic Smoke Prototype Closure Evidence

## Status

- `evidence_id`: `af-ka-01-phase-1-smoke-closure`
- `version`: `1.0.0`
- `date`: `2026-08-24`
- `result`: `phase_1_synthetic_smoke_closed`
- `runtime`: `Dify Cloud Sandbox Preview`
- `question_id`: `KA-E01`
- `model_requests`: `1`
- `technical_retries`: `0`
- `last_recorded_pre_run_credits`: `36`
- `post_run_credits`: `unverified_not_visible_in_result_view`
- `credit_delta`: `unverified`
- `publication_status`: `Unpublished`
- `gate_g1_status`: `open_not_approved`
- `frozen_25_question_evaluation_status`: `open_not_executed`

## Authorization

The Owner authorized exactly one `KA-E01` Preview request under a six-Credit ceiling, with an immediate stop after the response and no retry, Indexing or Publish. After the result, the Owner separately approved local-only closure of Phase 1 as a `Synthetic Smoke Prototype`; no further Dify action, Runtime, Indexing, Publish, Commit or Push was authorized.

## Observed Configuration

The read-only pre-run check immediately preceding the request confirmed:

- graph: `User Input → Knowledge Retrieval → Citation Context → LLM 2 → Answer 2`;
- Template input: `Knowledge Retrieval / result` as `Array[Object]`;
- Template allow-list: `AFD-001` through `AFD-006`;
- citation metadata path: `item.metadata.doc_metadata.source_id`;
- LLM model: `gpt-4.1-mini-2025-04-14`;
- LLM prompt inputs: `Citation Context / output`, Retrieval Context and `User Input / query`;
- Dify Checklist: `All issues are resolved`;
- workflow state: `Auto-Saved` and `Unpublished`.

## Frozen Request and Response

Question:

> באילו ימים ושעות הארגון פעיל?

Response:

> הארגון פעיל מיום ראשון עד יום חמישי, בין השעות 09:00 ל-17:00. הוא סגור בימי שישי ושבת. ימים אלה אינם נחשבים כימי עסקים במדיניות הסינתטית [AFD-001 § שעות פעילות], [AFD-001 § ימי סגירה].

Dify reported `Workflow Process succeeded` and displayed native attribution to `AFD-001.md`.

## Verdicts

| Check | Verdict | Evidence |
|---|---|---|
| Request ceiling | Pass | Exactly one Preview request was submitted |
| Retry ceiling | Pass | No retry was attempted |
| Hebrew-only answer | Pass | The answer is Hebrew apart from approved identifiers and times |
| Factual grounding | Pass | Operating days, hours and closed days match `AFD-001` |
| Citation presence | Pass | Both material claims include inline citations |
| Citation format | Pass | Both citations use `[SOURCE_ID § Section]` |
| Citation correctness | Pass | Both Section names are exact stable headings in `AFD-001` |
| Native attribution | Pass | Dify displayed `AFD-001.md` |
| External action safety | Pass | No Tool or external action was observed |
| Publish exclusion | Pass | The workflow remained Unpublished |
| Credit ceiling evidence | Unverified | The result view did not expose post-run Credits; no value is inferred |

## Closure Boundary

Phase 1 is closed only as a bounded synthetic smoke prototype. This evidence proves one supported question on the persisted unpublished flow; it does not prove the unsupported, conflict, ambiguity, injection, isolation or full cost scenarios in the frozen 25-question set. Gate G1, K4 evaluation, Production, real data, external users, additional Runtime, Indexing and Publish remain open, blocked or unauthorized as applicable.
