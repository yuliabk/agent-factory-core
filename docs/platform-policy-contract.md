# PlatformPolicy and ExceptionPolicy Contracts

**Status:** Core Skeleton v1 implementation contract

## Purpose

`PlatformPolicy` is the typed platform boundary used by the compiler. `ExceptionPolicy` is a scoped, expiring overlay for dimensions the PlatformPolicy explicitly declares overrideable.

The first executable contracts intentionally cover only the dimensions already needed by the thin Core Skeleton:

- allowed and denied permissions;
- allowed provider profiles;
- allowed budget override keys;
- allowed memory configuration keys;
- maximum trust profile ceiling (`maxTrustProfile`);
- Capability Registry enforcement mode (`soft` / `strict`);
- default data classification for the first ExecutionContext;
- explicit exception allowances.

## Trust ceiling

`maxTrustProfile` is the maximum trust level a ClientInstanceConfig may request. The order is:

```text
sandbox < internal < business < privileged
```

Trust profile selects runtime ceilings/defaults and does not itself grant permissions. In Core Skeleton v1, `maxTrustProfile` is intentionally not an ExceptionPolicy override dimension.

## Non-overridable behavior in the first skeleton

`deniedPermissions` are treated as non-overridable by the compiler. An ExceptionPolicy cannot weaken them.

The trust ceiling is also non-overridable in this first implementation.

An exception can only add values that appear in `spec.exceptionAllowances` of the exact PlatformPolicy name/version it references.

## Exception validation

Before an exception changes effective policy, the compiler verifies:

- exact PlatformPolicy name/version reference;
- tenant/environment scope;
- optional Agent name/version scope;
- expiry;
- that every requested override dimension/value is declared overrideable.

Each applied exception is recorded in `EffectiveReleaseConfig.policy.exceptionPolicyRefs`.

## Source boundary

Canonical external schemas:

- `schemas/platform-policy.schema.json`
- `schemas/exception-policy.schema.json`

Python runtime models:

- `agent_factory_core/contracts/platform_policy.py`
- `agent_factory_core/contracts/exception_policy.py`
- `agent_factory_core/contracts/trust.py`

The JSON Schemas remain the external contract; Pydantic models are internal projections.
