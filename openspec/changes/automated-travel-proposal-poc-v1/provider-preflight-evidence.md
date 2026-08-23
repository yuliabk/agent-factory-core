# ראיות G1: Public Provider Preflight

## גבול הבדיקה

- תאריך: 2026-08-22.
- הרשאה: `G1-Provider-A0` ציבורי בלבד.
- בוצע: עיון בתיעוד, תנאים ותמחור ציבוריים רשמיים; הגדרת allow-list מועמד; הערכת פערים; בחירת ספק חשבון מועמד אחד.
- לא בוצע: הרשמה, Login, קבלת תנאים, יצירת Credential, API call, Billing, Payment, Runtime, Model, Botpress, Commit או Push.
- כל ממצא הוא Preflight ארכיטקטוני ואינו ייעוץ משפטי או התחייבות ספק.

## Duffel

### ראיות רשמיות

| נושא | ממצא | משמעות ל-PoC | מקור רשמי |
|---|---|---|---|
| Test mode | Test אינו משתמש בכסף או בהזמנות אמיתיות; Duffel Airways יציב לבדיקות אך המחירים ולוחות הזמנים אינם מציאותיים | מתאים לבדיקת Contract, Schema וכשל בלבד | <https://duffel.com/docs/api/overview/test-mode> |
| Flight search | חיפוש מתחיל ביצירת Offer Request; אפשר להחזיר Offers מיד או לקרוא אותם בנפרד | מאפשר Adapter חיפוש מצומצם | <https://duffel.com/docs/api/v2/offer-requests> |
| Offers | `GET /air/offers` דורש `offer_request_id`; Offer בודד עשוי להשתנות או לפוג | נדרש `searched_at`, `expires_at` ואזהרת מחיר | <https://duffel.com/docs/api/offers/get-offers> |
| תמחור | תמחור פומבי כולל Order fee, Managed Content ו-Excess Search מעל יחס 1,500:1 | אין להניח שחיפוש Production הוא חינם | <https://duffel.com/pricing> |
| אפס הזמנות | לצורך יחס Search-to-Order, אפס Orders מחושב כ-Order אחד; Duffel רשאית להגביל שימוש | יש לתכנן quota קשיח ולקבל הבהרת עלות בכתב | <https://duffel.com/services-agreement> |
| Metasearch | ההסכם הציבורי אוסר שימוש למטרות Metasearch | Search-only Production חסום עד אישור כתוב לסיווג המוצר | <https://duffel.com/services-agreement> |
| Live | מעבר ל-Live דורש פרטי כרטיס והוספת יתרה | פעולה פיננסית מחוץ לתחום | <https://help.duffel.com/hc/en-gb/articles/360019685579-How-do-I-go-live-once-I-ve-built-my-integration> |
| פרטיות ושמירה | המדיניות מתארת שמירה לפי צורך סביר/חובה חוקית וזכויות מחיקה מסוימות; ההסכם כולל DPA והעברות אפשריות מחוץ ל-EEA/UK עם safeguards | אין עדיין Retention/Deletion מדויק ל-Evidence ה-PoC | <https://duffel.com/privacy-policy>, <https://duffel.com/services-agreement> |

### allow-list מועמד ל-Test בלבד

Hostname יחיד: `api.duffel.com`. אותו Host משרת Test ו-Live; זהות הסביבה נגזרת מה-Token ומהשדה `live_mode`, ולכן G5 יצטרך לחסום Token שאינו Test ולדרוש `live_mode=false` בכל תשובה.

| Method | Path | תכלית | מגבלה |
|---|---|---|---|
| `POST` | `/air/offer_requests` | יצירת חיפוש טיסה | Synthetic passengers בלבד; ללא Loyalty או Private fares; עדיפות ל-`return_offers=false` |
| `GET` | `/air/offer_requests/{id}` | קריאת בקשת חיפוש קיימת | רק ID שנוצר באותה ריצה ובאותו Tenant |
| `GET` | `/air/offers` | רשימת Offers לפי `offer_request_id` | Limit קשיח, Pagination מוגבל, ללא crawl |
| `GET` | `/air/offers/{id}` | רענון Offer נבחר | קריאה בלבד; אין Price action או Order |

### deny-list

- כל `/air/orders`, Order change, cancel, refund, hold או payment.
- `POST /air/offers/{id}/actions/price` וכל פעולת ancillary/seat בתשלום.
- עדכון Passenger, Loyalty, Private fares או Airline credits.
- כל Endpoint שאינו מופיע ב-allow-list, גם אם ה-Token מאפשר אותו.

### פערים והחלטה

