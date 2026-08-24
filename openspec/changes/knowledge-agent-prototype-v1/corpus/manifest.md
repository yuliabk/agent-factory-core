# Corpus Manifest: AF Demo Services Hebrew V1

## Corpus Metadata

- `corpus_id`: `af-demo-services-he`
- `corpus_version`: `1.0.0`
- `tenant_id`: `af-demo-services`
- `language`: `he`
- `classification`: `synthetic`
- `owner`: `agent-factory-owner`
- `approval_date`: `2026-08-20`
- `corpus_version_status`: `approved_by_owner`
- `corpus_version_approval_date`: `2026-08-20`
- `indexing_status`: `all_six_indexed_available`
- `indexing_authorization_reference`: `K3.3-B1, K3.3-C, K3.3-C1`
- `indexed_source_count`: `6`
- `preview_chunk_count`: `35`
- `indexing_credit_delta`: `140`
- `runtime_status`: `full_corpus_indexed_app_linked_not_executed`

## Approved Source Set

| Source ID | File | Document version | Effective date | Status | SHA-256 |
|---|---|---|---|---|---|
| `AFD-001` | `AFD-001.md` | `1.0.0` | `2026-08-20` | `approved` | `D17DDE969830845047DF97AC826D9F065FC893BF1CBCD19837ED45ED047C149F` |
| `AFD-002` | `AFD-002.md` | `1.0.0` | `2026-08-20` | `approved` | `E89467DA3951D3B4BE185F924AF46FD0544428DA68C44A35BA8721358CC4DEC9` |
| `AFD-003` | `AFD-003.md` | `1.0.0` | `2026-08-20` | `approved` | `0BB38CD61338029DE68CC015112559C6F830EE187506E9F27B1F2ACC7007C3F3` |
| `AFD-004` | `AFD-004.md` | `1.0.0` | `2026-08-20` | `approved` | `8D063D54E214BE3D2B8E92646B03A9E73A007C2F5C0CB0A09387E4CFC13ABFFE` |
| `AFD-005` | `AFD-005.md` | `1.0.0` | `2026-08-20` | `approved` | `4EF08D1E8049C3824F70826D2EC5805DBFCEF8A3FFD85DB120A9794AF14C9080` |
| `AFD-006` | `AFD-006.md` | `1.0.0` | `2026-08-20` | `approved` | `AF6448B760E6A87E4A360B7D28F2E11677C1B71D6AC29A0CC56C3D9A575EA13A` |

## Excluded Fixtures

- `AFD-005-conflict-fixture` is not materialized in the active corpus and is not authorized for indexing.
- Superseded and withdrawn versions are excluded from the active source set.
- No external URL, web source, upload, or client document is included.

## Safety Declaration

The source set is intended to contain only fictional organization content and synthetic policy facts. It contains no real customer records, employee records, contact details, credentials, medical records, financial records, account identifiers, or Production data.

## Gate

Corpus version `1.0.0` is approved as the materialized source set. K3.3-B1, C and C1 Indexed `AFD-001` through `AFD-006` after stable boundary previews. All six sources are Available, totaling 35 Preview Chunks and 140 Indexing Credits. Runtime execution remains blocked.
