# PF-S Routing and Response Contract

## Routing Order

1. Validate `tenant_id = af-demo-retail`, synthetic classification, locale and request identifier.
2. Reject real sensitive data, Prompt Injection and foreign-tenant requests before policy selection.
3. Detect protected actions before informational routing.
4. Route one informational request to `product_policy`, `delivery_policy`, `warranty_policy` or `unsupported`.
5. Check required fields and ask one focused clarification when a missing field changes the answer.
6. Select only approved `CSR-001`–`CSR-004` evidence at version `1.0.0`.
7. Produce a Hebrew draft, canonical fallback, refusal or escalation status.
8. Keep `external_message_status = not_sent` and `ticket_status = not_created`.
9. Record minimized local evidence.

## Required Fields by Category

| Category | Required fields |
|---|---|
| `product_policy` | `query`; `item_id` only when identity is ambiguous |
| `delivery_policy` | `demo_zone`; `submitted_time` only for cut-off questions |
| `warranty_policy` | `item_id`; no real order or customer identifier |
| `unsupported` | `query` |
| `protected_action` | `query`; no executable target is accepted |

## Response Types

- `draft_answer`: supported by stable evidence references.
- `clarification`: asks only for the missing synthetic field.
- `insufficient_evidence`: uses the canonical `CSR-004` response and requires Owner review.
- `refusal`: blocks Injection, sensitive data, foreign tenant or execution demand.
- `escalation`: records local Owner review status only.
- `blocked`: fail-closed when the escalation owner or required invariant is missing.

## Conflict and Failure Rules

- current approved version wins only when no competing approved version exists;
- stale, unknown or conflicting evidence is not silently selected;
- conflict produces evidence references plus `human_review_required`;
- unavailable policy storage produces `blocked_dependency_unavailable`;
- cost or request ceiling produces `blocked_cost_ceiling` before any provider request;
- every response has empty `external_actions`.
