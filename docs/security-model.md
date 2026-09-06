# מודל אבטחה ופרטיות - Platform Baseline

**Status:** Accepted direction after Owner Review  
**Principle:** Security is mandatory, risk-based and inherited by every Agent.

## 1. כלל יסוד

Agent אינו אחראי להגן על הפלטפורמה מפני עצמו. בקרות קריטיות נמצאות מחוץ ל-Prompt וללוגיקה העסקית של Agent, בתוך ה-Core או בתשתית המאושרת.

Agent repo ולקוח יכולים להחמיר Policy. הם אינם יכולים להחליש Non-overridable Platform Invariants.

## 2. Default deny + least privilege + policy before execution

ברירת המחדל ל-Capability, Tool, Network egress, Secret, persistent memory ו-Agent-to-Agent delegation היא `deny` עד שיש grant תקף.

עם זאת, `default deny` אינו אומר approval ידני לכל פעולה. PlatformPolicy ממפה risk/trust/action class ל-auto-allow, policy check או human approval.

Prompt, Tool output, Web content, retrieved document או Agent אחר אינם מקור סמכות להרשאות.

## 3. Trust Levels

הפלטפורמה משתמשת ב-Trust Profiles כדי להימנע מקונפיגורציית permissions ידנית בכל Agent.

| Level | Typical use | Default posture |
|---|---|---|
| `sandbox` | development, synthetic data | flexible warnings, no production secrets, bounded side effects |
| `internal` | internal business use | authenticated tenant, restricted tools, audited writes |
| `business` | client production workflows | stronger isolation, policy gates, defined approvers, cost/retention controls |
| `privileged` | high-impact or elevated access | explicit review, strongest isolation, narrow scopes, enhanced evidence |

ה-Factory מציע Trust Level מתוך ה-Spec. PlatformPolicy מגדירה את ה-ceiling. הלקוח יכול לבחור רמה נמוכה/מחמירה יותר בתוך המסגרת המותרת, אך אינו יכול להעלות סמכות מעבר ל-ceiling ללא ExceptionPolicy תקפה ואם הכלל בכלל overridable.

Trust Level הוא profile, לא הרשאה עצמאית. ה-EffectiveReleaseConfig מכיל את grants האפקטיביים.

## 4. Risk-based approval

פעולות מסווגות לפי risk class.

- **Low risk** - ניתן לבצע אוטומטית אם Policy מאפשרת.
- **Medium risk** - Policy עשויה לדרוש תנאים, warning, preflight או approval לפי context.
- **High risk** - Human approval או stronger gate לפי PlatformPolicy.
- **Non-overridable prohibited** - חסום ללא קשר ל-Agent/client request.

המטרה היא לא לייצר אינסוף approvals אלא להציב אדם רק במקום שבו הסיכון מצדיק זאת.

## 5. Platform invariants and exceptions

יש שתי קבוצות כללים:

1. **Non-overridable invariants** - לא ניתנים לעקיפה דרך Agent, Client config, prompt או exception.
2. **Overridable policy rules** - ניתנים ל-ExceptionPolicy מבוקרת.

הרשימה המדויקת של non-overridable invariants תתייצב לפני Production, אך מנגנון ההבחנה הוא חלק מהארכיטקטורה כבר עכשיו.

ExceptionPolicy חייבת לכלול:

```text
exception_id
rule_id
scope (tenant/agent/environment/action)
reason
approved_by
created_at
expires_at_or_review_at
compensating_controls
audit_reference
status
```

Exception אינה משנה את PlatformPolicy הגלובלית. היא overlay תחום, מתועד וניתן לביטול.

## 6. סיווג מידע

| רמה | דוגמאות | שימוש ראשוני | בקרות מינימום |
|---|---|---:|---|
| Public | תוכן פומבי | כן | provenance, integrity |
| Internal | מידע עסקי רגיל | Pilot מוגבל | auth, isolation, encryption, audit |
| Confidential | חוזים, אסטרטגיה | לאחר review | stronger isolation, DPA/contract, retention, restricted egress |
| Personal | פרטי אדם/לקוח | לאחר review | purpose limitation, consent/legal basis, deletion, minimization |
| Sensitive | רפואי, פיננסי וכדומה | מסלול נפרד | enhanced controls, legal/security/domain approval |

## 7. Threat model חובה

לפחות:

