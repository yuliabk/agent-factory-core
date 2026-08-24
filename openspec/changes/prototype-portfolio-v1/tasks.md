# Tasks: Prototype Portfolio V1

## 0. Planning Package — Current Authorized Scope

- [x] PF0.1 Define the three bounded patterns, synthetic tenants, exclusions and proof goals in `proposal.md`. Requirements: PP-101, PP-102, PP-104, PP-105, PP-106.
- [x] PF0.2 Define testable requirements and GIVEN/WHEN/THEN scenarios for reuse, isolation, Service, Controlled Action, audit, evaluation, cost and gates. Requirements: PP-101–PP-112.
- [x] PF0.3 Define architecture boundaries, flows, permissions, failures, observability, rollout, rollback and alternatives in `design.md`. Requirements: PP-102, PP-103, PP-105–PP-112.
- [x] PF0.4 Define task groups in dependency order with a named approval gate before every Materialization, provider or Runtime step. Requirements: PP-111, PP-112.
- [x] PF0.5 Run `openspec validate prototype-portfolio-v1 --strict`, review the scoped diff and confirm no implementation or external artifacts were created. Requirements: PP-103, PP-112.

## 1. Gate PF-G0 — Portfolio Plan Approval

- [x] PF1.1 Present the three selected patterns, tenants, success metrics, cost recommendation, risks and open decisions to the Owner. Requirements: PP-101, PP-109, PP-110, PP-111.
- [x] PF1.2 Obtain explicit Owner approval for `PF-G0` planning baseline only. Approved by the Owner on `2026-08-24`; no fixture Materialization, provider configuration, account access, Runtime, Indexing, Tools, Payment, Publish, Commit or Push was authorized. Requirements: PP-111, PP-112.

## 2. Gate PF-G1-K — Knowledge Reference Adoption

- [x] PFK1.1 After separate `PF-G1-K` approval, reference the hash-bound Phase 1 Knowledge evidence and populate only the supported fields in `evidence/pf-k-scorecard.md`. Completed locally on `2026-08-24`. Requirements: PP-104, PP-109.
- [x] PFK1.2 Mark unsupported categories, the 25-question evaluation, current cost balance and Gate G1 as `not_run`, `not_measured` or open without inference. Requirements: PP-104, PP-109, PP-111, PP-112.
- [x] PFK1.3 Validate that no Dify inspection, Runtime, Indexing, Publish or provider change occurred. No external action was performed; Commit and Push were also excluded. Requirements: PP-111, PP-112.

## 3. Gate PF-G1-S — Local Customer Service Materialization

- [x] PFS1.1 Obtain explicit `PF-G1-S` approval for local synthetic Service artifacts only, with zero provider requests and zero authorized spend. Approved by the Owner on `2026-08-24`; branch `codex/prototype-portfolio-pf-g1-s` was created without Commit or Push. Requirements: PP-111, PP-112.
- [x] PFS1.2 Materialize the `af-demo-retail` synthetic Intake with process owner, users, language, volume assumptions, forbidden outcomes and escalation owner in `service/intake.md`. Requirements: PP-101, PP-102, PP-105.
- [x] PFS1.3 Define four versioned synthetic Service policies and six cases with stable source identifiers, classification and tenant metadata under `service/policies/` and `service/cases/`. Requirements: PP-102, PP-105, PP-108.
- [x] PFS1.4 Define request, response, audit, routing, clarification, fallback, refusal and escalation contracts under `service/contracts/`, without a messaging or Ticket connector. Requirements: PP-103, PP-105.
- [x] PFS1.5 Freeze thirteen `CS-*` scenarios covering three functional successes, missing information, conflict, unsupported request, Injection, cross-tenant, protected action, escalation failure, dependency failure, cost stop and sensitive data in `service/evaluation/cs-scenarios.json`. Requirements: PP-105, PP-109, PP-111.
- [x] PFS1.6 Validate all Service schemas and synthetic fixtures locally. Final deterministic validation passed six cases, thirteen scenarios and three audit fixtures; failures during validator setup were preserved in `service/evidence/validation-evidence.md`. Evidence state is `dry_validated`. Requirements: PP-108, PP-109, PP-112.
- [x] PFS1.7 Record `433` seconds of bounded materialization/validation time, mark preceding planning time `not_measured`, and map eight canonical Factory references in `service/evidence/`. Requirements: PP-103, PP-110.

## 4. Gate PF-G1-A — Local Controlled Action Materialization

