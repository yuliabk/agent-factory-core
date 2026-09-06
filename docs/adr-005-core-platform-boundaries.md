# ADR-005: Agent Factory Core platform boundaries

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

המערכת צפויה לשרת מספר הולך וגדל של Agents ולקוחות. אם כל Agent יממש מחדש Security, Memory, Tool access, Model selection, Cost control ו-Orchestration, התחזוקה תהפוך לאיטית ומסוכנת.

במקביל, חלק ממנגנוני ה-Core פועלים בזמן Build/Release וחלקם פועלים בזמן Runtime. ערבוב האחריות תחת "Control Plane" יחיד יוצר גבול לא ברור ועלול להפוך את ה-Core למונולית שקשה להחליף או לתקן.

## Decision

`Agent Factory Core` יהיה Platform Core אחד עם שני Planes לוגיים נפרדים:

1. **Build / Control Plane** - Intent, Specs, Templates, Manifest validation, contract compilation, Evals, Releases ו-registry metadata.
2. **Runtime Governance Plane** - Orchestration, Execution Context, Policy enforcement, Capability routing, Model routing, Tool Gateway, Memory Gateway, Budget/runtime guards ו-Audit/Tracing.

בשלב הראשון שני ה-Planes יכולים לחיות באותו repository/project, אך הם חייבים לשמור על Contract boundary ברור כדי לאפשר פיצול פיזי בעתיד ללא Rewrite של Business Agents.

Business Agents יישבו ב-repositories נפרדים ויצרכו את יכולות ה-Core דרך Contracts ו-Manifest.

ה-Core לא יכיל Business Logic של Agent ספציפי.

בנוסף, יש להפריד בין:

`Agent Definition + Client Instance Configuration + Core Policy/Contract Versions = Deployed Agent Instance`

Agent Definition reusable אינו מחזיק Secrets, PII או Client-specific business state.

## Consequences

### Positive

- שינוי Provider, Runtime או Policy נשאר מקומי יותר.
- ניתן להחליף Runtime implementation בלי לשנות את Factory specification flow.
- Security baseline אחיד.
- פחות שכפול בין Agents.
- Client-specific configuration אינו מזהם Agent repositories reusable.
- קל יותר לבנות Agents מתבניות ולבדוק תאימות.
- ניתן בעתיד לפצל Build ו-Runtime פיזית אם scale או reliability דורשים זאת.

### Negative

- דורש חוזים ברורים בין Planes לפני מימוש.
- שינויים ב-Core דורשים backward compatibility discipline.
- Core הופך לרכיב קריטי ולכן חייב להישאר קטן ומודולרי.
- נדרש להבדיל במפורש בין metadata ב-Control Plane לבין Client Data ב-Data Plane.

## Guardrails

כל Feature חדש נבחן בשתי שאלות:

> האם זה כלל שצריך לחול על רוב Agents, או Business Logic של Agent מסוים?

אם זו Business Logic ספציפית, היא אינה נכנסת ל-Core.

> האם זה Build/Release responsibility או Runtime Governance responsibility?

אם האחריות אינה ברורה, ה-Contract צריך להתבהר לפני Implementation.
