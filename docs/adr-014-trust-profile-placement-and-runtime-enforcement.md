# ADR-014: Trust Profile Placement and Runtime Enforcement

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

ADR-009 established the trust profiles `sandbox`, `internal`, `business` and `privileged`, with PlatformPolicy defining the maximum permitted level. The executable Core Skeleton still needed one explicit authority path for where trust is requested, compiled and enforced.

## Decision

Trust is represented and enforced as follows:

```text
ClientInstanceConfig.trustProfile
        <= PlatformPolicy.maxTrustProfile
        -> EffectiveReleaseConfig.trustProfile
        -> ExecutionContext.trustProfile
        -> request-time policy enforcement
```

The order is:

```text
sandbox < internal < business < privileged
```

Rules:

- `ClientInstanceConfig` requests the trust profile for a concrete tenant/environment deployment.
- `PlatformPolicy.maxTrustProfile` is the ceiling.
- The compiler rejects any request above the ceiling.
- The compiled trust profile is immutable runtime authority in `EffectiveReleaseConfig` and is projected into `ExecutionContext`.
- Runtime may require a minimum trust profile for an operation but cannot elevate above the compiled value.
- Trust profile does not itself grant permissions; permission checks remain independent.
- In Core Skeleton v1, the trust ceiling is not an ExceptionPolicy override dimension.
- AgentManifest and untrusted prompt/model/tool content cannot set or expand trust authority.

## Consequences

### Positive

- reusable Agent definitions remain client-neutral;
- trust authority is explicit and reconstructable;
- no runtime authority is inferred from prompts;
- ceiling enforcement is deterministic at compile time and runtime.

### Cost

Adding trust as a required field is an intentional contract migration for ClientInstanceConfig, PlatformPolicy, EffectiveReleaseConfig and ExecutionContext.
