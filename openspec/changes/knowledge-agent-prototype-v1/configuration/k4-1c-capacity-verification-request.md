# K4.1C Capacity and Configuration-Drift Read-only Verification Gate

## Status

- `gate_id`: `af-ka-01-k4-1c`
- `version`: `1.0.0`
- `date`: `2026-08-24`
- `status`: `pending_owner_approval`
- `data_scope`: `af-demo-services-he@1.0.0` synthetic only
- `current_authorized_stage`: `none`
- `prerequisite`: `configuration/k4-0-capacity-evaluation-plan.md` (complete)
- `blocks`: `K4.1, K4.2, K4.3` (Section 4, `tasks.md`) עד לאישור נפרד
- `requirements`: `KA-107, KA-108, KA-109, KA-110, KA-111`

## Purpose

מסמך זה הוא בקשת השער שהוגדרה ב-K4.0 (`Gate K4.1C`, ראו `k4-0-capacity-evaluation-plan.md` שורה 119) ועדיין לא אושרה. המסמך עצמו אינו מהווה הרשאה. הוא מנוסח כך שה-Owner יוכל לאשר אותו במדויק, במילים הזהות לאלו שמופיעות תחת "Exact Owner Approval Syntax" למטה, לפני כל בדיקה.

K4.1C הוא צעד ביניים חובה לפני K4.1 (Provisioning בפועל של ה-tenant הסינתטי). לפי תהליך העבודה המבוסס Stage שהוגדר ב-`k3-3-staged-authorization.md`, אין לדלג משלב תכנון מקומי (K4.0) ישירות לשלב מימוש חיצוני (K4.1) בלי לעבור קודם דרך שער אימות לקריאה בלבד.

## Why Codex/Claude Cannot Execute This Gate Autonomously

- הבדיקה מחייבת Login ידני ל-Dify Cloud (`cloud.dify.ai`) עם חשבון ה-Owner בפועל; לסוכן האוטומטי אין ואסור שיהיו לו Credentials של Dify.
- לסביבת העבודה הנוכחית אין הרשאת דפדפן מול חשבון Dify אמיתי; כל בדיקת UI קודמת (החל מ-K3.2c) בוצעה רק לאחר Login ידני שביצע ה-Owner בעצמו.
- לפי `AGENTS.md` ("Non-Negotiable Constraints"), פעולה חיצונית הדורשת Credential, Payment או Runtime מחייבת אישור אנושי מפורש ואינה מבוצעת אוטומטית או מנוחשת.
- לכן התוצר הזמין כרגע הוא בקשת השער המנוסחת במדויק, לא ביצוע הבדיקה עצמה.

## Bounded Scope — Text for Owner Approval

הפעולות היחידות המותרות תחת שער זה, לאחר אישור Owner מפורש:

1. Reload בלבד של ה-Workspace, ה-App וה-Knowledge Base הקיימים (ללא יצירה, מחיקה או שינוי).
2. אימות יתרת Credits נוכחית: נדרש `≥ 180` מתוך המכסה החודשית המחודשת.
3. אימות שה-Graph בן חמשת הצמתים (`User Input → Knowledge Retrieval → Citation Context → LLM 2 → Answer 2`), בחירת המודל, ה-Knowledge Base, ששת המסמכים (`AFD-001`–`AFD-006`), ה-`source_id` metadata, ה-Prompt וה-Corpus hashes תואמים בדיוק את התצורה המתועדת ב-Stage D3T (`k3-3-staged-authorization.md`) וב-`configuration/manifest.md`.
4. אימות שה-Workspace עדיין Sandbox, Membership `1/1` Owner-only, וללא Billing management גלוי, BYOK, Payment, Tool, Trigger או Publish.

### Forbidden Actions

`Runtime request, Preview, Test Run, Indexing, Upload, Payment, Upgrade, Subscription, Credential connection, Graph change, Prompt change, Publish, external Tool/Trigger` — אף אחת מאלו אינה כלולה בשער זה.

### Exact Owner Approval Syntax

> מאשרת K4.1C בלבד: Reload וקריאה בלבד של ה-Workspace, ה-App וה-Knowledge Base הקיימים כדי לאמת יתרת Credits ≥180 והתאמה מלאה לתצורה המאושרת. ללא Runtime, Preview, Indexing, Payment, Upgrade, Subscription, Credentials, שינוי Graph/Prompt, Publish או Tool חיצוני.

אישור קצר יותר, כללי או מעורפל ייחשב כאי-הרשאה לכל פעולה חיצונית, בהתאם לכלל שנקבע ב-`k3-3-staged-authorization.md` ("Approval Syntax").

## What Happens After This Gate

- **Pass** (יתרה `≥180` וללא Drift): מכין — אך אינו מאשר — בקשת שער נפרדת `K4.3E` להרצת 25 השאלות תחת התקרות שהוגדרו ב-K4.0 (עד 30 ניסיונות כולל retries, עד 180 Credits, עם נקודות עצירה אחרי שאלה 10/60 Credits ואחרי שאלה 20/120 Credits).
- **Fail** (יתרה `<180` או Drift כלשהו): לעצור לפני K4.1/K4.2/K4.3, לתעד את הפער כאן, ולחזור ל-K4.0 לבחינה מחדש של האלטרנטיבות B–E.

## Evidence to Record After Owner-performed Verification

לאחר שה-Owner מבצע את הבדיקה בעצמו, או מאשר ל-Codex/Claude reload לקריאה בלבד תחת ההרשאה המדויקת שלמעלה, יש לעדכן כאן:

- `observed_credits_available`: —
- `observed_credits_used`: —
- `workspace_status`: —
- `membership_status`: —
- `graph_drift`: —
- `model_drift`: —
- `knowledge_base_drift`: —
- `metadata_drift`: —
- `prompt_drift`: —
- `corpus_hash_drift`: —
- `paid_state_drift`: —
- `result`: `pass` / `fail`
- `next_action`: —

## Traceability

- K4.0 plan: `configuration/k4-0-capacity-evaluation-plan.md`
- Staged authorization: `configuration/k3-3-staged-authorization.md`
- Readiness checklist: `configuration/k3-3-readiness-checklist.md`
- Manifest: `configuration/manifest.md`
- Tasks: `../tasks.md` (`K4.1C`, `K4.1`)
