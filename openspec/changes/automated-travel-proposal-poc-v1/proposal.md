# הצעה: Automated Travel Proposal PoC v1

## תקציר

להגדיר PoC אוטומטי, סינתטי וקריאה-בלבד עבור סוכני נסיעות. ה-PoC יקבל דרישות נסיעה מובנות, יחפש הצעות ניסוי לטיסות ולמלונות דרך מתאמי API מאושרים, ינרמל את התוצאות, יבנה מסלול יומי ויפיק טיוטת הצעה בעברית לבדיקת סוכן אנושי.

השינוי הזה הוא מפרט בלבד. הוא אינו פותח חשבונות, אינו יוצר Credentials, אינו מפעיל Billing, אינו משנה Botpress ואינו מריץ API, מודל או Runtime.

## למה

סוכן נסיעות צריך לקצר את הזמן שבין קבלת דרישות הלקוח לבין טיוטת הצעה מותאמת. תהליך ידני אינו משיג את יעד האוטומציה, ול-Owner אין כרגע גישת API ל-Travel Booster או ל-Amadeus. PoC עם ספקי Sandbox/Evaluation מאפשר לבדוק את זרימת העבודה, הנרמול, הדירוג, תכנון המסלול ובקרות הכשל לפני התחייבות לספק Production או שימוש במידע אמיתי.

## סיווג היכולת

- Knowledge: בניית מסלול והסבר הבחירות מתוך ראיות מנורמלות.
- Service: חיפושי API לקריאה בלבד בסביבות ניסוי מאושרות.
- Action: מחוץ לתחום; אין הזמנה, שמירת PNR, תשלום, כרטוס או שליחה.
- משתמשים: Owner וסוכן נסיעות מורשה בלבד בממשק בדיקה עתידי.

## בתחום

- קלט סינתטי מובנה: מוצא, יעד, תאריכים, מספר והרכב נוסעים, תקציב, העדפות ואילוצים.
- `Duffel Test` כמועמד לחיפוש טיסות ניסוי בלבד.
- `Hotelbeds Evaluation` כמועמד לחיפוש מלונות ניסוי בלבד.
- מתאמי ספק נפרדים שממפים תשובות לסכימה קנונית אחת.
- דירוג חלופות לפי אילוצים מפורשים, מחיר ניסוי, משך, עצירות והתאמה להעדפות.
- מסלול יומי סינתטי עם שאלות להשלמת מידע, הנחות גלויות וחלופות.
- טיוטת הצעה בעברית הכוללת מקור, זמן חיפוש, מטבע, סטטוס טריות ואזהרת מחיר.
- כשל סגור כאשר אין ראיות מספיקות, ספק אינו זמין או מכסה חסומה.
- Audit ממוזער ללא Prompt מלא, Secret או מידע אישי.
- תכנון ספק-ניטרלי המאפשר להחליף ספק מאוחר יותר בלי לשנות את חוזה הפלט.

## מחוץ לתחום

- מידע אמיתי על לקוח, נוסע, דרכון, מועדון נוסע מתמיד, אמצעי תשלום או הזמנה קיימת.
- Travel Booster, Amadeus, Expedia Rapid, Skyscanner, Booking.com או API מסחרי אחר.
- Google Places, Google Routes, Google Flights או Google Hotels. Google Maps Platform דורש Billing ולכן הוא Gate נפרד.
- כל API לא רשמי שסורק Google Flights או Google Hotels.
- פתיחת חשבון, יצירת Token, Secret, API key, Service Account או Payment method.
- קריאת מחירים מסחריים, תעריפי חוזה, מלאי Production או הבטחת זמינות.
- הזמנה, Hold, Book, Order, PNR, תשלום, ביטול, Refund, כרטוס או שינוי חיצוני.
- שליחת Email או WhatsApp, פרסום Website, Publish או גישה ללקוח חיצוני.
- יצירת Bot או שימוש בשני משאבי Botpress שמקורם אינו ידוע. `INCIDENT-HOLD` נשאר בתוקף.
- Production, SLA, תמיכה תפעולית או התחייבות למחיר כלפי לקוח.

