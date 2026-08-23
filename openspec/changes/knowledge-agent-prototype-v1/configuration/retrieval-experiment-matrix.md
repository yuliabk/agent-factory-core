# Retrieval Experiment Matrix

## Metadata

- Matrix ID: `ka-retrieval-matrix-v1`
- Version: `1.2.0`
- Previous version: `1.1.0`
- Status: One-document Dify pilot measured; further Indexing and Runtime execution not authorized
- Corpus: `af-demo-services-he@1.0.0`
- Evaluation set: `ka-prototype-he-v1`
- Requirements: KA-102, KA-103, KA-109

## Principle

No Retrieval configuration is selected before measured evidence. Candidate settings are provider-neutral intentions; a later provider mapping must document the exact equivalent and create a new configuration version.

## Candidate Configurations

| Candidate | Chunking | Overlap | Retrieval mode | Result count | Reranking | Purpose |
|---|---|---:|---|---:|---|---|
| `R-A` | Preserve each stable Markdown section as one unit | 0 | Semantic or nearest provider equivalent | 3 | Off | Lowest complexity and cost baseline |
| `R-B` | Approximately 350-500 tokens without crossing source boundaries | Approximately 50 tokens | Hybrid keyword + semantic when available | 5 | Off | Test Hebrew recall and multi-source questions |
| `R-C` | Preserve headings with smaller subsection chunks when needed | Approximately 50 tokens | Hybrid when available | 5 | On when measurable | Test citation precision and conflict detection |

If a provider does not support an option, the mapping is recorded as `unsupported`; it is not silently replaced.

## Controlled Variables

The following remain identical across candidates:

- corpus and source hashes;
- question wording and order;
- answer, citation, fallback and policy contracts;
- model and generation settings within a comparison round;
- tenant and actor policy;
- request and monthly cost limits.

## Required Measurements

| Measurement | Purpose |
|---|---|
| Supported factual correctness | Detect lost or distorted evidence |
| Citation presence and correctness | Verify traceability |
| Unsupported fallback rate | Detect over-retrieval and hallucination |
| Prompt-injection safety | Verify retrieved text remains untrusted |
| Conflict and ambiguity handling | Verify multiple-source behavior |
| Retrieved source IDs and sections | Explain each result |
| Latency indicator | Compare Owner experience |
| Cost indicator | Enforce the approved cap |

## Selection Gates

A candidate is ineligible if it causes any mandatory safety failure, external action, cross-tenant disclosure, secret exposure, or personal-data exposure. It must also satisfy the thresholds in `evaluation-plan.md`.

Among eligible candidates, select in this order:

1. Higher citation correctness.
2. Higher supported factual correctness.
3. Better unsupported fallback behavior.
4. Lower measured cost.
5. Lower latency and lower Owner maintenance effort.

Ties favor the simpler configuration.

## Dify Mapping for the First Authorized Candidate

`R-A` is mapped locally as follows; it is not yet configured or proven:

| Provider field | Planned value | Verification rule |
|---|---|---|
| Knowledge type | Dedicated Standard Knowledge Base | Stop if it attaches another Knowledge source |
| Indexing | High Quality / vector-capable nearest equivalent | Exact UI option recorded before use |
| Chunking | General; separator `\n##`; measured Dify minimum overlap 1 | Five-Chunk Preview preserved metadata/title separately and one stable business Section per Chunk for `AFD-001.md` |
| Retrieval | Semantic/vector nearest equivalent | No silent hybrid substitution |
| Top K | 3 | Must be visible in exported or recorded configuration |
| Score threshold | Off initially | A later value requires a new Configuration version |
| Rerank | Off | Workspace default `qwen3-rerank` SHALL NOT be inherited |
| Embedding | `text-embedding-3-small` | Explicit selection; no Workspace-default drift |

If Dify cannot preserve Section boundaries with this mapping, `R-A` is marked `unsupported_in_current_ui`; Indexing stops and a new mapping is presented to the Owner.

## Experiment Limits

- Maximum candidate configurations per authorized comparison round: 3.
- Maximum billable question attempts per candidate: 30, including up to 5 documented technical retries.
- A failed content answer is not a technical retry and remains a failure.
- No candidate run begins without K3.3 approval and an enforceable cost measurement.
- Changes after viewing results create a new configuration version and a new run; prior evidence remains intact.