- Direct and indirect prompt injection.
- Cross-tenant data access.
- Credential leakage.
- Data exfiltration דרך Tool, URL, response, memory או logs.
- Permission escalation.
- Approval replay/forgery.
- Exception abuse.
- Agent-to-Agent confused deputy.
- Infinite/recursive agent loops.
- Runaway tool/model cost.
- Malicious/compromised provider, MCP or tool response.
- Runtime drift from EffectiveReleaseConfig.
- Dependency/supply-chain compromise.

## 8. Untrusted content boundary

Web, Email, uploaded files, retrieved documents, Tool output, MCP output ו-external Agent output נחשבים Data ולא Instruction, אלא אם ה-Core סימן אותם במפורש כ-policy-approved control content.

ה-Orchestrator מפריד בין Platform Policy, trusted compiled configuration ו-untrusted content.

## 9. Prompt injection containment

הגנה שכבתית:

1. trusted instructions מופרדות מ-untrusted data;
2. Tool/capability allowlists + typed schemas;
3. permission checks מחוץ למודל;
4. least-privilege credentials;
5. egress restrictions;
6. risk-based approvals;
7. output/data-loss checks לפי classification;
8. attack/security eval corpus;
9. runtime/cost/hop limits;
10. minimized audit.

גם אם המודל "משתכנע" מהזרקה, הוא לא אמור לקבל סמכות חדשה.

## 10. Identity and tenant isolation

כל invocation כולל trusted identifiers כגון `request_id`, `tenant_id`, `actor_id`, `environment`, `agent_release_id`, `trace_id`.

Cross-tenant access נחסם מחוץ ל-Agent. בידוד לוגי נחשב תקף רק לאחר negative tests שמוכיחים שאין read/search/action/export בין Tenants ללא grant מפורש.

## 11. Tool and Agent-to-Agent security

כל Tool עובר Tool Gateway עם schema, authorization, tenant binding, side-effect/risk classification, input validation, budget/preflight, approval כאשר נדרש, timeout, retry/idempotency ו-audit.

Agent-to-Agent הוא delegation מבוקר דרך Capability Registry. אין permission inheritance אוטומטי. כל hop מקבל Context מינימלי, מוגבל ב-budget/deadline/hops ונרשם ל-trace.

## 12. Secrets

- Secrets אינם ב-Git, Prompt, OpenSpec, AgentManifest, ClientInstanceConfig, log או Release bundle.
- Credentials נפרדים לפי Tenant/Environment כאשר נדרש.
- נשמרים references בלבד ונפתרים Runtime-time.
- rotation/revocation אינם דורשים שינוי Business Agent code.

## 13. Memory and RAG

Memory write/read עוברים Memory Gateway ו-Policy.

Agent רשאי להחליט שמידע מועיל לזיכרון ולבקש/לבצע write במסגרת Policy, אך ה-Policy היא שמחליטה אם ה-write מותר, באיזו memory class, לאיזה retention ולפי איזה purpose.

PII/Personal data אינם נכתבים ל-persistent memory ללא בסיס/consent/policy מתאימים. Cross-tenant memory אסורה.

Retrieved memory/knowledge נשאר untrusted data.

## 14. Runtime and cost safety

כל Agent מקבל limits על timeout, tool calls, agent hops, retries, parallelism, context ו-cost.

Business budget הוא warn-and-approve לפי policy. Emergency safety cap הוא safety control נפרד שמפסיק runaway loop/anomaly ואינו ניתן לביטול על ידי business overage approval.

## 15. Audit

Audit event ממוזער כולל לפי הצורך:

```text
tenant_id
request_id
trace_id
actor_id
agent_id
agent_release_id
trust_level
capability/tool
policy_decision
exception_reference
approval_reference
cost_event
result
timestamp
environment
```

אין לשמור raw prompt, secret או sensitive content כברירת מחדל.

## 16. Supply chain

Skills, plugins, MCP servers, packages, model providers, tools ו-templates חיצוניים עוברים source verification, pinning/versioning, license review, permission inventory, security review ו-regression evaluation לפי risk.

## 17. Production gates

Production promotion דורש את blocking checks שה-PlatformPolicy מגדירה ל-risk/trust/domain הרלוונטי. Security invariant failure תמיד חוסם. Human approval נדרש רק כאשר release/action policy מחייבת אותו.

## 18. Incident response

Runtime Governance Plane יכול לבצע scoped `Suspend`, block external actions, revoke/rotate credentials, freeze capabilities, preserve minimized evidence and roll back release.

Rollback של Agent אינו מבטל אוטומטית side effect שכבר בוצע בעולם החיצוני.