## ספקי הניסוי המוצעים

### Duffel Test

ישמש לבדיקת חוזה חיפוש הטיסות, טיפול בתוצאות ובמצבי כשל. נתוני ה-Sandbox עשויים להיות מלאכותיים, אינם מוכיחים כיסוי Production ואינם מיועדים להצעה מסחרית.

מקור ציבורי רשמי: <https://duffel.com/docs/api/overview/test-mode>

### Hotelbeds Evaluation

ישמש לבדיקת חיפוש מלונות, תוכן, זמינות ניסוי ונרמול תעריפים. סביבת Evaluation מוגבלת לפי התיעוד הציבורי ל-50 בקשות ביום ומחזירה תנאים כלליים שאינם מייצגים בהכרח הסכם מסחרי.

מקור ציבורי רשמי: <https://developer.hotelbeds.com/documentation/getting-started/>

## קריטריוני הצלחה

- כל תרחישי הקבלה משתמשים בנתונים סינתטיים בלבד.
- 10 מתוך 10 בקשות בדיקה תקינות מפיקות טיוטה או כשל מוסבר ללא פעולה חיצונית.
- כל הצעת טיסה ומלון שמופיעה בטיוטה ניתנת למיפוי לראיית ספק מנורמלת.
- 100% מהמחירים כוללים מטבע, מקור, זמן חיפוש וסטטוס `test` או `evaluation`.
- 100% מהתוצאות מסומנות כלא-ניתנות למכירה וככפופות לאימות סוכן.
- כל חוסר כיסוי, Timeout, חריגת מכסה או תשובה פגומה מפעילים fallback מוגדר ללא המצאת חלופה.
- אין קריאה ל-Booking, Payment, Order, Email, WhatsApp, Publish או Botpress.
- Audit שומר מזהים ומדדים ממוזערים בלבד ואינו שומר Secret או פרטי נוסע.
- השימוש העתידי, אם יאושר, נשאר בתוך תקרת הניסוי הכוללת של 200-500 ש"ח לחודש ובתת-תקרה ייעודית שתאושר מראש.

## השפעה צפויה

- חוזה קנוני לשילוב מקורות טיסה ומלון בלי תלות בספק יחיד.
- בסיס להערכת זמן יצירת הצעה, איכות דירוג, כשלי ספק ועלות חיפוש.
- הפרדה ברורה בין הוכחת אוטומציה לבין מוכנות מסחרית או Production.

## סיכונים ופשרות

- נתוני Sandbox/Evaluation אינם מוכיחים מחירים, זמינות או כיסוי חברות אמיתיים.
- תכנון יעד ללא Google Places/Routes או מקור POI חי יהיה מוגבל ל-fixtures סינתטיים ב-PoC.
- ספקי Travel Production עשויים לדרוש הסכם, Conversion או הזמנות; התאמת Search-only נשארת לא מוכחת.
- ריבוי ספקים מוסיף שגיאות סכימה, Rate limits, תנאי שימוש ותלות בזמינות חיצונית.
- מידע ספק עלול להיות שגוי או זדוני ולכן ייחשב קלט לא מהימן.
- שימוש ב-LLM עלול לצרוך תקציב ולהמציא פרטים אם בקרות הראיות אינן נאכפות.

## החלטות Owner

