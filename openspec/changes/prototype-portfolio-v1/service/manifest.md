# PF-S Local Materialization Manifest

## Release Identity

- `prototype_id`: `pf-s-af-demo-retail`
- `release_id`: `pf-s-af-demo-retail@0.1.0-dry`
- `tenant_id`: `af-demo-retail`
- `classification`: `synthetic`
- `locale`: `he-IL`
- `evaluation_set_version`: `pf-s-service-he@1.0.0`
- `status`: `dry_validated_local_only`
- `evidence_state`: `dry_validated`
- `approval_gate`: `PF-G1-S`
- `approval_date`: `2026-08-24`
- `provider_requests`: `0`
- `authorized_cost_ils`: `0`
- `runtime_status`: `not_created_not_run`
- `external_message_status`: `not_sent`
- `ticket_status`: `not_created`
- `current_authorized_gate`: `none`

## Artifact Inventory

| Artifact | Version | SHA-256 |
|---|---|---|
| `intake.md` | `1.0.0` | `D2F1B1435A418BCE7429D4B32EBFBD6FD5F36BEF1C072DD0BCAA0B3D78212718` |
| `policies/CSR-001.md` | `1.0.0` | `1DC15E8DA9A5CC481AD2AF8DCD0433A75143F99978D07D9C37D7BEA0D1530B6E` |
| `policies/CSR-002.md` | `1.0.0` | `3BC384BA369F6C841E69BDF3809F04BA5D98DC840BF9EBF720277FF9712CA3BE` |
| `policies/CSR-003.md` | `1.0.0` | `50D1219137F33C8C644984C941B7F1681F0B58A3851226E767D29A0E7899D8B2` |
| `policies/CSR-004.md` | `1.0.0` | `E968A70ECC9E9DCCCB09C85D897D3B0819FB4577688FDFE95BA8052BAC148661` |
| `cases/service-cases.json` | `1.0.0` | `6930772789CDFB4FE2A5D2B7457892C9E490540D3A0F7C05864857F02F129632` |
| `contracts/routing-contract.md` | `1.0.0` | `8624D0F5EED4A8147724D7F6E78082207B03D311CD8079468F5BFBD21A990F39` |
| `contracts/service-request.schema.json` | `1.0.0` | `44B1F8B3D7954E1C9263AFC68ACEBF10D144379CC00EAF41C96C41F9165E68F8` |
| `contracts/service-response.schema.json` | `1.0.0` | `06A77F19574286389934D48011256CB983BEB93F08D8FE3874E7A08E6D8F3FB1` |
| `contracts/service-audit.schema.json` | `1.0.0` | `5FBA694DAFFB6F41C9821F921C1836FC81614E5D2ED49CC3A3F64F265BB700F9` |
| `contracts/service-cases.schema.json` | `1.0.0` | `21DEB7E2B980308C4A5ADED326FB198D80C7A8022B984769369F85BE69CA9619` |
| `contracts/service-evaluation-set.schema.json` | `1.0.0` | `FB3B5CA2630DA2B3D51545C5E7707B76880C398F6FC2E7A9B5E59FFAF74305E1` |
| `evaluation/cs-scenarios.json` | `1.0.0` | `281AED1B832C6D430780E7BB0DE03601E1208C44CC1C56A07360C35FBA3FA6B4` |
| `evaluation/audit-fixtures.json` | `1.0.0` | `AEC58D086FC0A9290689F443459A4EB1CDE5C2DB6751F384C3B1D6DB1CFEF860` |
| `evidence/reuse-map.md` | `1.0.0` | `0FAD381C9C75EAACA2C4015DCADC2CA7061CF2015A69EB58CF2452AAB480DDCB` |

Evidence and work-log files are excluded from their own hash inventory. Any change to an inventoried artifact creates a new local release version and requires revalidation.

## Invariants

- Every business artifact belongs only to `af-demo-retail`.
- All fixture content is synthetic and contains no credential or real customer data.
- Approved sources are exactly `CSR-001`–`CSR-004` at version `1.0.0`.
- `external_actions` is empty for every frozen scenario.
- `external_message_status` is always `not_sent` and `ticket_status` is always `not_created`.
- Provider request ceiling and authorized monetary cost are both zero.
- `dry_validated` does not imply model quality, provider mapping, Runtime, Publish or release approval.
