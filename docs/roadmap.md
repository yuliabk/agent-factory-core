# תוכנית עבודה

קצב מתוכנן: 6-10 שעות בשבוע.

## Phase 0 - Architecture and OpenSpec

משך: שבוע 1

- לאשר Scope, גבולות וסוגי סוכנים.
- לאשר ארכיטקטורת Control Plane ו-Client Data Plane.
- לאשר מודל אבטחה ומגבלות MVP.
- לאשר זהות, הרשאות, בידוד לקוחות ומחזור חיי מופע.
- לאשר Release manifest, טיפול ב-Drift וגבולות Rollback.
- להחליט ב-ADR-001, ADR-002 ו-ADR-003.
- לבחור החלטות פתוחות הנדרשות ל-Prototype.

תוצר: Architecture Baseline ו-ADRs מאושרים ב-Gate G0, ללא קוד או חיבורי Runtime.

## Phase 1 - Knowledge Agent Prototype

משך: שבועות 2-3

- להקים סביבת Dify ניסיונית.
- לטעון מסמכים סינתטיים.
- להגדיר תשובות עם מקורות ו-Fallback.
- לבנות 20-30 שאלות Evaluation.

תוצר: סוכן ידע באתר בדיקה.

## Phase 2 - Action and Service Workflow

משך: שבועות 4-5

- להקים n8n בסביבת בדיקה.
- לחבר פעולה פנימית אחת הפיכה.
- להוסיף Approval Gate, Audit ו-Escalation.
- לחבר דוא"ל כ-Draft בלבד.

תוצר: סוכן שמציע ומבצע פעולה מאושרת.

## Phase 3 - Hardening and Packaging

משך: שבועות 6-7

- לבצע Security Review ו-Prompt Injection tests.
- להוסיף Monitoring, Cost limits ו-Runbook.
- להשלים Client Intake ו-Clone checklist.
- לבדוק Recovery ו-Deletion.

תוצר: תבנית הניתנת לשכפול עבור לקוח ראשון.

## Phase 4 - WhatsApp Pilot

משך: שבוע 8 ואילך

- לבחור ספק וארכיטקטורת Consent.
- להגדיר Templates ו-Handoff לאדם.
- לבצע פיילוט עם מידע לא רגיש.

תוצר: ערוץ WhatsApp מבוקר, לאחר אישור נפרד.

## שערי החלטה

| Gate | החלטה | מאשר | סטטוס |
|---|---|---|---|
| G0 | אישור ארכיטקטורה | Owner | Approved — 2026-08-20 |
| G1 | אישור Prototype | Owner | Pending |
| G2 | אישור פעולה אוטומטית | Owner + Process Owner | Pending |
| G3 | אישור מידע אישי או חסוי | Security/Privacy Owner | Pending |
| G4 | אישור Production | Owner + Client | Pending |

