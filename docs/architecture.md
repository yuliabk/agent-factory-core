# ארכיטקטורת Agent Factory Core

**Status:** Accepted after Owner Review  
**Date:** 2026-09-06

## 1. מטרת המערכת

`Agent Factory Core` הוא שכבת הפלטפורמה והחוזה המשותף לכל Agent שנבנה על המערכת. הוא אינו Agent עסקי בפני עצמו ואינו מכיל לוגיקה ספציפית של Travel, Sales, CRM, Research או לקוח מסוים.

המטרה היא לאפשר לבנות, להחליף, לתקן ולתחזק Agents במהירות, בלי לשנות את כל המערכת כאשר Provider, Model, Tool, Runtime או דרישת לקוח משתנים.

העיקרון המנחה הוא:

> שינוי באחריות אחת צריך להיות מקומי ככל האפשר. לשאלה "איפה משנים את זה?" צריכה להיות בדרך כלל תשובה אחת ברורה.

## 2. חלוקת אחריות

### Core אחראי על

- Spec compilation ו-Agent Manifest validation.
- Template selection והרכבת Agent.
- Orchestration ו-Execution Context.
- Capability Registry וניתוב בין Agents.
- Model/Provider routing.
- Tool Gateway והרשאות לכלי.
- Memory contracts ו-Memory access policy.
- Security policy, tenant isolation ו-data controls.
- Budget, quota ו-cost guardrails.
- Audit, observability, traces ו-release evidence.
- Evaluations, release gates, rollback ו-drift detection.
- Runtime adapters וחוזים משותפים.

### Core אינו אחראי על

- Prompts עסקיים של Agent ספציפי.
- Workflow עסקי ייחודי ללקוח.
- Knowledge base של לקוח.
- Credentials של לקוח.
- Business rules שאינם כלל פלטפורמה.
- UI עסקי ייחודי ל-Agent מסוים.

### כל Agent repo אחראי על

- Business intent ו-Scope.
- Agent-specific behavior.
- Capabilities שהוא מספק ודורש.
- Agent-specific tools או adapters שאינם כלליים.
- Acceptance tests ו-evaluation set שלו.
- Reusable Agent Definition, ללא Secrets, PII או Client-specific business state.

## 3. מבנה לוגי של המערכת

`Agent Factory Core` נשאר בשלב הראשון Project/Repository אחד, אך מתחלק ארכיטקטונית לשני Planes נפרדים עם אחריות ברורה. ההפרדה היא Contract boundary ולכן בעתיד אפשר יהיה לפצל אותם פיזית בלי לשנות Business Agents.

### Build / Control Plane

אחראי על מה שקורה לפני Release:

- Client Intent ו-Spec compilation.
- Template Engine.
- Manifest validation.
- Policy/contract compilation.
- Evaluation planning ותוצאות Release.
- Release manifests ו-versioning.
- Registry metadata ו-contract versions.

### Runtime Governance Plane

אחראי על אכיפת כללים בזמן invocation:

- Orchestrator.
- Execution Context.
- Policy Engine.
- Capability routing.
- Model routing.
- Tool Gateway.
- Memory Gateway/Broker.
- Budget Guard.
- Runtime limits.
- Audit, traces ו-runtime evidence.

### Agent Repositories

מחזיקים את ה-Agent Definitions העסקיים והגרסאות שלהם, ולא את מנגנוני ה-Core.

### Client Data Plane

מחזיק את נתוני הלקוח בפועל, Secrets, business state, knowledge, channels ו-tenant-scoped audit/storage.

```mermaid
flowchart TB
    subgraph BCP["Build / Control Plane - Agent Factory Core"]
        INTAKE["Intent + Spec Compiler"]
        TMP["Template Engine"]
        MAN["Manifest Validator"]
        REL["Evals + Release Builder"]
        META["Registry + Contract Metadata"]
    end

    subgraph RGP["Runtime Governance Plane - Agent Factory Core"]
        ORCH["Orchestrator"]
        POL["Security + Policy Engine"]
        REG["Capability Router"]
        MR["Model Router"]
        TG["Tool Gateway"]
        MEM["Memory Gateway"]
        BUD["Budget + Runtime Guard"]
        OBS["Audit + Observability"]
    end

    subgraph AR["Agent Repositories"]
        A1["Research Agent Definition"]
        A2["Travel Agent Definition"]
        A3["Sales Agent Definition"]
        A4["Future Agent Definitions"]
    end

    subgraph DP["Client Data Plane"]
        DATA["Client Data + Knowledge + State"]
        SEC["Client Secrets"]
        CHANNELS["Channels + Systems"]
        LOGS["Tenant Audit Partition"]
    end

    INTAKE --> TMP --> MAN --> REL
    MAN --> META
    REL --> ORCH
    POL --> ORCH
    BUD --> ORCH
    ORCH --> REG
    ORCH --> MR
    ORCH --> TG
    ORCH --> MEM
    ORCH --> OBS
    META --> REG
    REG --> A1
    REG --> A2
    REG --> A3
    REG --> A4
    TG --> CHANNELS
    MEM --> DATA
    POL --> SEC
    OBS --> LOGS
```

