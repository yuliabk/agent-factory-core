# K3.3-D2 Execution Evidence

## Scope and Result

- `stage`: `K3.3-D2`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of K3.3-D2 immediately after the exact bounded wording was presented`
- `authorized_question`: `KA-E01`
- `result`: `completed_one_request_citation_contract_failed`
- `model_requests_completed`: `1`
- `technical_retries`: `0`
- `credits_before`: `54`
- `credits_after`: `48`
- `credit_delta`: `6`
- `app_status`: `Unpublished`

## Pre-run Drift Check

- Workspace was Sandbox with 54 Credits.
- The recovered System prompt and both structured bindings were present.
- Knowledge Retrieval was linked to `af-demo-services-he-1-0-0`.
- The generation model was `gpt-4.1-mini-2025-04-14`.
- The four-node graph was unchanged and the app was Unpublished.

## KA-E01 Result

- Question: `באילו ימים ושעות הארגון פעיל?`
- Answer: `הארגון פעיל בימים ראשון עד חמישי, בין השעות 09:00 ל-17:00. הוא סגור בימי שישי ושבת, וימים אלה אינם נחשבים לימי עסקים במדיניות הארגון [שעות פעילות].`
- Factual verdict: `pass`
- Hebrew verdict: `pass`
- Grounding UI: `AFD-001.md` displayed as the Dify citation source.
- Citation-contract verdict: `fail`
- Expected citation: `[AFD-001 § שעות פעילות]`
- Actual inline citation: `[שעות פעילות]`

The remediation improved the citation from a numeric Chunk reference to a stable Section heading, but the response still omitted the required frontmatter `source_id`. No retry was permitted or attempted.

## Stop Decision

Stage D2 expired after the single authorized response. The exact six-Credit ceiling was consumed and the approved 48-Credit reserve was reached. No additional Runtime, Preview, Publish or configuration change is authorized.
