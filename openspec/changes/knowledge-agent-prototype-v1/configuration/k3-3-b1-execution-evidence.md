# K3.3-B1 Execution Evidence — One-Document Indexing Pilot

## Status

- `evidence_id`: `af-ka-01-k3-3-b1`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `result`: `complete`
- `source`: `AFD-001.md`
- `sha256`: `D17DDE969830845047DF97AC826D9F065FC893BF1CBCD19837ED45ED047C149F`
- `credits_before`: `200 available`
- `credits_after`: `180 available`
- `actual_credit_delta`: `20`
- `credit_reserve_ceiling`: `25`
- `documents_indexed`: `1`
- `generation_model_calls`: `0`

## Preview Evidence

The approved General-mode configuration used delimiter `\n##`, maximum Chunk length 1024, Dify minimum overlap 1, `text-embedding-3-small`, Vector Search, Top K 3, Score Threshold off and no Rerank.

Preview produced five bounded Chunks: document metadata; title and synthetic-data notice; `אודות`; `שעות פעילות`; and `ימי סגירה`. Stable Section headings remained visible and no Chunk mixed two business-policy Sections. The conditional Indexing gate therefore passed.

## Indexing Result

Dify reported `Embedding completed`. The document list showed exactly one document, `AFD-001.md`, in `Available` status with General Chunking, High Quality/Vector retrieval and zero Retrieval count. The measured delta was 20 Credits, below the 25-Credit ceiling, leaving 180 of 200 Credits.

## Stop Confirmation

- No `AFD-002` through `AFD-006` upload or Indexing.
- No Retrieval Test, App Preview, generation call or scored question.
- No Knowledge-to-App link was added under this Stage.
- No Publish, Credential, BYOK, Payment, Upgrade, Subscription or Workspace change.

## Forecast and Next Decision

Linear extrapolation is five remaining documents × 20 Credits = 100 Credits, leaving an estimated 80 Credits. This clears the 50-Credit reserve rule but does not authorize Stage C.

The smallest safe next action is a zero-expected-Credit K3.3-B2 Stage to link the now-indexed dedicated Knowledge Base to the existing Knowledge Retrieval node and complete the linear four-node graph without a run.
