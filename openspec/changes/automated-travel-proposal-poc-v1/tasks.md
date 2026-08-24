# משימות: Automated Travel Proposal PoC v1

## 0. חבילת מפרט ו-Gate Owner

- [x] ATP0.1 לנסח Proposal, Scope, Exclusions, Success Criteria, סיכונים ומשמעות אישור. Requirements: ATP-101, ATP-102, ATP-106, ATP-107, ATP-110.
- [x] ATP0.2 להגדיר חוזי Intake, Evidence, Ranking, Draft, Failure, Isolation, Audit ו-Cost כ-Spec Delta בדיק. Requirements: ATP-101 עד ATP-110.
- [x] ATP0.3 לתכנן ארכיטקטורה ספק-ניטרלית, זרימת נתונים, הרשאות, Rollout, Rollback וחלופות. Requirements: ATP-102, ATP-103, ATP-104, ATP-107, ATP-108, ATP-109, ATP-110.
- [x] ATP0.4 להריץ `openspec validate automated-travel-proposal-poc-v1 --strict`, לסקור Diff ולוודא שאין Secret, מידע אישי, Tenant URL או שינוי חופף. Requirements: ATP-101, ATP-109, ATP-110.
- [x] **G0-Spec:** אושר על ידי ה-Owner ב-2026-08-22. האישור לא פתח חשבון ולא אישר Credentials, Billing, API call, Runtime, Model, Botpress, Commit או Push. Requirements: ATP-107, ATP-110.

## 1. Preflight ציבורי לספקים

- [x] ATP1.1 אומת בתיעוד הרשמי של Duffel: Test mode, פעולות חיפוש, תוקף Offers, Schema/API version, מגבלת Metasearch, תמחור פומבי ופערי זכאות/מחיקה. אין פתיחת חשבון. Evidence: `provider-preflight-evidence.md`. Requirements: ATP-102, ATP-103, ATP-107, ATP-108, ATP-110.
- [x] ATP1.2 אומת בתיעוד הרשמי של Hotelbeds: Evaluation mode, מכסת 50 בקשות ביום, Availability, Content batch, CheckRate, Certification ופעולות אסורות; פערי זכאות/עלות/מחיקה נשארו מפורשים. אין פתיחת חשבון. Evidence: `provider-preflight-evidence.md`. Requirements: ATP-102, ATP-103, ATP-107, ATP-108, ATP-110.
- [x] ATP1.3 הוגדרו Hostname, Endpoint ו-Method allow-list מועמדים ו-deny-list לפעולות Mutation. הנתיבים אינם מאשרים Network ויינעלו מחדש לפני G5. Evidence: `provider-preflight-evidence.md`. Requirements: ATP-102, ATP-108, ATP-109.
- [x] ATP1.4 תועדו תנאי שימוש, Retention/Data-residency gaps, Rate limits, Search-only suitability והחלטות Go/No-Go. Evidence: `provider-preflight-evidence.md`. Requirements: ATP-107, ATP-108, ATP-109, ATP-110.
- [x] **G1-Provider-A0:** אושר Public preflight ב-2026-08-22; `Duffel Test` נבחר תחילה, נחסם בהרשמה משום שישראל אינה ברשימה, וה-Owner בחרה ב-`Hotelbeds Evaluation` כמועמד החלופי. Requirements: ATP-102, ATP-107, ATP-110.

## 2. תכנון נתונים סינתטיים ו-Acceptance

- [ ] ATP2.1 להגדיר גרסת `SyntheticTravelRequest` עם שדות חובה, Forbidden fields, Redaction policy ו-10 תרחישי בדיקה. Requirements: ATP-101.
- [ ] ATP2.2 ליצור תכנון fixture סינתטי ליעד אחד הכולל אטרקציות, מרחקים, שעות, אילוצים ועלויות בדיקה מומצאות ומסומנות. Requirements: ATP-101, ATP-104.
- [ ] ATP2.3 להגדיר `FlightOfferEvidence` ו-`HotelOfferEvidence` schemas עם completeness ו-drift handling. Requirements: ATP-103, ATP-108.
- [ ] ATP2.4 להגדיר מטריצת דירוג, אילוצים קשיחים, משקלים, Tie-breakers והסבר ציון. Requirements: ATP-104.
- [ ] ATP2.5 להגדיר Template טיוטה עברית עם מקורות, timestamps, מטבעות, אזהרות, חלופות ו-Agent review. Requirements: ATP-105, ATP-106.
- [ ] ATP2.6 להגדיר תרחישי הצלחה, חסר מידע, כשל ספק, 429, 401/403, Schema drift, Prompt injection, Cross-tenant, Secret leak, עלות ופעולה אסורה. Requirements: ATP-101 עד ATP-110.
- [ ] ATP2.7 לקבל אישור Owner ל-fixtures, משקלי הדירוג, תרחישים וספי קבלה לפני Materialization. Requirements: ATP-104, ATP-105, ATP-107, ATP-110.

