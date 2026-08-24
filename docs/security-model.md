# מודל אבטחה ופרטיות

## 1. סיווג מידע

| רמה | דוגמאות | שימוש ב-MVP | בקרות מינימום |
|---|---|---:|---|
| Public | תוכן אתר ונהלים פומביים | כן | בקרת מקור ושינויים |
| Internal | נהלים ומסמכים עסקיים רגילים | רק בפיילוט מוגבל | הרשאות, Encryption ו-Logs |
| Confidential | אסטרטגיה, חוזים ומידע עסקי חסוי | לא לפני Security Review | בידוד לקוח, DPA, Retention, Audit |
| Personal | פרטי קשר ונתוני לקוח | לא ב-MVP הראשוני | Consent, מינימיזציה, מחיקה והרשאות |
| Sensitive | מידע רפואי או פיננסי | לא במסלול MVP | מסלול Enterprise נפרד ובדיקה משפטית ואבטחתית |

## 2. עקרונות

- Least Privilege לכל משתמש, Connector ו-Workflow.
- Data Minimization: לאסוף רק את המידע הנדרש לביצוע המטרה.
- Tenant Isolation: הפרדה מלאה בין לקוחות.
- Human-in-the-Loop לפעולות בעלות סיכון או השפעה חיצונית.
- Defense in Depth: בקרות ברמת Channel, Agent, Workflow, Storage ו-Provider.
- Traceability: אפשרות להבין מה התבצע, על סמך איזה קלט ובאמצעות איזה כלי.

## 3. בקרות לפי שכבה

### GitHub ו-OpenSpec

- Repository פרטי.
- Branch Protection לאחר הקמת CI.
- Pull Request לכל שינוי מהותי.
- Secret scanning ו-Dependency review כאשר יתווסף קוד.

### Dify

- Project נפרד לכל לקוח.
- Knowledge Base נפרד והרשאות מסמך מוגדרות.
- הגנת Prompt Injection והפרדת System Instructions ממסמכים.
- הגבלת Context והסרת PII לפי צורך.

### n8n

- Credentials נפרדים לכל לקוח.
- Workflow נפרד לכל פעולה עסקית משמעותית.
- Idempotency Key לפעולות חוזרות.
- Timeout, Retry מוגבל ו-Dead-letter path.
- Approval Gate לפני פעולות מסוכנות.

### Providers ו-Storage

- Encryption in transit and at rest.
- Region ו-Retention מתועדים.
- DPA או תנאים חוזיים מתאימים לפני מידע חסוי או אישי.
- מחיקה ניתנת לאימות.

## 4. פעולות המחייבות אישור אנושי

- שליחת הודעה חיצונית בשם ארגון, אלא אם מדובר בתבנית שאושרה מראש.
- מחיקה או שינוי של רשומה עסקית.
- התחייבות כספית, Refund, תשלום או שינוי חיוב.
- החלטה רפואית, פיננסית, משפטית או זכאותית.
- שינוי הרשאות משתמש.
- העברת מידע בין מערכות או בין לקוחות.

## 5. שער כניסה ל-Production

אין להפעיל לקוח אמיתי לפני שכל התנאים הבאים מתקיימים:

- Data Inventory ו-Data Flow מאושרים.
- Threat Model ו-Prompt Injection Review הושלמו.
- Access Control, Retention ו-Deletion נבדקו.
- Evaluation Set כולל מקרי תקיפה וכשל.
- Incident Response Owner מוגדר.
- Backup ו-Restore נבדקו.
- הלקוח אישר את ה-Scope ואת מגבלות הסוכן.

## 6. זהות והרשאות

- הרשאות נגזרות מ-Role ומ-Policy מאושרים; Prompt או תשובת מודל אינם מעניקים הרשאה.
- משתמש אנושי ו-Service Account מזוהים בנפרד ונרשמים ב-Audit.
- כל Credential מוגבל ללקוח, Environment ופעולות נדרשות בלבד.
- גישת Admin ניתנת לזמן מוגבל ככל האפשר ונבדקת תקופתית.
- Approval לפעולה מוגנת כולל מאשר, פעולה, יעד, `request_id`, זמן ותפוגה.

## 7. Threat Model מינימלי

לפני Pilot בודקים לפחות:

- Prompt injection ממסמך, אתר, הודעה או Tool output.
- Cross-tenant retrieval, logs, cache, export ו-Credentials.
- Broken authorization ו-Approval replay.
- Data exfiltration דרך תשובה, Tool, URL או Log.
- Secret exposure ב-Prompt, Export, Screenshot או Error message.
- Duplicate או forged action request.
- ספק חיצוני לא זמין או מחזיר תוכן זדוני.
- שינוי Runtime ידני שאינו תואם Release מאושר.

## 8. Audit, Retention ומחיקה

Audit event ממוזער כולל: `tenant_id`, `request_id`, `actor_id` או pseudonymous reference, `agent_release_id`, `action`, `policy_decision`, `approval_reference`, `tool`, `result`, `timestamp` ו-`environment`.

- אין לשמור Prompt מלא, מסמך מלא או Secret כברירת מחדל.
- לכל Data type מוגדרים Purpose, Owner, Retention, Access ו-Deletion method.
- מחיקה כוללת Primary storage, indexes, caches, exports ו-backups לפי חלון מתועד.
- Decommissioning מסתיים רק לאחר ביטול גישה וראיית מחיקה או החזרה ללקוח.

## 9. Secrets ושרשרת אספקה

- Secrets נשמרים ב-Credential store של הסביבה ולא ב-Git, OpenSpec, Prompt או Release manifest.
- Integrations ו-Skills חיצוניים נשארים חסומים עד Pinning, License review, Scan ו-Owner approval.
- שינוי Provider, Model major version או Tool schema מחייב Regression evaluation.

## 10. גיבוי, שחזור ותגובה לאירוע

- לפני Production מוגדרים RPO, RTO, Backup owner ו-Restore test לפי לקוח.
- באירוע חשוד עוצרים פעולות חיצוניות, משמרים Audit ממוזער, מסובבים Credentials לפי צורך ומפעילים Runbook.
- Rollback מחזיר ל-`agent_release_id` ידוע; הוא אינו משחזר אוטומטית פעולה עסקית שכבר בוצעה.
- Owner, Client Process Owner ו-Security/Privacy Owner מקבלים תחומי אחריות והסלמה מתועדים.

