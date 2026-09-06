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
- [x] C1.14 Accept minimal `ClientInstanceConfig`: metadata(name/environment) + spec(agentRef/tenant/variables/trustProfile/releaseStrategy/providerProfile/secretsRef/memoryConfig/budgetOverrides/permissionOverrides/toolBindings). Maps: CORE-202, CORE-203, CORE-210, CORE-213.
- [x] C1.15 Confirm `EffectiveReleaseConfig` is the only runtime-executable configuration artifact. Maps: CORE-203, CORE-218.
- [x] C1.16 Accept trust placement/enforcement: ClientInstanceConfig requests one of `sandbox/internal/business/privileged`; PlatformPolicy sets `maxTrustProfile`; compiler rejects requests above the ceiling; EffectiveReleaseConfig and ExecutionContext carry the compiled trust profile; trust does not grant permissions. Maps: CORE-204, CORE-208, CORE-210.

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
- [x] C2.11 Compiler validation errors expose path/rule/remediation for the current enforced rules.

## C3 - Runtime Governance kernel

- [x] C3.1 Complete request-time policy evaluator: deadline/tenant/permission/data-classification plus compiled trust-profile enforcement. Compile-time trust ceiling is `ClientInstanceConfig.trustProfile <= PlatformPolicy.maxTrustProfile`; runtime cannot elevate above `ExecutionContext.trustProfile`. Maps: CORE-208, CORE-210.
- [x] C3.2 Permission/tenant/data-class enforcement tests, including conservative exact classification matching until a hierarchy is approved. Maps: CORE-204, CORE-208.
- [x] C3.3 Runtime limits/hop/cycle enforcement. Maps: CORE-205, CORE-214.
- [x] C3.4 Business-budget precheck + emergency safety-cap interface/tests; safety-cap stop is independent from business overage handling. Maps: CORE-211.
- [x] C3.5 Minimal audit/trace event canonical JSON Schema + aligned Pydantic model including policy/exception/approval/operation/target/cost/result evidence. Maps: CORE-217.

## C4 - Thin adapter vertical slice

- [x] C4.1 Provider-neutral Model Router with deterministic working adapter + compatible stub adapter. Routing is selected from trusted `ExecutionContext.providerProfile`; Agent requests do not carry provider/adapter IDs; permission/trust/classification/deadline checks and fallback are enforced; costed adapters remain blocked until runtime budget accounting is attached. Maps: CORE-207.
- [x] C4.2 Add first in-process Capability Registry resolver with authoritative records, override validation and soft/strict resolution behavior. Richer health/version routing remains later depth. Maps: CORE-205, CORE-206.
- [x] C4.3 Tool Gateway interface + deterministic read-only synthetic tool. Trusted ExecutionContext binding, tenant/permission/trust/classification checks, JSON Schema input/output validation and audit are enforced; costed or write-capable tools remain blocked in this first slice. Maps: CORE-208.
- [x] C4.4 Memory Gateway interface + ephemeral `session` / `task_working` implementation. Session scope uses trusted request ID; task scope uses trusted trace ID; namespace includes tenant/release/class/scope/key; memory read/write permissions, trust, classification, purpose, retention and enable flags are enforced; malformed config is default-deny; persistent/client-knowledge classes remain blocked. Maps: CORE-209.
- [x] C4.5 Bounded Hybrid Orchestrator executes an Agent-prepared plan across compiled capability/model/tool/memory steps. Tenant/classification come only from trusted ExecutionContext; each step retains its gateway checks; max-step/repeat limits and deadline are enforced; execution fails closed on the first denial and records per-step audit evidence. Maps: CORE-214.

## C5 - Eval/release kernel

- [x] C5.1 Canonical decision-neutral EvalResult JSON Schema + frozen Pydantic model for functional/business, security/policy, cost/runtime and contract/portability families. Raw statuses are `PASS`, `PASS_WITH_WARNINGS`, `FAIL`; blocking/warning/advisory and release decisions are intentionally excluded from the result contract. Maps: CORE-212.
- [x] C5.2 PlatformPolicy evalRules map every release-gated check explicitly to `blocking`, `warning` or `advisory`; unmapped/duplicate rules, mixed releases and malformed security-invariant policy fail closed; securityInvariantChecks cannot be downgraded from blocking. Maps: CORE-212.
- [x] C5.3 ClientInstanceConfig requests `human-required`, `policy-auto` or `policy`; PlatformPolicy defines a concrete minimum strategy; compiler writes only concrete `human-required`/`policy-auto` to EffectiveReleaseConfig. Eval gate failures block every strategy; eligible policy-auto can auto-release and eligible human-required requires human approval. Maps: CORE-213.
- [x] C5.4 Canonical HumanApprovalRecord, ReleaseDecisionRecord and EvidencePack contracts. Approval is bound to exact release/policy/exception refs and validity window; policy-auto/human-required decisions are recorded; blocking evals cannot be overridden; EvidencePack links versioned source/config/policy/component/eval/decision/rollback references without raw sensitive payloads. Maps: CORE-217.
- [x] C5.5 Canonical SHA-256 fingerprint binds EvidencePack to the exact EffectiveReleaseConfig. Drift verification compares approved spec/release/policy/exception/provider evidence plus runtime ExecutionContext authority (release/environment/agent/tenant/trust/permissions/classification/capabilities/provider/tools/memory/budget); any mismatch marks the release unmanaged. Maps: CORE-218.

