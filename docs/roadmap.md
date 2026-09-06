# Agent Factory Core - Roadmap

**Updated:** 2026-09-06  
**Current mode:** The Core Skeleton and the real Research path are complete in sandbox. `travel.flight.search@1` now has a canonical provider-neutral contract, a separate sandbox provider, Core Registry binding, a Travel consumer, deployed-runtime bridge logic, manual webform/shared-agent wiring, and proposal rendering for observed flight evidence. The remaining blocker is deployment activation: the latest Travel release has not yet been proven on the production alias `api.yb-designs.com`. Hotels are still legacy-SerpAPI dependent and therefore non-functional while that quota/path is exhausted.

## North Star

Build a platform where a non-technical client describes a business need and receives a governed Agent, while Core owns Spec, Templates, Security, Providers, Tools, Memory, Budget, Evals, Release and Audit.

The specification and release evidence are primary artifacts. Deployments are reproducible outputs.

## Architecture rules that remain fixed

- JSON Schema is the canonical external contract; Pydantic is an internal projection.
- Capability Registry owns capability contracts and implementation resolution.
- AgentManifest carries lightweight capability refs, never provider internals.
- ClientInstanceConfig contains client/environment values, never reusable business logic.
- Runtime executes only compiled EffectiveReleaseConfig and trusted ExecutionContext.
- Consumers receive consumer authority only; provider-internal permissions do not leak.
- Remote calls preserve tenant, request/trace, deadline, hop budget, classification, budget and audit boundaries.
- Endpoint URLs and credentials are runtime configuration, not business-Agent input.
- Research evidence and commercial live evidence remain separate.
- Scraper-derived commercial results are `observed`, never booking-ready or provider-verified.
- Green CI is not equivalent to a working customer deployment; deployment activation must be proven explicitly.
- Production registration remains blocked until provider outbound network/egress is governed.

## Phase 1 - Core Skeleton Vertical Slice

**Status: COMPLETE.**

- [x] AgentManifest / ClientInstanceConfig / PlatformPolicy / ExceptionPolicy / EffectiveReleaseConfig.
- [x] Registry resolution and bounded overrides.
- [x] trusted ExecutionContext.
- [x] runtime permission, tenant, trust, classification, deadline, hop/cycle and budget checks.
- [x] minimized audit/trace events.
- [x] provider-neutral Model Router, Capability Gateway, Tool Gateway, Memory Gateway and bounded Orchestrator.
- [x] four EvalResult families.
- [x] ReleaseDecisionRecord, HumanApprovalRecord and EvidencePack.
- [x] canonical EffectiveReleaseConfig fingerprint + drift verification.
- [x] synthetic end-to-end compile -> execute -> eval -> release -> reconstruct gate.

## Phase 2 - Research/Brain Agent v1

Repository: `yuliabk/agent-factory-research-agent`.

- [x] canonical `research.lookup@1` contract.
- [x] separate Research Agent repository and CI.
- [x] real Wikipedia background source with bounded results, timeout, normalization and freshness honesty.
- [x] sandbox HTTP capability endpoint with bearer auth and scope/classification/deadline/hop/release validation.
- [x] exact Research release: `024367572ca001dec385ca0f781495b5fa91d181`.
- [x] Core Registry resolves via `endpointRef=research-agent-sandbox`.
- [x] one real Travel -> Core -> Research -> Wikipedia cross-repository invocation.
- [ ] move Research outbound Wikipedia/network access behind Core-governed egress before production.
- [ ] add broader recent/current sources only after evaluation proves need.

**Research status:** end-to-end sandbox path proven.

## Phase 3 - Travel Agent external consumer

Repository: `yuliabk/travel-agent-bot`.

### 3A. Research consumer

- [x] provider-neutral `research.lookup@1` consumer.
- [x] PII-minimized research requests.
- [x] non-commercial PLACE/TRANSPORT evidence separation.
- [x] no `web.search` authority leakage.
- [x] real remote Research path proven in CI.

