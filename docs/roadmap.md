# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** Phase 1 Core Skeleton and C7.1-C7.4 are complete for the sandbox vertical slice. Travel now invokes the external Research Agent through a Core-owned governed HTTP JSON capability transport and receives real Wikipedia-backed background evidence. Production remains disabled. The next executable step is the real consumer eval/release/evidence gate plus provider-side outbound-network governance before any production registration.

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
- remote Agent-to-Agent invocation preserves Core authority/trace/budget/deadline/audit boundaries; endpoint URLs and credentials are runtime configuration rather than consumer business logic;
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
- [x] Research/Brain Agent exists in `yuliabk/agent-factory-research-agent`, is contract-locked to Core and passes its own CI;
- [x] smallest useful real source set is implemented: internal evidence plus English Wikipedia through the official MediaWiki REST API, without changing `research.lookup@1`;
- [x] source path uses bounded result count, explicit User-Agent, timeout, deterministic normalization and graceful failure handling;
- [x] live CI smoke test proves the Wikipedia path makes a real network call and returns contract-compatible evidence;
- [x] freshness honesty is enforced: Wikipedia supports background (`any`) only and is not presented as `recent/current` evidence;
- [x] Research release `024367572ca001dec385ca0f781495b5fa91d181` exposes the canonical sandbox HTTP capability endpoint and independently validates bearer auth, capability/scope/classification/deadline/hop/release boundaries;
- [x] Core Registry binds `research.lookup@1` to the exact HTTP-capable Research release through `endpointRef=research-agent-sandbox` rather than a committed URL/credential;
- [x] return `research.lookup@1` structured answer/findings/evidence/limitations output;
- [x] degrade gracefully if the external source is unavailable;
- [ ] pass provider-side outbound Wikipedia/network access through Core Runtime Governance / Tool Gateway before any production registration;
- [ ] route model usage through Core policy if/when a real model adapter is added;
- [ ] add broader recent/current sources only after the first consumer eval proves the need.

**Phase 2 sandbox status:** functional external capability provider and HTTP transport endpoint are proven. Production remains intentionally disabled.

## Phase 3 - Travel Agent as first external consumer

- [x] Travel Agent external commit `9da84b635d1ea3b1d62f4b4e8652acd22e42ead6` contains a provider-neutral `research.lookup@1` consumer slice and green Contract v1 CI;
- [x] locked Travel manifest resolves through Core Capability Registry in sandbox to the exact Research Agent HTTP release;
- [x] Travel EffectiveReleaseConfig/ExecutionContext contain only `research.lookup`; provider-internal `web.search` and direct tool bindings do not leak;
- [x] Travel maps research output into separate non-commercial background evidence and keeps commercial SerpAPI evidence distinct;
- [x] Travel background-research requests are PII-minimized and do not contain caller-selected provider/model/tool IDs;
- [x] consumer capability failure degrades safely without failing the draft workflow;
- [x] governed HTTP JSON transport v1 carries trusted request/trace, caller release, tenant/environment, data classification, delegated permission, deadline, hop budget and budget context from Core to Research;
- [x] one real Travel -> Core -> Research -> Wikipedia sandbox call is executed in cross-repository CI using exact locked commits and an ephemeral runtime bearer token;
- [x] real Wikipedia-backed structured evidence reaches the Travel consumer and is mapped to non-commercial `PLACE` evidence;
- [x] Core audit for the real invocation preserves Travel request/trace IDs and exact Research implementation target;
- [x] no Travel-specific routing/business logic is required in Core transport; Travel sees only the generic capability invoker;
- [ ] run consumer-side functional/security/cost/contract EvalResults and release/evidence reconstruction on the real remote path;
- [ ] test remote provider/capability unavailable fallback as a cross-repository scenario while preserving trace/budget/deadline/audit evidence;
- [ ] keep production disabled until Research provider-side outbound network/tool governance is routed through Core.

**C7.4 status:** complete for the real sandbox consumer/provider transport path. Integration run `34041728655` proves the real cross-repository call; Core contract run `34041728604` validates the same PR contracts.

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

**Phase 1 Core Skeleton and C7.1-C7.4 are complete for the sandbox vertical slice.** Travel business code invokes only `research.lookup`; Core resolves the exact Research release, builds the trusted delegated envelope, authenticates the HTTP hop from runtime endpoint configuration, validates the correlated response and audits the call; Research independently rejects invalid scope/deadline/hop/release requests and retrieves real Wikipedia evidence; Travel receives that evidence without gaining Research-internal permissions.

**Next executable step:** run the existing Core Eval/Release/Evidence machinery against this real remote consumer path, including functional, security, cost/runtime and contract/portability results. In parallel, before any production registration, move the Research Agent's outbound Wikipedia/network access behind Core-governed tool/network policy rather than allowing the provider implementation to own unrestricted outbound HTTP.

Keep contracts stable, implementations replaceable and decisions just-in-time.
