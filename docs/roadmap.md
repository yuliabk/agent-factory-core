# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** Architecture and contract hardening before implementation.

## North Star

לבנות פלטפורמה שבה לקוח לא טכני מתאר צורך עסקי במספר דקות ומקבל Agent מוכן, בעוד שה-Core מטפל מאחורי הקלעים ב-Spec, Template, Security, Models, Tools, Memory, Budget, Evals, Release ו-Audit.

## Phase 0A - Baseline שכבר קיים

- Control Plane / Client Data Plane.
- OpenSpec workflow.
- Client isolation principles.
- Release manifest concept.
- Initial security model.
- Prototype runtime exploration.

**Status:** Baseline exists. יש לעדכן אותו לפי ההחלטות החדשות לפני הרחבת קוד.

## Phase 0B - Core Contracts

**Status:** Current.

### Deliverables

- [ ] Owner review של `docs/architecture.md`.
- [ ] Owner review של `docs/agent-manifest.md`.
- [ ] Owner review של `docs/agent-lifecycle.md`.
- [ ] Owner review של `docs/security-model.md`.
- [ ] Owner review של `docs/capability-registry.md`.
- [ ] Owner review של `docs/provider-and-cost-policy.md`.
- [ ] Owner review של `docs/client-experience.md`.
- [ ] Accept/modify ADR-005 עד ADR-008.
- [x] לפתוח OpenSpec change שמרכז את השינוי: `core-contracts-v1`.

**Exit gate:** Owner מאשרת את contracts לפני implementation.

## Phase 1 - Manifest + Policy Skeleton

מימוש קטן וממוקד בלבד:

- [ ] JSON/YAML schema ל-Agent Manifest.
- [ ] Manifest validator.
- [ ] ExecutionContext contract.
- [ ] Permission default-deny check.
- [ ] Runtime limit validation.
- [ ] Budget policy validation.
- [ ] Minimal audit event schema.

**Goal:** להוכיח שכל Agent עתידי נכנס למסגרת לפני Runtime.

## Phase 2 - Provider-neutral Model Router

- [ ] Model profile schema.
- [ ] Provider adapter interface.
- [ ] לפחות שני adapters לצורך portability test.
- [ ] Fallback policy.
- [ ] Cost accounting hooks.
- [ ] Regression evaluation between providers.

**Goal:** החלפת Model/Provider ללא שינוי Business Logic.

## Phase 3 - Tool Gateway + Capability Registry

- [ ] Capability registration.
- [ ] Capability resolution.
- [ ] Agent-to-Agent context delegation.
- [ ] max hop enforcement.
- [ ] Tool schema validation.
- [ ] Side-effect classification.
- [ ] Human approval gate.
- [ ] Audit chain.

**Goal:** Agent יכול להשתמש ב-Agent/Tool אחר בלי direct coupling.

## Phase 4 - Template Engine + Spec Compiler

- [ ] Base agent template.
- [ ] Template registry contract.
- [ ] ClientIntent schema.
- [ ] Spec compiler prototype.
- [ ] Conversational intake flow.
- [ ] Assumption/confidence handling.
- [ ] Budget-aware solution profiles.

**Goal:** לא לבנות Agents מאפס.

## Phase 5 - Research/Brain Agent v1

ריפו נפרד מה-Core.

### Capability

`research.lookup`

### Responsibilities

- [ ] להחליט האם יש מספיק מידע פנימי.
- [ ] לבחור Knowledge, Web, API, MCP או approved external capability.
- [ ] לבצע source/provenance tracking.
- [ ] לעבוד דרך Model Router ולא מול Provider hard-coded.
- [ ] לכבד Budget, data policy ו-tool permissions.
- [ ] להחזיר structured result ל-Agent caller.

**Goal:** capability משותפת לכל Agents עתידיים.

## Phase 6 - Travel Agent Integration

Travel Agent ישמש Consumer ראשון ל-`research.lookup`.

- [ ] להסיר תלות ישירה בחיפוש ספציפי ככל האפשר.
- [ ] לחבר דרך Capability Registry.
- [ ] להריץ end-to-end cost/security/quality eval.
- [ ] לבדוק provider fallback.

**Goal:** להוכיח שהארכיטקטורה באמת reusable.

## Phase 7 - Client Factory UX

- [ ] Conversational intake של פחות מ-10 דקות ברוב המקרים.
- [ ] 5-6 שאלות קריטיות לכל היותר במסלול רגיל.
- [ ] Non-technical language.
- [ ] Assumption confirmation.
- [ ] Budget options.
- [ ] Build status.
- [ ] Plain-language permissions/approvals.
- [ ] Delivery summary.

## Phase 8 - Hardening and Multi-client Operations

- [ ] Security attack corpus.
- [ ] Cross-tenant negative tests.
- [ ] Budget anomaly detection.
- [ ] Provider outage tests.
- [ ] Backup/recovery/deletion evidence.
- [ ] Incident runbooks.
- [ ] Support/SLA model.

## Current stop point

הנקודה הנוכחית היא **Phase 0B - Core Contracts**.

הצעד הבא לאחר Review הוא לא לבנות מיד את Research Agent, אלא קודם לאשר את Manifest, Lifecycle, Security baseline, Capability routing ו-Provider/Cost contracts. לאחר מכן מממשים Skeleton קטן של ה-Core ורק אז פותחים את ריפו ה-Research/Brain Agent.
