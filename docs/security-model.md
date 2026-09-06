# מודל אבטחה ופרטיות - Platform Baseline

**Status:** Proposed update for Owner Review  
**Principle:** Security is mandatory and inherited by every Agent.

## 1. כלל יסוד

Agent אינו אחראי להגן על הפלטפורמה מפני עצמו. בקרות קריטיות חייבות להיות מחוץ ל-Prompt ומחוץ ללוגיקה העסקית של Agent, בתוך ה-Core או בתשתית המאושרת.

Agent repo רשאי להוסיף בקרות. הוא אינו רשאי לבטל Minimum Baseline.

## 2. Default deny

ברירת המחדל לכל Capability, Tool, Network egress, Storage, Secret ו-Agent-to-Agent call היא `deny` עד שיש Policy מפורשת שמאפשרת אותו.

Prompt, Tool output או מסמך retrieved אינם יכולים להעניק Permission.

## 3. סיווג מידע

| רמה | דוגמאות | שימוש ראשוני | בקרות מינימום |
|---|---|---:|---|
| Public | תוכן פומבי | כן | provenance, integrity |
| Internal | מידע עסקי רגיל | Pilot מוגבל | auth, isolation, encryption, audit |
| Confidential | חוזים, אסטרטגיה | לאחר review | stronger isolation, DPA, retention, restricted egress |
| Personal | פרטי אדם/לקוח | לאחר review | purpose limitation, consent/legal basis, deletion, minimization |
| Sensitive | רפואי, פיננסי וכדומה | מסלול נפרד | enhanced controls, legal/security approval |

## 4. Threat model חובה

לפחות:

- Direct prompt injection.
- Indirect prompt injection מתוך Web, Email, Documents, Tool outputs או MCP.
- Cross-tenant data access.
- Credential leakage.
- Data exfiltration דרך Tool, URL, response או logs.
- Permission escalation.
- Approval replay או forged approval.
- Agent-to-Agent confused deputy.
- Infinite/recursive agent loops.
- Runaway tool usage ועלות.
- Malicious or compromised provider/tool response.
- Runtime drift.
- Dependency/supply-chain compromise.

## 5. Untrusted content boundary

כל תוכן שמגיע מ:

- Web.
- Email.
- Uploaded files.
- Retrieved documents.
- Tool output.
- MCP server.
- External Agent.

נחשב Data ולא Instruction, אלא אם ה-Core סימן אותו במפורש כ-policy-approved control content.

ה-Orchestrator שומר הפרדה לוגית בין System Policy, trusted configuration ו-untrusted content.

## 6. Prompt injection containment

אין מנגנון יחיד שמבטיח חסינות. ההגנה היא שכבתית:

1. הפרדת trusted instructions מ-untrusted data.
2. Tool allowlist ו-schema validation.
3. Permission checks מחוץ למודל.
4. Least-privilege credentials.
5. Egress restrictions.
6. Human approval לפעולות מוגנות.
7. Output/data-loss checks לפי סיווג.
8. Security evaluations עם attack corpus.
9. Runtime limits ו-audit.

גם אם המודל "משתכנע" מהזרקה, הוא לא אמור לקבל סמכות לבצע פעולה אסורה.

## 7. Identity and tenant isolation

כל בקשה כוללת לפחות:

```text
request_id
tenant_id
actor_id
actor_type
environment
agent_release_id
```

Cross-tenant access נחסם מחוץ ל-Agent.

Project לוגי נחשב Isolation boundary רק לאחר negative tests שמוכיחים שמשתמש או Workflow של Tenant A אינם יכולים לקרוא, לחפש, להפעיל או לייצא משאבים של Tenant B.

## 8. Tool security

כל Tool עובר Tool Gateway עם:

- Typed schema.
- Authorization.
- Tenant binding.
- Side-effect classification.
- Input validation.
- Approval check.
- Timeout.
- Idempotency כאשר רלוונטי.
- Retry policy מוגבל.
- Audit.

Tools עם file/system/network access מקבלים scope מינימלי.

## 9. Agent-to-Agent security

Agent-to-Agent call הוא privileged delegation, לא chat פנימי חופשי.

- כל call עובר Capability Registry.
- Provider Agent מקבל רק Context נדרש.
- אין Permission inheritance אוטומטי.
- Caller אינו יכול להעניק Permission שאין לו.
- מספר hops מוגבל.
- כל hop נרשם ל-trace ול-budget.

## 10. Secrets

- Secrets אינם ב-Git, Prompt, OpenSpec, Manifest, log או Release bundle.
- Credentials נפרדים לפי Tenant ו-Environment.
- Secret reference נפתר רק בזמן Runtime.
- Rotation ו-revocation חייבים להיות אפשריים בלי שינוי Agent code.

## 11. Memory and RAG

Memory writes דורשים Purpose ו-Retention profile.

Retrieval חייב לאכוף:

- Tenant.
- Actor permissions.
- Document access.
- Data classification.
- Query purpose כאשר נדרש.

Retrieved text אינו הופך ל-System instruction.

## 12. Human approval

Approval חובה לפחות עבור:

- External messages כאשר Policy מחייב.
- Irreversible writes.
- Payments/refunds/financial commitments.
- Permission changes.
- Data transfer בין מערכות או Tenants.
- פעולה רגישה לפי Domain.
- Budget overage כאשר חוצה Business Limit.

Approval כולל:

`approver + action + target + request_id + scope + timestamp + expiry`

Approval כללי בשיחה אינו מספיק לפעולה מוגנת.

## 13. Runtime limits

כל Agent מקבל מגבלות על:

- Request timeout.
- Tool calls.
- Agent hops.
- Retries.
- Parallel tasks.
- Context size.
- Cost.

מטרת המגבלות היא למנוע גם abuse וגם failure loops.

## 14. Cost security

Runaway spend הוא אירוע תפעולי-אבטחתי.

- Cost check בסיסי לכל request.
- Preflight לפעולה יקרה.
- Warning thresholds.
- Explicit approval לחריגה מתקציב עסקי.
- Emergency safety cap ל-loop או anomaly.

## 15. Audit

Audit event ממוזער כולל לפי הצורך:

```text
tenant_id
request_id
trace_id
actor_id
agent_id
agent_release_id
capability
tool
policy_decision
approval_reference
cost_event
result
timestamp
environment
```

אין לשמור raw Prompt, Secret או sensitive content כברירת מחדל.

## 16. Supply chain

Skills, plugins, MCP servers, packages, model providers ו-tools חיצוניים עוברים:

- Source verification.
- Pinning/versioning.
- License review.
- Security scan/review.
- Permission inventory.
- Owner approval.
- Regression evaluation לאחר שינוי מהותי.

## 17. Production gates

אין Production release לפני:

- Manifest validation.
- Data flow review.
- Permission review.
- Prompt injection/security tests.
- Cost tests.
- Agent hop/loop tests אם רלוונטי.
- Retention/deletion policy.
- Incident owner.
- Rollback target.
- Human approvals.
- Client acceptance.

## 18. Incident response

באירוע חשוד ניתן להפעיל `Suspend` דרך ה-Core:

- Block external actions.
- Revoke/rotate credentials.
- Freeze risky capabilities.
- Preserve minimal audit evidence.
- Roll back release כאשר רלוונטי.
- Notify responsible owner.

Rollback של Agent אינו מבטל אוטומטית פעולה עסקית שכבר בוצעה בעולם החיצוני.
