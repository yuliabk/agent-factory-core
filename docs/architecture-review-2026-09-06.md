# Architecture Review - 2026-09-06

**Status:** Completed synchronization review  
**Scope:** Agent Factory Core architecture/contracts after Owner brainstorming session

## Executive conclusion

The repository now has one coherent architectural direction suitable for starting a thin executable Core Skeleton.

The review found that the main risk was not missing ideas, but several contracts still reflected earlier assumptions: one mixed Manifest, universally human-gated release, overly uniform approval language, unclear Agent autonomy, and a roadmap that sequenced subsystems too serially. These have been synchronized to the accepted platform vision.

No production runtime/customer-data migration is authorized by this review.

## Canonical architecture after review

```text
Business Intent
 -> Versioned Spec
 -> Template / Modular Composition
 -> AgentManifest
 + ClientInstanceConfig
 + PlatformPolicy / ExceptionPolicy
 -> EffectiveReleaseConfig
 -> Runtime Governance Plane
    -> bounded autonomous Agent planning
    -> Capability / Model / Tool / Memory gateways
 -> Evals / Evidence / Release Decision
 -> Versioned Release / Monitor
```

Core remains one repository initially but is logically split between Build / Control Plane and Runtime Governance Plane. Business Agents remain separate repositories.

## Inconsistencies identified and resolved

### 1. Reusable Agent vs client-specific state

**Before:** Agent Manifest mixed reusable Agent definition with concrete client budget, permissions, approvers, retention and provider constraints.

**Resolved:** AgentManifest is reusable requirements; ClientInstanceConfig contains tenant-specific grants/config; PlatformPolicy/ExceptionPolicy compiles them into immutable EffectiveReleaseConfig.

### 2. Human approval everywhere

**Before:** Lifecycle/release wording implied every production release needed final human approval.

**Resolved:** release strategy is `human-required`, `policy-auto` or policy-derived. PlatformPolicy can always require stronger control. Auto-release still requires all blocking gates and a release decision/evidence record.

### 3. Security strictness vs scalability

**Before:** default deny/approval language risked being interpreted as manual approval for routine operations.

**Resolved:** default deny remains, but actions are risk-based. Trust Profiles provide safe defaults/ceilings. Low risk may auto-execute; high risk uses stronger gates. Non-overridable invariants remain absolute.

### 4. Exceptions

**Before:** no canonical mechanism for legitimate exceptions without changing global policy.

**Resolved:** ExceptionPolicy is a scoped, approved, expiring/audited overlay for explicitly overridable rules only.

### 5. Memory autonomy

**Before:** persistent memory language could be interpreted as always requiring explicit manual opt-in per write or as Agent-controlled storage.

**Resolved:** Agent can autonomously identify/request/write useful memory when effective policy permits. Memory Gateway enforces tenant, purpose, classification, retention and consent/legal-basis requirements.

### 6. Capability Registry rigidity

**Before:** architecture was strict enough to risk slowing development.

**Resolved:** soft-strict enforcement: warnings/mocks/degraded optional resolution in dev/sandbox; strict registration/compatibility/policy for critical production capabilities.

### 7. Provider selection

**Before:** provider-neutrality existed, but optimization priority was not explicit.

**Resolved:** routing is policy-driven across cost, quality, privacy, latency, availability and client/task constraints. Neither cheapest-first nor quality-first is universal.

### 8. Template rigidity

**Before:** template-first could be read as selecting one fixed template.

**Resolved:** use smallest suitable base template plus modular capabilities. Follow progressive complexity.

### 9. Eval thresholds

**Before:** release language could imply one universal quality threshold.

**Resolved:** policy maps eval results to blocking/warning/advisory. Business-quality thresholds vary by risk/domain; non-overridable security failures always block.

### 10. Orchestration vs Agent autonomy

**Before:** Orchestrator responsibilities could be read as centralizing Agent planning.

**Resolved:** hybrid bounded autonomy. Core owns authority/routing/limits; Agent owns task planning/decomposition/replanning inside effective boundaries.

### 11. Primary artifact

**Before:** concept existed but was not consistently elevated across docs.

**Resolved:** versioned specification/history is explicitly the primary platform artifact. Deployed Agent instances are reproducible outputs; unmapped runtime state is drift.

### 12. Delivery speed

**Before:** roadmap developed major subsystems in largely serial phases before a real reference Agent.

**Resolved:** implement a thin vertical Core slice: schemas/compiler -> Runtime Governance kernel -> minimal adapters/gateways -> eval/release kernel -> one synthetic end-to-end Agent -> Research/Brain Agent.

## Files synchronized

Architecture/governance:
- `platform-vision.md`
- `architecture.md`
- `agent-manifest.md`
- `agent-lifecycle.md`
- `security-model.md`
- `governance.md`
- `orchestration.md`
- `capability-registry.md`
- `provider-and-cost-policy.md`
- `tool-gateway.md`
- `memory-contract.md`
- `template-engine.md`
- `client-experience.md`
- `evidence-and-evals.md`
- `decision-log.md`
- `roadmap.md`

ADRs:
- ADR-006, ADR-007, ADR-008 accepted/updated
- ADR-009 Trust Profiles/Exceptions added
- ADR-010 Policy-driven Release Strategy added
- ADR-011 Specification as Primary Artifact added

Machine-readable starting contracts:
- `templates/agent-manifest.yaml`
- `templates/client-instance-config.yaml`
- `templates/effective-release-config.yaml`
- `templates/client-intake-conversational.md`

OpenSpec:
- `openspec/project.md`
- `core-contracts-v1/proposal.md`
- `core-contracts-v1/design.md`
- `core-contracts-v1/specs/core-contracts/spec.md`
- `core-contracts-v1/tasks.md`

Repository guidance:
- root `README.md`
- `AGENTS.md`
- `docs/README.md`

## Historical artifacts intentionally retained

ADR-001 through ADR-004 and older Dify/n8n/Knowledge/Travel prototype/OpenSpec artifacts are retained as historical evidence. They do not override the newer accepted Core contracts.

Provider-specific prototype decisions are therefore not deleted, but they are no longer platform-wide dependencies.

## Remaining decisions - intentionally deferred

The following are implementation choices and do not block the Core Skeleton:

- exact schema technology (JSON Schema/Pydantic combination);
- physical Registry backend after initial in-process implementation;
- first two provider adapters;
- pricing/currency normalization source;
- concrete safety-cap values by workload;
- final production invariant catalog;
- persistent-memory backend;
- approval identity mapping per channel;
- Factory UI repo/deployment location;
- long-term template package registry.

Resolve them just-in-time at the corresponding implementation task unless a new architectural conflict appears.

## Readiness assessment

### Ready now

- design of Core Skeleton contracts;
- schema/compiler implementation planning;
- synthetic data tests;
- in-process capability/model/tool/memory interfaces;
- policy/eval/release kernel design.

### Not ready yet

- production sensitive/customer data;
- broad external side effects;
- production Research/Travel migration;
- final multi-client security hardening.

## Next step

Begin `Core Contracts v1` task group C2/C3 as a thin vertical slice, then complete C4/C5 only to the depth needed for one synthetic end-to-end Agent. After that, open the separate Research/Brain Agent repository and define `research.lookup` as the first real reusable capability.
