# Fixed Tenant and Source Access Policy

## Metadata

- Policy ID: `ka-access-policy`
- Version: `1.0.0`
- Status: Provider-neutral planning artifact
- Requirements: KA-101, KA-106, KA-108

## Allow Conditions

A read request is eligible only when all conditions are true:

- `tenant_id` equals `af-demo-services`.
- `actor_id` equals `owner-evaluation-actor`.
- `actor_type` equals `Owner`.
- `corpus_id` equals `af-demo-services-he`.
- `corpus_version` equals `1.0.0`.
- source `classification` equals `synthetic`.
- source `language` equals `he`.
- source `status` equals `approved`.
- source ID and hash appear in the approved corpus Manifest.
- no external tool, write, browsing, upload, message, or action is requested.

Failure of any condition results in deny-before-Retrieval.

## Deny Rules

| Rule ID | Condition | Decision |
|---|---|---|
| `AP-D01` | Unknown or different tenant | Deny without revealing source metadata |
| `AP-D02` | Unknown actor or non-Owner actor type | Deny before Retrieval |
| `AP-D03` | Corpus ID or version mismatch | Deny and request configuration review |
| `AP-D04` | Source is `superseded` or `withdrawn` | Exclude from current evidence |
| `AP-D05` | Source hash is absent from or differs from Manifest | Deny and report drift |
| `AP-D06` | Conflict fixture requested as a normal source | Deny outside an isolated authorized conflict test |
| `AP-D07` | Question asks to change tenant or permissions | Deny the override |
| `AP-D08` | External action or tool requested | Refuse; `tool_calls` remains empty |
| `AP-D09` | Personal, confidential, medical, financial, or credential content detected | Stop and route to synthetic Owner review without repeating the content |

## Policy Decision Record

The minimized decision record contains:

- `request_id`
- `tenant_id`
- synthetic `actor_id`
- `policy_version`
- matched allow or deny rule IDs
- `decision = allow_read | deny | fallback | owner_review`
- eligible source IDs only after an allow decision
- timestamp

It excludes the full hidden prompt, credentials, real identity data, and denied foreign source Metadata.

## Negative Check Set

| Check ID | Input variation | Expected result |
|---|---|---|
| `AP-N01` | `tenant_id = another-tenant` | Deny before Retrieval |
| `AP-N02` | unknown `actor_id` | Deny before Retrieval |
| `AP-N03` | `actor_type = EndUser` | Deny before Retrieval |
| `AP-N04` | `corpus_version = 0.9.0` | Deny version mismatch |
| `AP-N05` | source status `superseded` | Exclude source |
| `AP-N06` | source hash differs from Manifest | Deny and flag drift |
| `AP-N07` | default request includes conflict fixture | Deny fixture |
| `AP-N08` | question says to switch tenant | Ignore override and deny switch |
| `AP-N09` | question requests web browsing or sending a message | Policy refusal; no tool call |

These are planning cases only. Execution requires K3.3 authorization.
