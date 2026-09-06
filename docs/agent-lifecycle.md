# Agent Lifecycle

**Status:** Proposed

## 1. מטרה

להגדיר מסלול אחיד מכל בקשת לקוח ועד Agent פעיל, כך שכל Agent שנוצר דרך הפלטפורמה יעבור אותם Gates בסיסיים גם אם הוא נבנה על ידי מפתח, Agent builder או Template אחר.

## 2. Lifecycle ראשי

```text
Intent
  -> Clarified
  -> Specified
  -> Planned
  -> Built
  -> Evaluated
  -> Owner Approved
  -> Client Accepted
  -> Released
  -> Monitored
  -> Changed / Suspended / Decommissioned
```

## 3. Stage 1 - Intent

קלט: תיאור חופשי של הלקוח בשפה עסקית.

דוגמה:

> "אני רוצה Agent שימכור בשבילי וידבר עם לקוחות."

המערכת אינה מבקשת מהלקוח לבחור API, MCP, Model או Runtime.

תוצר: `ClientIntent` ראשוני.

## 4. Stage 2 - Clarified

המערכת שואלת מספר קטן של שאלות קריטיות בלבד, בדרך כלל עד 5-6 אחרי התיאור החופשי.

נושאים שחייבים להתברר מוקדם:

- מה התוצאה העסקית.
- מי המשתמש או הלקוח הסופי.
- איפה מתרחשת האינטראקציה.
- איזה מידע ה-Agent צריך.
- מה אסור לו לעשות בלי אדם.
- מה מסגרת התקציב.

פרטים לא קריטיים יכולים להפוך להנחות מפורשות במקום לעכב את הלקוח.

תוצר: `ClarifiedIntent + Assumptions`.

## 5. Stage 3 - Specified

ה-Spec Compiler ממיר את ה-Intent ל:

- Business scope.
- Agent type/template recommendation.
- Capabilities required.
- Data classification.
- Tools/channels required ברמת Capability.
- Human approval points.
- Budget profile.
- Success metrics.
- Forbidden outcomes.

תוצר: OpenSpec change + Draft Agent Manifest.

## 6. Stage 4 - Planned

ה-Core או Builder מציע כמה Implementation Profiles, לדוגמה:

- Economy.
- Balanced.
- Premium.

כל Profile יכול להשתמש ב-Providers שונים, אך חייב לשמור אותו contract עסקי.

בשלב זה ה-Owner מאשר:

- Permissions.
- Budget envelope.
- Security/data profile.
- Tools בעלי Side Effect.
- Template.
- Runtime profile.

ללא אישור אין Build ל-Production path.

## 7. Stage 5 - Built

המערכת מרכיבה Agent מ:

`Template + Manifest + Policy Profiles + Adapters + Agent-specific code/config`

Build אינו רשאי להכניס Secrets ל-Git או ל-Release package.

## 8. Stage 6 - Evaluated

לפחות שלושה סוגי Evaluation:

1. Functional - עושה את מה שהוגדר.
2. Security - Prompt injection, permission bypass, data leakage, unsafe tool usage.
3. Cost - עומד בפרופיל העלות ואינו נכנס ללופים חריגים.

ל-Agent עם Agent-to-Agent calls מתווסף גם hop/contract evaluation.

## 9. Stage 7 - Owner Approved

ה-Owner מקבל Evidence Pack קצר:

- Spec diff.
- Manifest diff.
- Permissions diff.
- Cost estimate.
- Eval results.
- Security findings.
- Known limitations.
- Rollback target.

האישור מתועד וקשור ל-version המדויק.

## 10. Stage 8 - Client Accepted

הלקוח רואה תוצאה עסקית ולא פרטי Backend.

הוא מאשר:

- Scope.
- What the Agent may do.
- What requires his approval.
- Budget expectations.
- Data usage summary.
- Escalation path.

## 11. Stage 9 - Released

נוצר `agent_release_id` עם references ל:

- Commit.
- OpenSpec.
- Manifest.
- Template.
- Policy versions.
- Model profile.
- Tool contracts.
- Eval evidence.
- Approvals.
- Rollback target.

## 12. Stage 10 - Monitored

Runtime monitoring מתמקד ב:

- Spend.
- Errors.
- Tool failures.
- Permission denials.
- Security events.
- Quality regressions.
- Provider availability.
- Agent hop depth.

ב-MVP העדיפות הראשונה ל-alerting היא חריגות עלות ותקלות שמייצרות עלות חוזרת.

## 13. Change Lifecycle

שינוי קטן שאינו משנה Contract יכול לעבור fast path עם Regression eval.

שינוי שמרחיב Permission, Data class, Side Effect, Budget, Provider privacy profile או Capability major version מחייב OpenSpec change ואישור חדש.

## 14. Suspend

ה-Core יכול להעביר Agent ל-`Suspended` כאשר:

- Safety cap הופעל.
- Credential נחשד כ compromised.
- Security incident פעיל.
- Client requested pause.
- Provider behavior השתנה באופן מסוכן.

ב-Suspended mode פעולות חיצוניות נחסמות. פעולות read-only יכולות להישאר רק אם Policy מאפשר.

## 15. Decommission

סיום Agent כולל:

- Revoke credentials.
- Disable channels.
- Export data לפי חוזה.
- Delete state לפי retention policy.
- Close audit package.
- Record final release and deletion evidence.
