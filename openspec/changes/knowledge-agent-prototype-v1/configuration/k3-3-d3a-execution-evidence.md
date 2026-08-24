# K3.3-D3A Execution Evidence

## Status

- `evidence_id`: `af-ka-01-k3-3-d3a`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `result`: `partial_safe_stop_visible_metadata_path_unavailable`
- `runtime_requests`: `0`
- `indexing_operations`: `0`
- `credits_before`: `48`
- `credits_after`: `48`
- `credit_delta`: `0`
- `publication_status`: `Unpublished`

## Completed Configuration

- Created one custom Knowledge metadata field named `source_id` with type `string`.
- Assigned and saved six values: `AFD-001` through `AFD-006`, matching `AFD-001.md` through `AFD-006.md`.
- Reload verification showed `source_id`, type `string`, with `6 Values`.
- Added one Template node named `Citation Context`.
- Connected `Knowledge Retrieval` to `Citation Context` as a parallel downstream branch while retaining the original `Knowledge Retrieval → LLM 2` edge for native Dify attribution.
- Bound the only relevant field exposed by the variable picker: `Knowledge Retrieval / result`, type `array[object]`, to input variable `results`.
- Retained the non-guessing template `{{ results }}`.
- Reload verification showed exactly five nodes: Start, Knowledge Retrieval, LLM 2, Answer 2 and Citation Context; the new edge persisted.

## Safe Stop

Dify exposed the Retrieval result only as the whole `array[object]`; it did not expose `metadata.source_id`, `document_name` or another nested document-metadata path as a selectable field. The approved fail-closed rule therefore prevented guessing a Jinja object path or editing the LLM prompt to consume an unverified template output. `Citation Context` is configured and connected to Retrieval, but it remains a parallel branch and is not yet an upstream input to `LLM 2`.

No Preview, step run, Model call, Retrieval Test, Indexing, document-content change, Publish, Code node, Tool, Credential, Payment or Workspace change occurred.

## Next Decision Boundary

Runtime remains blocked. A later stage requires a separate Owner decision for one of these bounded options:

1. manual UI wiring after Dify exposes a verified nested metadata path;
2. a versioned provider-supported transformation that does not guess fields; or
3. rollback of the unused `Citation Context` branch while retaining the six document metadata values.