- אושר ב-2026-08-22: אפיון `PoC-Spec` אוטומטי בלבד.
- האישור כולל כתיבת Proposal, Spec Delta, Design ו-Tasks מקומיים.
- האישור אינו כולל חשבונות, Credentials, Billing, API calls, Runtime, Indexing, Model calls, Botpress, Commit או Push.
- אושר ב-2026-08-22: `G0-Spec` לחבילת המפרט הקיימת.
- אושר ב-2026-08-22: `G1-Provider-A0` ציבורי בלבד, לצורך אימות מקורות רשמיים ובחירת ספק חשבון מועמד אחד.
- תוצאת G1: `Duffel Test` נבחר כספק החשבון המועמד הראשון. הבחירה אינה אישור לפתוח חשבון, לקבל תנאים, ליצור Token או לבצע קריאת API.
- אושר ב-2026-08-22: `G2-Duffel-Account` לפתיחת דף הרשמה והנחיית Owner בלבד. ההרשמה נחסמה משום שישראל אינה מופיעה ברשימת `Country of incorporation`; לא נבחרה מדינה חלופית ולא נשלח הטופס.
- ה-Owner בחרה ב-2026-08-22 לעבור ל-`Hotelbeds Evaluation`, ואישרה `G2-Hotelbeds-Account` לפתיחת דף ההרשמה הרשמי בלבד.
- Hotelbeds מנפיקה Evaluation API Keys ו-Secret אוטומטית עם השלמת הרשמה, ולכן G2 ו-G3 אינם ניתנים להפרדה טכנית אצל הספק. ה-Owner אישרה `G2/3-Hotelbeds-Doc` בלבד; Codex לא קרא, העתיק, שמר או השתמש ב-Credential.
- ה-Owner הצהירה במפורש ב-2026-08-22 שחשבון Hotelbeds נוצר. קיום או תוכן ה-Credential לא נבדקו.
- אושר והושלם ב-2026-08-22: `G3-Hotelbeds-A0` לקריאה מבנית בלבד ו-`G3-Hotelbeds-A0-Doc`. זוהו לפחות שתי רשומות Credential ושדות מדיניות, בלי לקרוא, להציג, להעתיק או לשמור API Key/Secret ובלי API call.
- ערכי `Environment`, מכסה ו-Rate limits לא היו חשופים במטא-נתונים הבטוחים ולכן נשארו `UNVERIFIED`.
- אושר ב-2026-08-22: `G3-Hotelbeds-Credential-Plan` בלבד. התכנון מגדיר Owner-operated handoff ישיר ל-Credential Store עתידי, ללא חשיפת Secret ל-Codex, ל-Prompt, ל-Log, ל-Git או לקובץ מקומי.
- אישור התכנון אינו בוחר Runtime, אינו יוצר Credential Store entry, אינו מעתיק ערכים ואינו מאשר API call.
- אושר והושלם ב-2026-08-22: `G3-Hotelbeds-Store-Selection` ציבורי בלבד. נבחר מותנה `n8n self-hosted Community` עם Credential Store מוצפן מובנה, ל-Instance מקומי ומבודד של ה-Tenant הסינתטי בלבד.
- הבחירה אינה מאשרת התקנה, Host, Account, Subscription, Runtime, Custom node, Credential entry, Secret, API call או Network. לפני Materialization נדרש Gate מוכנות נפרד ל-Encryption-key custody, backup/restore, Owner-only access, redaction ודרך חתימה דינמית שאינה חושפת Secret.
- אושר והושלם ב-2026-08-22: `G3-Hotelbeds-Store-Readiness-Spec` בלבד. ננעל חוזה מוכנות ל-Host Windows בשליטת ה-Owner, Instance מקומי containerized עם HTTPS ו-loopback-only, Full-disk encryption, Owner יחיד עם 2FA, מפתח n8n חיצוני ל-Database ול-Repository, גיבוי מוצפן, Restore עם Credential דמה, אפס שמירת execution payloads ו-first-party Hotelbeds credential/node.
- אישור ה-Readiness Spec אינו מאשר Provisioning, Docker, n8n Runtime, יצירת מפתח, Credential דמה או אמיתי, Custom node, Network, Hotelbeds Secret או API call.
- אושר ב-2026-08-22: `G3-Hotelbeds-Store-Provisioning` בלבד, להתקנת baseline מקומי ללא Hotelbeds Credential וללא Provider Network או API call. נבחרה n8n `2.35.7` וננעל linux/amd64 image digest. ההתקנה נעצרה Fail-Closed לפני יצירת Volume: Docker Desktop נשאר ב-`starting` עקב כשל WSL/vsock, ו-Full-disk encryption לא ניתנה לאימות ללא הרשאת Administrator. הוכנה חבילת תצורה לא-סודית בלבד; תיקון host דורש אישור נפרד.
- אושר ב-2026-08-22: `G3-Host-Remediation` לתיקון WSL/Docker ולאימות BitLocker בלבד. ה-Owner אישרה שני Windows restarts והם בוצעו. חבילת WSL `2.7.12.0` הרשמית, חתומה בידי Microsoft ותואמת ל-SHA-256 שפורסם ב-release, הותקנה ישירות בהצלחה. בדיקת BitLocker מוגבהת וממוזערת עברה: `C:` מוצפן במלואו וה-Protection פעיל; Recovery Key לא נקרא או הוצג. גם לאחר האתחול השני Docker נשאר ב-`starting` ונכשל ב-DrvFS/Plan9 mount עם `UtilConnectVsock` port `50002`; `docker-desktop` רשום עם Flags `15`, ולכן Drive mounting אינו כבוי. Docker installer validation עבר. המסלול הבטוח הבא הוא החלטה נפרדת על Docker VMM Beta או repair/reinstall עם backup; אף מסלול לא אושר עדיין. לא נוצרו n8n Container/Volume/Network ולא הייתה Provider network access.
- אושר ובוצע ב-2026-08-22: `G3-Docker-VMM-Pilot` לשינוי Docker backend וליצירת Docker data disk בלבד, ללא n8n Volume, Credential, Provider Network או מחיקת data קיים. ניסיון install-in-place עם `--backend=docker-vmm` החזיר `-5` ולא שינה את ההתקנה. בחירת `Docker VMM BETA` ו-`Apply` הופעלו דרך ה-UI הרשמי בלי לקרוא או לערוך `settings-store.json`; לאחר סגירה מלאה, `wsl --shutdown` והפעלה מחדש, Docker חזר ל-`linux/wsl`, נשאר ב-`starting`, וה-daemon לא היה מוכן. ה-Pilot הסתיים `FAIL / BACKEND-NOT-PERSISTED`; repair/reinstall, upgrade או עריכת settings דורשים אישור נפרד.
- אושר ובוצע ב-2026-08-22: `G3-Docker-Upgrade-Pilot` לשדרוג Docker Desktop במקום בלבד, תוך שמירת Docker data קיים. חבילת `4.87.0.236836` הורדה מהקישור הרשמי, תאמה ל-SHA-256 שפורסם ונשאה חתימת Docker Inc תקפה. השדרוג per-user הסתיים במקום ללא Reset או uninstall; `docker_data.vhdx`, דיסק נתוני ה-containers/images, נשאר באותו נתיב עם אותו זמן יצירה וגודל. `main/ext4.vhdx`, דיסק מערכת ה-backend, נבנה מחדש בזמן startup של הגרסה החדשה. לאחר ההפעלה Docker עדיין השתמש ב-`linux/wsl`, נכשל ב-`UtilConnectVsock` port `50002`, וה-daemon לא היה מוכן. תוצאת ה-Gate: `UPGRADE-PASS / DATA-DISK-PRESERVED / HOST-BLOCKED`; לא נוצרו משאבי n8n ולא הייתה Provider Network או API call.
- אושר ובוצע ב-2026-08-22: `G3-Docker-VMM-Retry-4.87` בלבד, לניסיון מעבר חוזר ל-Docker VMM בגרסה `4.87.0`. `Docker VMM BETA` נבחר ו-`Apply` הופעלו דרך ה-UI הרשמי; לאחר full quit, `wsl --shutdown` והפעלה מחדש, Docker חזר ל-`linux/wsl` וה-daemon נשאר חסום. `docker_data.vhdx` נשמר, ולא נוצר דיסק VMM. תוצאה: `FAIL / VMM-BACKEND-BLOCKED`; לא בוצעו Reset, uninstall, n8n Container/Volume/Network, Credential, Provider Network או API call.
- אושר ובוצע ב-2026-08-22: `G3-Docker-Offline-Backup` — Docker ו-WSL נעצרו, ו-`docker_data.vhdx` הועתק ליעד נשלף `D:` בלי overwrite. גודל המקור והעותק היה `51380224` bytes וה-SHA-256 שלהם תאם. ה-Owner בחרה במפורש ביעד FAT בלתי מוצפן לאחר שהסיכון הובהר; היעד הוא recovery copy בלבד ולא מאשר repair או reinstall. לא בוצעו n8n, Credential, Provider Network או API call.
- אושר ובוצע ב-2026-08-22: `G3-Docker-Reinstall` — עותק D ומתקין `4.87.0` אומתו לפני uninstall; Docker הוסר, הותקן מחדש, ו-`docker_data.vhdx` שוחזר עם checksum תואם. ניסיון daemon ראשון נכשל שוב ב-`UtilConnectVsock` port `50002`, ולכן Docker ו-WSL נעצרו בלי repair נוסף. ניסיון העלייה כתב לדיסק המקומי ושינה את hash המקור אחרי השחזור; עותק D נותר קיים ושלם. תוצאה: `REINSTALL-PASS / RESTORE-PASS / HOST-BLOCKED`; לא בוצעו Factory Reset, `wsl --unregister`, n8n Container/Volume/Network, Credential, Provider Network או API call.
- אושר ובוצע ב-2026-08-22: `G3-Windows-Integrity-Remediation` — עותק D נותר זמין; `DISM /RestoreHealth` השלים `S_OK` ותיקן את מאגר רכיבי Windows ללא דרישת restart. `sfc /scannow` השלים ואיתר/תיקן את `rndismp6.sys` ואת `usb80236.sys`. מפתחות reboot הסטנדרטיים לא סומנו, אך `PendingFileRenameOperations` קיים; Windows אותחל להחלת תיקוני הדרייברים. לאחר האתחול WSL `2.7.12.0` והשירותים `WSLService`, `vmcompute`, `hns` היו תקינים, אך Docker daemon נשאר לא מוכן: `docker version` הגיע ל-timeout והלוג הציג המתנה ל-`socketforwarder-receive-fds.sock` וכשל `_ping`. התוצאה היא `WINDOWS-INTEGRITY-PASS / DOCKER-HOST-BLOCKED`; אין Factory Reset, `wsl --unregister`, מחיקת VHDX או גיבוי D, n8n Container/Volume/Network, Credential, Provider Network או API call. תיקון נוסף דורש Gate נפרד.
- אושר והושלם ב-2026-08-22: `G3-Docker-Vsock-Repair-Assessment` לקריאה בלבד. `docker-desktop` עולה כ-WSL2, אך `/tmp/host/c` קיים וריק; מיפוי `C:` נכשל עם `UtilConnectVsock:610` ל-port `50002` לפני עליית ה-daemon. שירותי WSL/Hyper-V הדרושים פעילים, וחשבון ה-Owner חבר בקבוצת Administrators אך מופיע עם token מסונן בהרצה הלא-מוגבהת. המסלול הבא הממוזער המוצע הוא `G3-Docker-Privilege-Pilot`: סגירה רגילה של Docker Desktop, הפעלה אחת כמנהלת ובדיקת `docker version` מקומית בלבד. הוא אינו מאושר עדיין ואסור לו לשנות Settings, VHDX, n8n, Credential או Provider Network.
- אושר ובוצע חלקית ב-2026-08-22: `G3-Docker-Privilege-Pilot`. בקשת `DockerCli -Shutdown` וסגירת החלון הרגילה לא השלימו: `DockerCli` נשאר תלוי וה־backend ממשיך להמתין ל-`socketforwarder-receive-fds.sock` ול-`_ping`. לא בוצע force-stop, ולכן לא ניתן היה להפעיל Docker מחדש כמנהלת. הצעד הבא דורש Gate נפרד ל-`G3-Docker-Forced-Quit-Pilot` עם עצירת תהליכי Docker ו-WSL ממוקדת, ללא Reset/uninstall/VHDX/n8n/Credential/Provider Network, ואז הפעלה מוגבהת אחת ובדיקת daemon מקומית.
- אושר ובוצע ב-2026-08-23: `G3-Docker-Forced-Quit-Pilot`. עותק הגיבוי ב-D והדיסק המקומי אומתו לפני הפעולה. תהליכי Docker ו-WSL נעצרו, Docker Desktop הופעל פעם אחת דרך UAC כמנהלת, ו-`docker version` המקומי הגיע ל-timeout. הלוג חזר לאותו כשל `UtilConnectVsock`/Plan9, המתנה ל-`socketforwarder-receive-fds.sock` וכשל `_ping`; לכן elevation אינו הפתרון. Docker ו-WSL נעצרו שוב בסיום והעותק ב-D נשאר קיים. התוצאה: `ELEVATED-DOCKER-FAIL / HOST-PLAN9-VSOCK-BLOCKED`. כל שינוי Windows/WSL נוסף דורש Gate נפרד.
- אושר והושלם ב-2026-08-23: `G3-WSL-Feature-Repair`. בדיקה מוגבהת אימתה ש-`Microsoft-Windows-Subsystem-Linux`, `VirtualMachinePlatform` ו-`HypervisorPlatform` כולם `Enabled`. מאחר שאף רכיב אינו חסר או כבוי, לא בוצעו תיקון, toggle או restart במסגרת ה-Gate. התוצאה: `FEATURES-PASS / PLAN9-VSOCK-REMAINS-BLOCKED`; כל feature-cycle או שינוי WSL מתקדם דורש Gate נפרד.
- אושר ב-2026-08-23: `G3-WSL-Feature-Cycle`. preflight אישר את קיום הדיסק המקומי והעותק ב-D, ו-Docker/WSL נעצרו. Stage 1 השבית את `Microsoft-Windows-Subsystem-Linux` ואת `VirtualMachinePlatform` ללא restart אוטומטי; אתחול Windows ראשון מבוצע להחלת ההשבתה. לאחר החזרה יש לאמת מצב Disabled, להפעיל מחדש את אותם רכיבים, ולאתחל פעם שנייה. אין מחיקת VHDX או גיבוי, Docker Reset/uninstall, n8n, Credential או Provider Network.

