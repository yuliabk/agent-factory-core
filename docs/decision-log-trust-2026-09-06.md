# Trust placement decision - 2026-09-06

Accepted implementation decision for Core Skeleton v1:

- ClientInstanceConfig requests `trustProfile`.
- PlatformPolicy sets `maxTrustProfile`.
- Order: `sandbox < internal < business < privileged`.
- Compiler rejects trust above the policy ceiling.
- EffectiveReleaseConfig records the compiled trust profile.
- ExecutionContext projects the compiled trust profile to runtime.
- Runtime cannot elevate above that profile.
- Trust does not grant permissions.
- The trust ceiling is non-overridable by ExceptionPolicy in this first skeleton.

Canonical rationale: ADR-014.