- זכאות עסק הרשום בישראל: `UNKNOWN`.
- אישור Search-only/טיוטה בלבד ב-Production: `UNKNOWN`; נדרש אישור כתוב.
- סיווג המוצר ביחס לאיסור Metasearch: `UNKNOWN`; נדרשת קביעה חוזית של Duffel.
- עלות Test calls וגבול Excess Search בפועל: אינה מוכחת מספיק לצורך Budget approval.
- מחיקת Evidence ו-Data residency ספציפיים: אינם מוכחים מספיק.
- Test: `CONDITIONAL-GO / ACCOUNT-BLOCKED`.
- Production: `NO-GO / OUT-OF-SCOPE`.

## Hotelbeds / HBX Group

### ראיות רשמיות

| נושא | ממצא | משמעות ל-PoC | מקור רשמי |
|---|---|---|---|
| Evaluation | הרשמה מספקת API key/secret לסביבת Evaluation ב-`api.test.hotelbeds.com` | Account ו-Credential דורשים Gates נפרדים | <https://developer.hotelbeds.com/documentation/getting-started/> |
| מכסה | 50 בקשות ביום; חריגה מחזירה 403 | נדרש counter מקומי ותקרה נמוכה יותר ב-G5 | <https://developer.hotelbeds.com/documentation/getting-started/> |
| Side effect | Booking ב-Evaluation אינו יוצר הזמנה אמיתית או חיוב | למרות זאת `/bookings` אסור כי ה-PoC הוא חיפוש בלבד | <https://developer.hotelbeds.com/documentation/getting-started/> |
| Availability | `/hotels` מחזיר זמינות ותעריפים; `/checkrates` מרענן Rate שמסומן `RECHECK` | מאפשר חיפוש מלון ותיקוף מחיר ניסוי ללא Booking | <https://developer.hotelbeds.com/documentation/hotels/booking-api/>, <https://developer.hotelbeds.com/documentation/hotels/booking-api/workflow/> |
| Content | Content API מיועד ל-Batch/cache; שימוש בזמן אמת עלול לגרום לחסימת Credentials | Content אינו חלק מהמסלול האינטראקטיבי | <https://developer.hotelbeds.com/documentation/hotels/content-api/how-use-content-api/> |
| Certification | תהליך Hotels Certification בודק Funnel של Availability, CheckRate ו-Booking; Production דורש פנייה ובדיקה | התאמת Search-only Production אינה מוכחת | <https://developer.hotelbeds.com/documentation/hotels/knowledge-base/certification-process/> |
| תנאי API | נדרשים סודיות, מינימום מידע אישי ואבטחה; שימוש מופרז עלול להביא להשעיה; קיימות חובות החזרה/השמדה בהקשרים מסוימים | אין להעביר PII; נדרשת סקירה חוזית לפני Production | <https://developer.hotelbeds.com/api-terms-use/> |

### allow-list מועמד ל-Evaluation בלבד

Hostname יחיד: `api.test.hotelbeds.com`. Host ה-Production `api.hotelbeds.com` חסום.

| Method | Path | תכלית | מגבלה |
|---|---|---|---|
| `POST` | `/hotel-api/1.0/hotels` | Availability | קודי מלון/יעד מאושרים בלבד; Synthetic occupancies; ceiling קשיח |
| `POST` | `/hotel-api/1.0/checkrates` | עדכון Rate | רק Rate שהוחזר באותה ריצה עם `rateType=RECHECK` |
| `GET` | `/hotel-content-api/1.0/hotels` | טעינת תוכן סטטי | Job נפרד, Batch בלבד; Pagination ו-Retention מאושרים מראש |
| `GET` | `/hotel-content-api/1.0/hotels/{code}/details` | פרט סטטי ממוקד, אם הנתיב יאומת שוב ב-API reference בזמן G5 | לא בזמן אמת; נתיב מותנה ולכן חסום כברירת מחדל |

### deny-list

- כל `/hotel-api/1.0/bookings`, לרבות create, list, detail, amend, cancel או cancellation simulation.
- Host ה-Production וכל Product אחר: Activities, Transfers או Cache API.
- Content crawling בזמן אמת, טעינה מלאה של הפורטפוליו או חריגה ממכסת Stage.
- כל Endpoint שאינו מופיע ב-allow-list המאושר ל-G5.

### פערים והחלטה

- זכאות עסק הרשום בישראל: `UNKNOWN`. הופעת ישראל בתוכן אינה הוכחת זכאות מסחרית.
- Search-only ב-Production ללא Booking funnel: `UNKNOWN`; נדרש אישור כתוב.
- תמחור, הסכם מסחרי, Data residency ו-Retention/Deletion מדויקים: `UNKNOWN`.
- תהליך Certification עשוי לדרוש פרטי מערכת ובדיקת Booking/Cancel; אין למסור מידע כזה או לבצע בדיקה ללא Gate נפרד.
- Evaluation: `CONDITIONAL-GO / ACCOUNT-BLOCKED`.
- Production: `NO-GO / OUT-OF-SCOPE`.

