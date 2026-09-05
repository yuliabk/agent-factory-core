# משימות: Travel Agent Instance Contract v1

## 0. Contract package

- [x] TAIC0.1 לתעד החלטות Owner, scope, exclusions, success criteria וסיכונים. Requirements: TAIC-101, TAIC-102, TAIC-107, TAIC-110.
- [x] TAIC0.2 להגדיר `TripRequest`, `EvidencePack`, `ProposalDraft`, `EvalResult`, `ApprovalRecord` ו-`AuditBundle` כולל versioning, IDs ו-statuses. Requirements: TAIC-101 עד TAIC-108.
- [x] TAIC0.3 להגדיר State transitions, approval invalidation ו-partial-draft behavior. Requirements: TAIC-104, TAIC-105, TAIC-106, TAIC-107.
- [x] TAIC0.4 להגדיר Channel-neutral Runtime direction עבור Web, Email ו-WhatsApp. Requirement: TAIC-109.
- [x] TAIC0.5 לתעד במפורש את הסתירה בין יעד המוצר ל-PII לבין מגבלת ה-MVP הנוכחית, ולשמור PII execution מאחורי Gate נפרד. Requirements: TAIC-102, TAIC-110.

## 1. Validation before Owner approval

- [ ] TAIC1.1 להריץ `openspec validate travel-agent-instance-contract-v1 --strict` בסביבה שבה OpenSpec CLI וה-repository המלא זמינים. Requirements: TAIC-110.
- [ ] TAIC1.2 לסקור Diff ולוודא שאין Secret, Credential, מידע אישי אמיתי, Tenant URL או Production data. Requirements: TAIC-102, TAIC-108, TAIC-110.
- [ ] TAIC1.3 לוודא שאין סתירה מהותית מול `automated-travel-proposal-poc-v1`; במקרה של סתירה, להעדיף את המגבלה המחמירה עד Change מפורש. Requirements: TAIC-102, TAIC-103, TAIC-110.
- [ ] TAIC1.4 לקבל Owner approval לחבילת Contract v1. Requirement: TAIC-110.

## 2. Future implementation group A - Runtime schemas and validation

> Blocked until explicit implementation approval.

- [ ] TAIC2.1 למפות את החוזים ל-Pydantic models ב-`travel-agent-bot` עם `schema_version` ו-strict validation. Requirements: TAIC-101 עד TAIC-108.
- [ ] TAIC2.2 להוסיף request lifecycle ו-error codes עבור `NEEDS_INFORMATION`, unresolved IATA ו-invalid date/traveler constraints. Requirements: TAIC-101, TAIC-104.
- [ ] TAIC2.3 להוסיף versioned Proposal persistence ו-hash generation. Requirement: TAIC-105.
- [ ] TAIC2.4 להוסיף contract tests שמוכיחים backward-compatible parsing או rejection מפורש של schema לא נתמך. Requirements: TAIC-101 עד TAIC-108.

## 3. Future implementation group B - Evidence and providers

> Blocked until separate Provider/Network approval.

- [ ] TAIC3.1 ליצור Provider Adapter interface קנוני ולמנוע direct provider calls משכבת UI. Requirements: TAIC-103, TAIC-109.
- [ ] TAIC3.2 להעביר יכולות חיפוש נבחרות מה-Web App ל-Backend adapter מאושר בלי לשנות UX. Requirements: TAIC-103, TAIC-109.
- [ ] TAIC3.3 ליישם `EvidencePack` normalization ו-price provenance rules. Requirement: TAIC-103.
- [ ] TAIC3.4 להוסיף tests ל-stale/invalid/missing evidence ול-provider schema drift. Requirements: TAIC-103, TAIC-104.

## 4. Future implementation group C - Planner and Evals

> Blocked until explicit implementation/model approval.

- [ ] TAIC4.1 לשנות Planner כך שיקבל normalized Evidence בלבד עבור claims מסחריים. Requirements: TAIC-103, TAIC-104.
- [ ] TAIC4.2 ליישם partial draft ו-clarification flow. Requirements: TAIC-101, TAIC-104.
- [ ] TAIC4.3 ליישם Eval suite versioned עם כל בדיקות החובה של TAIC-106. Requirement: TAIC-106.
- [ ] TAIC4.4 לחסום Review/Approval כאשר Eval הוא `FAIL`. Requirements: TAIC-106, TAIC-107.

## 5. Future implementation group D - Human approval and delivery

> Blocked until explicit messaging/action approval.

- [ ] TAIC5.1 ליישם `ApprovalRecord` המחובר ל-`proposal_version` ול-`proposal_hash`. Requirements: TAIC-105, TAIC-107.
- [ ] TAIC5.2 לוודא שכל שינוי חומרי יוצר גרסה חדשה ומחייב Re-Approval. Requirement: TAIC-105.
- [ ] TAIC5.3 לחייב Approval תקף לפני Final PDF, Email, WhatsApp או publication. Requirement: TAIC-107.
- [ ] TAIC5.4 להשאיר Booking/Payment/Ticketing תחת Gate action-specific נפרד גם כאשר Proposal מאושר. Requirement: TAIC-107.

## 6. Future implementation group E - Audit and Web consolidation

- [ ] TAIC6.1 ליישם `AuditBundle` ממוזער עם References ו-hashes במקום שכפול secrets/PII. Requirement: TAIC-108.
- [ ] TAIC6.2 לשנות את Next.js `/api/submit` כך שיפנה ל-Travel Agent Runtime במקום ליצור authoritative Proposal דרך LLM/provider ישירות. Requirement: TAIC-109.
- [ ] TAIC6.3 לבצע parity tests בין ה-Web flow הישן ל-Runtime החדש לפני הסרת orchestration כפול. Requirement: TAIC-109.
- [ ] TAIC6.4 לחבר Email ו-WhatsApp לאותו request/proposal chain ולוודא שאין source of truth נוסף. Requirement: TAIC-109.

## Definition of Done לחבילת Contract

חבילת המפרט מוכנה לאישור כאשר TAIC1.1-TAIC1.3 הושלמו, כל requirements ניתנים לבדיקה, אין Secret או PII אמיתי ב-Diff, וה-Owner מאשר במפורש את Contract v1. אישור Contract אינו מאשר אף קבוצת Implementation עתידית.
