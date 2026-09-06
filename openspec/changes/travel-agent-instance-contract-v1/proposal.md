# הצעה: Travel Agent Instance Contract v1

## תקציר

להגדיר חוזה קנוני, versioned ו-provider-neutral עבור Travel Agent Instance כך שכל ערוץ - Web, Email ו-WhatsApp - ישתמש באותו backend ובאותה שרשרת נתונים:

`TripRequest -> EvidencePack -> ProposalDraft -> EvalResult -> ApprovalRecord -> AuditBundle`

החוזה נועד לאחד את ה-Web App שיוצא מ-Abacus עם `travel-agent-bot` בלי לשמר שני מנועי Agent נפרדים, ובו בזמן לשמור את `agent-factory-core` כ-Control Plane ומקור האמת ל-Specs, Evals, Policies ו-Release contracts.

## החלטות Owner שננעלו

1. המערכת תשרת גם לקוח קצה וגם סוכן נסיעות.
2. `AI Draft` יכול להיות מוצג ללקוח לפני אישור אנושי, עם סימון ברור שהוא טיוטה.
3. הצעה סופית מחייבת אישור סוכן נסיעות.
4. PDF סופי, Email/WhatsApp רשמי וכל פעולה עתידית של Booking, Payment, Ticketing או mutation חיצוני מחייבים אישור אנושי תקף לגרסה המדויקת.
5. מחיר שמוצג כמאומת חייב להיות מגובה ב-Evidence עם מקור, זמן חיפוש, מטבע ו-provider reference. ללא Evidence ניתן להציג רק estimate מסומן.
6. כאשר חסר מידע, המערכת תציג טיוטה חלקית ותבקש השלמה במקום להמציא מידע.
7. שינוי לאחר אישור יוצר גרסה חדשה ומבטל את תוקף האישור לגרסה החדשה.
8. יעד המוצר כולל מידע אמיתי של לקוחות, אך כל Runtime שמקבל PII נשאר חסום עד Gate נפרד של Security/Privacy ו-Implementation. מגבלת ה-MVP הנוכחית של המאגר לסינתטי/לא-רגיש נשארת בתוקף עד אישור כזה.

## מטרות

- מקור אמת אחד לחוזי הנתונים של Travel Agent.
- backend אחד לכל ערוצי המשתמש.
- traceability מלאה בין בקשה, Evidence, טיוטה, Eval, אישור ופלט סופי.
- הפרדה ברורה בין `AI_DRAFT` לבין `APPROVED_PROPOSAL`.
- fail-closed עבור מחיר לא נתמך, פעולה חיצונית לא מאושרת או שינוי אחרי Approval.
- תמיכה ב-partial draft וב-clarification בלי לאבד עבודה שכבר בוצעה.
- בסיס לשכפול Travel Agent Instance נוסף מתוך ה-Factory בעתיד.

## בתחום

- Versioned contracts עבור ששת האובייקטים הקנוניים.
- Status machines ו-transition rules.
- Evidence requirements למחירים ול-recommendations חומריים.
- Eval gate לפני Agent Approval.
- Human approval המחובר ל-`proposal_version` ול-`proposal_hash`.
- Audit Bundle ממוזער שמאפשר לשחזר מה קרה בלי לשמור Secret או PII מיותר.
- Actor model עבור `customer`, `agent` ו-`system`.
- Data classification metadata שמאפשרת מעבר עתידי מסינתטי ל-PII רק לאחר Gate.
- API contract direction ל-Travel Agent Runtime, ללא מימוש קוד בשינוי זה.

## מחוץ לתחום

- שינוי בקוד `travel-agent-bot`.
- העברת Web App בפועל ל-repository אחר.
- Provider credentials, Billing או Network calls.
- Production database migration.
- Booking, Payment, Hold, Ticketing, Refund או PNR mutation.
- שליחת Email/WhatsApp בפועל.
- ביטול המגבלה הנוכחית של `agent-factory-core` על נתוני MVP סינתטיים/לא-רגישים.

## קריטריוני הצלחה

- לכל אובייקט יש `schema_version`, מזהה קנוני ויחסי foreign-key ברורים.
- כל Proposal הוא versioned ו-hashable.
- כל מחיר מאומת ניתן למיפוי ל-Evidence תקף.
- Eval מסוג `FAIL` חוסם Approval.
- Approval קשור לגרסה ול-hash ואינו מועבר אוטומטית לגרסה חדשה.
- Draft חלקי נשמר ומציג `missing_information` מפורש.
- External delivery דורש Approval תקף לגרסה הסופית.
- Audit Bundle כולל manifest, request, evidence, ranking, model/eval metadata, approval ו-final output hash, ללא Secret או PII מיותר.
- החוזה נשאר provider-neutral ו-channel-neutral.

## סיכונים ופשרות

- תמיכה חוזית ב-PII אינה אישור לעבד PII בפועל; נדרש Gate Privacy/Security נפרד.
- יותר versioning ו-audit מוסיפים מורכבות, אך מונעים מצב שבו גרסה לא מאושרת נשלחת ללקוח.
- Evidence קשיח למחירים עשוי להחזיר יותר partial drafts, אך מונע הצגת מחיר מומצא כעובדה.
- Human approval מוסיף latency להצעה סופית, ולכן `AI Draft` נשאר זמין מיד כדי לשמור על UX מהיר.

## משמעות אישור השינוי

אישור Change זה מאשר את חוזה הנתונים והארכיטקטורה בלבד. הוא אינו מאשר Implementation, Runtime, PII processing, Provider calls, Messaging, Billing או Production deployment. כל מימוש ידרוש Gate נפרד בהתאם ל-`AGENTS.md`.
