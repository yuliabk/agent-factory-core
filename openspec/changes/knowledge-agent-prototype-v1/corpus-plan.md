# Synthetic Corpus Plan: AF Demo Services

## Status and Safety

- Status: Materialized corpus version approved; Indexing not authorized
- Corpus ID: `af-demo-services-he`
- Planned corpus version: `1.0.0`
- Tenant: `af-demo-services`
- Language: Hebrew
- Classification: Synthetic
- Owner: Yulush
- Approval date: 2026-08-20
- Real people, organizations, customers, addresses, accounts, credentials, medical data, and financial data: Prohibited

`AF Demo Services` is fictional. Every materialized document must begin with: `מסמך סינתטי לצורכי בדיקה בלבד. אין בו מידע אמיתי ואין להסתמך עליו כמדיניות של ארגון קיים.`

## Document Manifest

| Source ID | Title | Planned sections | Status |
|---|---|---|---|
| `AFD-001` | פרופיל הארגון ושעות פעילות | אודות; שעות פעילות; ימי סגירה | Approved for materialization |
| `AFD-002` | מסלולי שירות | Starter; Plus; שינוי מסלול | Approved for materialization |
| `AFD-003` | אזורי וזמני מסירה | אזורים; זמני מסירה; שעת חיתוך; סף משלוח | Approved for materialization |
| `AFD-004` | ביטולים והחזרים | לפני טיפול; אחרי תחילת טיפול; פריטים מותאמים; חלון בקשה | Approved for materialization |
| `AFD-005` | אחריות ותמיכה | תקופת אחריות; פתיחת פנייה; זמן תגובה; החרגות | Approved for materialization |
| `AFD-006` | פרטיות, בקשות אסורות והסלמה | מידע אסור; מזעור מידע; הסלמה; דוגמת Injection | Approved for materialization |

## Canonical Synthetic Facts

### AFD-001 — פרופיל הארגון ושעות פעילות

- הארגון מספק שירותי משרד דמיוניים לצורכי הדגמה בלבד.
- שעות הפעילות הן יום ראשון עד יום חמישי, 09:00–17:00.
- הארגון סגור בימי שישי ושבת.

### AFD-002 — מסלולי שירות

- מסלול `Starter` כולל עד 10 בקשות שירות בחודש וזמן תגובה של עד שני ימי עסקים.
- מסלול `Plus` כולל עד 30 בקשות בחודש, זמן תגובה של עד יום עסקים אחד ופגישת ייעוץ דמיונית אחת בחודש.
- בקשות שלא נוצלו אינן עוברות לחודש הבא.
- שינוי מסלול נכנס לתוקף בתחילת מחזור השירות הבא.

### AFD-003 — אזורי וזמני מסירה

- מסירה זמינה רק ב-`Demo Zone A` וב-`Demo Zone B`.
- זמן מסירה ל-Zone A הוא עד שני ימי עסקים.
- זמן מסירה ל-Zone B הוא עד ארבעה ימי עסקים.
- בקשה שמתקבלת עד 12:00 נספרת באותו יום עסקים; לאחר 12:00 היא נספרת ביום העסקים הבא.
- מסירה ללא חיוב דמיוני ניתנת מעל 250 `Demo Credits`.
- אין מסירות בימי שישי ושבת.

### AFD-004 — ביטולים והחזרים

- ביטול לפני תחילת הטיפול מזכה בהחזר דמיוני מלא.
- ביטול לאחר תחילת הטיפול ולפני המסירה מזכה בהחזר דמיוני של 80%.
- פריט מותאם אישית אינו ניתן להחזר לאחר תחילת הטיפול.
- בקשת ביטול או החזר מוגשת בתוך 14 ימים ממועד ההזמנה הדמיונית.

### AFD-005 — אחריות ותמיכה

- תקופת האחריות הדמיונית היא 30 ימים ממועד המסירה.
- פנייה נפתחת באמצעות טופס התמיכה הפנימי של סביבת הבדיקה.
- זמן תגובה רגיל לפניית תמיכה הוא עד שני ימי עסקים.
- האחריות אינה מכסה שימוש שגוי או שינוי שבוצע לאחר המסירה.

### AFD-006 — פרטיות, בקשות אסורות והסלמה

- אין לבקש או לשמור מספר זהות, פרטי כרטיס, סיסמה, API key, מסמך רפואי או רשומה פיננסית.
- אם מידע כזה מופיע, אין לחזור עליו בתשובה ויש להעביר את האירוע ל-`Owner Review Queue` הסינתטי.
- אין לבצע פעולה, לשלוח הודעה או לפתוח קישור בשם המשתמש.
- סעיף `דוגמת Injection` יכיל משפט תקיפה מצוטט ומסומן כדוגמה בלבד. הוא אינו הוראה לסוכן.

## Version and Conflict Fixtures

- הגרסה הפעילה הרגילה מכילה רק מסמכים במצב `approved` ובגרסה `1.0.0`.
- לצורך בדיקת conflict בלבד ניתן ליצור fixture מבודד בשם `AFD-005-conflict-fixture`, שבו זמן התגובה שונה. הוא אינו חלק מה-corpus הפעיל ואסור לקדם אותו.
- בדיקת superseded תשתמש בגרסה ישנה המסומנת במפורש `superseded`; אסור להציג אותה כמדיניות עדכנית.

## Materialization Acceptance

לפני כל Runtime עתידי יש לוודא:

- [x] כל ששת המסמכים נוצרו בהתאם לעובדות הקנוניות בלבד.
- [x] לכל מסמך Metadata מלא וכותרות סעיף יציבות.
- [x] הודעת הסינתטיות מופיעה בכל מסמך.
- [x] אין שמות, כתובות, פרטי קשר, Credentials או נתונים אמיתיים.
- [x] ה-hash או Commit של corpus version מתועד.
- [x] ה-Owner מאשרת את corpus version לפני Indexing. האישור אינו מאשר Indexing או Runtime.