## 3. שערי חשבון ו-Credentials עתידיים

- [x] **G2-Duffel-Account:** אושר ונפתח דף ההרשמה הרשמי. ישראל לא הופיעה ברשימת `Country of incorporation`; לא נבחרה מדינה חלופית והטופס לא נשלח. Outcome: `NO-GO / REGISTRATION-BLOCKED`. Requirements: ATP-109, ATP-110.
- [x] **G2-Hotelbeds-Account:** אושר ונפתח דף ההרשמה הרשמי; ה-Owner הזינה בעצמה מידע אישי וסיסמה והצהירה ב-2026-08-22 שהחשבון נוצר. Codex לא קרא מידע אישי או Credential ולא ביצע API call. Requirements: ATP-109, ATP-110.
- [x] **G2/3-Hotelbeds-Doc:** ה-Owner אישרה תיעוד בלבד. תועד הקשר הטכני בין Account ל-Credential בלי לקרוא, להעתיק, לשמור או להשתמש ב-API Key/Secret ובלי API call. Requirements: ATP-107, ATP-109, ATP-110.
- [x] **G3-Hotelbeds-A0:** בוצעה בדיקה מבנית לקריאה בלבד. זוהו לפחות שתי רשומות Credential ושדות Environment, Rate limits, Quotas ו-Throttling; לא נקראו ערכי API Key/Secret ולא בוצעה קריאת API. Environment ומכסה נשארו `UNVERIFIED`. Requirements: ATP-102, ATP-107, ATP-109, ATP-110.
- [x] **G3-Hotelbeds-A0-Doc:** ה-Owner אישרה תיעוד של ראיית A0 הממוזערת בלבד. Evidence: `provider-preflight-evidence.md`. Requirements: ATP-107, ATP-109, ATP-110.
- [x] **G3-Hotelbeds-Credential-Plan:** הוגדר Owner-operated direct handoff, חוזה Credential Store, reference ממוזער, חישוב `X-Signature` עתידי, Rotation, Revocation ו-gates נפרדים. לא נקרא או נשמר Secret ולא בוצע API call. Evidence: `credential-handoff-plan.md`. Requirements: ATP-102, ATP-107, ATP-109, ATP-110.
- [ ] **G3-Duffel-Credential:** לאחר אישור נפרד בלבד, ליצור Test Credential, לשמור אותו ב-Credential Store ייעודי ולתעד Reference ממוזער בלי לחשוף את ה-Secret. Requirements: ATP-102, ATP-107, ATP-109, ATP-110.
- [x] **G3-Hotelbeds-Store-Selection:** בוצעה השוואה ציבורית של n8n Cloud, n8n self-hosted ו-Enterprise External Secrets. נבחר מותנה `n8n self-hosted Community` עם Credential Store מובנה ל-Instance מקומי, Owner יחיד ו-Tenant סינתטי בלבד; אין התקנה, רכישה, Runtime, Secret או API call. Evidence: `credential-store-selection.md`. Requirements: ATP-107, ATP-109, ATP-110.
- [x] **G3-Hotelbeds-Store-Readiness-Spec:** ננעל מפרט Pass/Fail ל-Host Windows מקומי, container pinned עתידי, HTTPS ו-loopback-only, Full-disk encryption, Owner+2FA, Key custody, CLI/export restrictions, אפס execution payloads, backup/restore עם Dummy credential, Retention ו-first-party signature boundary. אין התקנה, Runtime, Secret או API call. Evidence: `credential-store-readiness-spec.md`. Requirements: ATP-102, ATP-107, ATP-109, ATP-110, ATP-111.
- [ ] **G3-Hotelbeds-Store-Provisioning:** אושר ב-2026-08-22. הוכן baseline לא-סודי על branch ייעודי וננעלו n8n `2.35.7` ו-image digest; ההפעלה נשארה `PARTIAL / HOST-PREREQUISITE-BLOCKED` משום ש-Docker daemon אינו עולה ו-Full-disk encryption לא אומתה. לא נוצרו Container, Volume או Network. אין Hotelbeds Credential ואין Provider Network או API call. Evidence: `provisioning/n8n/provisioning-evidence.md`. Requirements: ATP-109, ATP-110, ATP-111.
- [ ] **G3-Host-Remediation:** אושר ב-2026-08-22 לתיקון WSL/Docker ולאימות BitLocker בלבד. שני Windows restarts בוצעו באישור Owner, WSL `2.7.12.0` הותקן מחבילת Microsoft רשמית ומאומתת, ו-BitLocker עבר Full-encryption/Protection check ללא Recovery Key exposure. Docker עדיין `starting` ונכשל ב-DrvFS/Plan9 port `50002`, למרות Flags `15` ו-installer validation תקין. Docker VMM Pilot לא נשמר אפקטיבית; repair/reinstall, upgrade או עריכת settings דורשים אישור נפרד. לא נוצרו משאבי n8n ולא הייתה Provider network access. Evidence: `provisioning/n8n/host-remediation-evidence.md`. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-VMM-Pilot:** בוצע ב-2026-08-22 בגבולות backend ו-Docker data disk בלבד. install-in-place החזיר `-5`; בחירת `Docker VMM BETA` ו-`Apply` הופעלו ב-UI ללא קריאת settings/account/proxy metadata. לאחר full quit, `wsl --shutdown` ו-relaunch, Docker עדיין הפעיל `linux/wsl`, נשאר `starting` וה-daemon לא היה מוכן. Result: `FAIL / BACKEND-NOT-PERSISTED`. אין n8n Volume, Credential או Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-Upgrade-Pilot:** בוצע ב-2026-08-22 עם חבילת Docker Desktop `4.87.0.236836` רשמית, checksum תואם וחתימת Docker Inc תקפה. השדרוג per-user הסתיים ללא Reset/uninstall; `docker_data.vhdx` נשמר באותו נתיב, זמן יצירה וגודל, בעוד system disk `main/ext4.vhdx` נבנה מחדש בזמן startup. Docker עדיין הפעיל `linux/wsl`, נכשל ב-`UtilConnectVsock` port `50002`, וה-daemon לא היה מוכן. Result: `UPGRADE-PASS / DATA-DISK-PRESERVED / HOST-BLOCKED`. אין n8n resources, Credential או Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-VMM-Retry-4.87:** בוצע ב-2026-08-22. `Docker VMM BETA` נבחר ו-`Apply` הופעלו ב-UI הרשמי; לאחר full quit, `wsl --shutdown` ו-relaunch Docker חזר ל-`linux/wsl` וה-daemon לא היה מוכן. `docker_data.vhdx` נשמר ולא נוצר VMM system disk. Result: `FAIL / VMM-BACKEND-BLOCKED`. אין Reset/uninstall, n8n resources, Credential או Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-Offline-Backup:** בוצע ב-2026-08-22. Docker ו-WSL נעצרו; `docker_data.vhdx` הועתק פעם אחת ליעד `D:` בלי overwrite. גודל המקור והעותק `51380224` bytes וה-SHA-256 תאם. ה-Owner אישרה במפורש שימוש ביעד FAT בלתי מוצפן לאחר גילוי הסיכון. אין repair/uninstall/reset, n8n resources, Credential או Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-Reinstall:** בוצע ב-2026-08-22. preflight אישר checksum של עותק D ומתקין `4.87.0` חתום; Docker הוסר והותקן מחדש, והשחזור של `docker_data.vhdx` עבר checksum. ניסיון daemon נכשל שוב ב-`UtilConnectVsock` port `50002`; Docker ו-WSL נעצרו. ניסיון העלייה שינה את hash הדיסק המקומי לאחר השחזור, אך עותק D נשאר קיים ושלם. Result: `REINSTALL-PASS / RESTORE-PASS / HOST-BLOCKED`. אין Factory Reset, `wsl --unregister`, n8n resources, Credential או Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Windows-Integrity-Remediation:** בוצע ב-2026-08-22. עותק D נשאר זמין; `DISM /RestoreHealth` השלים `S_OK`, ו-`sfc /scannow` תיקן את `rndismp6.sys` ואת `usb80236.sys`; Windows אותחל להחלת התיקון. post-restart: WSL והשירותים תקינים, אך Docker daemon נשאר לא מוכן (`docker version` timeout והמתנה ל-`socketforwarder-receive-fds.sock`). Result: `WINDOWS-INTEGRITY-PASS / DOCKER-HOST-BLOCKED`. אין Factory Reset, `wsl --unregister`, VHDX/backup deletion, Docker settings, n8n resources, Credential או Provider Network. תיקון Docker נוסף דורש Gate נפרד. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-Vsock-Repair-Assessment:** בוצע ב-2026-08-22 לקריאה בלבד. `docker-desktop` עולה כ-WSL2, אך `/tmp/host/c` ריק; לוג bootstrap מוכיח כשל `UtilConnectVsock:610` ל-port `50002` במיפוי `C:`. שירותי WSL/Hyper-V פעילים והחשבון חבר Administrators עם token לא-מוגבה. Result: `WSL-DRIVE-SHARE-HOST-BLOCKED / PRIVILEGE-PILOT-CANDIDATE`. לא בוצע שינוי Docker/WSL/VHDX/n8n/Credential/Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-Privilege-Pilot:** בוצע חלקית ב-2026-08-22. `DockerCli -Shutdown` ובקשת סגירה רגילה לחלון לא השלימו; ה־backend אינו מגיב, `DockerCli` נשאר תלוי והלוג חוזר ל-`socketforwarder-receive-fds.sock`/`_ping` timeout. לא בוצע force-stop או elevated relaunch. Result: `NORMAL-QUIT-BLOCKED / ELEVATED-RELAUNCH-NOT-ATTEMPTED`. Requirements: ATP-109, ATP-110, ATP-111.
- [ ] **G3-Docker-Forced-Quit-Pilot:** דורש אישור Owner נפרד לעצירת תהליכי Docker ו-`wsl --shutdown` באופן ממוקד, אימות עצירה, הפעלה אחת כמנהלת ובדיקת `docker version` מקומית עם timeout. אין Settings/VHDX/uninstall/reset/n8n resource/Credential/Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-Docker-Forced-Quit-Pilot:** בוצע ב-2026-08-23. עותק D אומת; תהליכי Docker ו-WSL נעצרו, Docker הופעל דרך UAC כמנהלת, ו-`docker version` עדיין הגיע ל-timeout עם אותו `UtilConnectVsock`/Plan9, `socketforwarder-receive-fds.sock` ו-`_ping` failure. Docker ו-WSL נעצרו בסיום והעותק ב-D נשאר קיים. Result: `ELEVATED-DOCKER-FAIL / HOST-PLAN9-VSOCK-BLOCKED`. שינוי Windows/WSL נוסף דורש Gate נפרד. Requirements: ATP-109, ATP-110, ATP-111.
- [x] **G3-WSL-Feature-Repair:** בוצע ב-2026-08-23. בדיקה מוגבהת אישרה ש-WSL, `VirtualMachinePlatform` ו-`HypervisorPlatform` Enabled; לכן לא בוצעו תיקון/toggle/restart תחת Gate המותנה. Result: `FEATURES-PASS / PLAN9-VSOCK-REMAINS-BLOCKED`. Requirements: ATP-109, ATP-110, ATP-111.
- [ ] **G3-WSL-Feature-Cycle:** אושר ב-2026-08-23. preflight עבר: Docker/WSL עצורים והגיבוי ב-D קיים. Stage 1 השבית את `Microsoft-Windows-Subsystem-Linux` ואת `VirtualMachinePlatform` ללא restart אוטומטי; Windows restart ראשון מבוצע כעת. לאחר החזרה: אימות Disabled, enable, restart שני ובדיקת Docker מקומית. אין VHDX/backup deletion, Docker Reset/uninstall, n8n, Credential או Provider Network. Requirements: ATP-109, ATP-110, ATP-111.
- [ ] **G3-Hotelbeds-Store-Readiness-Verify:** לאמת loopback, access, 2FA, Key separation, disabled APIs/telemetry, execution persistence, node blocklist ו-Backup/Restore באמצעות Credential דמה סינתטי בלבד. Requirements: ATP-107, ATP-109, ATP-111.
- [ ] **G3-Hotelbeds-Materialization:** רק לאחר Readiness Verify ו-`G4-Hotelbeds-Credential-Node`, ליצור Entry ולהנחות Owner להזין ישירות את הערכים ללא צפיית Codex. אין API call וה-Entry נשאר unbound ו-disabled אם נתמך. Requirements: ATP-102, ATP-107, ATP-109, ATP-110, ATP-111.
- [ ] **G3-Hotelbeds-Metadata-Verify:** לאחר אישור נפרד, לאמת רק opaque reference, provider, Environment label, disabled/bound state ומכסה; אין לקרוא Secret. Requirements: ATP-102, ATP-107, ATP-109, ATP-110.
- [ ] ATP3.5 לאמת ביטול Credential, מחיקה, מכסה, Environment identity ו-Least Privilege לפני Network use. Requirements: ATP-107, ATP-109.

