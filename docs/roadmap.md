# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** Phase 1 Core Skeleton and the first real Research/Travel sandbox path are complete end-to-end. A second real external capability, `travel.flight.search@1`, now has a canonical provider-neutral contract, a separate working sandbox provider repository, exact Core Registry binding, and a merged Travel consumer. Production remains disabled. The next executable gate is one real cross-repository `Travel -> Core -> Flight Provider` invocation using the exact merged releases, followed by Eval/Release/Evidence reconstruction on the real commercial-evidence path.

## North Star

Build a platform where a non-technical client describes a business need in minutes and receives a governed Agent, while Core handles Spec, Templates, Security, Providers, Tools, Memory, Budget, Evals, Release and Audit behind the scenes.

The specification and its history remain the primary artifact. Deployments are reproducible outputs.

## Delivery strategy - move fast without building a fragile monolith

We build a thin vertical slice that proves critical contracts end-to-end, then deepen only modules proven necessary.

Principles:

- one architectural decision -> synchronize affected docs/specs immediately;
- Owner spends time on material authority/contract decisions, not repetitive editing;
- defaults/profiles reduce manual approvals/configuration;
- progressive complexity;
- thin interfaces before sophisticated infrastructure;
- do not add schema fields before a real use case needs them;
- external contracts stay implementation-neutral even when the first runtime is Python;
- Capability Registry owns capability contracts/metadata; manifests carry lightweight refs;
- ClientInstanceConfig contains client/environment deployment values only, never reusable business logic;
- Runtime executes only compiled EffectiveReleaseConfig;
- ExecutionContext is derived from EffectiveReleaseConfig rather than prompts or drafts;
- release evidence is bound to the exact EffectiveReleaseConfig fingerprint and approved specification;
- external capability consumers receive only consumer authority, never provider-internal tool/provider permissions;
- remote capability invocation preserves Core authority/trace/budget/deadline/audit boundaries;
- endpoint URLs and credentials are runtime configuration, not consumer business logic;
- commercial live evidence and background research remain separate evidence classes;
- scraper-derived commercial evidence must not be represented as booking-ready or provider-verified;
- production registration remains blocked until provider-side outbound network access is governed.

## Phase 0A - Historical baseline

Existing assets include OpenSpec workflow, client isolation concepts, release manifests, security/prototype work and earlier Dify/n8n/runtime exploration.

**Status:** Historical baseline preserved; newer accepted contracts take precedence.

## Phase 0B - Core architecture/contracts synchronization

**Status:** Complete after Owner review and repository-wide architecture synchronization on 2026-09-06.

## Phase 1 - Core Skeleton Vertical Slice

**Goal:** prove the smallest complete Core path without pretending the entire platform exists.

### 1A. Contract schemas and compiler

- [x] Minimal AgentManifest contract shape accepted.
- [x] JSON Schema is canonical externally; Pydantic is the internal Python projection.
- [x] Registry-backed capability references and bounded overrides.
- [x] ClientInstanceConfig, PlatformPolicy, ExceptionPolicy and immutable EffectiveReleaseConfig.
- [x] Compiler path: AgentManifest + ClientInstanceConfig + Policy/Exception + Registry -> EffectiveReleaseConfig.
- [x] Trusted ExecutionContext builder from EffectiveReleaseConfig.
- [x] Compiler errors expose path/rule/remediation for enforced rules.

### 1B. Runtime Governance kernel

- [x] permission/tenant/data-classification/deadline/trust checks;
- [x] runtime hop/cycle limits;
- [x] budget precheck + independent emergency safety cap;
- [x] minimized runtime audit/trace contract.

### 1C. Adapter contracts

- [x] provider-neutral Model Router;
- [x] Capability Registry resolver;
- [x] Tool Gateway;
- [x] ephemeral governed Memory Gateway;
- [x] bounded Hybrid Orchestrator.

### 1D. Eval/release kernel

- [x] four decision-neutral EvalResult families;
- [x] PlatformPolicy maps evals to blocking/warning/advisory;
- [x] human-required / policy-auto / policy release strategy;
- [x] HumanApprovalRecord, ReleaseDecisionRecord and EvidencePack;
- [x] canonical EffectiveReleaseConfig fingerprint + drift verification.

### 1E. Synthetic end-to-end gate

- [x] synthetic reference Agent compiles;
- [x] executes capability/model/tool/memory through Runtime Governance;
- [x] emits all four eval families;
- [x] produces policy-auto release decision and EvidencePack;
- [x] proves audit/fingerprint/drift chain;
- [x] blocking security invariant remains fail-closed.