### 3B. Governed flight evidence

Canonical capability: `travel.flight.search@1`.

#### Contract and provider

- [x] Core contract merged at `8abfbaeb724cda38bc26d647b320cc93863a750c`.
- [x] public request is provider-neutral: route, dates, passengers, cabin, currency and bounded controls only.
- [x] output distinguishes `observed` from `provider-verified`; observed results require `bookingReady=false`.
- [x] separate provider repository: `yuliabk/agent-factory-flight-provider`.
- [x] initial `fast-flights==3.1.0` rejected after live parser failure.
- [x] accepted sandbox source uses `faster-flights==3.8.0`, upstream release commit `10b99740b15bd6e0d77b0ae6cd26f2e1f2cc2c84`.
- [x] Flight Provider exact release: `d2f4e18d5e8f5911a4365a48da80617b4304e77a`.
- [x] provider deterministic/security tests + live TLV->ATH source gate passed.
- [x] Core Registry binds the exact provider release in sandbox via `endpointRef=flight-provider-sandbox`.
- [x] Core registration commit: `1aff3bf5e3300202dd46aa24e878d52fbdaba2b7`.
- [x] production resolution remains fail-closed.

#### Travel consumer and runtime wiring

- [x] PR #19: `FlightSearchConsumerV1` added; request is PII-minimized and provider-neutral.
- [x] PR #20: `/v1/web/draft` and `/v1/evidence/search` wired to a sandbox flight runtime bridge so SerpAPI exhaustion no longer blocks flights on Contract v1 API paths.
- [x] PR #21: the actual shared-agent/manual `/api/webform` path was fixed; its legacy `search_flights_google()` name now acts only as a compatibility shim over canonical `travel.flight.search@1`, not SerpAPI.
- [x] all existing channels using the shared agent can therefore use the new flight source without changing their public channel contracts.
- [x] PDF wording no longer presents observed fares as guaranteed booking offers.
- [x] when hotel search is empty, output states that live hotel evidence is unavailable instead of fabricating hotel prices.
- [x] PR #22: observed flight evidence is surfaced in `proposal.flight_options` without trust escalation.
- [x] observed flight prices use observed fields/status and do not populate verified-price fields, booking-ready claims or aggregate verified totals.
- [x] unverified hotel prices remain suppressed.
- [x] current Travel `main`: `734d6ca442b2f16bb1f359795a197feb46105d04`.
- [x] current Travel Contract v1 CI run `34049530023`: SUCCESS.

#### Deployment state

- [x] Vercel project identified: `yb-travel-api` / `prj_mlijKLJl8W8a9n5l29NsgajSCILi`.
- [x] production alias remains `api.yb-designs.com`.
- [x] automatic GitHub deployment was not observed after the Travel merges; deployment activation must therefore be handled explicitly.
- [x] Vercel preview deployment `dpl_BB4HB4ZGBpWS6NwexRNREepXrxvf` reached READY.
- [ ] prove that the preview contains the current Travel release rather than merely a platform-side current-project snapshot.
- [ ] deploy/promote current Travel release `734d6ca442b2f16bb1f359795a197feb46105d04` to the production `yb-travel-api` project.
- [ ] verify `GET /v1/contract` on production reports governed flight search enabled.
- [ ] perform a real manual `/api/webform` request and confirm at least one observed flight is visible in the returned customer output/PDF without SerpAPI.
- [ ] inspect production logs for the same request and confirm no SerpAPI flight call is made.

**Flight status:** code, contracts, provider, CI, manual-channel wiring and rendering are green. The only immediate blocker to the user's manual retest is production deployment/promotion and production-path verification.

### 3C. Hotels

Current deployed hotel path still relies on legacy SerpAPI.

