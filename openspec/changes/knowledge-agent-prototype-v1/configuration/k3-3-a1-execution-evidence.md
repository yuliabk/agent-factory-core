# K3.3-A1 Execution Evidence — Model and Empty Retrieval Node

## Status

- `evidence_id`: `af-ka-01-k3-3-a1`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `result`: `partial_complete_blocked_empty_knowledge_not_selectable`
- `credits_before`: `200 available`
- `credits_after`: `200 available`
- `model_calls`: `0`
- `documents_uploaded`: `0`
- `documents_indexed`: `0`

## Authorized Changes Performed

1. Reverified Sandbox, one of one Members, one of five Apps, zero of fifty Documents, 200 available Credits and API usage 0/5000.
2. Replaced the default `gpt-5` selection with the Owner-approved `gpt-4.1-mini-2025-04-14` model.
3. Added one `Knowledge Retrieval` node. The App now contains Start, Knowledge Retrieval, LLM and Answer nodes and remains unpublished.

## Platform Constraint and Stop

When `Add Knowledge` was opened from the Knowledge Retrieval node, Dify displayed `No Knowledge found`. The dedicated empty Knowledge Base `af-demo-services-he-1-0-0` remained visible in the Workspace with zero Documents, but Dify did not make it selectable from the App.

The Knowledge Base therefore could not be linked and the intended linear graph could not be completed under Stage A1. Work stopped without an API workaround. The next operation that could make the Knowledge Base selectable would require a document Upload and processing/Indexing preview, which belongs to separately authorized Stage B.

## Forbidden Actions Confirmed Absent

- No Upload, document content, Chunk preview or Indexing.
- No Model call, Preview, Test Run or Retrieval Test.
- No Publish, API use, Credential, BYOK, Payment, Upgrade or Subscription.
- No Tool, MCP, Trigger, external integration or Workspace-wide change.
- No screenshot, account identifier, email address, token or personal data retained.

## Required Owner Decision

K3.3-A1 authorization is consumed. Completing the Knowledge link now requires a separate Stage B decision for one approved synthetic document only, with the existing 25-Credit reserve ceiling and a mandatory stop after the first measured Indexing delta. No Stage B action is authorized by this evidence.
