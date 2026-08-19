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

