# Citation Metadata Path Plan

## Status

- `plan_id`: `af-ka-01-citation-metadata-path`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `stage`: `K3.3-D3B`
- `status`: `local_plan_complete_implementation_not_authorized`
- `provider_changes`: `none`
- `runtime_requests`: `0`
- `credit_delta`: `0`

## Critical Finding

Dify's current Workflow UI exposes `Knowledge Retrieval / result` as `Array[Object]` and describes `metadata` only as an opaque object. The official backend source, however, constructs each internal Knowledge result with the document's custom metadata under `metadata.doc_metadata`. The Template node officially supports loops, nested object access, conditionals and defaults.

Therefore the source-backed candidate path for the approved custom field is:

```text
item.metadata.doc_metadata.source_id
```

This is stronger than an undocumented guess but remains unverified against the current hosted Dify build until an separately authorized Runtime validation occurs.

## Selected Configuration Design

The next configuration-only candidate is `M-DOCMETA-TEMPLATE`:

1. Keep `Knowledge Retrieval / result` as the Template input variable `results`.
2. Iterate over `results` in `Citation Context`.
3. Read `item.metadata.doc_metadata.source_id`.
4. Accept only the fixed allow-list `AFD-001` through `AFD-006`.
5. Derive the Section label from the first non-empty content line while preserving the complete Chunk content unchanged.
6. Emit no evidence block for missing or foreign metadata and emit a single `INSUFFICIENT_EVIDENCE` marker when no valid block remains.
7. Rewire the graph to `Start → Knowledge Retrieval → Citation Context → LLM 2 → Answer 2` while retaining the original Retrieval result as the LLM Context input for native Dify attribution.
8. Add the Template text output to the LLM instruction only through a verified manual variable chip; do not automate rich-text prompt editing.

## Approval-Ready Template Candidate

```jinja2
{% set allowed = ['AFD-001', 'AFD-002', 'AFD-003', 'AFD-004', 'AFD-005', 'AFD-006'] %}
{% set ns = namespace(valid=0) %}
{% for item in results %}
{% set sid = item.metadata.doc_metadata.source_id | default('') %}
{% if sid in allowed and item.content %}
{% set ns.valid = ns.valid + 1 %}
SOURCE_ID={{ sid }}
SECTION={{ item.content.split('\n')[0] | trim }}
CONTENT:
{{ item.content }}
---
{% endif %}
{% endfor %}
{% if ns.valid == 0 %}INSUFFICIENT_EVIDENCE{% endif %}
```

## Fail-Closed Rules

- Missing `metadata`, `doc_metadata`, `source_id` or `content` SHALL NOT create a citation block.
- A `source_id` outside the six-value allow-list SHALL NOT be passed to the LLM.
- The template output SHALL NOT replace Dify's native Retrieval Context until the graph and both variable bindings are reload-verified.
- Any Template error, empty output, model drift, Credit decrease, unexpected Tool, or publication state SHALL stop the stage.
- No Code node, external API, Tool, reindexing or corpus rewrite is selected.

## Options Rejected

| Option | Decision | Reason |
|---|---|---|
| Guess `metadata.source_id` | rejected | Contradicts observed Dify structure and fail-closed policy. |
| Code node | rejected | Adds executable logic and a wider security surface without necessity. |
| Corpus 1.1.0 reindex | rejected | High Credit cost and duplicates metadata already stored by Dify. |
| Use only `document_name` | fallback only | Deterministic but does not satisfy the approved `SOURCE_ID` contract without an explicit filename mapping. |
| Roll back `Citation Context` now | deferred | The isolated branch is inert and useful for the approved next configuration stage. |

## Evidence Sources

- [Dify Template node](https://docs.dify.ai/en/cloud/use-dify/nodes/template): nested properties, arrays, loops, conditionals and defaults are supported.
- [Dify Knowledge Retrieval node](https://docs.dify.ai/en/cloud/use-dify/nodes/knowledge-retrieval): `result` is an array containing content, metadata, title and other attributes.
- [Dify retrieval implementation](https://github.com/langgenius/dify/blob/main/api/core/rag/retrieval/dataset_retrieval.py): internal Knowledge results set `doc_metadata=document.doc_metadata` in `SourceMetadata`.
- [Dify Workflow UI implementation](https://github.com/langgenius/dify/blob/main/web/app/components/workflow/nodes/knowledge-retrieval/panel.tsx): the picker exposes `metadata` as an object but does not enumerate its nested keys.

## Next Gate

`K3.3-D3S` may be approved separately for configuration only: replace `{{ results }}` with the reviewed fail-closed template, manually rewire `Citation Context` between Retrieval and LLM, insert only the verified Template output variable chip, reload-verify and stop. It includes no Preview, step run, Retrieval Test, Model call, Indexing, Publish, Code node or expected Credit use.

