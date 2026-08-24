# Citation Remediation Plan

## Metadata

- `plan_id`: `af-ka-01-citation-remediation`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `status`: `approval_ready_local_only`
- `selected_candidate`: `M-TEMPLATE`
- `provider_changes_authorized`: `no`
- `runtime_authorized`: `no`
- `credits_remaining`: `48`

## Problem Statement

D2 proved that the model can answer KA-E01 factually and identify the stable Section heading, but it cannot produce `[SOURCE_ID § Section]` because the retrieved Section Chunk omits frontmatter `source_id`. D3R confirmed that Dify separately retains and displays `AFD-001.md` in its citation UI.

## Verified Dify Capabilities

- The Knowledge Retrieval node outputs `result` as an array of document Chunks containing content, metadata, title and other attributes: https://docs.dify.ai/en/cloud/use-dify/nodes/knowledge-retrieval
- A Template node can iterate over arrays and access nested object properties using Jinja2, without an LLM call: https://docs.dify.ai/en/cloud/use-dify/nodes/template
- A Code node can receive upstream objects and arrays and transform them in an isolated sandbox with no file, network or system-command access: https://docs.dify.ai/en/cloud/use-dify/nodes/code
- Dify supports document-level custom metadata and built-in `document_name`: https://docs.dify.ai/en/cloud/use-dify/knowledge/metadata
- The Knowledge API retrieval response demonstrates that a retrieved segment retains its parent document name and metadata: https://docs.dify.ai/en/api-reference/knowledge-bases/retrieve-chunks-from-a-knowledge-base-test-retrieval

These documents establish capability, not the exact field path exposed by the current Cloud UI. The implementation Stage SHALL verify the selectable field path without a Runtime request and SHALL stop if it is unavailable.

## Candidate Comparison

| Candidate | Design | Model/Indexing cost | Complexity | Portability | Decision |
|---|---|---:|---|---|---|
| `M-TEMPLATE` | Add document metadata `source_id`; use a Template node to enrich each retrieved Chunk before the LLM | 0 expected for configuration | Low-Code | Medium | **Selected** |
| `M-CODE` | Normalize Retrieval result objects in a Code node | 0 expected for configuration | Custom code and schema coupling | Medium-low | Fallback only if Template cannot access the required fields |
| `C-1.1` | Create Corpus 1.1.0 with `source_id` repeated inside every Section and reindex | Six-document reindexing previously measured at 140 Credits | Content duplication and corpus migration | High | Deferred; current 48-Credit balance cannot support measured reindexing |
| `RELAX` | Accept Dify's native filename citation or `[Section]` | 0 | Lowest | Low | Rejected because it weakens KA-103 and evaluation traceability |

## Selected Design: M-TEMPLATE

### Configuration Delta

1. Create one Knowledge metadata field named `source_id`, type String.
2. Assign exactly one approved value to each existing document: `AFD-001` through `AFD-006`.
3. Add one Template node named `Citation Context` after Knowledge Retrieval.
4. Bind `Knowledge Retrieval / result` as the Template input.
5. Render each result as an explicit evidence block containing:
   - `SOURCE_ID` from document metadata;
   - `SECTION` from the first stable heading line of the Chunk content;
   - the unmodified Chunk content.
6. Keep the original Knowledge Retrieval `result` connected to the LLM Context so Dify's native citation UI remains available.
7. Add `Citation Context / output` to the LLM System message as the only source for constructing inline `[SOURCE_ID § Section]` citations.
8. Keep Answer bound only to the LLM text output.

Target flow:

`User Input → Knowledge Retrieval → Citation Context (Template) → LLM → Answer`

The Retrieval result also remains bound directly to the LLM Context for native attribution. No Tool, HTTP, Agent, external call or Credential is introduced.

### Fail-closed Rules

- If `source_id` is missing, not one of `AFD-001`–`AFD-006`, or cannot be selected from the Retrieval result, configuration SHALL stop before any Runtime.
- If a Chunk does not expose a stable Section heading, the Template SHALL mark the evidence invalid and the LLM SHALL use the insufficient-evidence response for claims dependent on it.
- The Template SHALL preserve the original Chunk content and SHALL NOT invent or infer a source identifier.
- Duplicate results SHALL NOT create contradictory identifiers for the same document and Section.
- Retry remains disabled for the Template node.

### Illustrative Template Contract

This is a planning contract, not an approved provider implementation:

```jinja2
{% for item in results %}
SOURCE_ID={{ item.metadata.source_id | default('MISSING_SOURCE_ID') }}
SECTION={{ item.content.split('\n')[0] | trim }}
CONTENT:
{{ item.content }}
{% endfor %}
```

The exact object path SHALL be selected from Dify's visible variable schema during an approved configuration-only Stage; no guessed field path may be saved silently.

## Acceptance Scenarios

### Exact citation context

- GIVEN a retrieved Chunk belongs to document metadata `source_id = AFD-001` and begins with Section `שעות פעילות`
- WHEN Citation Context formats the Chunk
- THEN its deterministic evidence header SHALL be `SOURCE_ID=AFD-001` and `SECTION=שעות פעילות`

### Missing metadata

- GIVEN a retrieved Chunk has no approved `source_id`
- WHEN Citation Context processes the result
- THEN the result SHALL be marked invalid and SHALL NOT support a grounded answer

### Foreign identifier

- GIVEN metadata contains a value outside `AFD-001`–`AFD-006`
- WHEN configuration or processing validates the value
- THEN execution SHALL stop or return insufficient evidence without disclosing foreign content

### No side effect

- GIVEN Citation Context processes retrieved objects
- WHEN the Template runs
- THEN it SHALL make no network, file, Tool, Credential or Workspace call

## Cost and Rollback

- Configuration forecast: 0 Credits; any decrease is a stop condition.
- A later one-question validation is forecast at the measured 6 Credits and requires a separate reserve decision; it is not part of this plan approval.
- Rollback removes the Template node and document metadata field assignments, restores the verified D1R four-node graph, and does not alter the indexed document content.
- Corpus 1.1.0 is not created unless M-TEMPLATE and M-CODE are both proven unavailable or unsafe and the Owner separately approves reindexing cost.

## Proposed Next Stage

`K3.3-D3A` may be approved separately for configuration only: add the six `source_id` metadata values and one Template node, bind visible variables, reload-verify, and stop. It SHALL include zero Runtime requests, zero expected Credits, no Indexing and no Publish.