**Exit gate: PASSED.** The first Core Skeleton works as a complete governed system.

## Phase 2 - Research/Brain Agent v1 - first real reference Agent

Separate repository: `yuliabk/agent-factory-research-agent`.

- [x] canonical `research.lookup@1` Registry/Input/Output contracts;
- [x] provider-neutral public payload and structured evidence/provenance output;
- [x] Research Agent exists in a separate repository and is contract-locked to Core;
- [x] internal evidence + real Wikipedia background source;
- [x] freshness honesty: Wikipedia supports background (`any`) only;
- [x] bounded live CI source test;
- [x] Research HTTP capability endpoint validates bearer auth, scope, classification, deadline, hop and release binding;
- [x] Core Registry binds exact sandbox Research release `024367572ca001dec385ca0f781495b5fa91d181` through `endpointRef=research-agent-sandbox`;
- [x] production resolution remains disabled;
- [ ] pass provider-side outbound Wikipedia/network access through Core-governed network/tool policy before production;
- [ ] add model routing only if a real Research use case needs it;
- [ ] add broader recent/current sources only after evaluation proves the need.

**Phase 2 sandbox status:** complete as a real external reference capability provider.

## Phase 3 - Travel Agent as first external consumer

Repository: `yuliabk/travel-agent-bot`.

### 3A. Research consumer path

- [x] Travel commit `9da84b635d1ea3b1d62f4b4e8652acd22e42ead6` introduced provider-neutral `research.lookup@1` consumption;
- [x] PII-minimized background-research requests;
- [x] research output remains separate non-commercial PLACE/TRANSPORT evidence;
- [x] Travel authority contains `research.lookup`, never provider-internal `web.search`;
- [x] one real Travel -> Core -> Research -> Wikipedia sandbox call runs in cross-repository CI;
- [x] Core preserves request/trace/deadline/hop/audit boundaries;
- [x] no Travel-specific routing/business logic is required in Core transport.

**Research consumer status:** end-to-end sandbox invocation proven.

### 3B. Governed commercial flight evidence sandbox

Canonical capability: `travel.flight.search@1`.

- [x] provider-neutral input/output contract merged to Core at `8abfbaeb724cda38bc26d647b320cc93863a750c`;
- [x] public input contains route, dates, passengers, cabin, currency and bounded search controls only;
- [x] callers cannot select Google, SerpApi, a scraper, adapter, API key or implementation ID;
- [x] output explicitly separates observed commercial evidence from booking claims with `bookingReady=false` and `evidenceStatus=observed`;
- [x] separate provider repository created: `yuliabk/agent-factory-flight-provider`;
- [x] initial `fast-flights==3.1.0` candidate rejected by the live gate because its current parser raises `IndexError` on Google's response shape; no private parser patch or bypass was adopted;
- [x] implementation switched to `faster-flights==3.8.0`, locked to upstream release commit `10b99740b15bd6e0d77b0ae6cd26f2e1f2cc2c84`;
- [x] Flight Provider release `d2f4e18d5e8f5911a4365a48da80617b4304e77a` passed deterministic contract/security tests and a live TLV->ATH source gate in run `34043947098`;
- [x] provider endpoint is sandbox-only, bearer-authenticated and validates capability/scope/classification/deadline/hop/release boundaries;
- [x] Core Registry on `main` commit `1aff3bf5e3300202dd46aa24e878d52fbdaba2b7` binds `travel.flight.search@1` to that exact provider release via `endpointRef=flight-provider-sandbox`;
- [x] Core production resolution still fails closed because no production implementation is registered;
- [x] Core `main` Contract Tests run `34044527079` passed after provider registration;
- [x] Travel PR #19 merged as release `5314ea8be564cac563a6a53eebf7c12247101688`;
- [x] current Travel sandbox manifest requests `travel.flight.search` plus optional `research.lookup`, and does not request `web.search` or a provider-specific permission;
- [x] `FlightSearchConsumerV1` sends a PII-minimized request and maps results to `EvidenceType.FLIGHT` with UNVERIFIED/observed semantics;
- [x] governed flight evidence can replace legacy flight evidence without replacing hotel evidence;
- [x] SerpApi remains legacy/fallback code but is not required by the new sandbox flight path;
- [x] Travel `main` Contract v1 CI run `34044510496` passed after the flight consumer merge;
- [ ] execute one real cross-repository Travel -> Core -> Flight Provider -> live flight source request using the exact merged releases;
- [ ] assert Core audit/correlation preserves Travel request/trace and exact Flight Provider implementation target;
- [ ] prove Travel runtime authority remains only `travel.flight.search` / `research.lookup`, with no provider internals;
- [ ] test provider unavailable/parser failure as a full remote scenario while preserving trace/deadline/budget/audit evidence;
- [ ] run functional/security/cost-runtime/contract-portability EvalResults on the real flight path;
- [ ] produce ReleaseDecisionRecord + EvidencePack + fingerprint/drift verification for the real commercial-evidence path;
- [ ] keep all flight results non-booking-ready until an official provider contract explicitly proves booking/availability semantics;
- [ ] keep production disabled until outbound network access of the Flight Provider is Core-governed.

