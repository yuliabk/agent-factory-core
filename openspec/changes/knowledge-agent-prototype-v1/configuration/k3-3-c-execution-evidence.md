# K3.3-C Execution Evidence

## Scope and Result

- `stage`: `K3.3-C`
- `approved_on`: `2026-08-20`
- `result`: `stopped_safely_at_credit_ceiling_guard`
- `authorized_sources`: `AFD-002` through `AFD-006`, sequentially
- `processed_sources`: `AFD-002` through `AFD-005`
- `not_uploaded`: `AFD-006`
- `stage_credit_ceiling`: `100`
- `stage_credit_delta`: `90`
- `credits_before`: `180`
- `credits_after`: `90`
- `minimum_required_remaining`: `50`

The run stopped before uploading `AFD-006.md`. Only 10 Credits remained inside the Stage ceiling, while each completed Stage C document had consumed 15–30 Credits. Starting the final document could therefore have exceeded the approved 100-Credit ceiling.

## Source Verification and Processing

| Source | Verified SHA-256 | Preview chunks | Credit delta | Final status | Retrieval count |
|---|---|---:|---:|---|---:|
| `AFD-002` | `E89467DA3951D3B4BE185F924AF46FD0544428DA68C44A35BA8721358CC4DEC9` | 5 | 15 | Available | 0 |
| `AFD-003` | `0BB38CD61338029DE68CC015112559C6F830EE187506E9F27B1F2ACC7007C3F3` | 6 | 30 | Available | 0 |
| `AFD-004` | `8D063D54E214BE3D2B8E92646B03A9E73A007C2F5C0CB0A09387E4CFC13ABFFE` | 6 | 25 | Available | 0 |
| `AFD-005` | `4EF08D1E8049C3824F70826D2EC5805DBFCEF8A3FFD85DB120A9794AF14C9080` | 6 | 20 | Available | 0 |
| `AFD-006` | `AF6448B760E6A87E4A360B7D28F2E11677C1B71D6AC29A0CC56C3D9A575EA13A` | not previewed | 0 | not uploaded | n/a |

All processed files passed the synthetic-only safety scan and manifest Hash comparison. Each Preview preserved one metadata chunk, one title/synthetic-notice chunk, and stable business-section chunks.

## Frozen Configuration

- Knowledge Base: `af-demo-services-he-1-0-0`
- Chunking mode: General
- Delimiter: newline plus `##`
- Maximum chunk length: `1024`
- Chunk overlap: `1`
- Embedding: `text-embedding-3-small`
- Retrieval: Vector Search, Top K `3`, Rerank off

## Boundary Confirmation

- No Retrieval Test, App Preview, generation Model call, Publish, Tool, Credential, Payment, Upgrade or Workspace change occurred.
- Five documents (`AFD-001`–`AFD-005`) are Available with Retrieval count `0`.
- `AFD-006` requires a new, separately bounded authorization; Stage D is not ready.
