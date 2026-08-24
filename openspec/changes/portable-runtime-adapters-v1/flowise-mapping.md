# P3 — Flowise Mapping

## Status

Public official-source preflight completed on 2026-08-21 under `PR-G2-Flowise-Preflight`. Decision: **NO-GO** for Flowise Cloud and the official upstream because Flowise is winding down operations, the official repository is archived, and EOL is scheduled for 2026-08-31. No account, flow, assistant, document store, vector store, credential, payment method, or runtime activity was authorized or created.

## Vendor Continuity Blocker

The official Flowise sunset notice states that active feature development has stopped, packages and Docker images are deprecated, the repository is archived, and official core-team support ends on 2026-08-31. This fails the required maintenance, security, support, and reconstruction controls before technical equivalence is considered.

## Concept Mapping

| Canonical concept | Flowise candidate concept | Planning assessment |
|---|---|---|
| Agent release | Exported Chatflow/Agentflow JSON plus Agent Factory manifest | Export must be sanitized and reconstructable |
| Prompt and policy | Prompt templates and flow nodes | Must prove external tools are absent/disabled |
| Approved corpus | Document Store, loader, splitter, and vector store | Must preserve corpus version and isolation |
| Retrieval evidence | Retriever/vector-store documents and metadata; `Text with Metadata` and source-document return are documented | Exact immutable `source_id` and section propagation remains unproven |
| Answer contract | LLM/chain output plus response formatting | Citation validation may require adapter logic |
| Evaluation run | Prediction/API call plus logs | Requires a separately approved live gate |
| Usage and cost | Cloud predictions, storage, and model-provider usage | Unified hard cap may not exist |
| Export/deletion | JSON Export/Import; credentials excluded; store/chunk/vector delete APIs | Vector deletion is conditional and logs/backups remain undefined |

## Cost Planning Snapshot

Official Flowise Cloud pricing reviewed on 2026-08-21 still displayed Free at USD 0, Starter at USD 35/month, and Pro at USD 65/month. The same official site announces the product sunset and 2026-08-31 EOL. Published prices therefore do not establish continuity or safe TCO, and no purchase or registration is recommended.

## Required Preflight Evidence

- Prediction, storage, and model-provider usage can be measured and bounded conservatively.
- Retriever metadata reaches the adapter with stable `source_id` and section provenance.
- The chosen flow contains no tool/action nodes and cannot use unapproved credentials.
- Flow, document store, vector store, logs, and credentials are isolated for one synthetic prototype.
- Exported JSON omits secrets and, with the canonical manifest, supports reconstruction.
- Deletion and retention cover documents, chunks, vectors, chat logs, runs, and backups.
- Hebrew answer and fallback behavior can be measured against the frozen set.

## Known Gaps and Risks

- Official upstream development has stopped and the repository is archived.
- Cloud availability, support, security response, and export windows after EOL are undefined.
- Metadata can be lost across loader, splitter, vector store, retriever, and output nodes.
- Inline citations may require explicit flow logic and must never be fabricated by the prompt.
- The free plan's 100 predictions may cover a bounded test, but model-provider charges and retries are separate.
- A unified provider-native cost hard cap across Flowise and the model provider is unproven.
- Multi-client isolation, deletion evidence, and retention controls may vary by deployment and plan.
- Hebrew quality and deterministic fallback behavior are unverified.
- Document-loader deletion does not automatically delete vector data; vector deletion has Record Manager conditions, while logs and backups remain unverified.
- Cloud data is documented in US East 1 and Cloud registration uses PostHog analytics; exact service-data retention is not stated.

## Fail-Closed Decision

Flowise Cloud and the official upstream are ineligible for a runtime pilot because vendor continuity and maintained security support fail closed. Citation, isolation, deletion, retention, Hebrew, and combined cost controls also remain incomplete. A community fork or internally maintained fork MUST be treated as a new candidate under a new OpenSpec change and approval gate.

## Official Sources

- Sunset and EOL: https://flowiseai.com/sunset
- Archived official repository: https://github.com/FlowiseAI/Flowise
- Pricing: https://flowiseai.com/
- Privacy: https://flowiseai.com/privacy
- Export/Import: https://docs.flowiseai.com/migration-guide/cloud-migration
- Metadata/retrieval: https://docs.flowiseai.com/using-flowise/agentflowv2
- Deletion API: https://docs.flowiseai.com/api-reference/document-store
- Detailed evidence: `pr-g2-flowise-preflight-evidence.md`
