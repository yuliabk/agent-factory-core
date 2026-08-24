# ADR-004: Dify Cloud Sandbox כ-Runtime לאב-טיפוס הסינתטי

**Status:** Accepted
**Date:** 2026-08-20
**Deciders:** Owner (Yulush)
**Scope:** K3.2 בלבד; בחירת Runtime וגישת Retrieval כתכנון מקומי

## Context

ה-Prototype `AF-KA-01` נועד לבדוק סוכן ידע בעברית מול הקורפוס הסינתטי `af-demo-services-he@1.0.0` ו-25 שאלות קפואות. ה-Owner עובדת 6-10 שעות בשבוע, מעדיפה Low-code, ואישרה תקרת Runtime עתידית של 100 ₪ בחודש. K3.1 השווה את Dify Cloud, Botpress Cloud ו-Flowise Cloud מול איכות עברית, בידוד, Export, Deletion, Region, בקרת עלות ומאמץ Owner.

החלטה זו נדרשת כדי למפות בהמשך את חוזי ה-Retrieval וה-Evaluation הנייטרליים לספק מוגדר. היא אינה מספקת ראיות איכות, אבטחה או עלות בפועל ואינה הרשאה להשתמש בשירות חיצוני.

## Decision

נבחר `Dify Cloud Sandbox` כ-Runtime המנוהל המיועד לאב-טיפוס הסינתטי, הלא-Production וה-Owner-only.

גישת ה-Retrieval שנבחרה היא:

- להשתמש ב-Dify Knowledge Base המנוהל עבור קורפוס יחיד ונפרד של `af-demo-services`.
- להתחיל במיפוי של Candidate `R-A`: כל Section יציב נשמר כיחידת Retrieval, ללא חציית גבולות Source, עם עד שלוש תוצאות וללא Reranking.
- לא לקבע Chunk size, Embedding model, Score threshold או Generation model לפני מדידה.
- לעבור ל-`R-B` או `R-C` רק במסגרת Configuration version חדש ולאחר כשל מתועד, בלי למחוק תוצאות קודמות.
- איכות Retrieval בעברית נקבעת רק באמצעות סט 25 השאלות והספים המאושרים; בחירת Dify אינה הוכחת איכות.

`Botpress Cloud PAYG` נשמר כחלופת גיבוי אם Dify אינו מאפשר בקרת עלות מספקת, Export/Deletion ניתנים לאימות או בידוד מתאים. `Flowise Cloud Free` נשמר כעתודה טכנית אם נדרשת שליטה עמוקה יותר ב-Retrieval.

## Authorization Boundary

ADR זה מאשר תיעוד מקומי בלבד. הוא אינו מאשר:

- יצירת חשבון, Workspace, App או Knowledge Base;
- התחברות ל-Dify או קבלת תנאי שירות;
- אמצעי תשלום, מנוי או שימוש בתשלום;
- Credentials, API keys או חיבור Model provider;
- העלאה, Indexing, Embedding, Retrieval, Runtime או Test execution;
- מידע אמיתי, משתמש חיצוני, Production, Channel, Tool, n8n או Side effect.

כל הפעולות האלה נשארות חסומות עד K3.3 מפורש. פעולות K4 נשארות חסומות גם לאחר K3.3 עד שהיקפן המדויק יאושר.

## Options Considered

### Option A: Dify Cloud Sandbox

| Dimension | Assessment |
|---|---|
| Complexity | נמוכה |
| Base cost | חינמי במסגרת מכסות Sandbox שאומתו ב-K3.1 |
| Knowledge fit | גבוהה; Knowledge Base ו-Chat/Workflow בממשק אחד |
| Hebrew evidence | לא ידוע עד Evaluation |
| Isolation | מספיק עקרונית ל-tenant סינתטי יחיד; לא הוכח ללקוחות אמיתיים |
| Cost enforcement | פער: לא אומת Hard Cap כספי מותאם אישית |
| Portability | פער: Export/Restore מלא של App, Knowledge ו-Chunks לא אומת |
| Region | פער: אזור Managed Cloud מדויק לא פורסם במקור שנבדק |
| Owner effort | נמוך |

**Pros:** התאמה ישירה לסוכן ידע, מעט תחזוקת תשתית, המשכיות עם ADR-001 ועם הארכיטקטורה הקיימת.

**Cons:** בקרת עלות, Region, Export, Deletion ואיכות עברית עדיין דורשים ראיה לפני פעולה.

### Option B: Botpress Cloud PAYG

| Dimension | Assessment |
|---|---|
| Complexity | נמוכה-בינונית |
| Base cost | 0 דולר במסלול PAYG שנבדק ב-K3.1, בתוספת Usage |
| Knowledge fit | טובה |
| Hebrew evidence | לא ידוע עד Evaluation |
| Isolation | Workspace ו-Bot boundaries; דורש בדיקות שליליות |
| Cost enforcement | חזקה יחסית; Custom AI Spend cap מתועד |
| Portability | Export מתועד אך קובצי Knowledge מקוריים מקושרים לשרת |
| Region | לא אומת עבור ברירת המחדל |
| Owner effort | נמוך-בינוני |

