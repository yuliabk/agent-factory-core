# ADR-008: Budget Warning, Approval and Safety Cap

**Status:** Proposed  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

עלות היא סיכון מרכזי גם לפלטפורמה וגם ללקוח. Hard stop עסקי פשוט עלול להפוך Agent ללא שמיש ברגע שמגיע לתקרה, בעוד שאין לאפשר חריגה שקטה או runaway spend.

## Decision

המערכת תפריד בין:

1. **Business Budget** - תקציב שנקבע עם Owner/Client. לפני חריגה, הפעולה החדשה נעצרת ונדרש explicit approval.
2. **Emergency Safety Cap** - guardrail תפעולי בלתי תלוי שנועד לעצור loops, recursion או anomaly קיצוני.

ב-Build time ה-Owner מאשר Budget profile. ב-Runtime גורם מאושר אצל הלקוח מאשר חריגה מה-Business Budget.

כל request מבצע Budget check בסיסי. פעולות יקרות מבצעות preflight estimate כאשר אפשר.

## Consequences

- אין silent overspend.
- Agent אינו נהפך אוטומטית ללא שמיש רק כי הגיע לסף העסקי.
- חריגה נשלטת ומתועדת.
- קיימת הגנה נפרדת מפני תקלה קיצונית.

## Audit requirement

כל Budget approval נשמר עם approver, amount/new limit, period, timestamp, reason ו-expiration/review date.
