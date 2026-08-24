# Dify Manual Reconstruction Runbook

## Status and Boundary

- `runbook_id`: `af-ka-01-dify-reconstruct`
- `version`: `1.1.0`
- `previous_version`: `1.0.0`
- `status`: `partially_executed_through_r3_one_document`
- `scope`: synthetic Dify Sandbox prototype only

Runbook זה אינו הרשאת Provisioning, Upload, Indexing, Model call, Publish או Delete. הוא מתאר כיצד לשחזר את ה-Prototype ללא Conversation history או hidden settings לאחר אישור של כל Stage.

## Recovery Authority

1. Git corpus `af-demo-services-he@1.0.0` וה-Hashes במניפסט.
2. Configuration manifest ו-`k3-2d-closure-package.md`.
3. App DSL export ללא Secrets, אם נוצר בעתיד.
4. Minimized evaluation records; Dify Logs אינם מקור האמת היחיד.

## Reconstruction Order

### R0 — Preconditions

- Verify `sandbox`, `1 / 1` Owner, no paid quota, no BYOK and unchanged Credit balance.
- Verify approved Stage authorization and expiry.
- Verify all six local source Hashes and rescan for PII, Secrets, URLs and real data.
- Record Dify/OpenAI plugin labels and observed versions without account identifiers.
- Stop on Drift.

### R1 — Empty Knowledge Base

- Create exactly one Standard Knowledge Base named `af-demo-services-he-1-0-0` only if the UI permits an empty Knowledge Base without Upload or Indexing; otherwise inspect without submission and defer creation to R3.
- Classification remains synthetic; no external Knowledge API or Data Source.
- Select `text-embedding-3-small` explicitly.
- Configure Candidate `R-A`: General mode, Dify-enforced overlap 1, semantic/vector retrieval, `top_k = 3`, Rerank off.
- Do not upload a document in this Stage and do not use an API workaround.

### R2 — Empty Chatflow

- Create one blank Chatflow named `AF-KA-01 - Synthetic Knowledge Agent`.
- Add only Start, Knowledge Retrieval, LLM and Answer.
- Bind only the dedicated Knowledge Base.
- Select `gpt-4.1-mini` explicitly at the LLM node; do not inherit `gpt-5` Workspace default.
- Add the approved Hebrew answer/fallback policy from `request-answer-contract.md`.
- Confirm zero Tools, Variables that select Tenant, Triggers or external calls.
- Do not Publish and do not Test Run.

### R3 — One-Document Preview and Indexing Pilot

- If R1 could not create an empty Knowledge Base, create it now as part of the separately approved pilot. Upload only `AFD-001.md` after its Hash is reverified.
- In preview, confirm every Chunk remains within one Source and one stable Section; test separator candidate `\n## ` only if supported exactly.
- If a Section boundary is lost, stop before Indexing and create a new retrieval mapping version.
- If preview passes, Index only `AFD-001` under its separately approved Stage.
- Record Credit delta, Chunk count, document status and configuration identifiers without account data.

### R4 — Remaining Corpus

- Recalculate the forecast from the pilot Credit delta.
- Continue only under separate approval and only if at least 50 Credits remain after forecast.
- Upload and Index `AFD-002`–`AFD-006` one at a time; verify Source/Section boundaries and approved status for each.
- Stop on foreign, superseded, withdrawn, duplicated or unexpected Chunk.

### R5 — Configuration Evidence

- Export App DSL with Secrets explicitly excluded.
- Name it `AF-KA-01_<agent_release_id>_config-<version>_<yyyy-mm-dd>.yaml`.
- Record Knowledge settings, Chunk counts and source mapping in a minimized local manifest; never export account/payment data.
- Compare the reconstructed state with the local Configuration manifest and mark `match` or `drift_detected`.

### R6 — Studio-only Validation

- Confirm no WebApp/API/Marketplace publication exists.
- Execute only the separately authorized smoke/evaluation Stage.
- Preserve failures and Credit deltas; never change the Model or Retrieval configuration mid-run.

## Rollback and Deletion Sequence

1. Stop all Test Runs and confirm no published access.
2. Export non-secret App DSL and minimized evidence if authorized.
3. Detach the App from Knowledge.
4. Delete indexed Documents and their Chunks.
5. Delete the Knowledge Base and Index.
6. Delete evaluation Conversations/Logs when supported.
7. Delete the App.
8. Confirm Credits do not continue changing and no resource remains visible.
9. Retain only approved synthetic Git artifacts and minimized evidence.

Deletion is a destructive external action and always requires action-time Owner confirmation even if a broader Stage was approved.

## Reconstruction Pass Condition

Reconstruction is `pass` only when the local corpus is recoverable, the four-node Chatflow and Knowledge settings match this Runbook, no secret is required from Git, no Tool or public access exists, and a DSL + local manifest are sufficient to reproduce the configuration. A real restore test remains a later separately authorized action.
