# מפרט G3: Hotelbeds Store Readiness

## מטרה וסטטוס

להגדיר תנאי Pass/Fail לפני הקמת Credential Store מקומי ולפני הכנסת Hotelbeds Credential אמיתי.

סטטוס: `READINESS-SPEC-COMPLETE / PROVISIONING-PARTIAL-HOST-BLOCKED / READINESS-VERIFY-BLOCKED / MATERIALIZATION-BLOCKED`.

המסמך הוא Specification בלבד. אין בו התקנה, Runtime, Container, Volume, Account, Key generation, Credential, Secret, Custom node, Network או API call.

## Topology נעול

| רכיב | החלטת PoC |
|---|---|
| Host class | תחנת Windows בשליטת ה-Owner עם Full-disk encryption מאומת |
| Packaging | Container מקומי; n8n `2.35.7`, linux/amd64 image digest `sha256:f410270e715c795b4935eb16f94c099f7aee8da81c340c9842e76f0d5e716ff3` |
| Exposure | HTTPS ו-loopback-only; אין Public URL, Reverse proxy או גישה ממחשב אחר |
| Tenant | `travel-poc-synthetic` בלבד |
| Environment | `evaluation` בלבד; דורש Metadata Verify לפני שימוש |
| Users | Owner יחיד עם 2FA; אין Invite או Sharing |
| Data volume | Volume ייעודי מחוץ ל-Repository וללא שיתוף עם Runtime/Tenant אחר |
| Egress | Deny by default; אין Hotelbeds traffic לפני G5 |
| Cost | אין Subscription או רכישה בשלב Spec; Provisioning עתידי חייב להישאר במעטפת Automation של 0-150 ₪ לחודש |

## Configuration Contract

הערכים הבאים הם חוזה עתידי ואינם מיושמים במסמך זה:

| Control | Required state | Evidence מותרת |
|---|---|---|
| Effective host exposure | Host mapping ו-listener אפקטיבי על `127.0.0.1` בלבד; ה-Container רשאי להאזין על `0.0.0.0` בתוך Docker network מבודדת מסוג `internal` כדי לאפשר את ה-port publishing | כתובת ו-Port בלבד |
| Local transport | `N8N_PROTOCOL=https`; תעודה מקומית מהימנה ומפתח TLS מוגן מחוץ ל-Repo/DB volume | Protocol, issuer class ו-expiry בלבד; ללא key/path אישי |
| Public API | disabled | Boolean בלבד |
| Swagger/API playground | disabled | Boolean בלבד |
| External webhooks / MCP | לא מופעלים ולא מפורסמים | Boolean/route count בלבד |
| Diagnostics/Templates | disabled | שמות flags ו-Boolean בלבד |
| Version notifications | disabled; בדיקת עדכון ידנית לפני Gate | version identifier בלבד |
| SSRF protection | enabled בגרסה תומכת, בנוסף ל-Egress firewall | enabled/version בלבד |
| Nodes | risky nodes ו-Community nodes חסומים; first-party node בלבד לאחר אישור | רשימת type identifiers, ללא config |
| Execution success data | `none` | setting name/value |
| Execution error data | `none` | setting name/value |
| Manual execution data | `false` | setting name/value |
| Progress data | `false` | setting name/value |
| Pruning | enabled | age/count policy בלבד |

## Key Custody

1. `N8N_ENCRYPTION_KEY` יגיע מ-protected file מחוץ ל-Repository, ל-Compose, ל-`.env`, ל-Database volume ול-backup set.
2. ACL יאפשר קריאה רק ל-Owner-controlled OS identity ול-Container process הנדרש.
3. Codex לא ייצור, יקרא, יציג, יעתיק או יאמת את ה-Key, גם לא באמצעות hash, length, prefix או suffix.
4. Database backup ומפתח ההצפנה יישמרו ב-Locations נפרדים. גישה לשניהם יחד נחשבת Privileged recovery action.
5. אם ה-Key חסר או שונה, ה-Instance ייכשל סגור; אין ליצור Key חדש אוטומטית מעל Store קיים.
6. n8n data-key rotation לא תופעל ב-PoC הראשוני. Hotelbeds Credential rotation תשתמש ב-Entry חדש וב-Gate נפרד.

## Access ו-Administrative Paths

- בדיוק Owner אחד; 2FA חובה לפני כל Credential.
- אין משתמש נוסף, Invite, shared project, shared workflow או shared credential.
- אין Public API key, remote shell, remote admin או instance MCP.
- Server CLI מוגבל ל-Owner OS context בלבד. לפי תיעוד n8n, CLI עוקף Access controls ולכן כל שימוש בו הוא פעולה privileged ומתועדת.
- `export:credentials --decrypted` אסור. Backup מותר רק כשה-Credentials נשארים מוצפנים.
- UI או Metadata verification לא יציגו API Key, Secret, Signature, length, prefix, suffix או fingerprint.

## Backup, Restore, Retention ו-Deletion

| נושא | יעד PoC |
|---|---|
| RPO | עד 24 שעות |
| RTO | עד יום עסקים אחד |
| Backup frequency | יומי לאחר Materialization, אם ה-Instance בשימוש |
| Backup retention | עד 7 ימים, לכל היותר 7 עותקים יומיים |
| Backup content | Database/Volume מוצפן; ללא decrypted credential export |
| Key location | נפרד מה-Backup |
| Restore test | לפני Credential אמיתי, עם Dummy credential סינתטי בלבד |
| Primary deletion | מיידית לאחר Gate מחיקה מאושר |
| Backup expiry | עד 7 ימים; אין Restore של Credential שבוטל |

