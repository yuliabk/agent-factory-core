# השוואת חלופות Runtime מנוהלות — K3.1

## סטטוס וגבול הרשאה

- מזהה מחקר: `ka-runtime-options-k3.1`
- תאריך אימות מקורות: 2026-08-20
- סטטוס: `research_complete_no_selection`
- היקף: השוואה לקריאה בלבד של Dify Cloud, Botpress Cloud ו-Flowise Cloud.
- לא בוצעו: פתיחת חשבון, התחברות, מסירת אמצעי תשלום, חיבור Credential, העלאת מסמך, Indexing, קריאת מודל או Runtime.
- מסמך זה אינו ADR ואינו בחירת ספק. בחירה שייכת ל-K3.2; כל פעולה בשירות חיצוני נשארת חסומה עד אישור K3.3.

## אילוצים וקריטריונים

ההשוואה נבחנה מול `AF-KA-01`, הקורפוס `af-demo-services-he@1.0.0`, סט השאלות `ka-prototype-he-v1` ותקרת Runtime עתידית של 100 ₪ לחודש. הקריטריונים הם:

1. יכולת למדוד Retrieval ומענה בעברית עם 25 השאלות הקפואות.
2. בידוד של ה-Owner, הסוכן והקורפוס, ונתיב עתידי לבידוד לקוחות.
3. ייצוא, גיבוי וניידות ללא Secrets.
4. מחיקה, Retention והוכחת סיום מחזור חיים.
5. אזור אחסון ו-Data Residency.
6. בקרת עלות מדידה ויכולת עצירה לפני 100 ₪.
7. מאמץ Owner נמוך והתאמה לעבודה Low-code.

## הנחת המרה לצורך סינון תקציבי

שער הייחוס האחרון שנמצא בבנק ישראל בעת המחקר הוא 2.9500 ₪ לדולר, מעודכן ל-2026-08-17. זהו שער אינדיקטיבי בלבד ואינו כולל מע"מ, עמלת כרטיס, הפרשי המרה או עלות ספק מודל. לכן מסלול בסיס של 35 דולר הוא כ-103.25 ₪ וכבר חורג מהתקרה לפני עלויות נוספות; 59 דולר הם כ-174.05 ₪; ו-89 דולר הם כ-262.55 ₪. לפני כל K3.3 יש לאמת מחדש מחיר ושער.

## טבלת החלטה

| קריטריון | Dify Cloud | Botpress Cloud | Flowise Cloud |
|---|---|---|---|
| מסלול רלוונטי לאב-טיפוס | Sandbox חינמי: 200 message credits, סביבת עבודה אחת, 5 Apps, 50 מסמכי Knowledge ו-50MB | PAYG ב-0 דולר לחודש; 100MB Vector DB ותקרת AI Spend ניתנת להגדרה; 5 דולר AI Spend כלולים לפי דף התמחור | Free ב-0 דולר: 2 Flows ו-2 Assistants, 100 Predictions בחודש ו-5MB |
| התאמה לתקרת 100 ₪ | מתאימה רק כל עוד נשארים ב-Sandbox ובקרדיטים; Professional ב-59 דולר לחודש חורג | מתאימה עקרונית ב-PAYG רק אם תקרת ההוצאה מוגדרת מתחת ל-100 ₪ וכל רכיבי השימוש נכללים במדידה; Plus ב-89 דולר חורג | Free עשוי להספיק לסבב של עד 90 ניסיונות; Starter ב-35 דולר חורג לפי שער הייחוס עוד לפני שימוש במודל |
| Knowledge/RAG ו-Low-code | UI חזותי ייעודי ל-Knowledge ול-Chat/Workflow; ההתאמה הישירה ביותר ל-Knowledge Agent קטן | Studio חזותי ו-Knowledge Bases; לוגים מציגים Query ותוצאות Retrieval | Assistant הוא המסלול הפשוט, ו-Chatflow נותן שליטה גבוהה ב-Retriever, Reranker ו-Vector DB; גמישות גבוהה אך יותר החלטות טכניות |
| עברית | אין בתיעוד הרשמי שנבדק התחייבות לאיכות Retrieval בעברית | אין בתיעוד הרשמי שנבדק התחייבות לאיכות Retrieval בעברית | אין בתיעוד הרשמי שנבדק התחייבות לאיכות Retrieval בעברית |
| בידוד | Sandbox כולל Workspace יחיד. מתאים ל-tenant הסינתטי היחיד; בידוד לקוחות עתידי יחייב Workspace/חשבון/Deployment נפרד ואימות הרשאות | Workspaces מארגנים Agents ותקציב; קבצים פרטיים כברירת מחדל, אך חברים בעלי גישה ל-Bot עשויים לקבל הרשאות רחבות. בידוד לקוחות דורש Workspace נפרד ובדיקות שליליות | Workspaces מתועדים כמחיצת משאבים עם RBAC, אך Unlimited Workspaces נמצא ב-Pro שעולה 65 דולר. Free מתאים רק ל-tenant הסינתטי היחיד |
| ייצוא וניידות | ה-DPA תומך בבקשות Data Portability, אך ייצוא מלא ושחזור של App, Knowledge Base, Chunks והגדרות לא אומתו בתיעוד הציבורי שנבדק | ייצוא `.bpz` כולל הגדרות, Workflows, Tables ו-Knowledge Bases, אך קובצי המקור נשארים בשרתי Botpress ומקושרים בלבד; לכן גיבוי מלא מחייב ייצוא מקורות נפרד | ייצוא/ייבוא JSON מתועד, IDs נשמרים ו-Credentials אינם מיוצאים. זהו נתיב הניידות הברור ביותר מבין השלוש |
| מחיקה ו-Retention | ה-DPA קובע שלקוח יכול למחוק מידע או לבקש מחיקה, ושמידע אישי נמחק לאחר סיום השירות. זמני מחיקה תפעוליים ו-Retention של לוגים/אינדקס דורשים אישור נוסף | API מתועד למחיקת Workspace וקבצים. Logs נשמרים 30 יום, Conversations/Messages כ-90 יום, Files ללא הגבלה אלא אם נקבע Expiry או נמחקו | מדיניות הפרטיות מאפשרת בקשת מחיקה, אך אינה נותנת SLA למחיקת Index/Logs; מידע אנונימי עשוי להישמר ללא הגבלת זמן |
| אזור אחסון | Dify מציינת "managed cloud region" בלי לזהות אזור בדף הציבורי שנבדק; Dedicated Enterprise יכול להיות באזור לקוח אך אינו מתאים לתקציב | אזור ברירת המחדל לא נמצא בתיעוד הציבורי שנבדק. Custom residency מופיע כיכולת בתמחור, אך הזכאות והעלות אינן מתאימות עדיין לאב-טיפוס | מדיניות הפרטיות מציינת במפורש US East 1 עבור Flowise Cloud |
| בקרת עלות | מכסות משאבים וקרדיטים קיימות, אך לא נמצא Hard Cap כספי מותאם אישית ב-Sandbox; יש להשאיר K3.3 חסום אם לא ניתן להבטיח עצירה | החזקה ביותר בתיעוד: Custom spending cap, פירוט AI Spend בלוגים, מכסות ברמת Workspace והתראות ב-75% | מכסת Predictions חודשית מתועדת, אך לא נמצא Hard Cap כספי מאוחד ל-LLM/Embedding/Vector DB; נדרש מנגנון חיצוני או חסימה |
| מאמץ Owner משוער | נמוך | נמוך-בינוני | בינוני |

