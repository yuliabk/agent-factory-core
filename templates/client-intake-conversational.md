# Conversational Client Intake Template

מטרת התבנית היא להפיק מספיק מידע ל-Draft Spec בלי להפוך את התהליך לטופס טכני ארוך.

## Opening

**Prompt:** "תאר/י במשפט או שניים מה היית רוצה שה-Agent יעשה בשבילך."

## Adaptive critical questions

שאל רק את השאלות שחסרות. יעד: עד 5-6 שאלות לאחר ה-Opening.

### Outcome

- מה התוצאה שהכי חשוב לך לקבל ממנו?

### Users

- עם מי ה-Agent ידבר או עבור מי הוא יעבוד?

### Channel

- איפה העבודה הזו מתרחשת היום - אתר, WhatsApp, מייל, CRM, מסמכים או מקום אחר?

### Knowledge

- איזה מידע הוא חייב לדעת כדי לעשות את העבודה טוב?

### Boundaries

- מה הוא לא צריך לעשות בלי אישור שלך?

### Budget

- איזה סדר גודל של תקציב חודשי מתאים לך להפעלה שלו?
  - מינימלי
  - בינוני
  - מתקדם
  - סכום מותאם אישית
  - לא יודע/ת - הציעו לי

## Inference rules

- אל תשאל שאלה טכנית אם ניתן להסיק את הצורך העסקי.
- אם הלקוח אומר "לא יודע", הצע 2-3 אפשרויות והמלצה.
- אל תבחר Permission, Data class או Side Effect מסוכן על בסיס הנחה בלבד.
- שאל Budget מוקדם מספיק כדי לא לתכנן פתרון שלא מתאים ללקוח.

## Confirmation summary

הצג סיכום קצר של:

- Goal.
- Users.
- Channels.
- Data needed.
- Actions allowed.
- Actions requiring approval.
- Budget.
- Important assumptions.

בקש אישור אחד לסיכום לפני יצירת Draft Spec.
