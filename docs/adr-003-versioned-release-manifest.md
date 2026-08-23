# ADR-003: Release Manifest ממוספר לכל מופע לקוח

**Status:** Accepted
**Date:** 2026-08-20
**Deciders:** Owner

## Context

GitHub ו-OpenSpec הם מקור האמת, אך Runtime Low-Code עלול להשתנות ידנית ולאבד קשר למפרט שאושר. ללא Manifest אי אפשר להוכיח איזו גרסת Prompt, Policy, Workflow ו-Evaluation פעלה בעת אירוע.

## Decision

כל Deployment מזוהה באמצעות `agent_release_id` ומקושר ל-Commit SHA, OpenSpec change, גרסאות התצורה, תוצאות Evaluation, אישורים ו-Rollback target. ה-Manifest אינו מכיל Secrets או נתוני לקוח. שינוי ידני ב-Runtime שאינו מיוצג ב-Manifest נחשב Drift וחוסם Promotion.

## Options Considered

| Option | Traceability | Effort | Drift risk |
|---|---|---|---|
| Manual screenshots only | Low | Low | High |
| Versioned release manifest | High | Medium | Low |
| Full deployment platform | High | High | Low |

## Consequences

- ניתן לשחזר, להשוות ולבטל גרסאות.
- נדרש Export או תיעוד עקבי של תצורת כלי Low-Code.
- Prototype יכול להתחיל ב-Manifest ידני מתבנית ולהפוך לאוטומטי בהמשך.

## Action Items

1. [ ] Owner מאשרת את שדות ה-Manifest ואת כלל ה-Drift.
2. [ ] להוסיף תבנית Manifest לפני ה-Prototype.
