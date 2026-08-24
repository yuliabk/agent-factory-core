# K3.3-B Execution Evidence — One-Document Pilot

## Status

- `evidence_id`: `af-ka-01-k3-3-b`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `result`: `partial_complete_blocked_minimum_overlap_drift`
- `authorized_source`: `AFD-001.md`
- `verified_sha256`: `D17DDE969830845047DF97AC826D9F065FC893BF1CBCD19837ED45ED047C149F`
- `credits_before`: `200 available`
- `credits_at_stop`: `200 available`
- `documents_indexed`: `0`
- `model_calls`: `0`

## Actions Performed

1. Verified the local SHA-256 matched the approved Corpus manifest and the focused safety scan found no URL, contact, Credential, Secret or sensitive-data pattern.
2. Reverified Sandbox, one of one Members, zero of fifty Documents, 200 available Credits, API usage 0/5000 and disabled Billing management.
3. Selected and uploaded only `AFD-001.md` into the dedicated `af-demo-services-he-1-0-0` creation wizard.
4. Entered the approved candidate settings: General mode, delimiter `\n##`, Top K 3, `text-embedding-3-small`, Score Threshold off and no Rerank.

## Drift and Stop

Dify did not accept Chunk overlap `0`. It coerced the field to its minimum value `1` and disabled further decrement. No `Preview Chunk` or `Save & Process` action was executed after this Drift was observed.

The document is staged in the Dify creation wizard but is not Indexed. Credits remained 200 available. The browser tab was preserved at the Document Processing step for a possible separately authorized continuation.

## Forbidden Actions Confirmed Absent

- No `AFD-002` through `AFD-006` upload.
- No Chunk preview, Indexing or measured embedding Credit delta.
- No Retrieval Test, App Preview, Model call or scored question.
- No Publish, Credential, BYOK, Payment, Upgrade, Subscription or Workspace change.

## Required Owner Decision

Continuing requires a bounded K3.3-B1 approval accepting Dify's minimum one-character overlap for this one-document Preview and conditional Indexing pilot. The existing 25-Credit reserve ceiling and all Stage B stop conditions remain unchanged.
