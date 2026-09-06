# Tooling and Cost Strategy

## Principle

The platform does not hard-code one model, search provider, low-code runtime or automation vendor. Providers are selected through approved profiles and adapters according to cost, quality, privacy, latency and availability.

See [`provider-and-cost-policy.md`](provider-and-cost-policy.md) for the normative architecture direction.

## Cost control layers

1. Client/business budget gathered during intake.
2. Solution profile selection (economy / balanced / premium or equivalent).
3. Per-request budget check.
4. Preflight estimate for expensive composite operations where practical.
5. Warnings before business limit.
6. Explicit authorized approval before exceeding the business limit.
7. Independent emergency safety cap for loops/anomalies.
8. Usage/cost audit events and periodic reporting.

## Provider categories

| Category | Examples / options | Core requirement |
|---|---|---|
| Model provider | OpenAI, Anthropic, Google, DeepSeek, others | Provider adapter + model profile |
| Search/research | Web search, search APIs, vertical APIs, MCP, internal KB | Capability/tool contract + provenance |
| Agent/runtime | Native code, managed low-code, Dify, others | Runtime adapter/contract where needed |
| Automation | n8n, direct API adapters, other workflow engines | Tool Gateway policy |
| Storage/RAG | managed DB/object/vector stores | Memory/knowledge contract + tenant isolation |
| Channels | Web, Email, WhatsApp, CRM | Channel adapter + identity/policy |

Specific vendors can be approved for a particular pilot without becoming a permanent Core dependency.

## Prototype history

Earlier prototypes explored Dify Cloud, n8n and OpenAI under a bounded experiment budget. Those artifacts remain useful historical evidence and portability test material, but the current Core architecture treats them as replaceable implementations.

## Avoid in early Core MVP

- Kubernetes/service mesh without a demonstrated need.
- Complex distributed multi-agent infrastructure.
- Dedicated vector infrastructure before scale requires it.
- Provider-specific business logic.
- Production sensitive-data workflows before security/privacy approval.