## ניתוח חלופות

### חלופה A — Dify Cloud Sandbox

יתרונות:

- התאמה ישירה לדפוס Knowledge Agent, עם Knowledge Base, Chat App, Workflow ולוגים באותו ממשק.
- ששת המסמכים נכנסים בנוחות למכסת 50 המסמכים ו-50MB.
- מסלול חינמי מאפשר, בכפוף לאישור עתידי, ניסוי סינתטי ללא מנוי בסיס.
- תואם לכיוון הארכיטקטוני שכבר תועד, ולכן מפחית שינוי מושגים ומאמץ Owner.

חסרונות ופערים:

- 200 message credits אינם בהכרח 200 תשובות; הצריכה משתנה לפי מודל. יש לחשב את כל 25 השאלות וה-Retries לפני ריצה.
- לא נמצא Hard Cap כספי מותאם אישית ב-Sandbox.
- אזור האחסון המדויק אינו מפורט בדף הציבורי שנבדק.
- לא אומת Export מלא ושחזור של ה-Knowledge Base, ה-Chunks והתצורה.

השלכה: מועמד מוביל ל-K3.2 עבור אב-טיפוס סינתטי בלבד, בתנאי שכל פערי ה-K3.3 נסגרים מראש.

### חלופה B — Botpress Cloud PAYG

יתרונות:

- מסלול בסיס ב-0 דולר ותקרת AI Spend מותאמת אישית הם ההתאמה הטובה ביותר למדיניות Hard Stop.
- Workspaces מפרידים שימוש, Billing ו-Agents; קיימים לוגים מפורטים ל-AI Spend ול-Retrieval.
- Export של Bot ומחיקת Workspace/קבצים מתועדים.

חסרונות ופערים:

- Export ה-Bot אינו גיבוי מלא של קובצי המקור: הם נשארים מקושרים בשרתים.
- Files נשמרים ללא הגבלת זמן כברירת מחדל עד Expiry או מחיקה.
- אזור ברירת המחדל לא אומת, ו-Custom Residency עשוי להיות זמין רק בתוכנית יקרה יותר.
- פלטפורמה רחבה יותר של Agent/Workflow עלולה להוסיף מורכבות ביחס לסוכן Knowledge מצומצם.

השלכה: חלופת גיבוי חזקה, ובמיוחד אם Dify אינה יכולה לאכוף את גבול העלות או לספק נתיב מחיקה/ייצוא מספק.

### חלופה C — Flowise Cloud Free

יתרונות:

