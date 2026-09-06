# Agent Manifest Contract

**Status:** Proposed  
**Owner approval:** Required before implementation

## 1. מטרה

Agent Manifest הוא החוזה הדקלרטיבי בין Agent repo לבין `Agent Factory Core`.

ה-Manifest אינו Prompt ואינו מכיל Secrets. הוא מתאר את ההרשאות, ה-Capabilities, מדיניות העלות, Memory, Tools, Security ו-Release requirements של ה-Agent.

ה-Core חייב לדחות Agent עם Manifest לא תקין או עם בקשה שחורגת ממדיניות הפלטפורמה.

## 2. עקרונות

- Manifest הוא Machine-readable ו-Versioned.
- מינימום שדות חובה, עם Profiles ו-Defaults כדי לא ליצור קונפיגורציה כבדה.
- Agent יכול לבקש Capability או Permission. הוא לא מעניק אותם לעצמו.
- Secrets מוזכרים רק כ-reference ל-Credential binding.
- Client-specific values מופרדים מה-Template ככל האפשר.
- כל שינוי מהותי ב-Manifest מחייב Regression evaluation לפני Production.

## 3. שדות חובה ל-MVP

| Section | Required | Purpose |
|---|---:|---|
| `apiVersion` | כן | Version של schema |
| `kind` | כן | תמיד `AgentManifest` בשלב הראשון |
| `metadata` | כן | identity, version, owner |
| `intent` | כן | למה ה-Agent קיים ומה התוצאה העסקית |
| `template` | כן | מאיזו תבנית הוא נבנה |
| `capabilities` | כן | מה הוא מספק ומה הוא דורש |
| `permissions` | כן | Default-deny allowlist |
| `modelPolicy` | כן | Profile ו-fallback policy |
| `toolPolicy` | כן | כלי מותר, side effects ו-approval |
| `memoryPolicy` | כן | סוגי memory ו-retention profile |
| `security` | כן | baseline profile ו-data classes |
| `budget` | כן | currency, warning, approval ו-safety cap reference |
| `runtime` | כן | timeout, concurrency, loop limits |
| `observability` | כן | audit/trace requirements |
| `release` | כן | evals, approvals ו-rollback |

## 4. Identity

```yaml
metadata:
  id: research-agent
  version: 0.1.0
  owner: platform-owner
  status: draft
```

`id` נשאר יציב. `version` משתנה עם contract או behavior. גרסת Deployment מזוהה בנפרד באמצעות `agent_release_id`.

## 5. Intent

```yaml
intent:
  businessGoal: "Provide verified information to other agents"
  primaryUsers:
    - internal-agent
  successOutcome: "Return useful evidence with provenance within policy and budget"
```

Intent נשמר כדי שהמערכת וה-Operator יבינו למה Agent קיים גם לאחר חודשים של שינויים טכניים.

## 6. Capabilities

```yaml
capabilities:
  provides:
    - name: research.lookup
      contractVersion: 1
  requires:
    - name: web.search
      optional: true
```

Agent-to-Agent dependency מוגדרת כ-Capability, לא ככתובת Agent קונקרטי.

## 7. Permissions

```yaml
permissions:
  default: deny
  allow:
    - capability: web.search
    - capability: knowledge.read
```

Permissions מקבלות אישור Platform/Owner בזמן Build. Client-specific bindings נבדקים שוב ב-Runtime.

## 8. Model Policy

```yaml
modelPolicy:
  profile: balanced
  allowFallback: true
  disallowedProviders: []
  dataResidencyProfile: default
```

Agent אינו בוחר Model hard-coded. ה-Core בוחר Provider/Model שעומד ב-Profile וב-Policy.

## 9. Tool Policy

```yaml
toolPolicy:
  default: deny
  tools:
    - capability: web.search
      sideEffect: none
      approval: never
    - capability: crm.write
      sideEffect: external-write
      approval: policy
```

כל Tool input/output חייב Schema. Tool עם Side Effect דורש Idempotency, failure behavior ו-approval policy.

## 10. Memory Policy

```yaml
memoryPolicy:
  session: enabled
  persistentUserMemory: disabled
  clientKnowledge: read-only
  operationalState: enabled
  retentionProfile: short
```

Agent אינו מקבל Storage credentials ישירים. ה-Core מספק גישה דרך Memory Broker.

## 11. Security

```yaml
security:
  baseline: platform-default
  dataClasses:
    - public
    - internal
  promptInjectionProfile: strict
  egressProfile: restricted
```

`platform-default` הוא Minimum Baseline ואינו ניתן להחלשה דרך Manifest.

## 12. Budget

```yaml
budget:
  currency: USD
  businessLimit:
    period: monthly
    amount: 50
    mode: warn-and-approve
  warnings:
    - 0.50
    - 0.80
    - 0.95
  buildApprover: platform-owner
  runtimeApprover: client-owner
  preflightForExpensiveOperations: true
  emergencySafetyCapProfile: platform-default
```

ה-Business Limit אינו Kill Switch אוטומטי. לפני חריגה המערכת עוצרת את הפעולה החדשה שתחצה את הגבול ומבקשת אישור. תקרת הבטיחות התפעולית נשארת נפרדת ומגינה על המערכת מ-loop או runaway spend.

## 13. Runtime Limits

```yaml
runtime:
  timeoutSeconds: 120
  maxToolCallsPerRequest: 12
  maxAgentHopsPerRequest: 4
  maxRetries: 2
  maxParallelTasks: 4
```

ערכים אלו מגינים גם על יציבות וגם על עלות. Agent יכול לבקש Override, אך אינו מאשר אותו בעצמו.

## 14. Observability

```yaml
observability:
  audit: required
  traces: required
  costEvents: required
  contentLogging: minimized
```

אין לשמור Secrets או raw sensitive content כברירת מחדל.

## 15. Release

```yaml
release:
  requiredEvals:
    - functional
    - security
    - cost
  humanApprovalRequired: true
  rollbackRequired: true
```

## 16. Validation invariants

Manifest יידחה אם מתקיים אחד מהבאים:

- `permissions.default` אינו `deny`.
- Agent מבקש Secret value בתוך הקובץ.
- Tool בעל Side Effect אינו כולל Approval policy.
- Agent מבקש לבטל Audit.
- Agent מבקש Security baseline חלש מהמינימום.
- אין Budget policy.
- אין Runtime limits.
- `requires` מצביע ל-Agent קונקרטי במקום Capability.
- Model קונקרטי hard-coded במקום Profile, אלא אם אושר exception מפורש.

## 17. שינויים שדורשים Re-approval

- הרחבת Permissions.
- Tool חדש בעל Side Effect.
- Data classification גבוהה יותר.
- שינוי Model/Provider policy שמשפיע על Privacy או Cost.
- העלאת Budget limit מהותית.
- שינוי Capability contract major version.
- שינוי Retention.
- שינוי Runtime limits מעבר לטווח המאושר.
