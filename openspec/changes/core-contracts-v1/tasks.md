# Tasks: Core Contracts v1

Architecture decisions were reviewed with the Owner on 2026-09-06. Implementation proceeds in bounded task groups; material architecture/authority changes return to Owner review.

## C1 - Documentation and contract synchronization

- [x] C1.1 Accept platform vision and Core boundaries. Maps: CORE-201, CORE-215, CORE-216, CORE-218.
- [x] C1.2 Accept reusable AgentManifest + ClientInstanceConfig + EffectiveReleaseConfig model. Maps: CORE-202, CORE-203.
- [x] C1.3 Accept trusted ExecutionContext and bounded-autonomy orchestration. Maps: CORE-204, CORE-214.
- [x] C1.4 Accept risk/trust security, governance and controlled ExceptionPolicy direction. Maps: CORE-208, CORE-210.
- [x] C1.5 Accept governed autonomous memory contract. Maps: CORE-209.
- [x] C1.6 Accept soft-strict Capability Registry. Maps: CORE-205, CORE-206.
- [x] C1.7 Accept provider-neutral policy-driven routing and budget/safety model. Maps: CORE-207, CORE-211.
- [x] C1.8 Accept policy-driven eval/release strategy. Maps: CORE-212, CORE-213.
- [x] C1.9 Accept ADR-005 through ADR-011.
- [x] C1.10 Synchronize roadmap and decision log.
- [x] C1.11 Accept minimal first AgentManifest shape: `apiVersion`, `kind`, `metadata(name/version/description)`, and `spec(template/capabilities/tools/permissions/memoryProfile/budgetProfile/evalProfile)`. Maps: CORE-202.
- [x] C1.12 Accept hybrid schema boundary: JSON Schema canonical externally; Pydantic internal for Python runtime/validation. Maps: CORE-202, CORE-203. ADR-012.
- [x] C1.13 Accept Registry-backed capability references and bounded overrides. Maps: CORE-202, CORE-205, CORE-206. ADR-013.
- [x] C1.14 Accept minimal `ClientInstanceConfig`: metadata(name/environment) + spec(agentRef/tenant/variables/providerProfile/secretsRef/memoryConfig/budgetOverrides/permissionOverrides/toolBindings). Maps: CORE-202, CORE-203.
- [x] C1.15 Confirm `EffectiveReleaseConfig` is the only runtime-executable configuration artifact. Maps: CORE-203, CORE-218.

## C2 - Core Skeleton schemas/compiler

- [x] C2.1 Choose executable schema approach: JSON Schema external contract + Pydantic internal models/validation. Maps: CORE-202, CORE-203.
- [x] C2.2 Add canonical JSON Schema for `AgentManifest` from the accepted minimal shape. Maps: CORE-202.
- [x] C2.3 Add matching Pydantic AgentManifest models. Maps: CORE-202.
- [x] C2.4 Add schema/Pydantic semantic-alignment tests. Maps: CORE-202, CORE-203.
- [x] C2.5 Contract CI is active in GitHub Actions; PR #16 run #4 passed all 16 contract tests on 2026-09-06.
- [x] C2.6 Implement `ClientInstanceConfig` JSON Schema + Pydantic model/validator and aligned template. Maps: CORE-202.
- [x] C2.7 Implement minimal typed `PlatformPolicy` + `ExceptionPolicy` JSON Schemas + Pydantic models. Maps: CORE-210.
- [x] C2.8 Add immutable `EffectiveReleaseConfig` JSON Schema/Pydantic contract and compiler using typed policy objects. Maps: CORE-203.
- [x] C2.9 Resolve required capability refs against an in-process Registry and reject non-overrideable override keys. Maps: CORE-202, CORE-205, CORE-206.
- [x] C2.10 Define trusted `ExecutionContext` JSON Schema + Pydantic model/builder. Maps: CORE-204.
- [x] C2.11 Compiler validation errors expose path/rule/remediation hints for current enforced rules.

## C3 - Runtime Governance kernel

- [ ] C3.1 Complete request-time policy evaluator. Compile-time permission/provider/memory/budget boundaries and scoped ExceptionPolicy validation are already implemented; trust ceilings/runtime checks remain. Maps: CORE-208, CORE-210.
- [ ] C3.2 Permission/tenant/data-class enforcement tests. Maps: CORE-204, CORE-208.
- [ ] C3.3 Runtime limits/hop/cycle enforcement. Maps: CORE-205, CORE-214.
- [ ] C3.4 Business-budget precheck + emergency safety-cap interface/tests. Maps: CORE-211.
- [ ] C3.5 Minimal audit/trace event schema including policy/exception/cost decisions. Maps: CORE-217.

## C4 - Thin adapter vertical slice

- [ ] C4.1 Provider-neutral model interface with one working adapter and one second test/stub adapter. Maps: CORE-207.
- [x] C4.2 Add first in-process Capability Registry resolver with authoritative records, override validation and soft/strict resolution behavior. Richer health/version routing remains later depth. Maps: CORE-205, CORE-206.
- [ ] C4.3 Tool Gateway interface + one read-only test tool. Maps: CORE-208.
- [ ] C4.4 Memory Gateway interface + session/task memory implementation. Maps: CORE-209.
- [ ] C4.5 Hybrid Orchestrator can execute one bounded capability/model/tool/memory plan. Maps: CORE-214.

## C5 - Eval/release kernel

- [ ] C5.1 EvalResult schema for functional/security/cost/contract families. Maps: CORE-212.
- [ ] C5.2 Policy mapping for blocking/warning/advisory. Maps: CORE-212.
- [ ] C5.3 Implement release strategies `human-required`, `policy-auto`, `policy`. Maps: CORE-213.
- [ ] C5.4 Build minimal Evidence Pack and release decision record. Maps: CORE-217.
- [ ] C5.5 Drift check: runtime release maps to approved Spec + EffectiveReleaseConfig. Maps: CORE-218.

## C6 - Synthetic end-to-end gate

- [ ] C6.1 Create a tiny synthetic reference Agent Definition using only the minimal AgentManifest fields.
- [x] C6.2 Compiler path supports AgentManifest + ClientInstanceConfig + typed Policy/Exception + Registry resolution -> EffectiveReleaseConfig.
- [ ] C6.3 Execute through Runtime Governance kernel using ExecutionContext.
- [ ] C6.4 Run required evals and release decision.
- [ ] C6.5 Verify audit/evidence reconstruction.

**Exit gate:** one complete thin path works without provider/business lock-in.

## C7 - Research/Brain Agent gate

- [ ] C7.1 Define/approve authoritative `research.lookup` Registry contract.
- [ ] C7.2 Create Research/Brain Agent in a separate repository using a lightweight `research.lookup` capability ref.
- [ ] C7.3 Start with the smallest useful source set and expand only after contract validation.
- [ ] C7.4 Use Travel Agent as the first external consumer after Research v1 is stable.