**Pros:** Hard Cap ולוג שימוש טובים יותר על הנייר.

**Cons:** ניידות Knowledge חלקית, Retention קבצים ממושך כברירת מחדל ומורכבות רחבה יותר מהנדרש.

### Option C: Flowise Cloud Free

| Dimension | Assessment |
|---|---|
| Complexity | בינונית |
| Base cost | חינמי במסגרת 100 Predictions; Starter חורג מתקרת ה-Prototype לפי K3.1 |
| Knowledge fit | טובה וגמישה |
| Hebrew evidence | לא ידוע עד Evaluation |
| Isolation | Workspace/RBAC מתקדם תלוי מסלול יקר יותר |
| Cost enforcement | מכסת Predictions; Hard Cap כספי מאוחד לא אומת |
| Portability | Export/Import JSON ברור |
| Region | US East 1 מתועד |
| Owner effort | בינוני |

**Pros:** ניידות ברורה ושליטה טכנית עמוקה ב-Retrieval.

**Cons:** יותר החלטות תפעוליות, ובידוד מתקדם או מסלול בתשלום אינם מתאימים לתקרה הנוכחית.

## Trade-off Analysis

Dify נבחר משום שהמטרה הנוכחית היא להוכיח במהירות ובמאמץ Owner נמוך את שרשרת Spec → Corpus → Retrieval → Evaluation, ולא למקסם גמישות תשתית. Botpress עדיף בתיעוד בקרת העלויות, ו-Flowise עדיף בניידות ובשליטה טכנית מסוימת, אך היתרונות האלה אינם גוברים כרגע על פשטות Dify עבור Prototype סינתטי יחיד.

הבחירה הפיכה: הקורפוס, החוזים, שאלות הקבלה ומטריצת ה-Retrieval נשארים ב-Git ובפורמט נייטרלי. אם תנאי K3.3 אינם ניתנים להוכחה ב-Dify, אין לבצע Runtime; פותחים ADR חדש שמחליף החלטה זו ובוחנים את Botpress.

## Consequences

- ניתן להכין בהמשך Mapping ממוקד ל-Dify במקום לתכנן שלושה ספקים במקביל.
- אין שינוי בתקרת 100 ₪, ב-25 השאלות או בקורפוס המאושר.
- אין אישור למודל, Embeddings או Retrieval settings סופיים.
- Dify Sandbox אינו מאושר למידע אמיתי, ללקוח, ל-Production או ל-Multi-tenant runtime.
- Region, Data flow, Deletion, Export/Restore ובקרת עלות נשארים תנאי חסימה לפני K3.3.
- כשל בתנאי חסימה מחזיר את ההחלטה ל-Owner; אין מעבר אוטומטי ל-Botpress.

## Action Items

1. [x] לאמת תמחור, מכסות ו-Credit consumption ל-`gpt-4.1-mini` ול-`text-embedding-3-small`; התחייבות כספית נשארת 0 ₪ ולכן אין שער המרה. יש לאמת שוב לפני כל Stage.
2. [x] לתעד זרימת Dify-managed OpenAI ל-Generation/Embedding; Region מדויק נשאר לא ידוע והתקבל כסיכון שיורי לקורפוס הסינתטי בלבד.
3. [ ] להוכיח נתיב Export/Restore מקומי ללא Secrets ונתיב מחיקת App, Knowledge, Index, Logs ו-Workspace.
4. [x] להגדיר Zero-spend boundary מבוסס Sandbox-only, ללא BYOK/Paid quota/Upgrade, עם Credit ו-request ceilings ו-Drift stop לפני כל Stage.
5. [x] להכין Mapping מקומי של `R-A`, החוזים וה-25 שאלות ל-Dify ללא Credentials וללא העלאה. ראיה: `configuration/k3-3-readiness-checklist.md`.
6. [ ] לקבל אישור Owner נפרד ל-K3.3 לפני פעולה חיצונית כלשהי.

Official and authenticated UI evidence for items 1-4 was collected on 2026-08-20. Exact Region and Backup/cache retention remain accepted only for synthetic data. A manual reconstruction Runbook closes the planning gap, but an actual Restore test remains separately gated. No K3.3 Stage is authorized.

## Traceability

- OpenSpec change: `openspec/changes/knowledge-agent-prototype-v1/`
- Comparison: `openspec/changes/knowledge-agent-prototype-v1/runtime-options-comparison.md`
- Retrieval matrix: `openspec/changes/knowledge-agent-prototype-v1/configuration/retrieval-experiment-matrix.md`
- Requirements: KA-101, KA-108, KA-109, KA-110, KA-111
