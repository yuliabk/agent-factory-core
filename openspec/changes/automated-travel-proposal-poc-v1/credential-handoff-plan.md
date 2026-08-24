# תוכנית G3: Hotelbeds Credential Handoff

## מטרת השלב

להגדיר מסלול בטוח ומאומת להעברת Hotelbeds Evaluation Credential ישירות מה-Owner אל Credential Store עתידי, בלי לחשוף את `API Key` או ה-`Secret` ל-Codex ובלי לבצע קריאת API.

סטטוס: `STORE-CONDITIONALLY-SELECTED / READINESS-SPEC-COMPLETE / PROVISIONING-BLOCKED / READINESS-VERIFY-BLOCKED / MATERIALIZATION-BLOCKED`.

## גבולות מחייבים

- אין לקרוא, להציג, להעתיק, להכתיב, לצלם או לשמור את הערכים בשיחה.
- אין להזין Secret ב-Terminal, קוד, Git, OpenSpec, `.env`, Issue, Screenshot, Log או מסמך.
- אין ליצור Credential Store entry עד Provisioning ו-Readiness Verify נפרדים ואישור Materialization נפרד.
- אין לחבר Credential ל-Workflow, לחשב `X-Signature` או לבצע API call.
- אין Production hostname, Booking, Payment, Certification או מידע לקוח אמיתי.

## נכס היעד

| שדה | ערך מתוכנן |
|---|---|
| Purpose | Hotel availability/content PoC בסביבת Evaluation בלבד |
| Tenant | `travel-poc-synthetic` |
| Provider | `hotelbeds` |
| Environment | `evaluation` — דורש אימות לפני binding |
| Proposed entry name | `travel-poc-synthetic__hotelbeds__evaluation__v1` |
| Selected store | `n8n self-hosted Community` built-in Credential Store, מותנה במוכנות Host ואבטחה |
| Secret fields | `api_key`, `secret` — masked, non-exportable ככל שהמערכת מאפשרת |
| Derived value | `x_signature` יחושב just-in-time ולא יישמר |
| Allowed host | `api.test.hotelbeds.com` בלבד, לאחר G5 |
| Production host | `api.hotelbeds.com` חסום |

## תנאי קבלה ל-Credential Store

ה-Store הנבחר SHALL:

1. להצפין Secrets במנוחה ובתעבורה.
2. להסתיר ערכים לאחר שמירה ולא להחזירם ב-UI, Export, API או Audit רגיל.
3. להגביל גישה ל-Owner ול-Service identity הייעודית; ב-Community PoC יחידני זה ימומש ב-Instance מקומי ללא משתמשים נוספים ובבקרות OS, ולא ייחשב RBAC מספק ל-Production.
4. לבודד Credential לפי Tenant ו-Environment.
5. לרשום create, update, bind, rotate, disable ו-delete בלי לרשום ערכים; כאשר אין audit trail מוצרי מלא, תידרש ראיית Gate ממוזערת נפרדת ולא יוזן Secret לפני אישורה.
6. לאפשר Rotation ו-Revocation עם ראיה ממוזערת.
7. למנוע חשיפת Secret ל-LLM, Prompt, Workflow output, Error stack או execution log; החתימה תחושב רק ב-first-party credential/node מאושר ולא ב-Code node שמקבל Secret כקלט.
8. לאפשר Backup/Restore שאינם חושפים Secret בטקסט גלוי.

אם תנאי אחד אינו מתקיים, ה-Materialization נכשל סגור.

## תהליך Owner-operated עתידי

1. Codex מציג ל-Owner את שם ה-Entry והשדות בלבד ועוזב את מסך ההזנה.
2. ה-Owner פותחת בעצמה את Hotelbeds ואת Credential Store המאושר.
3. ה-Owner מעתיקה ישירות את `API Key` ואת `Secret` לשדות masked המתאימים.
4. לפני לחיצה סופית על Save, נדרש אישור פעולה בזמן אמת כי נוצרת גישה מתמשכת.
5. לאחר השמירה, Codex רשאי לבדוק רק metadata מאושר: קיום Entry, שם סינתטי, provider, environment label, timestamps, disabled/bound state ו-opaque reference.
6. Codex אינו בודק ערך, אורך, prefix, suffix, checksum או fingerprint של Secret.
7. ה-Entry נשאר לא-משויך; אם המוצר תומך disable מפורש, גם disabled, עד G5.

## Authentication עתידי

Hotelbeds דורשת `Api-key` ו-`X-Signature`. התכנון הוא:

- ה-`Api-key` וה-`Secret` נשמרים יחד ב-Credential Store.
- בזמן execution מאושר בלבד, Workflow מחשב `SHA-256(api_key + secret + unix_timestamp)`.
- ה-signature קיים בזיכרון לזמן הבקשה בלבד ואינו נשמר.
- Headers רגישים עוברים Redaction לפני Log, Error או Trace.
- Clock skew, retry ו-signature expiry ייבדקו ב-G5 תחת מכסה קבועה.

## Reference ממוזער מותר

```yaml
provider: hotelbeds
environment: evaluation
tenant_id: travel-poc-synthetic
credential_store: n8n-self-hosted-community
credential_reference: pending
state: conditionally-selected-not-provisioned
secret_exposed_to_codex: false
network_calls: 0
```

אין להחליף את `credential_reference` ב-API Key, Secret או hash שלהם.

## Rotation, Revocation ויציאה

- Rotation דורשת Gate נפרד וגרסה חדשה בשם `...__v2`.
- אין למחוק Credential ישן עד שהחדש אומת ב-smoke מאושר; לאחר ביטול אין לחזור אליו.
- בסיום PoC, ה-Owner מבטלת את Credential אצל Hotelbeds ומוחקת/משביתה את ה-Entry ב-Store.
- ראיית יציאה כוללת provider, reference אטום, פעולה, actor, timestamp ו-result בלבד.
- אם ביטול או מחיקה אינם ניתנים לאימות, לא עוברים ל-Production.

## Gates נדרשים

1. `G3-Hotelbeds-Store-Selection` — הושלם ציבורית: `n8n self-hosted Community`, מותנה ול-PoC סינתטי בלבד.
2. `G3-Hotelbeds-Store-Readiness-Spec` — הושלם: ננעל חוזה Host, Key custody, access, backup/restore, retention, redaction ו-dynamic signature; ללא התקנה או Secret.
3. `G3-Hotelbeds-Store-Provisioning`: התקנת Instance מקומי ללא Hotelbeds Credential וללא Network provider call.
4. `G3-Hotelbeds-Store-Readiness-Verify`: אימות בקרות ו-Backup/Restore באמצעות Credential דמה סינתטי בלבד.
5. `G4-Hotelbeds-Credential-Node`: מימוש וסקירה של first-party credential/node עם fixtures בלבד וללא Network או Hotelbeds Secret.
6. `G3-Hotelbeds-Materialization`: יצירת Entry אמיתי והזנת Owner ללא צפיית Codex; אין API call.
7. `G3-Hotelbeds-Metadata-Verify`: בדיקה ממוזערת של Reference, Environment, unbound/disabled-if-supported state ומכסה בלי Secret.
8. `G5-Hotelbeds-Network-Smoke`: Hostname ו-Endpoint allow-list, מספר קריאות, Retry ceiling ונתונים סינתטיים בלבד.

אף Gate אינו יורש אישור מה-Gate הקודם.