## 4. Agent Definition, Client Instance ו-Deployed Agent Instance

יש להפריד בין Agent reusable לבין מופע לקוח:

```text
Agent Definition
        +
Client Instance Configuration
        +
Core Policy/Contract Versions
        =
Deployed Agent Instance
```

### Agent Definition

נמצא ב-Agent repository וכולל:

- Agent identity ו-version.
- Business scope ו-behavior.
- Capabilities provided/required.
- Agent-specific prompt/workflow logic.
- Agent-specific evals ו-acceptance tests.
- Manifest defaults שאינם Client-specific.

### Client Instance Configuration

מכיל רק את ההתאמה ללקוח:

- Tenant identity ו-environment.
- Permissions ו-approval routes.
- Budget profile.
- Enabled tools/capabilities.
- Provider/model profile.
- Data-source references.
- Memory/retention policy.
- Channels ו-client-specific constraints.

Secrets עצמם אינם נשמרים ב-Agent repo או ב-Manifest. נשמרים רק references מאושרים.

### Deployed Agent Instance

הוא Release קונקרטי שמחבר Agent Definition versioned, Client Instance Configuration, Core policy versions ו-adapter selections. כך ניתן להפעיל אותו Agent עבור כמה לקוחות בלי Fork של ה-Agent עצמו ובלי לערבב את נתוניהם.

## 5. Execution Context חובה

כל Agent invocation מקבל Context אחיד מה-Runtime Governance Plane. Agent אינו רשאי להמציא, להרחיב או לעקוף אותו.

```text
ExecutionContext
- request_id
- tenant_id
- actor_id
- actor_type
- environment
- agent_id
- agent_release_id
- permissions
- data_classification
- budget_context
- model_policy
- tool_policy
- memory_policy
- trace_id
- deadline
```

ה-Context הוא המקור להרשאה, תקציב, Traceability ו-Isolation. Prompt אינו מקור סמכות.

## 6. Agent Manifest

כל Agent חייב לספק Manifest תקין לפני Build או Runtime. ה-Manifest מתאר מה ה-Agent הוא, מה הוא יודע לעשות, מה הוא דורש ומה אסור לו לעשות.

ה-Core משתמש בו כדי:

- לבחור Template.
- לבדוק Capabilities.
- להחיל Security profile.
- לבחור Model/Provider policy.
- לחבר Tools ו-Memory.
- להגדיר Budget ו-approval routes.
- להריץ Evals ו-Release gates.

הסכמה המלאה מוגדרת ב-`docs/agent-manifest.md` וב-`templates/agent-manifest.yaml`.

## 7. Template-first

Agent חדש אינו נבנה מאפס.

תהליך ברירת המחדל:

`Client Intent -> Spec -> Template -> Manifest -> Adapters/Tools -> Evals -> Release`

ה-Core מחזיק את Template Engine ואת חוזי התבניות. תבניות מערכת בסיסיות יכולות להישמר ב-Core. תבניות Agent עסקיות גדולות יכולות להישמר כריפו או Package נפרד ולהירשם ב-Template Registry.

המטרה היא להימנע מ-Monorepo שבו כל Agent וכל Business Logic מתערבבים.

## 8. תקשורת בין Agents

Agents אינם קוראים זה לזה לפי URL, repo name או implementation detail. Agent מבקש Capability.

דוגמה:

```text
Travel Agent requires: research.lookup
Core resolves: Research Agent v1.3
```

ה-Runtime Governance Plane בודק לפני הניתוב:

- Tenant.
- Permissions.
- Data classification.
- Cost policy.
- Capability contract version.
- Availability ו-health.

כך ניתן להחליף Research Agent, להפעיל כמה implementations או לבצע fallback בלי לשנות את Travel Agent.

## 9. Provider ו-Model independence

Business logic אינו תלוי ישירות ב-OpenAI, Anthropic, Google, DeepSeek או Provider אחר.

Agent מבקש `Model Profile`, לדוגמה:

- `fast-cheap`
- `balanced`
- `high-reasoning`
- `private-data-compatible`
- `long-context`

ה-Model Router ממפה Profile ל-Provider ול-Model בפועל לפי Policy, תקציב, זמינות, latency, data requirements ו-quality target.

החלפת Provider אמורה להיות שינוי Policy/Configuration עם Regression Eval, לא Rewrite של Agent.

## 10. Tool Gateway

Agent אינו מקבל גישה חופשית ל-Network, Files, Database או SaaS.

כל Tool invocation עובר דרך Tool Gateway שמבצע:

