# Tool Gateway Contract

**Status:** Accepted direction; first executable read-only slice implemented in Phase 1C / C4.3

## Purpose

Agents never receive unrestricted direct access to files, networks, databases, SaaS systems or side-effecting actions. Tool/API/MCP access is mediated by the Runtime Governance Plane.

## Tool contract

Each governed tool declares:

- `tool_ref`, concrete binding ID and version;
- typed JSON Schema input/output contract;
- required permission;
- minimum trust profile;
- supported data classifications;
- risk/side-effect class;
- expected cost for preflight integration;
- an implementation handler behind the gateway boundary.

Longer-term tool metadata may add explicit idempotency, timeout/retry, approval-policy and latency classes when the first real use cases need them.

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
Trusted ExecutionContext binding
 -> registered compatible ToolSpec
 -> read-only side-effect gate for C4.3
 -> tenant / permission / trust / data-classification authority
 -> input JSON Schema
 -> execute handler
 -> output JSON Schema
 -> minimized RuntimeAuditEvent
```

The first executable slice deliberately permits only `read_only` registrations. Any other side-effect class is denied before handler execution. Later Tool Gateway depth will connect policy-defined approvals, idempotency and richer budget/accounting state before writes are enabled.

## Binding authority

The Agent requests a logical tool reference such as `synthetic.lookup`. The Tool Gateway does not choose arbitrary implementations from Agent output. It reads the concrete binding only from trusted `ExecutionContext.toolBindings` and resolves that binding against its registered ToolSpec.

An unbound or incompatible tool is denied.

## Runtime authority

Before execution, Tool Gateway calls the Runtime Governance policy evaluator. The request must remain inside:

- trusted tenant identity;
- compiled permission set;
- compiled `trustProfile`;
- effective data classification;
- request deadline.

Tool-specific supported classifications are additionally checked after the general ExecutionContext authority check.

## Schema boundary

Input is validated before the handler. Output is validated after the handler. Tool output is always treated as untrusted data and cannot modify PlatformPolicy, EffectiveReleaseConfig, ExecutionContext or grant permissions.

## Audit

Both allow and deny decisions produce minimized `RuntimeAuditEvent` evidence containing the trusted request/actor/tenant/release identity, policy references, target binding, decision and result. Payload bodies and prompts are not copied into the audit event.

## First synthetic implementation

`agent_factory_core/synthetic_readonly_tool.py` provides a deterministic in-process `synthetic.lookup` tool for contract validation only. It performs no network, file, SaaS or customer-data side effects.

## Source boundary

- Gateway implementation: `agent_factory_core/tool_gateway.py`
- Synthetic read-only adapter: `agent_factory_core/synthetic_readonly_tool.py`
- Runtime authority: `agent_factory_core/runtime/policy.py`
- Audit contract: `schemas/runtime-audit-event.schema.json`
- Contract tests: `tests/contracts/test_tool_gateway.py`

## Development vs production

Sandbox/dev policy may allow explicit mocks, warnings or narrower development credentials. Production consequential tools require registered contract/version, effective grants, risk classification, budget/approval behavior and audit evidence before write-capable execution is enabled.

## Failure behavior

- missing trusted binding -> deny/audit;
- incompatible/unregistered binding -> deny/audit;
- non-read-only side effect in the first slice -> deny/audit;
- tenant/permission/trust/classification/deadline failure -> deny/audit;
- invalid input schema -> deny/audit before execution;
- invalid output schema -> deny/audit and do not expose invalid output;
- handler/provider timeout and policy-defined retry/fallback remain later adapter depth.
