# Proposal: Prototype Portfolio V1

## Summary

להגדיר תיק הוכחה מקומי ומבוסס OpenSpec לשלושה דפוסי סוכן: `Knowledge`, ‏`Customer Service` ו־`Controlled Action`. התיק יוכיח שה־Agent Factory מסוגלת לעבור באופן חוזר מ־Intake למפרט, תכנון תצורה, Evaluation וראיות — תוך בידוד מלא בין ארגונים סינתטיים וללא תלות באישור Runtime בשלב התכנון.

## Why

פרוטוטייפ הידע של `AF Demo Services` הוכיח Smoke Flow אחד עם Retrieval וציטוטים, אך אינו מוכיח לבדו שה־Factory ניתנת לשימוש חוזר עבור סוגי סוכנים ותהליכים שונים. נדרש Portfolio קטן שמודד שימוש חוזר, בידוד, איכות, עלות, זמן הקמה ושערי אישור, בלי לבלבל בין Smoke Evidence לבין Release או Production Readiness.

## Capability Classification

- `Knowledge`: Reference pattern קיים עבור `af-demo-services`.
- `Customer Service`: דפוס חדש עבור tenant סינתטי `af-demo-retail`.
- `Controlled Action`: דפוס חדש עבור tenant סינתטי `af-demo-operations`.
- Combination: מחוץ להיקף V1; כל דפוס נמדד בנפרד כדי לשמור על Attribution ברור.

## Portfolio Members

| Pattern | Synthetic tenant | Bounded use case | Proof target |
|---|---|---|---|
| `Knowledge` | `af-demo-services` | מענה בעברית ממקורות מאושרים עם ציטוטים ו־Fallback | Grounding, provenance ו־fail-closed evidence |
| `Customer Service` | `af-demo-retail` | סיווג פניות שירות סינתטיות, איסוף מידע חסר, תשובת מדיניות והסלמה ל־Owner | Routing, clarification, refusal ו־human escalation ללא שליחה חיצונית |
| `Controlled Action` | `af-demo-operations` | הכנת Draft של בקשת ציוד משרדית סינתטית והצגתה לאישור | Action proposal, approval boundary, idempotency ו־audit ללא ביצוע חיצוני |

## In Scope

- Intake סינתטי וממוזער לכל Prototype.
- חוזה משותף לזהות, tenant, release, cost, audit ו־evaluation.
- Spec delta נפרד להתנהגות Service ולהתנהגות Controlled Action.
- מטריצת שימוש חוזר המבחינה בין Factory assets משותפים לבין דלתאות Prototype.
- Evaluation sets קטנים ומדורגים ל־Smoke, כולל הצלחה, כשל, חוסר מידע, Prompt Injection, Cross-tenant ו־Authorization.
- מדדי זמן הקמה, איכות, בטיחות, בידוד, שימוש חוזר ועלות.
- שערי אישור נפרדים לתכנון, Materialization מקומי, Provider configuration, Runtime ו־Portfolio review.
- Case-study evidence plan שאינו כולל פרטי חשבון, Secrets או מידע אמיתי.

## Out of Scope

- שינוי ב־Dify או שימוש נוסף ב־Dify Credits.
- שימוש ב־Botpress כל עוד הוא ב־`INCIDENT-HOLD`.
- n8n, Tool, Connector, Email, WhatsApp או מערכת חיצונית.
- Runtime, Model call, Indexing, Upload, Publish או Payment.
- Credentials, API keys, חשבונות חדשים או שינוי Workspace.
- פעולה עסקית אמיתית, Purchase, הודעה, רשומה, Refund או שינוי הרשאה.
- מידע אישי, חסוי, רפואי, פיננסי או נתוני לקוח אמיתי.
- Gate G1, Production, External users או טענה שהמערכת מוכנה למסירה ללקוח.
- Commit, Push, Pull, Fetch, Merge, Checkout או יצירת ענף במסגרת אישור התכנון הנוכחי.

## Success Criteria

- שלושת הדפוסים משתמשים באותו Control Plane של Git/OpenSpec ובחוזי Factory משותפים, וכל דלתא התנהגותית מתועדת במפורש.
- לכל tenant קיימת זהות נפרדת, corpus/fixtures נפרדים, evaluation records נפרדים ודרישת data-plane isolation נפרדת.
- 100% מתרחישי Cross-tenant נחסמים ללא חשיפת תוכן או metadata זר.
- 100% מתרחישי פעולה מוגנת נעצרים לפני ביצוע ללא Approval תקף.
- 100% מתרחישי Safety החובה — Injection, unauthorized action, foreign tenant ו־sensitive data — עוברים לפני כל Runtime gate.
- כל Prototype חדש עושה שימוש חוזר בלפחות חמישה נכסי Factory מאושרים: Intake, release identity, cost gate, minimized audit schema ו־evaluation contract.
- יעד זמן התכנון לכל Prototype חדש הוא עד שמונה שעות Owner/Codex, ללא זמני המתנה לספק וללא Runtime execution.
- כל Smoke plan מגדיר לפחות עשרה תרחישים, request ceiling, stop conditions ו־cost indicator לפני אישור Runtime.
- כל הראיות מבדילות בין `planned`, ‏`dry_validated`, ‏`smoke_passed` ו־`release_approved` ואינן מקדמות סטטוס ללא Gate מתאים.
- Portfolio review מפיק Scorecard אחיד עם זמן, reuse, איכות, safety, isolation, cost ו־open risks לכל דפוס.

## Cost Impact

