# החלטת G3: Hotelbeds Credential Store Selection

## גבול והרשאה

- תאריך: 2026-08-22.
- הרשאה: `G3-Hotelbeds-Store-Selection` ציבורי בלבד.
- בוצע: עיון במקורות ציבוריים רשמיים והשוואת Region, encryption, masking, access, audit, backup, retention, deletion, התאמת חתימה ועלות.
- לא בוצע: הרשמה, Trial, רכישה, התקנה, Runtime, Credential entry, Secret, API call, Network smoke, Commit או Push.

## תוצאה

`CONDITIONAL-SELECTION: n8n self-hosted Community built-in Credential Store`.

הבחירה חלה רק על PoC סינתטי, Instance מקומי ומבודד, Owner יחיד ו-Environment Evaluation יחיד. היא אינה אישור להקים את ה-Instance או להזין Credential.

## הסיבה המכריעה

Hotelbeds דורשת בכל בקשה `X-Signature = SHA-256(api_key + secret + unix_timestamp)`. לכן ה-Store חייב לא רק לשמור שני ערכים, אלא לאפשר לקוד אינטגרציה מאושר להשתמש בהם בזיכרון כדי ליצור חתימה רגעית בלי להחזיר אותם ל-Workflow data.

התיעוד הציבורי של n8n מציג `Custom Auth` כמיזוג JSON לבקשה ואת `Simplified Custom Auth` כתבנית לערכי אימות סטטיים; הוא אינו מתעד חישוב hash דינמי מתוך Secret מוגן. מטריצת התמחור מציגה `Custom nodes` כזמינים ב-self-hosted. לכן Cloud Starter אינו מוכיח מסלול בטוח לחתימת Hotelbeds הדינמית, ואילו self-hosted מאפשר first-party credential/node ייעודי. מימוש node כזה אינו מאושר בשלב זה.

## השוואה

| אפשרות | Region ו-Hosting | Secrets וחתימה | Access ו-Audit | Backup/Rotation | עלות ותפעול | החלטה |
|---|---|---|---|---|---|---|
| n8n Cloud Starter | n8n מציינת שמידע Hosted נשמר בפרנקפורט, גרמניה | Credential store מוצפן; Generic Custom Auth ציבורי הוא סטטי, ו-Custom nodes מסומנים self-hosted | מתאים ל-Owner יחיד; Admin roles מופיעים רק מ-Pro, ושיתוף Workflow עשוי לאפשר לעורך להשתמש ב-Credentials המחוברים | מופעל על ידי הספק; אין שליטה ב-DB, מפתח או backup | €20 לחודש בחיוב שנתי, 2,500 executions; Trial ללא כרטיס לפי הדף הציבורי | לא נבחר: פער חתימה דינמית ושליטה מוגבלת |
| n8n Cloud Pro | כמו Cloud Starter | אותו פער חתימה; מוסיף global variables אך Secret אינו אמור להפוך ל-variable | Admin roles ויותר Projects, אך אין External secret store | מופעל על ידי הספק | €50 לחודש בחיוב שנתי | לא נבחר: עלות גבוהה יותר בלי לפתור את פער החתימה |
| n8n self-hosted Community | ה-Owner בוחרת Host; ל-PoC מוצע Host מקומי בלבד | n8n מצפין Credentials במסד באמצעות `N8N_ENCRYPTION_KEY`; Custom node ייעודי יכול לחשב חתימה בזיכרון | אין מעטפת Enterprise מלאה; מתקבל רק ל-Owner יחיד, ללא משתמשים נוספים, עם OS access control וראיית Gate ממוזערת | ה-Owner אחראית ל-DB backup, הפרדת המפתח, Restore test ו-Retention; Rotation זמינה בכל מהדורות self-hosted | אין Subscription שנבחר או נרכש; Infrastructure וזמן תחזוקה נשארים על ה-Owner | נבחר מותנה ל-PoC הסינתטי בלבד |
| n8n Enterprise + External Secrets | Hosted או self-hosted לפי הסכם | External secret store integration מופיע ב-Enterprise ויכול להתאים לממשל חזק יותר | RBAC/Log streaming/ממשל רחבים יותר לפי החבילה | תלוי Store והסכם | Contact Sales; מחיר לא פומבי | לא נבחר ל-PoC; מועמד Production עתידי |

## תנאי מוכנות לפני Materialization

הבחירה נכשלת סגור עד שחוזה `G3-Hotelbeds-Store-Readiness-Spec` מאושר וכל הבקרות מאומתות ב-`G3-Hotelbeds-Store-Readiness-Verify` נפרד:

1. Host מקומי מדויק ומבודד ל-`travel-poc-synthetic`, ללא חשיפה ציבורית.
2. הצפנת דיסק וחשבון OS ייעודי או מוגבל ל-Owner.
3. `N8N_ENCRYPTION_KEY` נוצר ומוחזק מחוץ ל-Git, OpenSpec, Chat, Prompt, Log ו-backup של ה-Database.
4. גיבוי מוצפן ו-Restore test עם מפתח נפרד; Retention ו-Deletion קצובים.
5. משתמש Owner יחיד, 2FA אם נתמך, ללא Workflow/Credential sharing וללא Community node צד שלישי.
6. first-party Hotelbeds credential/node מתוכנן כך שה-Secret אינו יוצא ל-item data, expression, Code node, Error stack או execution log.
7. Execution-data retention ו-redaction מונעים שמירת headers, request body מלא ו-provider payload מלא.
8. ה-Entry נשאר unbound/disabled עד Metadata Verify ו-G5 נפרד.

## מגבלות

- אין כאן הוכחה שה-Credential של החשבון הוא Evaluation או שמכסתו 50; ערכים אלה נשארים `UNVERIFIED`.
- Community אינו עונה על דרישות Production ל-RBAC, Audit מרכזי, SLA ו-External Secrets.
- אין להשתמש בבחירה עבור מידע לקוח אמיתי, משתמשים מרובים, Production או Tenant נוסף.
- אין להתקין Community node של צד שלישי. כל first-party node עתידי דורש מפרט, סקירת קוד ואישור יישום נפרד.

## מקורות רשמיים

- n8n pricing, plan capabilities, Region ו-Community Edition: <https://n8n.io/pricing/>
- n8n HTTP Request credentials ו-Custom Auth: <https://docs.n8n.io/integrations/builtin/credentials/httprequest/>
- n8n custom encryption key: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/set-a-custom-encryption-key>
- n8n encryption-key rotation: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/rotate-encryption-keys>
- n8n workflow sharing and credential-access behavior: <https://docs.n8n.io/workflows/sharing/>
- n8n security audit: <https://docs.n8n.io/hosting/securing/security-audit/>
- Hotelbeds authentication: <https://developer.hotelbeds.com/documentation/getting-started/>
