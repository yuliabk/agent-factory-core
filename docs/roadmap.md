# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** Phase 1B Runtime Governance and Phase 1C adapter/orchestration vertical slice are complete; Phase 1D Eval/Release kernel starts with C5.1 EvalResult.

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
- [x] Compiler now consumes typed PlatformPolicy/ExceptionPolicy rather than a temporary dictionary boundary.
- [x] Compiler validates scoped exceptions against explicit PlatformPolicy exception allowances.
- [x] In-process Capability Registry resolves required capability refs and rejects protected/invalid overrides.
- [x] EffectiveReleaseConfig records resolved capability bindings and applied policy/exception versions.
- [x] Trusted `ExecutionContext` JSON Schema + Pydantic builder from EffectiveReleaseConfig.
- [x] Compiler errors expose path/rule/remediation for the current enforced rules.

**Contract rule:** JSON Schema is externally authoritative. Pydantic is an internal implementation projection and must remain aligned.

**Runtime rule:** `AgentManifest + ClientInstanceConfig + PlatformPolicy/valid ExceptionPolicy + Registry resolution -> EffectiveReleaseConfig -> ExecutionContext`.

### 1B. Runtime Governance kernel

- [x] first trusted `ExecutionContext` contract and builder.
- [x] trust/risk + request-time permission evaluation, including compile-time trust ceiling and request-time minimum trust enforcement.
- [x] runtime limits/hop/cycle enforcement.
- [x] business-budget precheck + emergency safety-cap interface.
- [x] minimal audit/trace event with canonical JSON Schema + aligned Pydantic model.

### 1C. Adapter contracts

- [x] provider-neutral Model Router with deterministic primary + compatible stub adapter, Core-owned profile routing, bounded fallback and Runtime Governance checks. Costed adapters remain blocked until budget accounting is connected.
- [x] first in-process Capability Registry resolver with authoritative records, bounded overrides and soft/strict behavior.
- [x] Tool Gateway interface with trusted binding resolution, Runtime Governance checks, schema validation, audit and one deterministic read-only synthetic tool. Costed/write-capable tools remain blocked in this first slice.
- [x] Memory Gateway interface with ephemeral `session` and `task_working` memory. Session scope is trusted request ID; task scope is trusted trace ID; tenant/release namespace isolation, permission/trust/classification/purpose/retention checks and minimized audit are enforced. Persistent memory remains later depth.
- [x] Hybrid Orchestrator executes one Agent-prepared bounded capability/model/tool/memory plan, preserves per-step gateway checks, enforces max-step/repeat/deadline boundaries and fails closed on the first denial.

### 1D. Eval/release kernel

- [ ] functional/security/cost/contract EvalResult schema.
- [ ] policy mapping: blocking/warning/advisory.
- [ ] `human-required`, `policy-auto`, `policy` release decision logic.
- [ ] Evidence Pack + release decision reference.

**Exit gate:** one synthetic reference Agent can be compiled, executed and released through the complete thin path.

## Phase 2 - Research/Brain Agent v1 - first real reference Agent

Separate repository exposing `research.lookup`.

- [ ] inspect request/context and decide whether available/internal knowledge is sufficient;
- [ ] choose internal knowledge, Web search, API, MCP, model knowledge or approved capability according to policy;
- [ ] return structured evidence/provenance;
- [ ] route model usage through Core policy rather than provider hard-code;
- [ ] respect data, trust, budget and tool permissions;
- [ ] degrade gracefully if optional sources are unavailable.

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

**Phase 1B and Phase 1C are complete for the thin skeleton.** A trusted ExecutionContext now governs compiled capability dispatch, provider-neutral model routing, read-only tools and ephemeral session/task memory through one bounded Hybrid Orchestrator. The Orchestrator receives an Agent-prepared plan and does not contain business planning logic.

**Next executable step:** Phase 1D C5.1 - define the canonical EvalResult JSON Schema + aligned Pydantic model for functional/business, security/policy, cost/runtime and contract/portability families. After that, map results to blocking/warning/advisory policy before implementing release decisions.

Keep contracts stable, implementations replaceable and decisions just-in-time.