- [ ] PFA1.1 Obtain explicit `PF-G1-A` approval for local synthetic Action artifacts only, with no Tool, executor, provider or Runtime. Requirements: PP-111, PP-112.
- [ ] PFA1.2 Materialize the `af-demo-operations` synthetic Intake, allow-listed office-supply catalog, request fixtures and cost-band policies. Requirements: PP-101, PP-102, PP-106.
- [ ] PFA1.3 Define the normalized Draft, approval-reference, idempotency and minimized action-audit contracts. Requirements: PP-103, PP-106, PP-107, PP-108.
- [ ] PFA1.4 Define a deterministic local idempotency rule based only on immutable request identity and exclude executable integration code. Requirements: PP-107.
- [ ] PFA1.5 Freeze at least ten `CA-*` scenarios covering valid Draft, clarification, missing approval, expired/mismatched approval, duplicate request, execution demand, Injection, cross-tenant, sensitive data and cost stop. Requirements: PP-106–PP-109, PP-111.
- [ ] PFA1.6 Validate Action schemas and fixtures locally; even a valid synthetic approval SHALL produce `approval_validated_dry_only` and `execution_status = not_executed`. Requirements: PP-106, PP-107, PP-112.
- [ ] PFA1.7 Record active planning/materialization time and canonical Factory references in the reuse map. Requirements: PP-103, PP-110.

## 5. Gate PF-G2-S — Optional Service Provider Smoke

- [ ] PFS2.1 Select exactly one maintained provider only after incident, isolation, export, deletion, cost and hard-stop preflight passes. Botpress SHALL remain excluded while on `INCIDENT-HOLD`. Requirements: PP-102, PP-111, PP-112.
- [ ] PFS2.2 Record the exact provider, plan, model, immutable configuration, synthetic data scope, request ceiling, zero-retry rule, measurable cost indicator and Owner cap. Requirements: PP-101, PP-111.
- [ ] PFS2.3 Obtain explicit `PF-G2-S` approval before account, resource, upload, Indexing, model or Runtime access. Requirements: PP-111, PP-112.
- [ ] PFS2.4 If approved, execute only the bounded Service Smoke, stop at the first guard condition and preserve all results. Requirements: PP-105, PP-108, PP-109, PP-111.
- [ ] PFS2.5 Keep external message and action counts at zero and leave the member below `release_approved`. Requirements: PP-105, PP-112.

## 6. Gate PF-G2-A — Optional Controlled Action Dry/Smoke

- [ ] PFA2.1 Decide whether PF-A needs a model Runtime; prefer deterministic dry validation when it proves the contract. Requirements: PP-106, PP-109, PP-111.
- [ ] PFA2.2 If Runtime is proposed, select exactly one maintained provider and record request/cost ceilings, immutable configuration and stop conditions. Requirements: PP-101, PP-111, PP-112.
- [ ] PFA2.3 Obtain explicit `PF-G2-A` approval before any provider access. The approval SHALL keep external execution, Tool calls, messages, purchase and record changes forbidden. Requirements: PP-106, PP-107, PP-111.
- [ ] PFA2.4 Execute only approved Draft/approval evaluation and verify `execution_status = not_executed` for every scenario. Requirements: PP-106–PP-109.

## 7. Gate PF-G3 — Portfolio Proof Review

- [ ] PF3.1 Build the normalized Scorecard with raw denominators for time, reuse, functional quality, safety, isolation, authorization, cost, operability, portability and open risk. Requirements: PP-109, PP-110.
- [ ] PF3.2 Verify all mandatory safety categories passed for every attempted member and that `not_run` or `not_measured` values remain explicit. Requirements: PP-104, PP-109, PP-112.
- [ ] PF3.3 Review actual active hours, manual recovery steps, cost evidence and reuse quality with the Owner. Requirements: PP-103, PP-109–PP-111.
- [ ] PF3.4 Obtain explicit `PF-G3` decision on whether the bounded Factory proof is sufficient. This decision SHALL NOT imply Gate G1, G2, G4, Production, real data or external actions. Requirements: PP-112.

## 8. Packaging After a Successful PF-G3

- [ ] PF4.1 After separate approval only, prepare a sanitized Hebrew Case Study using synthetic names, evidence states, measured metrics and disclosed limitations. Requirements: PP-108–PP-110.
- [ ] PF4.2 Define a reusable Client Intake checklist and clone checklist that preserve tenant, credential, storage, index, log and evaluation isolation. Requirements: PP-102, PP-103.
- [ ] PF4.3 Stop for a new Owner decision before any first-client, non-synthetic, Production, channel or external-action work. Requirements: PP-111, PP-112.
