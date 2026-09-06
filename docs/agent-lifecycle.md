# Agent Lifecycle

**Status:** Accepted direction after Owner Review

## 1. Purpose

Define a common path from client intent to a governed deployed Agent while keeping the path flexible enough for low-risk automation and stricter high-risk flows.

The specification is the primary artifact. The deployed Agent is a reproducible result of the approved specification, AgentManifest, ClientInstanceConfig and PlatformPolicy.

## 2. Lifecycle

```text
Intent
 -> Clarified
 -> Specified
 -> Planned
 -> Built
 -> Evaluated
 -> Release Eligible
 -> Released
 -> Monitored
 -> Changed / Suspended / Deprecated / Decommissioned
```

`Release Eligible` does not always mean a human must click approve. The release strategy is declared in specification/configuration and validated by Platform Policy.

## 3. Intent and Clarification

The client describes the business goal in plain language. The platform asks only critical missing questions and may infer non-critical configuration.

Normal UX target: under 10 minutes and typically 5-6 critical follow-up questions. This is a target, not a hard technical limit.

For an underspecified request the default pattern is:

`infer -> show assumptions -> client confirms/corrects`

## 4. Specified

The Spec Compiler produces at least:

- business scope and success criteria;
- forbidden outcomes;
- recommended Agent/template composition;
- required/provided capabilities;
- requested tool/memory/data requirements;
- risk/trust recommendation;
- budget profile and alternatives;
- evaluation requirements;
- release strategy requirement;
- approval/escalation requirements.

Output: approved/proposed OpenSpec change + reusable AgentManifest draft + ClientInstanceConfig draft.

## 5. Planned

The Factory proposes implementation profiles such as economy, balanced or premium according to policy, not a hard-coded provider.

The Build / Control Plane compiles requested requirements against PlatformPolicy. Material permission, cost, data and trust decisions are surfaced for the appropriate approver.

Low-risk decisions MAY be auto-resolved by policy. The platform does not require a human approval for every routine configuration choice.

## 6. Built

The build composes:

```text
Approved Spec
+ Versioned Templates
+ AgentManifest
+ ClientInstanceConfig
+ PlatformPolicy / ExceptionPolicy
+ Adapters / Agent-specific assets
= Release Candidate
```

No secret value or raw client production data is committed to Git or embedded in the reusable Agent Definition.

## 7. Evaluated

Evaluation families are policy-driven and include at least:

1. Functional/business quality.
2. Security/policy compliance.
3. Cost/runtime behavior.
4. Contract/portability where relevant.
5. Agent-hop/delegation where relevant.

Evaluation thresholds are not universally hard-coded. PlatformPolicy maps risk/trust/domain/release strategy to blocking, warning or advisory thresholds.

## 8. Release eligibility and strategy

A release candidate becomes `Release Eligible` only after all blocking policy gates pass.

Release strategy is explicit and versioned. Initial supported strategies:

- `human-required` - named approver must approve the exact release.
- `policy-auto` - release may proceed automatically after all policy-defined blocking gates pass.
- `policy` - PlatformPolicy selects the effective strategy from risk, trust level, environment and change class.

A specification or ClientInstanceConfig may request a strategy, but PlatformPolicy sets the maximum allowed automation.

Example:

- low-risk sandbox/read-only update -> may use `policy-auto`;
- permission expansion or elevated data class -> human approval required;
- non-overridable security failure -> never releasable until remediated.

Every release decision, including automatic release, produces a release decision record.

## 9. Client acceptance

Client-facing acceptance is business-oriented. The client sees:

- scope and expected outcome;
- material assumptions;
- what the Agent may do;
- actions requiring client approval;
- budget expectations/options;
- data-use summary;
- known limitations and escalation path.

Technical implementation details remain hidden unless requested or materially relevant.

## 10. Effective release

The Build / Control Plane emits immutable `EffectiveReleaseConfig` and `agent_release_id` linked to:

- approved spec;
- AgentManifest version;
- ClientInstanceConfig version;
- PlatformPolicy and ExceptionPolicy versions;
- template versions;
- effective permissions/capabilities;
- provider/model profile;
- tool/memory contracts;
- eval evidence;
- release decision/approval reference;
- rollback target.

Runtime executes this effective release, not uncompiled drafts.

## 11. Monitoring

Runtime monitoring includes:

- spend and budget projection;
- errors/retries/tool failures;
- permission denials and exception use;
- security events;
- quality regressions;
- provider availability;
- agent hop depth/cycles;
- drift from EffectiveReleaseConfig.

Cost anomalies and failure loops receive high-priority alerting.

## 12. Change lifecycle

Changes are classified by policy.

- documentation-only -> normal review;
- compatible low-risk change -> regression fast path may be automatic;
- permission/data/trust/cost expansion -> stronger gates and usually fresh approval;
- breaking contract -> major version + migration/rollback plan;
- emergency security response -> capability may be suspended immediately with retrospective documentation.

## 13. Suspend

Runtime Governance Plane can suspend risky capabilities or an Agent instance when safety cap, security incident, credential compromise, client request or dangerous provider drift occurs.

Suspension may be scoped to a capability rather than the entire Agent where safe. Read-only degraded behavior is allowed only when policy permits.

## 14. Deprecation and decommission

Deprecation provides a migration period. Decommission includes credential revocation, channel disablement, state export/deletion according to retention policy, audit closure and final deletion/release evidence.