Restore Pass מחייב שה-Dummy entry וה-metadata הצפוי חוזרים, שהערך אינו מופיע ב-Terminal, Log, Screenshot או File חיצוני, ושמשך השחזור נמדד. Restore Fail חוסם Materialization.

## Execution Data ו-Audit

- n8n לא ישמור payloads של execution מוצלח, כושל, ידני או progress.
- Workflow לא יעביר Credential או Signature ב-item data, expression או Code node.
- Errors ימופו ל-category ממוזערת כגון `AUTHENTICATION_FAILED`, `RATE_LIMITED` או `PROVIDER_UNAVAILABLE`; אין raw stack עם headers.
- Audit נפרד וממוזער יכיל רק את שדות ATP-109. Retention יעד ל-Audit ה-PoC: 30 יום.
- Raw provider payload לא נשמר כברירת מחדל. חריג Debug עתידי דורש Gate נפרד, Redaction ו-Retention של עד 24 שעות.

## First-party Hotelbeds Credential/Node Contract

ה-node העתידי, אם יאושר ב-G4, SHALL:

1. להיות first-party במאגר, עם source review, tests, version pin ו-Owner approval; אין Community node.
2. לקבל `api_key` ו-`secret` רק דרך n8n Credential interface בשדות masked.
3. לנעול `https://api.test.hotelbeds.com` ולהיכשל על כל Host אחר.
4. לחשב `SHA-256(api_key + secret + unix_timestamp)` just-in-time בתוך ה-node.
5. להחזיק את ה-Signature לזמן הבקשה בלבד ולא להחזירו ל-Workflow.
6. לחשוף רק Availability, conditional CheckRate ו-Content read שאושרו; אין Booking או mutation.
7. לבצע Redaction לפני כל Error/Log ולהחזיר רק normalized result או error category.
8. לעבור unit/fixture tests עם Dummy values בלבד לפני Hotelbeds Credential אמיתי.

## Readiness Verification Matrix

| ID | בדיקה | Pass | Fail response |
|---|---|---|---|
| RSV-01 | Effective listeners and TLS | HTTPS על loopback בלבד ותעודה מהימנה | עצירה וכיבוי Instance |
| RSV-02 | Disk/volume isolation | הצפנה פעילה ו-Volume מחוץ ל-Repo | מחיקת Volume ריק ועצירה |
| RSV-03 | Owner/2FA | Owner יחיד ו-2FA enabled | אין Credential |
| RSV-04 | APIs/telemetry/templates | כולם disabled | אין Credential |
| RSV-05 | Key separation | metadata מאשר Locations נפרדים ללא ערך | אין Store initialization |
| RSV-06 | CLI/export policy | אין decrypted export; CLI Owner-only | אין Credential |
| RSV-07 | Execution persistence | כל payload saves disabled | אין Workflow binding |
| RSV-08 | Node inventory | אין Community/risky nodes זמינים | Quarantine/Removal ואימות חוזר |
| RSV-09 | Dummy backup/restore | Restore מצליח ללא value exposure | Materialization חסום |
| RSV-10 | Egress | Hotelbeds ו-Internet חסומים | כיבוי Instance ותיקון policy |
| RSV-11 | Version pin | version+digest+advisory review מתועדים | Provisioning חסום |

כל הבדיקות חייבות לעבור. אין Pass חלקי.

## ראיה ממוזערת מותרת

```yaml
tenant_id: travel-poc-synthetic
store_type: n8n-self-hosted-community
host_scope: owner-controlled-windows
network_scope: loopback-only
owner_count: 1
two_factor_enabled: pending-verification
encryption_key_value_observed: false
hotelbeds_credential_materialized: false
dummy_restore_result: pending
provider_network_calls: 0
decision: provisioning-partial-host-prerequisite-blocked
```

אין להוסיף Path אישי, Username, Email, IP שאינו loopback, Key, Credential, hash, Screenshot או Container environment dump.

## Gates הבאים

1. `G3-Hotelbeds-Store-Provisioning` — התקנת baseline ללא Hotelbeds Credential וללא Provider Network.
2. `G3-Hotelbeds-Store-Readiness-Verify` — RSV-01 עד RSV-11 עם Dummy credential בלבד.
3. `G4-Hotelbeds-Credential-Node` — first-party code ו-fixtures בלבד.
4. `G3-Hotelbeds-Materialization` — Owner-operated entry אמיתי, ללא API call.
5. `G3-Hotelbeds-Metadata-Verify` — metadata בלבד.
6. `G5-Hotelbeds-Network-Smoke` — קריאות Evaluation מוגבלות, לאחר אישור נפרד.

אף Gate אינו יורש אישור מהקודם.

## מקורות רשמיים

- n8n deployment variables: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/deployment>
- n8n execution variables: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions>
- n8n custom encryption key: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/set-a-custom-encryption-key>
- n8n CLI and credential export: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/use-the-command-line>
- n8n 2FA: <https://docs.n8n.io/administer/manage-users-and-access/verify-user-identity/require-two-factor-auth>
- n8n disable public API: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/disable-the-public-api>
- n8n telemetry controls and isolation: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/control-telemetry>, <https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/isolate-n8n>
- n8n node blocking and SSRF protection: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/block-specific-nodes>, <https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/enable-ssrf-protection>
- n8n encryption-key rotation: <https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/rotate-encryption-keys>
