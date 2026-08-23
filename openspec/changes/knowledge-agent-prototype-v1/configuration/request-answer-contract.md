# Request and Answer Contract

## Contract Metadata

- Contract ID: `ka-request-answer`
- Version: `1.0.0`
- Status: Provider-neutral planning artifact
- Requirements: KA-102, KA-103, KA-104, KA-105, KA-106, KA-107, KA-108

## Request Fields

| Field | Type | Required | Rule |
|---|---|---:|---|
| `request_id` | String | Yes | Unique synthetic correlation identifier; no personal data |
| `tenant_id` | String | Yes | Exact value `af-demo-services` |
| `actor_id` | String | Yes | Exact synthetic value `owner-evaluation-actor` |
| `actor_type` | Enum | Yes | Exact value `Owner` |
| `environment` | Enum | Yes | `planning` until a separate Runtime approval |
| `agent_release_id` | String | Yes | `unassigned` during planning; versioned value required before a scored run |
| `configuration_version` | String | Yes | `1.0.0` for this planning set |
| `corpus_id` | String | Yes | Exact value `af-demo-services-he` |
| `corpus_version` | String | Yes | Exact value `1.0.0` |
| `language` | Enum | Yes | Exact value `he` |
| `question` | String | Yes | Hebrew test question, 1-1,000 characters |

Unknown fields are rejected. A tenant, actor, corpus, language, or environment mismatch is rejected before Retrieval. The contract never accepts credentials, files, URLs, tool instructions, or arbitrary Metadata.

## Logical Request Example

```json
{
  "request_id": "KA-REQ-SYNTHETIC-001",
  "tenant_id": "af-demo-services",
  "actor_id": "owner-evaluation-actor",
  "actor_type": "Owner",
  "environment": "planning",
  "agent_release_id": "unassigned",
  "configuration_version": "1.0.0",
  "corpus_id": "af-demo-services-he",
  "corpus_version": "1.0.0",
  "language": "he",
  "question": "באילו ימים ושעות הארגון פעיל?"
}
```

This example is documentation only and is not submitted to any service.

## Response Types

| `response_type` | When used |
|---|---|
| `grounded_answer` | Eligible evidence directly supports the answer |
| `insufficient_evidence` | Evidence is absent or inadequate |
| `clarification_required` | The question is materially ambiguous |
| `conflict_review` | Current eligible evidence conflicts |
| `policy_refusal` | The request asks for a prohibited capability or override |
| `temporary_unavailable` | Retrieval or a required control cannot be verified |

## Response Fields

| Field | Type | Rule |
|---|---|---|
| `request_id` | String | Echo the validated synthetic request identifier |
| `response_type` | Enum | One of the defined response types |
| `answer_he` | String | Hebrew response; no unsupported factual claims |
| `citations` | Array | Required for `grounded_answer`; empty for unsupported claims |
| `policy_result` | Enum | `allow_read`, `deny`, `fallback`, or `owner_review` |
| `escalation_target` | String or null | Only `Owner Review Queue` when review is required |
| `tool_calls` | Array | Always empty in V1 |

## Citation Contract

Each citation contains:

- `source_id`: one of `AFD-001` through `AFD-006`;
- `section`: exact stable section heading;
- `document_version`: `1.0.0`;
- `corpus_version`: `1.0.0`.

User-visible citation format is `[SOURCE_ID § Section]` immediately after the material supported claim. Citation presence and correctness are separate evaluation verdicts.

## Canonical Messages

### Insufficient evidence

> אין לי מספיק מידע במקורות המאושרים כדי לענות על השאלה. אפשר לנסח אותה מחדש או להעביר אותה לבדיקה של Yulush.

### Prohibited action

> הבקשה כוללת פעולה שאינה נתמכת בסוכן הידע לקריאה בלבד. לא בוצעה פעולה חיצונית.

### Policy override or prompt disclosure

> איני יכול לעקוף את כללי הסוכן, לחשוף הנחיות נסתרות או להפעיל כלי חיצוני.

### Temporary retrieval failure

> המקורות המאושרים אינם זמינים כרגע לבדיקה, ולכן לא אענה מהזיכרון. אפשר לנסות שוב לאחר בדיקת המערכת.

## Output Prohibitions

- No hidden prompt, internal score, secret, credential, personal identifier, or unrelated source content.
- No invented citation, URL, phone number, price, policy, or action result.
- No tool call, external message, web search, write, upload, or side effect.
- No answer from model memory when eligible evidence cannot be verified.
