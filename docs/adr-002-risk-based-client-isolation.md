# ADR-002: בידוד לקוחות מבוסס סיכון

**Status:** Accepted
**Date:** 2026-08-20
**Deciders:** Owner; Security/Privacy Owner לפני מידע אישי או רגיש

## Context

ה-Factory צריך לשכפל תבניות בין לקוחות בלי לשתף Data Plane. המונח "Project נפרד" אינו הוכחה מספקת לבידוד אם Credentials, חיפוש, Logs, משתמשי Admin או Export עדיין חוצים את הגבול.

## Decision

Reuse מתבצע רק דרך מפרטים ותבניות. לכל לקוח נוצרים מזהים, Credentials, Knowledge indexes, State, Audit ו-Evaluations חדשים. גבול לוגי מותר ב-MVP לא רגיש רק לאחר Negative isolation tests. מידע בסיכון גבוה דורש החלטה נפרדת שעשויה לחייב Workspace, Account או Deployment ייעודי.

## Options Considered

| Option | Cost | Isolation | Operational effort |
|---|---|---|---|
| Shared workspace with projects | Low | Provider-dependent | Low |
| Workspace/account per client | Medium | Stronger | Medium |
| Dedicated deployment per client | High | Strongest | High |

## Consequences

- אין מאגר Knowledge, Credential או Audit משותף ללקוחות.
- Onboarding ו-Decommissioning דורשים Checklist וראיות.
- רמת הבידוד גדלה עם Classification וסיכון ולא רק עם גודל הלקוח.

## Action Items

1. [ ] להגדיר Isolation tier לכל Classification לפני Production.
2. [ ] ליצור Acceptance Tests לניסיונות Cross-tenant Retrieval, Tool use, Logs ו-Export.
