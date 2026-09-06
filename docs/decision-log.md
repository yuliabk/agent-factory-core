# Architecture Decision Log

מסמך זה אינו מחליף ADR. הוא משמש אינדקס קצר כדי לדעת במהירות מה כבר סוכם ומה עדיין פתוח.

## 2026-09-06

| Decision | Status | ADR / Doc |
|---|---|---|
| Agent Factory Core הוא Platform Control Plane, לא Agent עסקי | Agreed direction; documented in main | ADR-005 |
| כל Agent עסקי יהיה בריפו נפרד | Agreed direction; documented in main | ADR-005 |
| Core מחזיק Contracts ומנגנונים משותפים: security, tools, memory, orchestration, budget, observability | Agreed direction; documented in main | architecture.md |
| Agent-to-Agent דרך Capability Registry ולא direct calls | Agreed direction; documented in main | ADR-006 |
| Model/Provider אינם hard-coded ב-Agent | Agreed direction; documented in main | ADR-007 |
| Model Router בוחר לפי profile, cost, privacy, quality ו-availability | Agreed direction; documented in main | provider-and-cost-policy.md |
| Agent נבנה מ-Template + Manifest + Client Spec | Agreed direction; documented in main | architecture.md |
| Manifest כולל permissions, budget, model policy, tools, memory, security, runtime limits, audit | Agreed direction; documented in main | agent-manifest.md |
| Permissions ו-limits מוצעים על ידי builder/master flow ומאושרים על ידי Owner בזמן Build | Agreed direction; documented in main | agent-lifecycle.md |
| Business budget הוא warn-and-approve, לא silent overrun | Agreed direction; documented in main | ADR-008 |
| Runtime budget overage מאושר על ידי גורם מאושר אצל הלקוח | Agreed direction; documented in main | ADR-008 |
| Emergency safety cap נפרד מ-business budget | Agreed direction; ADR acceptance pending | provider-and-cost-policy.md |
| Client UX הוא Black Box טכני אך שקוף לגבי scope, assumptions, services, cost ו-approvals | Accepted | platform-vision.md |
| Intake רגיל מכוון לפחות מ-10 דקות ובדרך כלל 5-6 שאלות קריטיות; זה UX target ולא hard limit | Accepted | platform-vision.md |
| ה-Intake שואל מינימום שאלות קריטיות ומשלים assumptions לא קריטיות | Accepted | platform-vision.md |
| בבקשה עמומה ה-Factory רשאי infer configuration סביר ואז להציג assumptions ל-confirm/correct | Accepted | platform-vision.md |
| Progressive complexity: מתחילים ב-Agent הפשוט ביותר שמספק outcome ורק אז מוסיפים autonomy/integrations/premium models | Accepted | platform-vision.md |
| Research/Brain Agent יהיה Agent נפרד ומשותף לכל המערכת | Agreed direction; planned | roadmap.md |
| Research Agent יבחר בין internal knowledge, web, API, MCP ו-approved capabilities | Agreed direction; planned | roadmap.md |
| Travel Agent יהיה consumer ראשון לבדיקת reusability | Planned after Core gate | roadmap.md |

## החלטות פתוחות

1. איפה יישמרו בפועל Template packages מעבר ל-base templates: בתוך Core, package registry או repos נפרדים.
2. Schema format סופי ל-Agent Manifest: JSON Schema, Pydantic, OpenAPI-derived או שילוב.
3. ה-implementation הראשון של Capability Registry: in-process registry, DB-backed registry או service נפרד.
4. Provider adapters הראשונים שישמשו portability test.
5. Cost currency normalization ו-source of pricing.
6. מהו emergency safety cap default לכל סוג workload.
7. Memory backend contract המדויק והאם יהיה service עצמאי בשלב ראשון.
8. אילו Security checks יהיו blocking ב-local development לעומת CI/release.
9. כיצד לייצג client approval identities בכל channel.
10. היכן יישב Factory client-facing UI ביחס ל-Core repo.