- עלות התכנון המקומי המאושר: `0 ILS` ו־`0 provider requests`.
- אין תקציב Runtime מאושר במסגרת שינוי זה.
- כל Runtime עתידי יחייב Gate נפרד עם ceiling לבקשות, עלות מדידה ו־Owner-approved cap.
- מעטפת הניסוי העתידית המומלצת לכל ה־Portfolio היא עד `100 ILS/month`, בכפוף לתקרת הפרויקט הכוללת `200–500 ILS/month`; ההמלצה אינה הרשאת הוצאה.
- כאשר Credit balance, price, hard stop או combined provider cost אינם מאומתים, Runtime נשאר חסום.

## Security and Privacy Impact

- כל הנתונים סינתטיים בלבד.
- אין שיתוף Corpus, storage, index, logs, credentials או evaluation records בין tenants.
- `Controlled Action` מפיק Draft בלבד; גם Approval סינתטי אינו מפעיל מערכת חיצונית במסגרת V1.
- Audit ממוזער כולל `tenant_id`, ‏`actor_id`, ‏`request_id`, ‏`decision`, ‏`approval_reference`, ‏`proposed_action`, ‏`result` ו־`timestamp` ללא Prompt מלא או מידע אישי.
- כל Tool או Runtime שלא אושר מוגדר `deny-by-default`.

## Risks

- נתונים סינתטיים עלולים להציג איכות גבוהה יותר מהמציאות.
- שלושה Smoke Prototypes עלולים ליצור תחושת כיסוי שגויה אם לא נשמרת הבחנה מול Gate G1.
- מדד reuse עלול להיות מנופח אם קבצים משוכפלים במקום להפנות לחוזים משותפים.
- Controlled Action עלול להיראות כפעולה אמיתית אם Draft, Approval ו־Execution אינם מופרדים במפורש.
- ספק יחיד עלול להטות את ההוכחה; Portability תימדד בשלב זה בחוזים וב־dry validation בלבד.
- Botpress אינו מועמד לביצוע כל עוד מצב האירוע אינו נפתר באישור נפרד.

## Approval Gates

| Gate | Meaning | Explicit exclusions |
|---|---|---|
| `PF-G0` | אישור Portfolio plan והחלטות התכנון בלבד | ללא Materialization, provider או Runtime |
| `PF-G1-K` | קבלת ראיות Knowledge הקיימות כ־reference evidence בלבד | ללא Runtime נוסף או Gate G1 |
| `PF-G1-S` | אישור Materialization מקומי של Service fixtures, contracts ו־evaluation | ללא provider או שליחה |
| `PF-G1-A` | אישור Materialization מקומי של Action drafts, approval fixtures ו־evaluation | ללא Tool או execution |
| `PF-G2-S` | אישור Provider mapping ו־Smoke Runtime נפרד ל־Service | דורש provider, request ו־cost ceiling מפורשים |
| `PF-G2-A` | אישור Dry/Smoke Runtime נפרד ל־Controlled Action | execution חיצוני נשאר אסור |
| `PF-G3` | Review של Scorecard והחלטה אם ה־Factory proof מספק | אינו Gate G1, G2 או Production approval |

## Expected Impact

- הוכחה מדידה שה־Factory מייצרת יותר מסוג סוכן אחד.
- בסיס להצגת Case Study ללקוחות בלי להשתמש בנתוני לקוח.
- זיהוי מוקדם של assets משותפים מול התאמות ייעודיות.
- בסיס להחלטה אם להשקיע בהערכת 25 שאלות, ב־Runtime נוסף או ב־Packaging ללקוח ראשון.

## Approval Status

- `change_id`: `prototype-portfolio-v1`
- `current_status`: `PF-G1-S_approved_local_materialization_only`
- `authorized_by`: `Owner (Yulush)`
- `approval_date`: `2026-08-24`
- `authorization_scope`: `PF-G1-S` בלבד — Materialization מקומי של Intake, מדיניות, cases, contracts ו־evaluation סינתטיים עבור `af-demo-retail`, כולל dry validation ללא ספק.
- `forbidden`: Dify, Botpress, n8n, network, model, provider, Runtime, Credentials, Payment, Indexing, external message, Ticket creation, Publish, Commit ו־Push.
- `next_gate`: לאחר dry validation, החלטה נפרדת אם לאשר `PF-G1-A` או להציע `PF-G2-S`; אף אחד מהם אינו מאושר כעת.

`PF-G0` נשאר בסיס התכנון המאושר. אישור `PF-G1-K` מאמץ רק את הראיות המקומיות הקיימות ואינו מרחיב אותן: שאלה נתמכת אחת יכולה לקבל `smoke_passed`, בעוד Gate G1, הערכת 25 השאלות וכל קטגוריה שלא נבדקה נשארים פתוחים או `not_run`.

אישור `PF-G1-S` מתיר רק יצירה ובדיקה מקומית של חבילת Service סינתטית. גם תוצאת dry validation מלאה אינה מוכיחה איכות מודל, Retrieval, Runtime, שליחת הודעה או Release readiness.

### Approval History

| Gate | Date | Result | Boundary |
|---|---|---|---|
| `PF-G0` | `2026-08-24` | `approved_planning_baseline_only` | ללא Materialization, provider או Runtime |
| `PF-G1-K` | `2026-08-24` | `approved_reference_evidence_only` | קישור מקומי בלבד; ללא Runtime נוסף, Gate G1 או שינוי ספק |
| `PF-G1-S` | `2026-08-24` | `approved_local_materialization_only` | נתונים סינתטיים ו־dry validation מקומי בלבד; ללא provider, Runtime או פעולה חיצונית |
