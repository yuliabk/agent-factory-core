# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** Phase 1 Core Skeleton thin vertical slice is complete end-to-end through the C6 synthetic gate; the next executable step is C7 / Research-Brain Agent as the first real external reference consumer.

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
- Research/Brain Agent becomes the first real reference consumer as soon as the Core slice is usable.

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

- [ ] define and approve the authoritative `research.lookup` Capability Registry contract;
- [ ] create the Research/Brain Agent in a separate repository with a lightweight capability reference rather than Core business logic;
- [ ] inspect request/context and decide whether available/internal knowledge is sufficient;
- [ ] choose internal knowledge, Web search, API, MCP, model knowledge or approved capability according to policy;
- [ ] return structured evidence/provenance;
- [ ] route model usage through Core policy rather than provider hard-code;
- [ ] respect data, trust, budget and tool permissions;
- [ ] degrade gracefully if optional sources are unavailable;
- [ ] run the first external-Agent integration/eval/release path through Core.

## Phase 3 - Travel Agent as first external consumer

- [ ] consume `research.lookup` through Capability Registry;
- [ ] remove avoidable direct search/provider dependency;
- [ ] run end-to-end quality/security/cost eval;
- [ ] test provider/capability fallback;
- [ ] prove no Travel-specific logic was needed in Core.

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

**Phase 1 Core Skeleton is complete end-to-end.** A checked-in synthetic Agent definition validates against canonical contracts, compiles to immutable EffectiveReleaseConfig, derives trusted ExecutionContext, executes capability/model/tool/memory through bounded governance, emits minimized audit evidence, passes all four eval families, creates release/evidence artifacts and verifies exact provenance/drift. A blocking security invariant also fails closed under policy-auto.

**Next executable step:** C7 / Phase 2 - define the authoritative `research.lookup` Registry contract and create the Research/Brain Agent in a separate repository as the first real external consumer of Core. Do not deepen production providers, persistent memory or domain-specific Core logic before this reference integration proves which depth is actually needed.

Keep contracts stable, implementations replaceable and decisions just-in-time.
