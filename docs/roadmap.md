# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** Phase 1 Core Skeleton is complete end-to-end; C7.1-C7.3 and the C7.4a Travel sandbox consumer/authority gate are complete. The next executable step is C7.4b: define and prove one governed Travel -> Core -> Research sandbox invocation path without direct peer URL coupling.

## North Star

Build a platform where a non-technical client describes a business need in minutes and receives a governed Agent, while Core handles Spec, Templates, Security, Providers, Tools, Memory, Budget, Evals, Release and Audit behind the scenes.

The specification and its history remain the primary artifact. Deployments are reproducible outputs.

## Delivery strategy - move fast without building a fragile monolith

We build a thin vertical slice that proves the critical contracts end-to-end, then deepen only the modules proven necessary.

Principles:

- one architectural decision -> synchronize all affected docs/specs immediately;
- Owner spends time on material decisions, not repetitive editing;
- defaults/profiles reduce manual approvals/configuration;
- progressive complexity;
- thin interfaces before sophisticated infrastructure;
- do not add schema fields before a real use case needs them;
- external contracts stay implementation-neutral even when the first Core runtime is Python;
- Capability Registry owns capability contracts/metadata; manifests carry lightweight refs;
- ClientInstanceConfig contains client/environment deployment values only, never reusable business logic;
- Runtime executes only compiled EffectiveReleaseConfig;
- ExecutionContext is derived from EffectiveReleaseConfig rather than prompts or drafts;
- release evidence is bound to the exact EffectiveReleaseConfig fingerprint and approved specification;
- external capability consumers receive only their consumer authority, not provider-internal tool/provider permissions;
- remote Agent-to-Agent invocation must preserve Core authority/trace/budget/deadline/audit boundaries rather than introduce direct peer URLs;
- Research/Brain Agent is the first real external reference provider/consumer boundary test.

## Phase 0A - Historical baseline

Existing assets include OpenSpec workflow, client isolation concepts, release manifests, security/prototype work and earlier Dify/n8n/runtime exploration.

**Status:** Historical baseline preserved; newer accepted contracts take precedence.

## Phase 0B - Core architecture/contracts synchronization

**Status:** Complete after Owner review and repository-wide architecture synchronization on 2026-09-06.

## Phase 1 - Core Skeleton Vertical Slice

**Goal:** get a small working Core as quickly as possible without pretending the entire platform exists.

### 1A. Contract schemas and compiler

- [x] Minimal `AgentManifest` contract shape accepted.
- [x] JSON Schema is canonical externally; Pydantic is internal Python validation/runtime representation.
- [x] Registry-backed capability reference model accepted and implemented.
- [x] Canonical AgentManifest JSON Schema + matching Pydantic models + alignment tests.
- [x] Minimal `ClientInstanceConfig` JSON Schema + Pydantic model + tests.
- [x] Immutable `EffectiveReleaseConfig` JSON Schema + frozen Pydantic model.
- [x] Minimal typed `PlatformPolicy` JSON Schema + Pydantic model.
- [x] Minimal scoped/expiring `ExceptionPolicy` JSON Schema + Pydantic model.
- [x] Compiler consumes typed PlatformPolicy/ExceptionPolicy.
- [x] Compiler validates scoped exceptions against explicit PlatformPolicy exception allowances.
- [x] In-process Capability Registry resolves required capability refs and rejects protected/invalid overrides.
- [x] EffectiveReleaseConfig records resolved capability bindings and applied policy/exception versions.
- [x] Trusted `ExecutionContext` JSON Schema + Pydantic builder from EffectiveReleaseConfig.
- [x] Compiler errors expose path/rule/remediation for enforced rules.

**Contract rule:** JSON Schema is externally authoritative. Pydantic is an internal implementation projection and must remain aligned.

**Runtime rule:** `AgentManifest + ClientInstanceConfig + PlatformPolicy/valid ExceptionPolicy + Registry resolution -> EffectiveReleaseConfig -> ExecutionContext`.

