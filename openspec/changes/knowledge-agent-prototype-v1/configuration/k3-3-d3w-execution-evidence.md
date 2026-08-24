# K3.3-D3W Execution Evidence

## Status

- `evidence_id`: `af-ka-01-k3-3-d3w`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `result`: `complete_reload_verified`
- `runtime_requests`: `0`
- `indexing_operations`: `0`
- `credits_before`: `42`
- `credits_after`: `42`
- `credit_delta`: `0`
- `publication_status`: `Unpublished`

## Authorization

The Owner authorized only the following bounded configuration change: connect `Citation Context` to `LLM 2`, remove the direct `Knowledge Retrieval → LLM 2` graph edge, and update the LLM prompt to consume deterministic evidence and `source_id`. Preview, Runtime, Indexing and Publish were explicitly excluded.

## Preconditions

- Before D3SR, the Owner confirmed that the Template had been pasted and that Preview/Run had also been invoked. That response was the canonical insufficient-evidence fallback. The subsequent read-only Credit check showed a six-Credit decrease from 48 to 42; no repeat was performed.
- D3SR read-only verification confirmed the complete fail-closed Template after the Owner's manual paste.
- `results` remained bound to `Knowledge Retrieval / result` as `array[object]`.
- The Template used `item.metadata.doc_metadata.source_id`, the fixed allow-list `AFD-001`–`AFD-006`, and the `INSUFFICIENT_EVIDENCE` fallback.
- The app was `Unpublished` and 42 Credits were available.

## Persisted Configuration

Reload verification confirmed the final graph:

`User Input → Knowledge Retrieval → Citation Context → LLM 2 → Answer 2`

The direct graph edge `Knowledge Retrieval → LLM 2` was removed. The separate `Knowledge Retrieval / result` binding remains in the LLM Context for Dify native attribution.

The LLM System message now contains a structured `Citation Context / output` variable chip and a superseding instruction that this output is the only source for inline `SOURCE_ID` and `Section` values. Missing or invalid Template evidence requires the approved insufficient-evidence response.

## Recovery Note

While selecting the direct graph edge, Dify retained the Template node selection and temporarily deleted `Citation Context`. One immediate Undo restored the node and both of its intended edges. The correct direct Retrieval-to-LLM edge was then selected and removed. A subsequent Reload verified five nodes, four intended edges, the structured prompt variable, `Unpublished` state and no Credit change.

No Preview, step run, Retrieval Test, model call, Indexing, document change, Publish, Tool, Credential, Payment or Workspace change occurred.