1. Schema validation.
2. Permission check.
3. Tenant check.
4. Side-effect classification.
5. Budget/preflight check כאשר רלוונטי.
6. Human approval כאשר נדרש.
7. Timeout ו-retry policy.
8. Audit event.

Web, MCP, API ו-Agent-to-Agent הם כולם מקורות חיצוניים מבחינת Trust Model. תוכן שמוחזר מהם נחשב Untrusted Data עד Policy evaluation.

## 11. Memory Gateway

Memory אינה API ישיר של Agent ל-Storage. ה-Core מספק חוזה Memory אחיד:

- Session memory.
- User-approved persistent memory.
- Client knowledge retrieval.
- Operational state.

כל read/write נבדק לפי Tenant, Classification, Purpose, Retention ו-Permissions.

Agent-specific memory strategy יכולה להשתנות, אבל אינה יכולה לעקוף Isolation או Retention.

## 12. Security as a platform invariant

Security אינו Feature אופציונלי של Agent.

ה-Core אוכף לפחות:

- Least privilege.
- Default deny.
- Tenant isolation.
- Secrets boundary.
- Prompt injection containment.
- Tool allowlists.
- Egress controls לפי סיכון.
- Human approval לפעולות מוגנות.
- Audit trail.
- Budget guardrails.
- Runtime limits.

Agent repo רשאי להחמיר Policy. הוא אינו רשאי להחליש Minimum Baseline.

## 13. Budget as a first-class control

יש להפריד בין שני סוגי גבול:

1. **Business budget** - גבול שנקבע עם הלקוח. המערכת מתריעה ומתבקשת הרשאה מפורשת לפני חריגה.
2. **Emergency safety cap** - תקרת בטיחות תפעולית שמונעת runaway spend או loop חריג. היא מוגדרת על ידי הפלטפורמה ואינה תחליף לתקציב העסקי.

ב-Build time ה-Owner מאשר את פרופיל העלות והחלופות. ב-Runtime הלקוח או גורם מאושר אצלו מאשר חריגה מתקציב שהוגדר לו.

## 14. Client-facing Black Box

הלקוח אינו אמור לבחור MCP, API, Model, Vector DB או Runtime.

הוא מתאר מטרה עסקית בשפה רגילה. הפלטפורמה:

1. מזהה Intent.
2. שואלת רק שאלות קריטיות.
3. משלימה הנחות לא קריטיות ומציגה אותן לאישור.
4. מציעה חלופות לפי תקציב.
5. יוצרת Spec ו-Manifest.
6. בונה ומעריכה Agent.
7. מציגה ללקוח את התוצאה, מגבלות, מחיר משוער ואישורים נדרשים.

יעד UX ראשוני: רוב ה-Intake הראשוני מסתיים בפחות מ-10 דקות. זהו יעד UX ולא hard runtime rule.

## 15. Client Data Plane

לכל לקוח נשמרים גבולות נפרדים עבור:

- Identity ו-Roles.
- Runtime context.
- Knowledge ו-State.
- Credentials.
- Audit.
- Evaluation data.
- Retention ו-deletion.

מידע לקוח ו-Secrets אינם חוזרים ל-Build/Control Plane כ-raw data. ה-Core מחזיק Metadata ו-Evidence נדרשים בלבד. Runtime Governance יכול לפעול על references והרשאות לפי הצורך, אך אינו הופך למאגר משותף של Client Data.

## 16. Release contract

כל Release מזוהה באמצעות `agent_release_id` ומקושר ל:

- Agent Definition version.
- Client Instance Configuration version.
- Agent Manifest version.
- OpenSpec change.
- Commit SHA.
- Template version.
- Policy versions.
- Model routing profile.
- Tool contract versions.
- Eval results.
- Security evidence.
- Human approvals.
- Rollback target.

Runtime drift שאינו מיוצג ב-Release contract חוסם Promotion.

## 17. גבולות MVP של ה-Core

בשלב הראשון ה-Core צריך להוכיח רק את החוזים הקריטיים:

- Manifest validation.
- Execution Context.
- Security/permission gate.
- Budget precheck.
- Provider-neutral model call.
- Capability registration/resolution.
- Audit event.
- Eval gate בסיסי.

אין צורך ב-MVP ב-Kubernetes, Service Mesh, multi-region או distributed agent bus מורכב.

## 18. Agent הבא לאחר ייצוב ה-Core

ה-Agent הראשון שנבנה לפי החוזים החדשים יהיה Research/Brain Agent בריפו נפרד.

הוא יספק Capability כללית כגון `research.lookup` ויחליט, תחת Policy, האם להשתמש ב:

- Knowledge פנימי.
- Web search.
- API.
- MCP.
- Agent אחר.
- Model knowledge כאשר מותר ומתאים.

Travel Agent ישמש בהמשך Consumer ראשון של Capability זו כדי לבדוק שה-Core אכן מאפשר שימוש חוזר ולא תלות ב-Provider יחיד.
