# Conversational Client Intake Template

מטרת התבנית היא להפיק מספיק מידע ל-Draft Spec בלי להפוך את התהליך לטופס טכני ארוך.

## UX target

- בדרך כלל פחות מ-10 דקות.
- בדרך כלל 5-6 שאלות קריטיות לאחר ה-Opening.
- אלה יעדים, לא hard limits. שאלה נוספת מותרת אם חסר מידע שחוסם החלטה בטוחה, תמחור סביר, data policy או consequential action boundary.

## Opening

**Prompt:** "תאר/י במשפט או שניים מה היית רוצה שה-Agent יעשה בשבילך."

## Adaptive critical questions

שאל רק מה שחסר.

### Outcome

- מה התוצאה שהכי חשוב לך לקבל ממנו?

### Users

- עם מי ה-Agent ידבר או עבור מי הוא יעבוד?

### Channel / current workflow

- איפה העבודה הזו מתרחשת היום - אתר, WhatsApp, מייל, CRM, מסמכים או מקום אחר?

### Knowledge / data

- איזה מידע הוא חייב לדעת כדי לעשות את העבודה טוב?

### Boundaries

- מה הוא לא צריך לעשות בלי אישור שלך?

### Budget

- איזה סדר גודל של תקציב מתאים להפעלה שלו?
  - חסכוני
  - מאוזן / מומלץ
  - מתקדם
  - סכום מותאם אישית
  - לא יודע/ת - הציעו לי

## Inference rules

- אל תשאל שאלה טכנית אם ניתן להסיק את הצורך העסקי.
- בבקשה עמומה: `infer -> show assumptions -> confirm/correct`.
- אם הלקוח אומר "לא יודע", הצע 2-3 אפשרויות והמלצה.
- אל תניח Permission, elevated Data class או consequential Side Effect בלי policy/confirmation מתאים.
- שאל Budget מוקדם כדי לא לתכנן פתרון לא מתאים.
- התחל מהארכיטקטורה הפשוטה ביותר שמספקת את ה-outcome; הוסף integrations/autonomy/persistent memory/premium models רק כאשר יש הצדקה.

## Confirmation summary

הצג סיכום קצר של:

- Goal.
- Users/workflow.
- Channels/services material to the client.
- Data needed + material data-use assumptions.
- Actions allowed.
- Actions requiring approval.
- Budget/range and expected overage behavior.
- Important assumptions.
- Known initial limitations.

בקש אישור אחד לסיכום המהותי לפני יצירת Draft Spec. אין צורך לבקש אישור נפרד לכל בחירה טכנית low-impact.

## Output

ה-Factory מייצר מאחורי הקלעים `ClientIntent`, assumptions, risk/trust recommendation, budget/optimization profile, capability/data/channel requirements, release/eval requirements ו-Draft Spec/AgentManifest/ClientInstanceConfig.