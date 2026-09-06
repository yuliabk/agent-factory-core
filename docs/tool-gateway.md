# Tool Gateway Contract

**Status:** Proposed

## Purpose

Agents never receive unrestricted direct access to files, networks, databases, SaaS systems or side-effecting actions. Tool access is mediated by the Core Tool Gateway.

## Tool contract

Each tool declares:

- `tool_id` and version;
- typed input/output schema;
- required permissions;
- supported data classifications;
- tenant-binding behavior;
- side-effect class;
- idempotency support;
- expected cost/latency class;
- timeout and retry policy;
- approval requirement;
- audit fields.

## Side-effect classes

- `read_only`
- `reversible_write`
- `external_message`
- `financial`
- `permission_change`
- `irreversible_write`
- `sensitive_domain_action`

Policies may further refine them.

## Invocation pipeline

`Schema -> Permission -> Tenant -> Data Policy -> Budget -> Approval -> Execute -> Validate -> Audit`

Tool output is untrusted data. It cannot modify system policy or grant permissions.

## Network and MCP

Web, API and MCP calls are treated as tool/capability invocations under the same policy model. MCP availability does not create automatic authorization to use every exposed action.
