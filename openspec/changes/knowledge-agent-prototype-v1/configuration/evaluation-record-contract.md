# Evaluation Record Contract

## Metadata

- Contract ID: `ka-evaluation-record`
- Version: `1.0.0`
- Status: Provider-neutral planning artifact
- Requirements: KA-110

## Per-question Record

| Field | Type | Required | Rule |
|---|---|---:|---|
| `evaluation_run_id` | String | Yes | Unique synthetic run identifier |
| `question_id` | String | Yes | One of `KA-E01` through `KA-E25` |
| `request_id` | String | Yes | Synthetic correlation identifier |
| `tenant_id` | String | Yes | Exact value `af-demo-services` |
| `actor_id` | String | Yes | Exact value `owner-evaluation-actor` |
| `agent_release_id` | String | Yes | Versioned value required before a scored run |
| `configuration_version` | String | Yes | Configuration used for the result |
| `corpus_version` | String | Yes | Exact approved version |
| `retrieved_sources` | Array | Yes | Eligible source IDs and section headings only |
| `policy_result` | Enum | Yes | `allow_read`, `deny`, `fallback`, or `owner_review` |
| `response_type` | Enum | Yes | From the response contract |
| `actual_answer_he` | String | Yes | Synthetic answer text |
| `answer_verdict` | Enum | Yes | `pass`, `fail`, or `blocked` |
| `citation_verdict` | Enum | Yes | `pass`, `fail`, `not_applicable`, or `blocked` |
| `fallback_verdict` | Enum | Yes | `pass`, `fail`, `not_applicable`, or `blocked` |
| `safety_verdict` | Enum | Yes | `pass`, `fail`, or `blocked` |
| `latency_ms` | Integer or null | Yes | Measured only during an authorized run |
| `cost_indicator_ils` | Decimal or null | Yes | Measured or allocated cost; no estimate presented as actual |
| `timestamp_utc` | Timestamp or null | Yes | Populated only during an authorized run |
| `notes` | String | No | Synthetic QA notes without secrets or personal data |

## Explicitly Excluded Fields

- credentials, tokens, API keys, cookies, private keys or authorization headers;
- real names, emails, phone numbers, addresses, account IDs or user exports;
- full hidden system or developer prompts;
- full provider traces when they contain unreviewed content;
- foreign-tenant source names, content or Metadata;
- unredacted rejected sensitive input.

## Retention Plan

| Record class | Proposed maximum retention | Purpose | Deletion rule |
|---|---|---|---|
| Provider-side transient logs | Shortest configurable period, not more than 30 days | Technical troubleshooting | Verify deletion or expiry before a real-data pilot |
| Exported synthetic per-question records | 90 days after the final run for this change | Compare candidates and reproduce G1 evidence | Delete after summary verification unless an approved investigation remains open |
| Aggregated verdict and release evidence | Retained in Git for the project lifecycle | Traceability of approval and release | Must contain only minimized synthetic evidence |
| Failed-run evidence | Same as corresponding record class | Prevent silent deletion of failures | Preserve through review; never remove only to improve score |

The exact provider retention must be mapped and approved in K3.1-K3.2. If retention cannot be configured or verified, Runtime remains blocked.

## Deletion Evidence

Deletion evidence records the record class, run IDs, storage location category, requested date, completed date, result, reviewer and any documented exception. It does not copy deleted content into the evidence.

## Planning Boundary

This contract defines future records only. No provider log, evaluation record, Runtime database or audit destination is created by this artifact.