- [x] manual test confirmed no usable hotel results while SerpAPI quota/path is exhausted.
- [ ] define provider-neutral `travel.hotel.search@1`.
- [ ] define explicit hotel evidence semantics: per-night vs stay-total, taxes/fees, room occupancy, cancellation/refundability and booking-readiness.
- [ ] choose a sandbox provider only after the contract is fixed.
- [ ] create an independent provider implementation and live source gate.
- [ ] register exact implementation release in Core.
- [ ] consume through generic CapabilityInvoker / Travel adapter.
- [ ] activate and manually prove deployed hotel results.
- [ ] run the same Eval/Release/Evidence gate used for flights.

**Rule:** flight and hotel capabilities remain separate even if a future source can provide both.

## Phase 4 - Real remote Eval / Release / Evidence

After the customer-path flight deployment is proven:

- [ ] functional/business EvalResult for real Research + Flight paths.
- [ ] security/policy EvalResult for authority isolation and fail-closed remote failures.
- [ ] cost/runtime EvalResult for network, deadlines, hop/budget behavior.
- [ ] contract/portability EvalResult proving provider replacement does not require Travel business-code rewrite.
- [ ] policy mapping -> ReleaseDecisionRecord.
- [ ] EvidencePack with exact Core/Travel/provider release refs.
- [ ] EffectiveReleaseConfig fingerprint + drift verification against the executed path.
- [ ] negative gate proving a blocking security eval prevents policy-auto release.

## Phase 5 - Replace temporary sandbox bridge with final remote deployment

The in-Travel flight bridge is intentionally temporary for manual sandbox validation.

- [ ] deploy Flight Provider as its own sandbox HTTP service.
- [ ] configure Core runtime `flight-provider-sandbox` endpointRef to that service.
- [ ] remove the in-process Travel source adapter once the remote provider is proven.
- [ ] run exact-release `Travel -> Core -> Flight Provider -> source` three-repository CI.
- [ ] prove correlated audit/trace across the remote hop.
- [ ] test remote provider unavailable/parser-failure fallback.
- [ ] move Flight Provider outbound network access behind Core-governed egress before production.

## Phase 6 - Spec Compiler + Template Factory UX

- [ ] ClientIntent schema.
- [ ] conversational intake.
- [ ] `infer -> assumptions -> confirm/correct` flow.
- [ ] under-10-minute UX target.
- [ ] modular template composition.
- [ ] economy/balanced/premium options.
- [ ] generated AgentManifest + ClientInstanceConfig.
- [ ] plain-language scope/cost/data/approval summary.

## Phase 7 - Runtime depth and multi-client hardening

- [ ] Core-governed outbound network/egress adapter.
- [ ] persistent memory policies/backends.
- [ ] production Tool Gateway adapters.
- [ ] Registry health/version resolution.
- [ ] exception-management workflow.
- [ ] security attack corpus and prompt-injection/exfiltration evals.
- [ ] cross-tenant negative tests.
- [ ] provider outage/fallback and budget-loop tests.
- [ ] backup/recovery/deletion and incident evidence.
- [ ] finalize non-overridable production invariants.

## Current stop point

**Research:** complete end-to-end in sandbox.

**Flights:** current code path is complete through the shared/manual webform logic and proposal rendering. Exact current refs:

- Core: `1aff3bf5e3300202dd46aa24e878d52fbdaba2b7`
- Travel Agent: `734d6ca442b2f16bb1f359795a197feb46105d04`
- Flight Provider: `d2f4e18d5e8f5911a4365a48da80617b4304e77a`
- Research Agent: `024367572ca001dec385ca0f781495b5fa91d181`

**Immediate next executable step:** deploy/promote the current Travel release to `yb-travel-api` production, verify the production contract endpoint, then repeat the user's manual website test and confirm observed flight options appear without SerpAPI.

**Hotels:** still blocked because they remain on exhausted legacy SerpAPI. After flight production-path proof, define `travel.hotel.search@1` and repeat the same provider-neutral pattern.

**Production remains intentionally blocked for Agent Factory capability registration** until Research/Flight provider outbound network access is governed and real remote Eval/Release/Evidence gates pass.

Keep contracts stable, implementations replaceable and deployment proof explicit.
