# Security and Platform Governance

**Status:** Accepted direction after Owner Review

## Policy hierarchy

From highest to lowest authority:

1. Non-overridable Platform Invariants.
2. Legal/privacy/tenant-isolation requirements.
3. PlatformPolicy risk/trust profiles.
4. Valid scoped ExceptionPolicy overlays for overridable rules only.
5. ClientInstanceConfig grants and restrictions.
6. AgentManifest requirements.
7. Agent-specific behavior/specification.
8. Runtime/model output.

A lower layer cannot create authority that a higher layer does not allow.

## Core rule

The Agent declares requirements. The Factory proposes configuration. PlatformPolicy defines the maximum allowed authority. The client can configure within that envelope, usually making it equal or stricter. Runtime executes only the compiled EffectiveReleaseConfig.

## Risk and trust governance

The platform uses trust levels such as `sandbox`, `internal`, `business` and `privileged` as policy profiles. Trust level does not itself grant permission; it selects ceilings, defaults, eval thresholds and approval requirements.

- Factory recommends the initial level from the specification/risk profile.
- PlatformPolicy defines the maximum allowed level.
- Client can lower/restrict within the permitted range.
- Raising beyond the ceiling requires a valid ExceptionPolicy if the relevant rule is overridable.

## ExceptionPolicy

Exceptions are first-class governance artifacts, not undocumented bypasses.

Every exception records rule, scope, reason, approver, compensating controls, creation time, expiration/review time, status and audit reference.

ExceptionPolicy MUST NOT override a rule classified as non-overridable.

Expired or out-of-scope exceptions are ignored by the compiler/runtime.

## Approval authorities

### Build / Control Plane

Human approval is required only when PlatformPolicy says it is required. Low-risk configuration may be auto-approved by policy.

Material changes commonly requiring stronger approval include:

- permission expansion;
- elevated data classification or trust level;
- material budget increase;
- provider/privacy boundary change;
- consequential tool activation;
- retention expansion;
- release-strategy change;
- new/expanded exception.

### Runtime

Authorized client approvers handle business-budget overages and client-owned consequential actions according to EffectiveReleaseConfig and policy.

### Elevated domains

Sensitive personal, medical, financial, legal or similarly elevated domains use dedicated policy profiles and domain/security/privacy approval paths.

## Release governance

Release strategy is specified and versioned:

- `human-required`;
- `policy-auto`;
- `policy` (derive from effective risk/trust/change class).

PlatformPolicy can always require stronger approval than the Agent/client requested. Automatic release never bypasses blocking security/policy gates.

Every release produces a release decision record, whether human or automatic.

## Change classes

- **Documentation only:** no runtime effect; normal review.
- **Compatible low-risk:** regression fast path may be policy-automated.
- **Permission/data/trust/cost expansion:** OpenSpec change and stronger gate.
- **Breaking contract:** major version, migration plan and rollback required.
- **Emergency security change:** capability/instance may be suspended immediately; retrospective documentation follows.

## Evaluation governance

Evaluation families include functional/business, security, cost/runtime and contract/portability. Thresholds and blocking behavior are policy-defined by risk/trust/domain rather than one universal score.

Non-overridable security failures block promotion. Business-quality thresholds may be blocking, warning or advisory according to policy.

## Required records

Material decisions are preserved as appropriate through:

- OpenSpec change;
- ADR for architecture decisions;
- AgentManifest and ClientInstanceConfig diff;
- EffectiveReleaseConfig;
- evaluation evidence;
- approval/release decision record;
- ExceptionPolicy reference;
- release reference;
- runtime audit events.

## Supply chain governance

External skills, plugins, MCP servers, packages, providers and templates require risk-appropriate source verification, pinning/versioning, license review, permission inventory, security review and regression evaluation before production use.