## החלטת G1

ספק החשבון המועמד הראשון היה `Duffel Test`.

הנימוקים:

1. חיפוש הטיסות הוא התלות הקשה יותר והמסוכנת יותר מבחינת חוזה, תפוגת Offer ומודל Search-to-Book.
2. Test mode מאפשר לבדוק Contract, Schema ותרחישי כשל בלי כסף או הזמנה אמיתיים.
3. עבודה עם ספק אחד בלבד מצמצמת חשיפה, Secrets ומורכבות Gate.

לאחר אישור `G2-Duffel-Account`, דף ההרשמה הרשמי נפתח. רשימת `Country of incorporation` לא כללה את ישראל. לא נבחרה מדינה אחרת, הטופס לא נשלח, ולא נוצר Account או Token. תוצאת Gate: `NO-GO / REGISTRATION-BLOCKED` עד לקבלת הבהרה כתובה מ-Duffel.

ה-Owner בחרה לעבור ל-`Hotelbeds Evaluation` ואישרה `G2-Hotelbeds-Account`. דף ההרשמה הרשמי נפתח בלבד. לפי התיעוד הרשמי, השלמת Registration מספקת אוטומטית API Keys ו-Secret ל-Evaluation; לכן G2 ויצירת Credential קשורים טכנית. Codex לא קרא, העתיק, שמר או השתמש ב-Credential ולא ביצע API call.

ב-2026-08-22 ה-Owner אישרה `G2/3-Hotelbeds-Doc` בלבד, ולאחר מכן הצהירה במפורש שהחשבון נוצר. סטטוס G2 הוא `ACCOUNT-CREATED / OWNER-ATTESTED`. Codex לא קרא מידע אישי ולא בדק את דף המפתחות; קיום ותוכן Credential נשארים `UNINSPECTED`, ואין להסיק אותם ממצב דפדפן סביבתי או מ-URL פתוח.

מקורות רשמיים נוספים:

- טופס Duffel ורשימת המדינות בזמן הבדיקה: <https://app.duffel.com/join>
- Hotelbeds registration: <https://developer.hotelbeds.com/register/>
- Hotelbeds automatic Evaluation credentials: <https://developer.hotelbeds.com/documentation/getting-started/>

## G3-Hotelbeds-A0 — ראיה מבנית ממוזערת

- תאריך: 2026-08-22.
- הרשאה: קריאה בלבד; אין לקרוא, להציג, להעתיק או לשמור API Key/Secret ואין לבצע API call.
- מקור: דף `My API Keys` בחשבון Hotelbeds שנוצר על ידי ה-Owner.
- זוהו לפחות שתי רשומות מבניות, עם שני שדות בשם `apikey` ושני שדות בשם `secret`.
- זוהו תוויות תצורה עבור `Environment`, `Rate Limits`, `Usage Quotas`, `Throttling`, `Associated certificates` ו-`Alias`.
- ערכי `Environment`, המכסות והקצב לא היו חשופים דרך המטא-נתונים הבטוחים שנבדקו; הם נשארים `UNVERIFIED`.
- לא נקראו ערכי Input, Account Name או מידע אישי; לא בוצע DOM snapshot רחב או צילום מסך.
- לא נלחצו Reveal, Copy או Submit; Alias לא שונה; לא בוצעה קריאת API.
- תוצאה: `STRUCTURE-CONFIRMED / VALUES-UNREAD / ENVIRONMENT-AND-QUOTA-UNVERIFIED`.
- משמעות: A0 אינו מאשר Credential לשימוש. לפני G5 נדרשים Gate נפרד, Credential Store ייעודי, אימות Environment ומכסה, ודרך שאינה חושפת Secret ל-Codex, ל-Prompt, ל-Log או ל-Git.

## שאלות חובה לספק לפני Production

1. האם עסק הרשום בישראל זכאי ל-Test ול-Production, ובאילו תנאים מסחריים?
2. האם מותר מוצר B2B שמחפש ומכין טיוטת הצעה אך אינו מבצע Booking דרך הספק?
3. האם שילוב תוצאות טיסה ומלון והשוואת חלופות מסווג כ-Metasearch או redistribution?
4. מהן עלויות Search, מינימום הזמנות, Overage, Currency, מס ותקופת התחייבות?
5. מהן מגבלות cache, display, attribution, retention, deletion ו-data residency?
6. האם ניתן להנפיק Credential בעל הרשאות Search-only טכניות, ללא Booking/Payment?
