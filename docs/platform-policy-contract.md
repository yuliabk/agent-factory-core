# PlatformPolicy and ExceptionPolicy Contracts

**Status:** Core Skeleton v1 implementation contract

## Purpose

`PlatformPolicy` is the typed platform boundary used by the compiler and release gate. `ExceptionPolicy` is a scoped, expiring overlay for dimensions the PlatformPolicy explicitly declares overrideable.

The first executable contracts intentionally cover only the dimensions already needed by the thin Core Skeleton:

- allowed and denied permissions;
- allowed provider profiles;
- allowed budget override keys;
- allowed memory configuration keys;
- maximum trust profile ceiling (`maxTrustProfile`);
- Capability Registry enforcement mode (`soft` / `strict`);
- default data classification for the first ExecutionContext;
- evaluation gate mapping (`evalRules`);
- non-overridable security evaluation identities (`securityInvariantChecks`);
- explicit exception allowances.

## Trust ceiling

`maxTrustProfile` is the maximum trust level a ClientInstanceConfig may request. The order is:

```text
sandbox < internal < business < privileged
```

Trust profile selects runtime ceilings/defaults and does not itself grant permissions. In Core Skeleton v1, `maxTrustProfile` is intentionally not an ExceptionPolicy override dimension.

## Evaluation gate mapping

`evalRules` maps each release-gated `EvalResult.checkId` explicitly to one of:

- `blocking`;
- `warning`;
- `advisory`.

The deterministic release-gate mapper fails closed when a result is not mapped, when rule IDs conflict, or when results from multiple release IDs are mixed into one gate.

`securityInvariantChecks` lists security checks that must remain `blocking`. The mapper rejects an invariant that is missing from `evalRules`, classified below blocking, or presented under a non-security eval family. ExceptionPolicy does not override this classification in the first skeleton.

Raw `EvalResult.status` remains separate from policy effect. A `PASS_WITH_WARNINGS` result on a blocking check warns but does not itself become a blocking failure. A `FAIL` blocks only when the effective rule classification is `blocking`.

## Non-overridable behavior in the first skeleton

`deniedPermissions` are treated as non-overridable by the compiler. An ExceptionPolicy cannot weaken them.

The trust ceiling and security-invariant eval classification are also non-overridable in this first implementation.

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

Python runtime models/logic:

- `agent_factory_core/contracts/platform_policy.py`
- `agent_factory_core/contracts/exception_policy.py`
- `agent_factory_core/contracts/trust.py`
- `agent_factory_core/eval_policy.py`

The JSON Schemas remain the external contract; Pydantic models are internal projections. Cross-object gate semantics that JSON Schema cannot express are enforced deterministically by the Core mapper rather than hidden in model-only validation.
