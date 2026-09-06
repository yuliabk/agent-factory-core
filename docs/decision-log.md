# Architecture Decision Log

מסמך זה הוא אינדקס מהיר להחלטות. ADRs ו-contract docs הם המקור המפורט.

## 2026-09-06 - Accepted directions

| Decision | Status | Source |
|---|---|---|
| Agent Factory Core הוא Platform Core, לא Agent עסקי | Accepted | ADR-005 |
| Core מחולק לוגית ל-Build/Control Plane ול-Runtime Governance Plane | Accepted | ADR-005 / architecture.md |
| שני ה-Planes יכולים להתחיל באותו repo עם contract boundary לפיצול עתידי | Accepted | ADR-005 |
| Business Agents נמצאים בריפו נפרד | Accepted | ADR-005 |
| Specification וה-history שלה הם הארטיפקט הראשי; Agent/deployment הם reproducible outputs | Accepted | ADR-011 / architecture.md |
| AgentManifest reusable מופרד מ-ClientInstanceConfig | Accepted | agent-manifest.md |
| `AgentManifest + ClientInstanceConfig + PlatformPolicy/ExceptionPolicy -> EffectiveReleaseConfig` | Accepted | agent-manifest.md / architecture.md |
| Agent מבקש Permission/Capability אך אינו מעניק אותם לעצמו | Accepted | agent-manifest.md / security-model.md |
| AgentManifest הראשון נשמר מינימלי: `apiVersion`, `kind`, `metadata(name, version, description)`, ו-`spec` בלבד | Accepted | agent-manifest.md |
| `spec` הראשון כולל רק `template`, `capabilities`, `tools`, `permissions`, `memoryProfile`, `budgetProfile`, `evalProfile` | Accepted | agent-manifest.md / templates/agent-manifest.yaml |
| Manifest profile/permission fields הם requirements/references ולא concrete client grants | Accepted | agent-manifest.md |
| שדות חדשים יתווספו ל-AgentManifest רק כאשר use case אמיתי מוכיח צורך | Accepted | agent-manifest.md |
| JSON Schema הוא ה-contract החיצוני הקנוני; Pydantic הוא ה-runtime/internal model ב-Python | Accepted | ADR-012 |
| Pydantic אינו contract עצמאי; הוא חייב להישאר semantically aligned ל-JSON Schema | Accepted | ADR-012 |
| Release strategy מוגדרת בספציפיקציה/קונפיגורציה ומוגבלת ע"י Policy | Accepted | ADR-010 / agent-lifecycle.md |
| Release modes: `human-required`, `policy-auto`, `policy` | Accepted | ADR-010 |
| לא נדרש Human approval לכל שינוי/פעולה; approvals הם risk-based | Accepted | security-model.md / governance.md |
| Trust Levels משמשים profiles: sandbox/internal/business/privileged | Accepted direction | ADR-009 / security-model.md |
| Factory מציע trust; PlatformPolicy קובעת ceiling; client יכול להחמיר בתוך הגבול | Accepted | ADR-009 |
| יש Non-overridable invariants ויש overridable rules עם ExceptionPolicy מבוקרת | Accepted | ADR-009 / governance.md |
| הרשימה הסופית של non-overridable production invariants תיקבע לפני Production | Open implementation detail | security-model.md |
| Agent-to-Agent דרך Capability Registry ולא direct coupling | Accepted | ADR-006 |
| Capability Registry הוא soft-strict: warnings/mocks ב-dev, strict critical resolution ב-production | Accepted | capability-registry.md |
| Orchestration הוא hybrid: Core קובע גבולות, Agent מתכנן אוטונומית בתוכם | Accepted | orchestration.md |
| Model/Provider אינם hard-coded ב-Business Agent | Accepted | ADR-007 |
| Provider/model routing הוא policy-driven לפי cost, quality, privacy, latency, availability ו-client/task | Accepted | ADR-007 / provider-and-cost-policy.md |
| Business budget הוא warn-and-approve לפי policy | Accepted | ADR-008 |
| Runtime overage מאושר ע"י authorized client approver כאשר policy דורשת | Accepted | ADR-008 |
| Emergency safety cap נפרד ואינו מתבטל ע"י business overage approval | Accepted | ADR-008 |
| Memory מופרדת למחלקות ו-Tenant boundaries | Accepted | memory-contract.md |
| Agent רשאי לזהות מידע שכדאי לזכור ולבצע/request write; Policy מחליטה אם/איך לשמור | Accepted | memory-contract.md |
| PII persistent memory דורש policy/consent/legal basis מתאים | Accepted | security-model.md / memory-contract.md |
| Template הוא starting point + modular composition, לא מסגרת קשיחה | Accepted | template-engine.md |
| Progressive complexity: מתחילים בהרכב הכי פשוט שמספק outcome | Accepted | platform-vision.md / template-engine.md |
| Eval families: functional/business, security/policy, cost/runtime, contract/portability | Accepted | evidence-and-evals.md |
| Eval thresholds ו-release blocking הם policy-driven; security invariant failure תמיד blocking | Accepted | evidence-and-evals.md |
| Client UX הוא technical black box אך business-transparent לגבי scope/assumptions/services/cost/approvals | Accepted | platform-vision.md |
| Intake: יעד מתחת ל-10 דקות ובדרך כלל 5-6 שאלות קריטיות, לא hard limit | Accepted | platform-vision.md |
| בקשה עמומה: `infer -> show assumptions -> confirm/correct` | Accepted | platform-vision.md |
| Research/Brain Agent יהיה Agent נפרד שמספק `research.lookup` | Accepted direction / planned | roadmap.md |
| Research Agent יבחר בין internal knowledge, web, API, MCP, model knowledge ו-approved capabilities לפי policy | Accepted direction / planned | roadmap.md |
| Travel Agent יהיה consumer ראשון לבדיקת reusability | Planned | roadmap.md |

## Open implementation decisions - resolve just-in-time

These do not block starting the thin Core Skeleton:

1. Physical Capability Registry backend after the initial in-process implementation.
2. First two real provider adapters for portability validation.
3. Pricing source and currency normalization.
4. Concrete default emergency safety-cap values by workload.
5. Final production list of non-overridable invariants.
6. Persistent-memory backend and whether/when it becomes a separate service.
7. Exact client approval identity representation for each channel.
8. Factory client-facing UI repository/deployment location.
9. Long-term template package registry/storage beyond base templates.

## Working rule

Decisions that affect architecture, authority, security, cost, data handling or external side effects come back to Owner review. Routine synchronization, wording, cross-document consistency and implementation details inside accepted contracts can be handled automatically and recorded in PR history.