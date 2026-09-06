# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** Architecture synchronized; preparing the first executable Core vertical slice.

## North Star

Build a platform where a non-technical client describes a business need in minutes and receives a governed Agent, while Core handles Spec, Templates, Security, Providers, Tools, Memory, Budget, Evals, Release and Audit behind the scenes.

The specification and its history remain the primary artifact. Deployments are reproducible outputs.

## Delivery strategy - move fast without building a fragile monolith

We will not implement every subsystem to full maturity one after another. We will build a **thin vertical slice** that proves all critical contracts end-to-end, then deepen only the modules proven necessary.

Principles:

- one architectural decision -> synchronize all affected docs/specs immediately;
- Owner spends time on material decisions, not repetitive editing;
- defaults/profiles reduce manual approvals/configuration;
- progressive complexity;
- thin interfaces before sophisticated infrastructure;
- Research/Brain Agent becomes the first real reference consumer as soon as the Core slice is usable.

## Phase 0A - Historical baseline

Existing assets include OpenSpec workflow, client isolation concepts, release manifests, security/prototype work and earlier Dify/n8n/runtime exploration.

**Status:** Historical baseline preserved; newer accepted contracts take precedence.

## Phase 0B - Core architecture/contracts synchronization

**Status:** Substantially complete after Owner brainstorming on 2026-09-06.

### Accepted/synchronized decisions

- [x] Platform Vision accepted.
- [x] Core split logically into Build / Control Plane and Runtime Governance Plane.
- [x] One Core, separate Agent repositories.
- [x] Spec/history is the primary artifact.
- [x] `AgentManifest + ClientInstanceConfig + PlatformPolicy/ExceptionPolicy -> EffectiveReleaseConfig`.
- [x] Configurable release strategy: `human-required | policy-auto | policy`.
- [x] Security is platform-level but approvals are risk-based.
- [x] Trust Profiles: sandbox/internal/business/privileged direction.
- [x] Controlled ExceptionPolicy for overridable rules.
- [x] Memory is separated by class; Agents may request/write persistent memory within policy.
- [x] Capability Registry uses soft-strict dev/production modes.
- [x] Provider/model selection is policy-driven across cost/quality/privacy/latency/availability.
- [x] Template is a starting point plus modular composition.
- [x] Eval thresholds/release eligibility are policy-driven; invariant security failures remain blocking.
- [x] Hybrid orchestration: Core sets boundaries, Agents plan autonomously inside them.
- [x] Research/Brain Agent remains a separate reusable Agent providing `research.lookup`.

### Remaining architecture decisions that do NOT block starting the Core Skeleton

- exact schema implementation technology: JSON Schema vs Pydantic combination;
- first physical Registry backend;
- first two provider adapters;
- pricing data source/currency normalization;
- concrete default emergency safety-cap numbers;
- final production list of non-overridable invariants;
- exact persistent-memory backend;
- client-facing UI repository/deployment location.

These should be resolved just-in-time when their implementation task begins.

## Phase 1 - Core Skeleton Vertical Slice

**Goal:** get a small working Core as quickly as possible without pretending the entire platform exists.

### 1A. Contract schemas and compiler

- [ ] `AgentManifest` schema.
- [ ] `ClientInstanceConfig` schema.
- [ ] `PlatformPolicy` minimal schema.
- [ ] `ExceptionPolicy` minimal schema.
- [ ] compiler -> immutable `EffectiveReleaseConfig`.
- [ ] validation errors that clearly state where/how to fix configuration.

### 1B. Runtime Governance kernel

- [ ] trusted `ExecutionContext`.
- [ ] trust/risk + permission evaluation.
- [ ] runtime limits/hop limits.
- [ ] business-budget precheck + emergency safety cap interface.
- [ ] minimal audit/trace event.

### 1C. Adapter contracts

- [ ] provider-neutral model interface with one working adapter and one stub/second adapter for portability.
- [ ] Capability Registry in-process implementation with soft-strict mode.
- [ ] Tool Gateway interface and one read-only example capability.
- [ ] Memory Gateway interface with session/task memory first.

### 1D. Eval/release kernel

- [ ] functional/security/cost eval result schema.
- [ ] policy mapping: blocking/warning/advisory.
- [ ] `human-required`, `policy-auto`, `policy` release decision logic.
- [ ] Evidence Pack + release decision reference.

**Exit gate:** one synthetic reference Agent can be compiled, executed and released through the complete thin path.

## Phase 2 - Research/Brain Agent v1 - first real reference Agent

Separate repository.

### Capability

`research.lookup`

### Minimum v1 responsibilities

- [ ] inspect request/context and decide whether available/internal knowledge is sufficient;
- [ ] choose among internal knowledge, Web search, API, MCP, model knowledge or approved capability according to policy;
- [ ] return structured evidence/provenance;
- [ ] route model usage through Core policy rather than provider hard-code;
- [ ] respect data, trust, budget and tool permissions;
- [ ] degrade gracefully if optional sources are unavailable.

**Speed rule:** start with the smallest useful source set. Add providers/MCP only after the contract works.

## Phase 3 - Travel Agent as first external consumer

- [ ] consume `research.lookup` through Capability Registry;
- [ ] remove avoidable direct search/provider dependency;
- [ ] run end-to-end quality/security/cost eval;
- [ ] test provider/capability fallback;
- [ ] prove no Travel-specific logic was needed in Core.

**Goal:** demonstrate real reuse.

## Phase 4 - Spec Compiler + Template Factory UX

Build the client-facing creation path only after the vertical Core contracts are proven.

- [ ] `ClientIntent` schema.
- [ ] conversational intake.
- [ ] `infer -> assumptions -> confirm/correct` flow.
- [ ] under-10-minute UX target, typically 5-6 critical questions.
- [ ] modular template recommendation/composition.
- [ ] economy/balanced/premium business options.
- [ ] generated AgentManifest + ClientInstanceConfig.
- [ ] plain-language scope/cost/data/approval summary.

## Phase 5 - Tool, Memory and Runtime depth

Deepen only proven needs:

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

Architecture synchronization is being completed in the repository now.

**Next executable step:** design and implement Phase 1A/1B as the smallest Core Skeleton, then attach enough adapter/eval functionality to run one synthetic end-to-end vertical slice.

Do not wait for every long-term infrastructure choice before starting. Keep contracts stable, implementations replaceable and decisions just-in-time.