### 1B. Runtime Governance kernel

- [x] trusted `ExecutionContext` contract and builder.
- [x] trust/risk + request-time permission evaluation, including compile-time trust ceiling and request-time minimum trust enforcement.
- [x] runtime limits/hop/cycle enforcement.
- [x] business-budget precheck + emergency safety-cap interface.
- [x] minimized audit/trace event with canonical JSON Schema + aligned Pydantic model.

### 1C. Adapter contracts

- [x] provider-neutral Model Router with deterministic primary + compatible stub adapter, Core-owned profile routing, bounded fallback and Runtime Governance checks.
- [x] in-process Capability Registry resolver with authoritative records, bounded overrides and soft/strict behavior.
- [x] Tool Gateway with trusted binding resolution, Runtime Governance checks, schema validation, audit and deterministic read-only synthetic tool.
- [x] Memory Gateway with ephemeral `session` and `task_working` memory, trusted scope isolation and governed reads/writes.
- [x] Hybrid Orchestrator executes one Agent-prepared bounded capability/model/tool/memory plan, preserves per-step gateway checks, enforces max-step/repeat/deadline boundaries and fails closed on denial.

### 1D. Eval/release kernel

- [x] canonical decision-neutral EvalResult for functional/business, security/policy, cost/runtime and contract/portability families.
- [x] typed PlatformPolicy eval mapping to blocking/warning/advisory with fail-closed handling and non-downgradeable security invariants.
- [x] requested `human-required` / `policy-auto` / `policy` strategy compiled to a concrete effective strategy.
- [x] HumanApprovalRecord, ReleaseDecisionRecord and EvidencePack contracts with exact release/policy/exception binding.
- [x] canonical SHA-256 EffectiveReleaseConfig fingerprint and drift verification against approved spec/evidence and runtime ExecutionContext authority.

**Phase 1D status:** complete for the thin skeleton.

## Phase 1E - Synthetic end-to-end gate

- [x] checked-in tiny synthetic reference Agent Definition uses only the accepted minimal AgentManifest fields;
- [x] compiler path supports AgentManifest + ClientInstanceConfig + typed Policy/Exception + Registry resolution -> EffectiveReleaseConfig;
- [x] synthetic Agent executes through trusted ExecutionContext + Runtime Governance + bounded Hybrid Orchestrator;
- [x] capability, provider-neutral model, read-only tool and task-memory steps execute in one governed flow;
- [x] all four EvalResult families are generated and mapped through PlatformPolicy;
- [x] policy-auto ReleaseDecisionRecord and EvidencePack are created from the same exact release;
- [x] C5.5 drift verification reconstructs a managed release and minimized audit/evidence chain;
- [x] blocking security invariant failure is proven fail-closed even under `policy-auto`.

**Exit gate: PASSED.** One complete thin path can be compiled, executed, evaluated, released and reconstructed without provider or business-domain lock-in. C6 is the executable proof that the first Core Skeleton works as a system rather than only as isolated contracts.

## Phase 2 - Research/Brain Agent v1 - first real reference Agent

Separate repository exposing `research.lookup`.

- [x] authoritative `research.lookup@1` Capability Registry contract is defined in Core with canonical Registry/Input/Output schemas, explicit read-only risk/cost/data scope and bounded override surface;
- [x] Research/Brain Agent exists in `yuliabk/agent-factory-research-agent`, is contract-locked to Core, passes its own CI, and is registered in Core by exact sandbox release commit;
- [x] smallest useful real source set is implemented: internal evidence plus English Wikipedia through the official MediaWiki REST API, without changing `research.lookup@1`;
- [x] source path uses bounded result count, explicit User-Agent, timeout, deterministic normalization and graceful failure handling;
- [x] live CI smoke test proves the Wikipedia path makes a real network call and returns contract-compatible evidence;
- [x] freshness honesty is enforced: Wikipedia supports background (`any`) only and is not presented as `recent/current` evidence;
- [x] return `research.lookup@1` structured answer/findings/evidence/limitations output;
- [x] degrade gracefully if the external source is unavailable;
- [ ] pass provider-side external network/tool access through Core Runtime Governance before any production registration;
- [ ] route model usage through Core policy if/when a real model adapter is added;
- [ ] add broader recent/current sources only after the first consumer integration proves the need;