## תוצאת Preflight ציבורי

- `Duffel Test`: `NO-GO / REGISTRATION-BLOCKED` לשלב החשבון הנוכחי, משום שישראל אינה זמינה בטופס ההרשמה. מחירים ולוחות זמנים ב-Test אינם מציאותיים, ושימוש Production במודל Search-only מחייב אישור מסחרי כתוב בגלל מגבלות Metasearch ותמחור חיפוש.
- `Hotelbeds Evaluation`: `CONDITIONAL-GO / ACCOUNT-CREATED / CREDENTIAL-STRUCTURE-CONFIRMED / VALUES-UNREAD` לבדיקת Availability ותוכן ניסוי בלבד. המכסה הציבורית המתועדת היא 50 בקשות ביום, אך מכסת החשבון ו-Environment לא אומתו בדף. התאמת Production למוצר שאינו מבצע הזמנה לא הוכחה, ותהליך ה-Certification הציבורי הוא Booking-centric.
- Production בשני הספקים: `NO-GO / OUT-OF-SCOPE` עד להבהרת זכאות העסק הישראלי, Search-only, תנאים מסחריים, Retention/Deletion ועלויות בכתב.
- פירוט הראיות, נתיבי ה-API המועמדים והפערים נמצא ב-`provider-preflight-evidence.md`.

## סטטוס

`G0-SPEC-APPROVED / G1-PREFLIGHT-COMPLETE / G2-HOTELBEDS-COMPLETE / G3-A0-COMPLETE / G3-PLAN-COMPLETE / G3-STORE-CONDITIONALLY-SELECTED / G3-READINESS-SPEC-COMPLETE / G3-HOST-REMEDIATION-PARTIAL-USER-ACTION-REQUIRED / G3-PROVISIONING-PARTIAL-HOST-BLOCKED / G3-READINESS-VERIFY-BLOCKED / G3-MATERIALIZATION-BLOCKED / IMPLEMENTATION-BLOCKED`

החשבון נוצר לפי הצהרת ה-Owner. גם אם Credential נוצר אוטומטית, נדרש Gate נפרד לפני קריאתו, שמירתו או שימוש בו. baseline לא-סודי הוכן, אך Runtime ו-Volume לא נוצרו. API call, Billing, Runtime פעיל, Model, Botpress ויתר היישום נשארים חסומים.