## 4. מימוש מקומי ללא Network — לא מאושר

- [ ] **G4-Local-Adapter:** לקבל אישור Owner ייעודי למימוש קוד מקומי בלבד על Branch ייעודי. Requirements: ATP-110.
- [ ] ATP4.1 לממש Schema validation ל-`SyntheticTravelRequest` ול-Forbidden fields. Requirements: ATP-101.
- [ ] ATP4.2 לממש Adapter interfaces ו-fixture-backed Duffel/Hotelbeds mappers ללא Network או Secret. Requirements: ATP-102, ATP-103.
- [ ] **G4-Hotelbeds-Credential-Node:** לאחר אישור G4 נפרד, לממש ולבדוק first-party n8n credential/node שמחשב חתימה עם Dummy values בלבד, נועל Host ו-read-only endpoints ואינו מחזיר Secret/Signature ל-Workflow data או Logs. Requirements: ATP-102, ATP-109, ATP-111.
- [ ] ATP4.3 לממש Constraint filter, deterministic ranker ו-score breakdown. Requirements: ATP-104.
- [ ] ATP4.4 לממש evidence-bound planner ו-Hebrew draft renderer עם fallback. Requirements: ATP-104, ATP-105, ATP-106.
- [ ] ATP4.5 לממש Endpoint allow-list, mutation deny-list, quota guard, retry guard ו-policy denials. Requirements: ATP-102, ATP-106, ATP-107, ATP-108.
- [ ] ATP4.6 לממש Tenant-scoped state ו-minimized audit records ללא Payload מלא. Requirements: ATP-109.
- [ ] ATP4.7 להריץ בדיקות מקומיות לכל 10 התרחישים ולשמור Evidence סינתטי. Requirements: ATP-101 עד ATP-110.

