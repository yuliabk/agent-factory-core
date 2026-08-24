# K3.3-B2 Execution Evidence — Knowledge Link and Linear Graph

## Status

- `evidence_id`: `af-ka-01-k3-3-b2`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `result`: `complete`
- `knowledge_base`: `af-demo-services-he-1-0-0`
- `credits_before`: `180 available`
- `credits_after`: `180 available`
- `actual_credit_delta`: `0`
- `model_calls`: `0`

## Persisted Configuration Evidence

Dify persisted exactly four nodes and three directed edges after an explicit page reload and the asynchronous Knowledge data load:

`Start → Knowledge Retrieval → LLM → Answer`

The Knowledge Retrieval node displays only `af-demo-services-he-1-0-0`. The downstream LLM uses `gpt-4.1-mini-2025-04-14`, receives the Retrieval `result` as context, includes the Owner-approved Hebrew-only grounded-answer and insufficient-evidence instructions, and passes its `text` output to the terminal Answer node.

Dify's next-step UI created replacement LLM and Answer nodes to form the linear path; the formerly disconnected LLM/Answer pair was removed. Node titles remain `LLM 2` and `Answer 2`, while their node types and roles are LLM and Answer respectively.

## Stop Confirmation

- The App remains `Unpublished` and Auto-Saved.
- No Preview, Retrieval Test, step run, App run or generation request occurred.
- No Upload, Indexing, additional document, Tool, Credential, Payment or Workspace change occurred.
- Credit usage remained `20 / 200 used`, with 180 Credits available.

## Next Decision

Stage B2 authorization is consumed. The smallest planned next decision is K3.3-C for the remaining five approved synthetic documents, one at a time, under the measured 100-Credit forecast and the existing 50-Credit reserve rule. Stage C is not authorized by this evidence.