- 100 Predictions בחודש מתאימים מספרית לתקרת 90 הניסיונות המתוכננת, לפני אימות משמעות Prediction ועלויות מודל.
- מסלול Assistant פשוט, לצד אפשרויות RAG מתקדמות לניסוי מבוקר.
- Export/Import JSON מתועד ו-Credentials אינם נכללים בייצוא.
- אזור Cloud מפורט כ-US East 1.

חסרונות ופערים:

- Starter ב-35 דולר כבר חורג מתקרת 100 ₪ לפי שער הייחוס, ו-Free מוגבל ל-5MB ולשני Assistants/Flows.
- Workspaces מרובים ו-RBAC מתקדם קשורים למסלולים יקרים יותר; בידוד לקוחות עתידי אינו מתאים לתקרה הנוכחית.
- לא נמצא Hard Cap כספי מאוחד, ו-RAG גמיש יותר דורש יותר החלטות תחזוקה.
- מדיניות המחיקה וה-Retention אינה מספקת SLA למחיקת Index ולוגים.

השלכה: חלופת ניסוי טכנית טובה כאשר ניידות ושליטה ב-Retrieval חשובות יותר מפשטות; אינה הבחירה הראשונה ל-Owner Low-code בתקציב הנוכחי.

## מסקנה והמלצה ל-K3.2

K3.1 אינו בוחר Runtime. הוא מצמצם את ההחלטה העתידית כך:

1. **Dify Cloud Sandbox — מועמד מועדף** לאב-טיפוס הסינתטי והמצומצם, בזכות התאמת Knowledge/Low-code, מכסות מספקות לקורפוס והמשכיות עם הארכיטקטורה.
2. **Botpress Cloud PAYG — מועמד חלופי** אם Hard Cap כספי ולוג עלויות מפורט גוברים על פשטות וניידות מלאה.
3. **Flowise Cloud Free — עתודה טכנית**, בעיקר אם נדרשת שליטה עמוקה יותר בניסוי Retrieval או Export JSON, אך עם מאמץ Owner גבוה יותר.

המלצה זו אינה החלטה. K3.2 יישאר פתוח עד החלטת Owner ו-ADR ייעודי.

## תנאי חסימה לפני K3.3

אין לאשר Provisioning, Credentials, Indexing או Runtime עד שכל התנאים הבאים מקבלים ראיה כתובה:

- מחיר, מכסות, תנאי Free/PAYG ושער המרה מאומתים מחדש ביום ההחלטה.
- מוגדרת עצירה בפועל לפני 60/80/100 ₪, לרבות עלויות LLM, Embedding, Storage ו-Indexing.
- אזור האחסון, ספקי המשנה וזרימת המידע למודל מתועדים.
- מחיקת Corpus, Index, Logs, Conversations ו-Workspace ניתנת לבדיקה, כולל Retention לאחר מחיקה.
- Export מקומי בר-שחזור של App, תצורה, מקורות ונתוני הערכה אפשרי; אין Secrets בייצוא.
- ה-Knowledge Base, ה-Actor וה-Workspace נעולים ל-`af-demo-services` ול-Owner בלבד.
- External tools, Channels, Web search, Writes ו-Side effects מושבתים.
- עברית אינה מאושרת על בסיס הצהרת ספק: היא נמדדת רק באמצעות 25 השאלות הקפואות וכל ספי KA-102–KA-109.

## מקורות רשמיים

### Dify

- Dify Cloud pricing and quotas: https://dify.ai/pricing/dify-cloud
- Dify Cloud product overview: https://dify.ai/dify-cloud
- Dify Data Protection Agreement: https://dify.ai/assets/legal/data-protection-agreement.pdf
- Dify Enterprise deployment and residency options: https://dify.ai/dify-enterprise

### Botpress

- Botpress pricing and AI Spend cap: https://botpress.com/en/pricing
- Workspace, usage, roles and quota documentation: https://botpress.com/docs/studio/get-started/configure-your-workspace/
- Knowledge Base behavior and retrieval logs: https://botpress.com/docs/studio/concepts/knowledge-base/introduction/
- Bot import/export: https://botpress.com/docs/studio/concepts/import-export-bots/
- Retention periods: https://botpress.com/docs/studio/guides/advanced/retention-period/
- Workspace deletion API: https://botpress.com/docs/api-reference/admin-api/openapi/deleteWorkspace/
- Files API access and deletion model: https://botpress.com/docs/api-reference/files-api/getting-started/

### Flowise

- Flowise Cloud pricing: https://flowiseai.com/
- Product and RAG builders: https://docs.flowiseai.com/
- Cloud recommendation: https://docs.flowiseai.com/getting-started
- Workspaces and RBAC: https://docs.flowiseai.com/using-flowise/workspaces
- Cloud export/import behavior: https://docs.flowiseai.com/migration-guide/cloud-migration
- Cloud region, retention and deletion rights: https://flowiseai.com/privacy

### שער המרה

- Bank of Israel representative exchange rates: https://boi.org.il/en/economic-roles/financial-markets/exchange-rates/