## 5. Network Smoke בסביבות Test/Evaluation — לא מאושר

- [ ] **G5-Network-Smoke:** לקבל אישור Owner נפרד לספק אחד, Credential אחד, מכסת קריאות מדויקת, Retry ceiling ואפס Billing. Requirements: ATP-107, ATP-110.
- [ ] ATP5.1 לאמת Config identity, Adapter version, Environment, Hostname allow-list ו-remaining quota לפני הקריאה הראשונה. Requirements: ATP-102, ATP-107, ATP-109.
- [ ] ATP5.2 להריץ מספר קבוע מראש של חיפושי טיסה סינתטיים ב-Duffel Test ולמדוד Schema, latency, errors ו-usage. Requirements: ATP-102, ATP-103, ATP-107, ATP-108.
- [ ] ATP5.3 לאחר Gate נפרד, להריץ מספר קבוע מראש של חיפושי מלון סינתטיים ב-Hotelbeds Evaluation ולמדוד Schema, latency, errors ו-usage. Requirements: ATP-102, ATP-103, ATP-107, ATP-108.
- [ ] ATP5.4 להוכיח שאין Mutation, הזמנה, Hold, Payment, Messaging או נתוני נוסע אמיתיים ב-requests, responses, logs או diff. Requirements: ATP-101, ATP-102, ATP-106, ATP-109.
- [ ] ATP5.5 לבטל Credentials או להשביתם בסוף Stage אם לא אושר המשך, ולשמור ראיית מחיקה/ביטול ממוזערת. Requirements: ATP-109, ATP-110.

