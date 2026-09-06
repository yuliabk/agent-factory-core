# Provider, Model and Cost Policy

**Status:** Proposed

## 1. מטרות

- למנוע תלות ב-Provider יחיד.
- לאפשר התאמה לתקציב לקוח.
- לאפשר מעבר מהיר כאשר מחיר, זמינות או איכות משתנים.
- לשלוט בעלות לפני ואחרי כל פעולה משמעותית.

## 2. אין Provider hard-code בלוגיקה עסקית

Agent מבקש Model Profile, לא Model name.

דוגמאות Profiles:

| Profile | Intent |
|---|---|
| `fast-cheap` | classification, extraction, simple drafting |
| `balanced` | general agent work |
| `high-reasoning` | complex planning or validation |
| `long-context` | large-context tasks |
| `private-data-compatible` | provider/runtime that satisfies data policy |

מיפוי Profile -> Provider/Model נשמר ב-Core configuration.

## 3. Router inputs

Model Router שוקל:

- Required capability.
- Data classification.
- Client restrictions.
- Region/privacy requirements.
- Cost budget.
- Latency.
- Context length.
- Eval quality score.
- Current provider health.

## 4. Fallback

Fallback מותר רק בין Models שעברו Compatibility Eval לאותו Profile.

Provider outage אינו סיבה לשלוח מידע ל-Provider שאינו מאושר ללקוח.

## 5. Budget levels

### Platform build budget

בזמן Build ה-Owner מקבל estimate וחלופות. ה-Owner מאשר את profile לפני הפעלת תהליך יקר.

### Client runtime budget

בזמן Runtime Budget שייך ללקוח או ל-Agent instance שלו. המערכת עוקבת אחרי שימוש מצטבר ומתריעה לפני חריגה.

### Emergency safety cap

קיימת תקרה נפרדת שמטרתה למנוע loop, runaway recursion או תקלה שמייצרת חיובים. הפעלתה עוצרת פעולות חדשות ודורשת Operator review.

## 6. Warning and approval flow

ברירת מחדל:

- 50% - informational event.
- 80% - warning ללקוח/Owner לפי שלב.
- 95% - high warning + cost projection.
- פעולה שתעבור את 100% - preflight pause + explicit approval.

אישור חריגה חייב לכלול:

- Amount or new limit.
- Period.
- Approver.
- Timestamp.
- Expiration או review date.
- Reason.

## 7. Per-request checks

כל request עובר בדיקת Budget בסיסית.

לפני פעולה מורכבת/יקרה מבוצע preflight estimate ככל שניתן, לדוגמה:

- Large web research.
- Batch document processing.
- Multi-agent plan.
- Long-context model.
- High-cost image/video processing.

## 8. Cost event

Audit cost event כולל לפחות:

```text
request_id
agent_id
agent_release_id
provider
model
operation_type
input_units
output_units
estimated_cost
actual_cost_if_available
budget_bucket
approval_reference
```

אין לשמור prompt content רק כדי לחשב עלות.

## 9. Client options

בשלב Planning הפלטפורמה יכולה להציג 2-3 חלופות עסקיות, בלי להציף את הלקוח בפרטים טכניים:

- חסכוני - עלות נמוכה יותר, ביצועים מתאימים למשימות רגילות.
- מאוזן - ברירת מחדל מומלצת.
- מתקדם - איכות/Reasoning גבוהים יותר כאשר יש הצדקה.

הלקוח בוחר לפי תוצאה ועלות, לא לפי מותג Model.

## 10. Provider change

שינוי Provider דורש:

- Regression eval.
- Cost comparison.
- Privacy/data policy check.
- Tool/function compatibility check.
- Rollback target.

אם כל החוזים נשמרים, אין צורך לשנות Business Logic של Agent.