**C7.3 status:** complete for the sandbox real-source slice. Research Agent release `4a8b308aeaf22228c6a03d438509b0717e6daf8b` contains the first real source and remains sandbox-only in the Core Registry.

## Phase 3 - Travel Agent as first external consumer

- [x] Travel Agent external commit `9da84b635d1ea3b1d62f4b4e8652acd22e42ead6` contains a provider-neutral `research.lookup@1` consumer slice and green Contract v1 CI;
- [x] locked Travel manifest resolves through Core Capability Registry in sandbox to the exact Research Agent release;
- [x] Travel EffectiveReleaseConfig/ExecutionContext contain only `research.lookup`; provider-internal `web.search` and direct tool bindings do not leak;
- [x] Travel maps research output into separate non-commercial background evidence and keeps commercial SerpAPI evidence distinct;
- [x] Travel background-research requests are PII-minimized and do not contain caller-selected provider/model/tool IDs;
- [x] consumer capability failure degrades safely without failing the draft workflow;
- [ ] execute one real Travel -> Core -> Research sandbox request through a governed remote capability transport;
- [ ] verify real structured evidence/limitations from the registered Research release reach the Travel workflow unchanged;
- [ ] run consumer-side quality/security/cost/contract evals on the real remote path;
- [ ] test remote provider/capability unavailable fallback with trace/budget/deadline/audit preservation;
- [ ] prove no Travel-specific routing/business logic is needed in Core remote transport;
- [ ] keep production disabled until Research provider-side network/tool governance is routed through Core.

**C7.4a status:** complete. Travel is now the first external sandbox consumer at the contract, workflow and authority-compile layers. The remaining C7.4b gate is actual governed cross-repository invocation.

## Phase 4 - Spec Compiler + Template Factory UX

- [ ] `ClientIntent` schema.
- [ ] conversational intake.
- [ ] `infer -> assumptions -> confirm/correct` flow.
- [ ] under-10-minute UX target, typically 5-6 critical questions.
- [ ] modular template recommendation/composition.
- [ ] economy/balanced/premium business options.
- [ ] generated AgentManifest + ClientInstanceConfig.
- [ ] plain-language scope/cost/data/approval summary.

## Phase 5 - Tool, Memory and Runtime depth

- [ ] persistent memory policies/backends;
- [ ] production Tool Gateway adapters;
- [ ] richer Capability Registry health/version resolution;
- [ ] exception-management workflow;
- [ ] policy/trust profile library;
- [ ] improved observability and anomaly detection.

## Phase 6 - Multi-client hardening

- [ ] security attack corpus;
- [ ] cross-tenant negative tests;
- [ ] prompt-injection and exfiltration evals;
- [ ] budget anomaly/loop tests;
- [ ] provider outage/fallback tests;
- [ ] backup/recovery/deletion evidence;
- [ ] incident/runbook flows;
- [ ] finalize non-overridable production invariants.

## Current stop point

**Phase 1 Core Skeleton, C7.1-C7.3 and C7.4a are complete for sandbox.** Research has a real governed-by-contract source path; Travel now consumes the public capability contract through a provider-neutral adapter, and Core proves the external Travel release receives only `research.lookup` authority while resolving to the exact registered Research release.

**Next executable step:** C7.4b - define the thinnest governed remote capability transport that carries the trusted caller context across a real Travel -> Core -> Research sandbox call. The transport must preserve request/trace IDs, deadline, hop/cycle limits, budget state, delegated authority and audit, and it must not expose Research URLs or provider-internal permissions to Travel business code. This is the next material architecture decision before implementation.

Keep contracts stable, implementations replaceable and decisions just-in-time.