**Phase 3B status:** contract, independent provider, live source gate, Core Registry binding and Travel consumer are all merged and green. The missing proof is the complete three-repository runtime invocation.

## Phase 3C - Hotels after the flight pattern is proven

- [ ] define provider-neutral `travel.hotel.search@1` contract;
- [ ] keep hotel evidence separate from flight evidence and background research;
- [ ] choose a sandbox provider only after contract semantics are fixed;
- [ ] prove independent provider CI and live source gate;
- [ ] register exact provider release in Core;
- [ ] consume through Travel via generic CapabilityInvoker;
- [ ] run the same remote Eval/Release/Evidence gate used for flights.

**Rule:** do not combine hotel and flight provider contracts merely because one source can return both.

## Phase 4 - Real remote Eval / Release / Evidence gate

Apply the existing Core release machinery to real external capability paths rather than only synthetic paths.

- [ ] functional/business EvalResult for real Research and Flight flows;
- [ ] security/policy EvalResult including authority isolation and fail-closed remote failures;
- [ ] cost/runtime EvalResult including bounded network/hop/deadline behavior;
- [ ] contract/portability EvalResult proving provider replacement does not require Travel business-code rewrite;
- [ ] policy mapping -> ReleaseDecisionRecord;
- [ ] EvidencePack with exact Travel/Core/provider release refs;
- [ ] canonical EffectiveReleaseConfig fingerprint and drift verification against the executed remote path;
- [ ] negative gate: blocking remote-security eval prevents release even if strategy is policy-auto.

## Phase 5 - Spec Compiler + Template Factory UX

- [ ] ClientIntent schema;
- [ ] conversational intake;
- [ ] `infer -> assumptions -> confirm/correct` flow;
- [ ] under-10-minute UX target, typically 5-6 critical questions;
- [ ] modular template recommendation/composition;
- [ ] economy/balanced/premium business options;
- [ ] generated AgentManifest + ClientInstanceConfig;
- [ ] plain-language scope/cost/data/approval summary.

## Phase 6 - Tool, Memory and Runtime depth

- [ ] Core-governed outbound network/egress adapter for external providers;
- [ ] persistent memory policies/backends;
- [ ] production Tool Gateway adapters;
- [ ] richer Capability Registry health/version resolution;
- [ ] exception-management workflow;
- [ ] policy/trust profile library;
- [ ] improved observability and anomaly detection.

## Phase 7 - Multi-client hardening

- [ ] security attack corpus;
- [ ] cross-tenant negative tests;
- [ ] prompt-injection and exfiltration evals;
- [ ] budget anomaly/loop tests;
- [ ] provider outage/fallback tests;
- [ ] backup/recovery/deletion evidence;
- [ ] incident/runbook flows;
- [ ] finalize non-overridable production invariants.

## Current stop point

**Research path:** complete end-to-end in sandbox. Travel -> Core -> Research -> Wikipedia is a real governed remote path.

**Flight path:** the public contract, separate Flight Provider, live source test, exact Core Registry registration and Travel consumer are all merged and green. The exact current releases are:

- Core: `1aff3bf5e3300202dd46aa24e878d52fbdaba2b7`
- Travel Agent: `5314ea8be564cac563a6a53eebf7c12247101688`
- Flight Provider: `d2f4e18d5e8f5911a4365a48da80617b4304e77a`

**Next executable step:** create a cross-repository Flight integration gate that checks out those exact releases, starts the real Flight Provider HTTP service with an ephemeral bearer token, compiles the current Travel manifest through Core, invokes `FlightSearchConsumerV1` through `GovernedCapabilityInvoker`, performs a real flight search, and asserts normalized observed FLIGHT evidence plus Core trace/audit/correlation and authority isolation.

**Immediately after that:** run the existing Eval/Release/Evidence machinery over the real Research + Flight remote paths, then define `travel.hotel.search@1` using the same proven pattern.

**Production remains intentionally disabled** until Research and Flight provider outbound network access is routed through Core-governed network/egress policy and production-specific safety/eval gates pass.

Keep contracts stable, implementations replaceable and decisions just-in-time.
