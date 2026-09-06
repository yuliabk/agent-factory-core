# ADR-005: Agent Factory Core as Platform Control Plane

**Status:** Proposed  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

המערכת צפויה לשרת מספר הולך וגדל של Agents ולקוחות. אם כל Agent יממש מחדש Security, Memory, Tool access, Model selection, Cost control ו-Orchestration, התחזוקה תהפוך לאיטית ומסוכנת.

## Decision

`Agent Factory Core` יהיה Platform Control Plane שמחזיק את החוזים והמנגנונים המשותפים. Agents עסקיים יישבו בריפו נפרד ויצרכו את יכולות ה-Core דרך Contracts ו-Manifest.

ה-Core לא יכיל Business Logic של Agent ספציפי.

## Consequences

### Positive

- שינוי Provider או Policy מקומי יותר.
- Security baseline אחיד.
- פחות שכפול.
- קל יותר לבנות Agents מתבניות.
- קל יותר לבדוק תאימות.

### Negative

- דורש חוזים ברורים לפני מימוש.
- שינויים ב-Core דורשים backward compatibility discipline.
- Core הופך לרכיב קריטי ולכן חייב להישאר קטן ומודולרי.

## Guardrail

כל Feature חדש נבחן בשאלה:

> האם זה כלל שצריך לחול על רוב Agents, או Business Logic של Agent מסוים?

אם התשובה השנייה נכונה, הוא אינו נכנס ל-Core.
