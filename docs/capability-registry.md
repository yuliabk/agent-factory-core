# Capability Registry and Agent-to-Agent Routing

**Status:** Proposed

## 1. מטרה

לאפשר ל-Agent להשתמש ב-Agent אחר בלי להכיר את שמו, ה-URL שלו, ה-Provider שלו או פרטי המימוש שלו.

## 2. עיקרון

Agent מבקש Capability, לדוגמה:

```text
research.lookup
crm.customer.read
message.draft
travel.inventory.search
```

ה-Core פותר את הבקשה ל-Implementation מתאים בזמן Runtime.

## 3. למה לא direct calls

Direct Agent-to-Agent calls יוצרים:

- Coupling בין repositories.
- קושי להחליף Agent.
- קושי לאכוף Permissions.
- קושי לחשב Cost.
- קושי לבצע Audit.
- שרשראות Agents לא נשלטות.

לכן כל call בין Agents עובר דרך Orchestrator + Capability Registry.

## 4. Registry record

כל Capability registration כולל לפחות:

```yaml
name: research.lookup
contractVersion: 1
providerAgent: research-agent
release: research-agent@1.3.2
risk: read-only
costClass: variable
supports:
  - public-web
  - client-knowledge
```

## 5. Resolution policy

ה-Core בוחר Implementation לפי:

1. Contract compatibility.
2. Tenant permissions.
3. Data classification.
4. Client/provider restrictions.
5. Cost profile.
6. Quality profile.
7. Availability/health.
8. Latency target.

## 6. Agent hops

כל Agent hop:

- יורש `request_id` ו-`trace_id`.
- מקבל Context מצומצם לצורך המשימה בלבד.
- אינו מקבל אוטומטית את כל Permissions של ה-Caller.
- נרשם כ-child span ב-Audit/Trace.
- נכלל בתקציב של הבקשה.

ה-Core אוכף `maxAgentHopsPerRequest` כדי למנוע loops ו-cost explosion.

## 7. Delegation

Caller אינו יכול להעניק Permission שאין לו. Capability provider מקבל רק את intersection של:

`Caller scope ∩ Provider allowed scope ∩ Tenant policy ∩ Request purpose`

## 8. Failure

אם Capability unavailable:

- ה-Core יכול לבחור Implementation חלופי אם contract תואם.
- אם אין fallback מאושר, מחזירים degraded result או escalation.
- אסור ל-Agent לעקוף Registry ולקרוא ל-implementation ישירות.

## 9. גרסאות

- Minor contract change יכול להיות backward compatible.
- Major version דורש explicit compatibility.
- Consumer Agent מצהיר איזו contract version הוא דורש.

## 10. Research/Brain Agent

ה-Research Agent המתוכנן יהיה ה-use case הראשון של Registry:

```text
Capability: research.lookup
Consumers: Travel Agent, Sales Agent, future agents
```

כך הוא הופך ליכולת משותפת בלי להיכנס לתוך ה-Core עצמו.
