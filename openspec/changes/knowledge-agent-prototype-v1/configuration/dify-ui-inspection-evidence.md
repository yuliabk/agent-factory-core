# Dify Authenticated UI Inspection Evidence

## Record

- `evidence_id`: `af-ka-01-dify-ui-inspection`
- `version`: `1.0.0`
- `inspected_on`: `2026-08-20`
- `mode`: authenticated read-only UI inspection
- `account_data_retained`: none
- `screenshots_retained`: none
- `provider_changes`: none
- `result`: `inspection_complete_partial_readiness`

## Authorization Boundary Observed

לא נוצרו או שונו Workspace, App, Knowledge Base, Model, Credential, API key, Payment method, Subscription, Integration או הרשאה. לא בוצעו Upload, Indexing, Embedding, Generation, Test, Publish, Install, Save או Upgrade. לא נשמרו Email, שם חשבון, Account ID, Token או Screenshot.

## Verified Current State

| Area | UI evidence | Assessment |
|---|---|---|
| Plan | Workspace מסומן `sandbox` ו-`Free Trial of Core Capabilities`. | `pass_current_state` |
| Membership | `1 / 1` Members; המשתמש היחיד מסומן `owner`. | `pass_owner_only_current_state` |
| Apps | `0 / 5`; Studio מציג `Build your first App`. | `pass_no_app_no_publication` |
| Knowledge | `0 / 50` Documents; Knowledge מציג `Build your first Knowledge base`. | `pass_no_knowledge_no_index` |
| Credits | `0 / 200` AI Credits used. | `pass_zero_usage` |
| Billing | `Billing and Subscriptions` / `Manage` מושבת; Upgrade מוצג כפעולה נפרדת. | `pass_no_paid_plan_visible`; אין הוכחה חוזית נגד שינוי עתידי |
| API usage | `0 / 5000` requests במחזור הנוכחי. | `pass_zero_usage` |
| BYOK | ספקי ה-Credits מציגים `Add API Key`; לא מוצג Key מחובר. | `pass_no_private_provider_key_visible` |
| Default generation model | `gpt-5` דרך `langgenius/openai/openai`. | `requires_explicit_selection`; לא הורץ |
| Default embedding model | `text-embedding-3-small` דרך `langgenius/openai/openai`. | `requires_explicit_selection`; לא הורץ |
| Default rerank model | `qwen3-rerank` דרך `langgenius/tongyi/tongyi`. | `must_not_use_for_R-A`; לא הורץ |
| Provider updates | Model Provider UI מציג `Auto-update Latest`. Tool/Data Source/Trigger pages מציגים `Auto-update Fix only`. | `drift_risk`; נדרש Pin/verification before run |
| Data sources | `Data Source not set up`. | `pass_none_connected` |
| Triggers | `No Trigger found`. | `pass_none_connected` |
| Extensions | `No Extension found`. | `pass_none_connected` |
| Custom endpoints | רק `Add Custom Endpoint`; לא מוצג Endpoint קיים. | `pass_none_visible` |
| MCP | רק `Add MCP Server (HTTP)`; לא מוצג Server קיים. | `pass_none_visible` |
| Workflow as Tool | `No workflows published as tools yet`. | `pass_none_published` |
| Swagger API as Tool | רק `Create a Swagger API as Tool`; לא מוצג Tool קיים. | `pass_none_visible` |
| Built-in tools | Audio, Code Interpreter, CurrentTime ו-WebScraper זמינים ברמת Workspace. | `app_level_block_required`; App עתידי SHALL attach none |
| Integration permissions | Install/manage ו-Debug מסומנים `Everyone`; בפועל יש Member יחיד. | `residual_least_privilege_gap`; שינוי דורש אישור נפרד |

## Readiness Interpretation

1. במצב הנוכחי אין App, Knowledge, Index, Published WebApp, שימוש Credits או חיבור BYOK.
2. מצב ה-Sandbox הנוכחי מספק גבול Zero-spend תפעולי כל עוד אין Upgrade, Paid quota או API key, ונבדק Drift לפני כל Run. זהו Control מבוסס מצב UI ולא Hard Cap כספי חוזי.
3. ברירות המחדל אינן מאושרות אוטומטית: `gpt-5`, `text-embedding-3-small` ו-`qwen3-rerank` אינם Selection של ה-Prototype.
4. Candidate `R-A` דורש `no reranking`, ולכן אסור להפעיל את ברירת המחדל `qwen3-rerank`.
5. Built-in tools קיימים ב-Workspace גם ללא Install; לפיכך KA-107 ייאכף ברמת App/Workflow באמצעות אפס Tool nodes ואפס Tool attachments.
6. אין כיום Publication לבדיקה מפני שאין App. לפני כל Runtime עתידי יש לאמת שוב `0 public links` או Studio-only Preview.

## Remaining Blockers Before K3.3

- בחירה ואישור של App type ושל Generation/Embedding models; `R-A` נשאר ללא Rerank.
- הגדרת Drift control מול `Auto-update Latest` וגרסאות Provider plugins.
- Manual reconstruction runbook שמכסה App, Knowledge metadata, Retrieval settings ו-restore order.
- החלטה אם לקבל את Integration permission `Everyone` עבור Workspace של Member יחיד או לאשר שינוי ל-`No one`/`Admins`.
- ניסוח Authorization מצומצם שמפריד בין יצירת Resources, Indexing ו-Runtime; אין לאשר אותם כמקשה אחת.

## Decision

- `k3_2c`: `complete`
- `k3_3`: `no-go`
- `smallest_safe_next_step`: הכנת חבילת Closure מקומית בלבד ל-Model/App selection, Drift controls, reconstruction runbook ו-K3.3 staged authorization; ללא שינוי ב-Dify.