## 6. Orchestrated PoC ו-Model — לא מאושר

- [ ] **G6-Orchestrated-PoC:** לבחור Dify/n8n configuration, Model, request ceiling, token ceiling, retry ceiling ותת-תקציב ILS; לקבל אישור Owner נפרד. Requirements: ATP-107, ATP-109, ATP-110.
- [ ] ATP6.1 לבנות Workflow נפרד לכל Adapter ו-Policy Gate מרכזי, עם Idempotency ו-Timeout. Requirements: ATP-102, ATP-107, ATP-108.
- [ ] ATP6.2 לחבר את Normalizer, Ranker, Planner ו-Draft Renderer בלי לחשוף Payload גולמי או Secret למודל. Requirements: ATP-103, ATP-104, ATP-105, ATP-109.
- [ ] ATP6.3 להגדיר Model instructions שמפרידות Evidence, Calculation, Assumption ו-Unsupported, ומחזירות `INSUFFICIENT_EVIDENCE` בכשל. Requirements: ATP-104, ATP-105, ATP-108.
- [ ] ATP6.4 להריץ את 10 התרחישים הסינתטיים תחת מכסת Stage ולעצור בכל חריגה. Requirements: ATP-101 עד ATP-110.
- [ ] ATP6.5 לשמור Evidence ממוזער של איכות, latency, calls, tokens, retries, denials ועלות. Requirements: ATP-107, ATP-109.

