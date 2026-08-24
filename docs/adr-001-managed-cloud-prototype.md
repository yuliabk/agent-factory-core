# ADR-001: Managed Cloud עבור Prototype לא רגיש

**Status:** Accepted
**Date:** 2026-08-20
**Deciders:** Owner

## Context

ל-Owner זמינות של 6-10 שעות בשבוע ותקציב ניסוי של 200-500 ₪ בחודש. תחזוקת תשתית Self-hosted עלולה לצרוך את רוב הזמן לפני שהערך העסקי וה-Evaluations הוכחו. מנגד, שירות מנוהל אינו מתאים אוטומטית לכל דרגת מידע או דרישת Data Residency.

## Decision

להשתמש ב-Managed Cloud או Sandbox מנוהל עבור Prototype עם מידע סינתטי, Public או Non-sensitive מאושר בלבד. אין בהחלטה זו אישור ל-Production או למידע `Confidential`, `Personal` או `Sensitive`. כל לקוח Production יקבל החלטת Hosting נפרדת לפי סיכון, חוזים, Region ויכולות בידוד.

## Options Considered

| Option | Complexity | Cost predictability | Isolation control | Owner effort |
|---|---|---|---|---|
| Managed Cloud Prototype | Low | Medium | Provider-dependent | Low |
| Self-hosted from day one | High | Medium | High if operated correctly | High |
| Hybrid | Medium-High | Medium | Flexible | Medium-High |

## Consequences

- ניתן להגיע מהר יותר ל-Evaluation עובד.
- Usage caps, Region, DPA, Export ו-Deletion נשארים תנאי חובה לפני מידע אמיתי.
- מעבר עתידי בין Hosting modes מחייב Release plan ו-Regression tests.

## Action Items

1. [ ] Owner מאשרת או דוחה את ההחלטה.
2. [ ] לפני בחירת ספק, מתעדים Region, Retention, Export, Deletion, Isolation ו-Cost caps.
