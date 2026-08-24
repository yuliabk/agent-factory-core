# K3.2d Closure Package — Dify Mapping

## Status

- `package_id`: `af-ka-01-k3-2d`
- `version`: `2.3.0`
- `previous_version`: `2.2.0`
- `date`: `2026-08-20`
- `status`: `partially_materialized`
- `provider_changes`: `linked_app_full_corpus_two_smoke_requests_six_source_ids_and_retrieval_bound_citation_context`
- `k3_3_status`: `stage_d3s_partial_safe_stop_manual_template_paste_required`

## Selected Prototype Mapping

| Decision | Selected value | Reason |
|---|---|---|
| App type | `Chatflow` | מאפשר Flow מפורש, Knowledge Retrieval node ו-Studio Test Run ללא WebApp publication. |
| App name | `AF-KA-01 - Synthetic Knowledge Agent` | זהות יציבה מול ה-Spec. |
| Interface | Studio Preview/Test Run בלבד | Owner-only; אין WebApp, API או Share link. |
| Flow | `Start → Knowledge Retrieval → LLM → Answer`, plus parallel `Knowledge Retrieval → Citation Context` | הענף החדש מחובר רק ל-`result` הגלוי; הוא אינו מוזן ל-LLM עד שנתיב metadata פנימי יוצג ויאומת. אין Tool, Agent, HTTP, Code, Trigger או side effect node. |
| Generation provider | `langgenius/openai/openai` | זמין באמצעות Dify AI Credits ללא BYOK. |
| Generation model | `gpt-4.1-mini-2025-04-14` | הגרסה המתוארכת שאושרה לאחר שה-alias לא היה זמין; טרם בוצעה קריאת Generation. |
| Embedding model | `text-embedding-3-small` | ברירת המחדל שנצפתה, 5 Credits לפי מחירון Dify; השימוש בפועל ב-Indexing יימדד במסמך אחד לפני הרחבה. |
| Rerank | `disabled` | Candidate `R-A` דורש no reranking; אין להשתמש ב-`qwen3-rerank` ברירת המחדל. |
| Retrieval | Semantic/vector nearest equivalent, `top_k = 3` | תואם ל-`R-A`; exact UI labels יאומתו לפני Indexing. |
| Chunking measured | General mode, separator `\n##`, overlap `1` | Dify אכף מינימום 1; Preview של `AFD-001.md` הוכיח חמישה Chunks עם גבולות Section יציבים. |
| Knowledge Base | Dedicated Standard Knowledge Base for `af-demo-services` | אין שיתוף עם Corpus או Tenant אחרים. |
| Permissions | Current 1/1 Owner-only Sandbox accepted for synthetic prototype | `Everyone` ב-Integration permissions שקול כרגע ל-Owner יחיד; Membership drift חוסם. |

## Non-Negotiable Configuration

- אין Tools או Tool attachments, כולל Audio, Code Interpreter, CurrentTime ו-WebScraper המובנים.
- אין MCP, Data Source, Trigger, Extension, Custom Endpoint, Swagger Tool או Workflow-as-Tool.
- אין BYOK, API key, paid quota, Subscription, Upgrade או Payment method.
- אין Rerank גם אם Workspace default מציג `qwen3-rerank`.
- אין Publish מכל סוג; Preview/Test Run בלבד.
- אין Model fallback או silent substitution.
- אין Indexing אם Chunk preview חוצה `source_id` או Section יציב.
- אין שימוש בנתון שאינו מתוך `af-demo-services-he@1.0.0` המאושר.

## Credit Forecast and Stop Rules

| Stage | Maximum action | Credit envelope | Stop rule |
|---|---|---:|---|
| Resource configuration | Create empty Chatflow; create empty Knowledge only if UI permits without Upload/Indexing | 0 expected model responses | Any Credit decrease stops the stage; no API workaround |
| Indexing pilot | One approved source document only | 25 Credits reserved maximum | Stop after one document and record actual delta |
| Remaining Indexing | Five remaining documents | Forecast derived from pilot; must leave at least 50 Credits | No separate Owner approval, no continuation |
| Smoke test | Up to 5 frozen questions with `gpt-4.1-mini` | 5 Credits expected; 10 hard request ceiling | Stop at 5 content attempts or unexpected delta |
| Scored run | 25 questions + up to 5 technical retries | 30 generation Credits expected | Separate K4 authorization required |

The official pricing page lists the `gpt-4.1-mini` family at 1 Credit and `text-embedding-3-small` at 5 Credits per applicable AI response. The measured one-document Indexing pilot consumed 20 Credits; this actual delta governs the remaining forecast.

## Drift Controls

Before every provider action, record only non-personal state:

1. Workspace is `sandbox`, Member count is `1 / 1`, and current role is Owner.
2. Paid quota, BYOK and enabled Billing management remain absent.
3. Credits used/remaining and API usage are recorded.
4. Generation model is exactly `gpt-4.1-mini`; Embedding is exactly `text-embedding-3-small`; Rerank is off.
5. OpenAI Provider plugin observed version is compared to the approved observation; any version change is `drift_detected` until reviewed.
6. App contains only Start, Knowledge Retrieval, LLM and Answer nodes.
7. Public WebApp/API, Tools and external integrations remain absent.
8. Corpus hashes match the approved local manifest.

`Auto-update Latest` cannot be treated as a pin. A changed Provider/plugin/model label blocks the run and creates a new Configuration version; it is never accepted silently.

## Residual Decisions

- D3S automated multi-line editor replacement was unsafe; `{{ results }}` was restored and reload-verified. Manual Template paste and separate read-only verification are required before graph wiring.
- D3B source review identifies custom metadata at `metadata.doc_metadata` and selects an allow-listed fail-closed Template. Hosted Runtime validation remains separately gated.
- D3A persisted six `source_id` values and one `Citation Context` Template with `Knowledge Retrieval / result`; nested `source_id` metadata was not selectable, so Runtime and prompt wiring remain blocked.
- Exact General chunk separator support and resulting Section boundaries require an authorized Upload preview.
- The one-document Indexing pilot consumed 20 Credits; five remaining documents forecast 100 Credits and an 80-Credit remainder, pending separate authorization.
- Hebrew quality remains unknown until the frozen evaluation.
- Region and Backup/cache retention acceptance remains synthetic-only.

## Traceability

- Requirements: KA-101–KA-111
- Retrieval: `retrieval-experiment-matrix.md`
- Reconstruction: `dify-reconstruction-runbook.md`
- Authorization: `k3-3-staged-authorization.md`
- UI evidence: `dify-ui-inspection-evidence.md`
- Official evidence: `dify-official-evidence.md`
