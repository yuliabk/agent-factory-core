# Tasks: Core Contracts v1

Architecture decisions were reviewed with the Owner on 2026-09-06. Implementation still proceeds in bounded task groups; material architecture/authority changes return to Owner review.

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

## C2 - Core Skeleton schemas/compiler

- [ ] C2.1 Choose minimal schema implementation approach (recommend JSON Schema as external contract + Pydantic/runtime types if Python is selected). Maps: CORE-202, CORE-203.
- [ ] C2.2 Implement `AgentManifest` schema/validator. Maps: CORE-202.
- [ ] C2.3 Implement `ClientInstanceConfig` schema/validator. Maps: CORE-202.
- [ ] C2.4 Implement minimal `PlatformPolicy` + `ExceptionPolicy` schemas. Maps: CORE-210.
- [ ] C2.5 Compile inputs into immutable `EffectiveReleaseConfig`. Maps: CORE-203.
- [ ] C2.6 Define trusted `ExecutionContext` schema. Maps: CORE-204.
- [ ] C2.7 Define clear validation errors with path/rule/remediation hint.

## C3 - Runtime Governance kernel

- [ ] C3.1 Policy evaluator: default deny, trust ceilings, exception validation. Maps: CORE-208, CORE-210.
- [ ] C3.2 Permission/tenant/data-class enforcement tests. Maps: CORE-204, CORE-208.
- [ ] C3.3 Runtime limits/hop/cycle enforcement. Maps: CORE-205, CORE-214.
- [ ] C3.4 Business-budget precheck + emergency safety-cap interface/tests. Maps: CORE-211.
- [ ] C3.5 Minimal audit/trace event schema including policy/exception/cost decisions. Maps: CORE-217.

## C4 - Thin adapter vertical slice

- [ ] C4.1 Provider-neutral model interface with one working adapter and one second test/stub adapter. Maps: CORE-207.
- [ ] C4.2 In-process Capability Registry with dev/production enforcement modes. Maps: CORE-205, CORE-206.
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

- [ ] C6.1 Create a tiny synthetic reference Agent Definition.
- [ ] C6.2 Compile AgentManifest + ClientInstanceConfig + Policy to EffectiveReleaseConfig.
- [ ] C6.3 Execute through Runtime Governance kernel.
- [ ] C6.4 Run required evals and release decision.
- [ ] C6.5 Verify audit/evidence reconstruction.

**Exit gate:** one complete thin path works without provider/business lock-in.

## C7 - Research/Brain Agent gate

- [ ] C7.1 Define/approve `research.lookup` capability contract.
- [ ] C7.2 Create Research/Brain Agent in a separate repository.
- [ ] C7.3 Start with the smallest useful source set and expand only after contract validation.
- [ ] C7.4 Use Travel Agent as the first external consumer after Research v1 is stable.
