# n8n local provisioning baseline

חבילה זו היא baseline ל-`G3-Hotelbeds-Store-Provisioning` עבור `travel-poc-synthetic` בלבד. היא אינה מכילה Credential, Secret, Hotelbeds configuration, Workflow, Custom node או Provider endpoint.

## מצב נוכחי

`PARTIAL / HOST-PREREQUISITE-BLOCKED / NO-GO-TO-VOLUME`

- נבחרה n8n `2.35.7`, וה-image נעול ל-linux/amd64 digest `sha256:f410270e715c795b4935eb16f94c099f7aee8da81c340c9842e76f0d5e716ff3` לאחר בדיקת release ו-security advisories ב-2026-08-22.
- Docker Desktop מותקן, אך ה-daemon לא עלה והיישום נשאר במצב `starting` עקב כשל WSL/vsock.
- Full-disk encryption בכונן המארח לא אומתה: `manage-bde -status` דורש הרשאת Administrator.
- משום ששני תנאי הקדם לא עברו, לא נוצרו Container, Network או Volume ולא אותחל n8n.

## גבולות בטיחות

- Host port ממופה רק ל-`127.0.0.1:5678`. ההאזנה על `0.0.0.0` קיימת רק בתוך ה-Container כדי לאפשר port publishing, וה-Container מחובר לרשת Docker פנימית מבודדת בלבד.
- רשת ה-Container היא `internal: true`, ולכן ברירת המחדל היא ללא Internet או Provider egress.
- Public API, Swagger, diagnostics, templates, version notifications, personalization ו-community packages מושבתים.
- שמירת execution payloads עבור success, error, manual ו-progress מושבתת.
- `HTTP Request`, `Execute Command`, `Local File Trigger` ו-`Read/Write Files from Disk` חסומים ב-baseline.
- מפתח ההצפנה ומפתח/תעודת TLS חייבים להגיע מקבצים מוגנים מחוץ ל-Repository ול-Volume. Codex אינו יוצר, קורא, מציג או מאמת את ערכיהם.
- אין להריץ `export:credentials --decrypted`.
- אין להוסיף Hotelbeds Credential או לפתוח Provider network במסגרת Gate זה.

## תנאים לפני הפעלה

1. Docker Desktop חייב להגיע ל-`running` ו-`docker info` חייב להצליח.
2. ה-Owner חייבת לאמת Full-disk encryption פעיל בכונן שבו Docker מאחסן את ה-Volume.
3. ה-Owner יוצרת בעצמה, מחוץ ל-Repository, מפתח n8n ותעודת HTTPS מקומית מהימנה עם מפתח מוגן.
4. ה-Owner יוצרת `.env` מקומי ignored מתוך `.env.example` ומזינה בו נתיבי קבצים בלבד. אין לשים בו ערכי Key או Certificate.
5. לפני `docker compose up`, יש להריץ `verify-baseline.ps1 -StaticOnly`; בדיקות Runtime שייכות ל-Gate נפרד `G3-Hotelbeds-Store-Readiness-Verify`.

אין להפעיל את Compose לפני שכל התנאים מתקיימים. אישור Provisioning זה אינו מאשר תיקון WSL/Docker ברמת מערכת, יצירת Key, Readiness Verify, Dummy restore, 2FA enrollment, Credential materialization או API call.