## C6 - Synthetic end-to-end gate

- [x] C6.1 Checked-in `examples/synthetic-reference-agent/agent-manifest.json` uses only the accepted minimal AgentManifest fields; companion client/policy fixtures remain outside reusable Agent behavior and are validated against canonical JSON Schemas.
- [x] C6.2 Compiler path supports AgentManifest + ClientInstanceConfig + typed Policy/Exception + Registry resolution -> EffectiveReleaseConfig.
- [x] C6.3 The checked-in synthetic definition compiles to trusted ExecutionContext and executes one bounded capability -> model -> read-only tool -> task-memory write/read plan through Runtime Governance.
- [x] C6.4 The same end-to-end path emits functional/business, security/policy, cost/runtime and contract/portability EvalResults, maps them through PlatformPolicy and produces a policy-auto ReleaseDecisionRecord.
- [x] C6.5 Per-step audit evidence, EvidencePack reconstruction, canonical release fingerprint and C5.5 drift verification are proven on the same release/context/spec chain.

**Exit gate: PASSED.** One complete thin Core path works end-to-end without provider or business-domain lock-in; PR #27 final C6 code run #89 passed 93 contract tests and the merged `main` push run #91 passed.

## C7 - Research/Brain Agent gate

- [x] C7.1 Authoritative `research.lookup@1` Registry contract is defined with canonical Registry/Input/Output JSON Schemas, `read_only` risk, `variable` cost, `public/internal` data scope, consumer permission `research.lookup`, bounded `qualityProfile` override, provider-neutral payload and structured evidence/provenance output. Provider-internal `web.search`/API/model/tool permissions do not leak into consumer authority.
- [x] C7.2 Research/Brain Agent exists in separate repository `yuliabk/agent-factory-research-agent`, provides lightweight `research.lookup@1`, is contract-locked to Core and is registered by exact sandbox release commit. Core resolution tests verify the exact external implementation and fail closed for production.
- [x] C7.3 Smallest useful real source set is proven without widening public authority: internal evidence plus a real keyless English Wikipedia source through the official MediaWiki REST API. Wikipedia is background-only (`freshness=any`); `recent/current` is not misrepresented. Source timeouts/failures degrade through limitations, deterministic tests pass and a live Wikipedia CI smoke test passes. The first real-source release was `4a8b308aeaf22228c6a03d438509b0717e6daf8b`; later C7.4 transport work advances the Registry to the HTTP-capable compatible release. Production remains blocked.
- [x] C7.4a Travel Agent is the first sandbox consumer boundary: external Travel commit `9da84b635d1ea3b1d62f4b4e8652acd22e42ead6` contains a provider-neutral `research.lookup` consumer, PII-minimized requests, non-commercial background evidence separation, fail-safe workflow handling and its own green Contract v1 CI. Core locks the external manifest and proves compile-time/ExecutionContext authority contains only `research.lookup`, and never grants provider-internal `web.search` or direct tool bindings.
- [x] C7.4b Governed HTTP JSON capability transport is proven end-to-end in sandbox. Core commit `78a893f02248728082139bbdbd1978b67df2e5c0` defines canonical invocation/response envelopes, Registry transport metadata, trusted-context delegation, bearer runtime endpoint config, schema/correlation validation and audit. Research Agent release `024367572ca001dec385ca0f781495b5fa91d181` exposes the sandbox-only authenticated endpoint and independently validates capability/scope/classification/deadline/hop/release boundaries. Core Registry resolves `research.lookup@1` to that exact release with `endpointRef=research-agent-sandbox`. PR #34 integration run `34041728655` checked out exact Travel/Research commits, started the real Research HTTP service, executed the actual Travel `ResearchLookupConsumerV1` through Core `GovernedCapabilityInvoker`, retrieved real Wikipedia evidence, mapped it back into non-commercial Travel evidence, and preserved Travel trace/audit while never delegating `web.search`. Core contract run `34041728604` also passed. Production remains disabled.
