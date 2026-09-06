# Design: Core Contracts v1

## Architecture direction

`Agent Factory Core` becomes the control plane for shared contracts and platform controls. Business agents remain separate repositories.

```text
Client Intent
 -> Spec Compiler
 -> Template Engine
 -> Agent Manifest
 -> Orchestrator + ExecutionContext
    -> Model Router
    -> Capability Registry
    -> Tool Gateway
    -> Memory Broker
 -> Evals / Evidence / Approval
 -> Versioned Release
```

## Boundary decisions

### Core owns

- contracts, policies and validation;
- capability resolution and orchestration;
- model/provider routing policy;
- tool/memory access controls;
- budget/runtime limits;
- eval/release/audit contracts;
- template registry/selection contracts.

### Agent repository owns

- domain/business behavior;
- domain prompts and workflow logic;
- capabilities provided/required;
- agent-specific evaluation dataset;
- domain-specific adapters not reusable platform-wide.

## Provider migration

Earlier Dify, n8n and OpenAI prototype artifacts remain historical/experimental evidence. They can continue as implementations where useful, but current Core contracts MUST NOT require them unless a bounded agent requirement explicitly does so.

## Security model

Authority lives outside the model. Untrusted content cannot grant permissions. Tools, capabilities, memory and network access are default-deny. Every invocation receives trusted execution context and bounded cost/runtime controls.

## Budget model

Business budget and emergency safety cap are distinct:

- business limit can be increased only by the authorized approver after warning;
- emergency cap stops loops/anomalies regardless of business approval.

## Agent-to-Agent model

Consumers request versioned capabilities. Core resolves an implementation and delegates only the minimum context/permissions/budget slice. Direct peer URLs are not the default architecture.

## Client intake

The client gives a plain-language goal. The platform asks only critical missing questions, including budget and consequential-action boundaries. It infers non-critical technical choices and presents assumptions/options for confirmation.

## Implementation strategy after approval

Start with a small deterministic skeleton: manifest schema/validator, execution context, permission/budget checks, minimal audit schema and adapter interfaces. Do not build a distributed platform before those contracts prove useful.
