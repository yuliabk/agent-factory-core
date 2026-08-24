# Agent Factory Core

תשתית פרטית לבנייה, בדיקה ושכפול של סוכני AI באמצעות Spec-Driven Development ו-OpenSpec.

המאגר נמצא כרגע בשלב ארכיטקטורה בלבד. אין בו סוכן פעיל, חיבורי Production או מידע אמיתי של לקוחות.

## מטרת המערכת

לבנות תבנית Low-Code שניתן להתאים לשלושה סוגי סוכנים:

- סוכן ידע המבוסס על מסמכים.
- סוכן שירות לקוחות באתר, בדוא"ל ובהמשך ב-WhatsApp.
- סוכן פעולה שמבצע אוטומציות בין מערכות תחת בקרות ואישורים.

המערכת מפרידה בין שכבת ה-Factory, שבה נשמרים מפרטים ותבניות, לבין Instance נפרד לכל לקוח. ההפרדה מונעת זליגת מידע ומאפשרת שכפול מבוקר.

## כללי עבודה

1. כל שינוי מתחיל בתיקיית `openspec/changes/`.
2. תחילה כותבים `proposal.md`, `design.md`, Spec Delta ו-`tasks.md`.
3. Codex אינו מממש קוד לפני אישור מפורש של Owner.
4. MVP משתמש רק בנתונים סינתטיים או לא רגישים.
5. Skills חיצוניים אינם מיובאים לפני בדיקת רישיון וסריקת אבטחה.

## מבנה המאגר

```text
AGENTS.md                         הנחיות קבועות ל-Codex
openspec/                         מקור האמת לדרישות ולשינויים
docs/                             ארכיטקטורה, אבטחה, תקציב ותוכנית עבודה
templates/                        טפסים לשכפול סוכן עבור לקוח
.agents/skills/                   Skills מקומיים של המאגר
```

החלטות ארכיטקטורה מוצעות מתועדות ב-`docs/adr-*.md`. מסמך ADR במצב `Proposed` אינו אישור למימוש; הוא נכנס לתוקף רק לאחר החלטת Owner ושינוי הסטטוס ל-`Accepted`.

## מצב נוכחי

- שלב: Architecture Baseline approved at Gate G0; detailed Prototype planning is next
- Change פעיל: `openspec/changes/agent-factory-v1/`
- קצב עבודה מתוכנן: 6-10 שעות בשבוע
- תקציב ניסוי: 200-500 ₪ בחודש
- החלטת מימוש: לא ניתנה; כל קבוצת משימות דורשת אישור Owner מפורש
- ADRs מאושרים: ADR-001, ADR-002, ADR-003, ADR-004

## התחלה עם Codex

```text
Read AGENTS.md and openspec/changes/agent-factory-v1/.
Review the architecture only. Do not implement code.
List contradictions, missing decisions, security risks, and proposed spec edits.
Stop for Owner approval.
```

