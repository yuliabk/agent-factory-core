# ADR-010: Policy-driven Release Strategy

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

Always requiring a human click before every release is safe but can become unacceptable for low-risk, repetitive or high-frequency changes. Always auto-releasing is too permissive for higher-risk changes.

## Decision

Release strategy is explicit, versioned and compiled into EffectiveReleaseConfig.

Initial strategies:

- `human-required` - exact release requires a named human approval;
- `policy-auto` - release may proceed automatically after all policy-defined blocking gates pass;
- `policy` - effective strategy is derived from PlatformPolicy using risk, trust level, environment, domain and change class.

Agent specification or ClientInstanceConfig may request a strategy. PlatformPolicy may always require a stricter strategy.

Automatic release never bypasses blocking security/policy checks and always produces a release decision/evidence record.

## Consequences

- fast paths are possible without creating an ungoverned release path;
- high-risk changes retain human control;
- release behavior can evolve through policy rather than Core rewrites;
- automated and human releases remain equally reconstructable.

## Examples

- low-risk sandbox documentation/config change -> `policy-auto` may be permitted;
- compatible provider substitution with passing regression evals -> policy may auto-release;
- permission expansion, elevated data class or privileged trust change -> policy may require human approval;
- non-overridable security failure -> release blocked regardless of requested strategy.