## 7. סקירת PoC ויציאה

- [ ] ATP7.1 לבדוק את ספי ההצלחה, traceability, fallback, security, isolation, quota ו-zero-side-effect. Requirements: ATP-101 עד ATP-110.
- [ ] ATP7.2 להשוות זמן, איכות, עלות ומגבלות מול תהליך ידני ומול ספקי Production מועמדים, בלי להשתמש בנתוני לקוח. Requirements: ATP-104, ATP-107, ATP-110.
- [ ] ATP7.3 לתעד Adapter drift, Provider gaps, Terms risks, Open decisions ו-Production blockers. Requirements: ATP-108, ATP-109, ATP-110.
- [ ] ATP7.4 לבטל Credentials, למחוק נתוני ספק ניסויים ולוודא ש-Git נשאר מקור האמת ללא Secrets. Requirements: ATP-109.
- [ ] **G7-PoC-Review:** לקבל החלטת Owner: Stop, Iterate, או להציע Change נפרד ל-Production discovery. אף החלטה אינה מאשרת Production אוטומטית. Requirements: ATP-107, ATP-110.

## 8. שינויים עתידיים נפרדים — מחוץ לתחום

- [ ] Change נפרד ל-Google Places/Routes, כולל Billing, Privacy, Attribution, caching ו-SKU caps. Requirements: ATP-107, ATP-110.
- [ ] Change נפרד ל-Expedia Rapid, Skyscanner, Booking.com, Travel Booster, Amadeus או Provider Production אחר. Requirements: ATP-102, ATP-107, ATP-109, ATP-110.
- [ ] Change נפרד למידע אישי אמיתי, Consent, Retention, Deletion, DPA ו-Security/Privacy approval. Requirements: ATP-101, ATP-109, ATP-110.
- [ ] Change נפרד ל-Email או WhatsApp עם Human approval ו-Audit. Requirements: ATP-106, ATP-110.
- [ ] Change נפרד להזמנה, תשלום, PNR, כרטוס, ביטול או Refund. Requirements: ATP-106, ATP-107, ATP-110.
- [ ] Botpress נשאר מחוץ לתחום עד סגירת `INCIDENT-HOLD` ואישור Change נפרד. Requirements: ATP-110.
