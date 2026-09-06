# Tool Gateway Contract

**Status:** Accepted direction after Owner Review

## Purpose

Agents never receive unrestricted direct access to files, networks, databases, SaaS systems or side-effecting actions. Tool/API/MCP access is mediated by the Runtime Governance Plane.

## Tool contract

Each governed tool declares:

- `tool_id` and version;
- typed input/output schema;
- required permissions/capabilities;
- supported data classifications/trust levels;
- tenant-binding behavior;
- risk/side-effect class;
- idempotency support;
- expected cost/latency class;
- timeout/retry policy;
- approval policy class;
- audit fields.

## Risk / side-effect classes

At minimum:

- `read_only`;
- `reversible_write`;
- `external_message`;
- `financial`;
- `permission_change`;
- `irreversible_write`;
- `sensitive_domain_action`.

PlatformPolicy may refine or map these to low/medium/high/non-overridable categories.

## Invocation pipeline

```text
Schema
 -> Effective permission / tenant / trust
 -> Data policy
 -> Risk/side-effect classification
 -> Budget/preflight
 -> Policy-defined approval or auto-decision
 -> Execute
 -> Validate
 -> Audit
```

Human approval is not universal. Low-risk tools may execute automatically when effective policy allows; high-risk/consequential operations use the required approval path.

## Trust boundary

Tool output is untrusted data. It cannot modify PlatformPolicy, EffectiveReleaseConfig, ExecutionContext or grant permissions.

## Network, Web and MCP

Web, API and MCP calls are treated as governed Tool/Capability invocations under the same policy model. Discovery/availability of an endpoint or MCP action does not authorize its use.

## Agent autonomy

A business Agent may autonomously decide that an approved tool/capability is useful for its plan. Tool Gateway remains the authority for whether that request may execute.

## Development vs production

Sandbox/dev policy may allow explicit mocks, warnings or narrower development credentials. Production consequential tools require registered contract/version, effective grants, risk classification and audit behavior.

## Failure behavior

- invalid schema -> reject before execution;
- missing permission -> deny/audit;
- expired/invalid exception -> deny;
- over-budget -> approved alternative/overage flow according to policy;
- approval required but absent -> pause/typed denial;
- duplicate consequential retry -> idempotency handling where supported;
- timeout/provider failure -> bounded policy-defined retry/fallback.