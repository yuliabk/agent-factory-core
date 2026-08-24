# PR-G2 Flowise Public Preflight Evidence

## Authorization and Boundary

- **Gate:** `PR-G2-Flowise-Preflight`
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-21
- **Permitted action:** Read-only review of public official Flowise sources and local documentation.
- **Excluded:** Registration, login, account, credentials, upload, Indexing, Runtime, payment, Publish, Commit, and Push.
- **Provider-side changes:** None.

## Executive Decision

**Decision: NO-GO for a new Flowise Cloud or official-upstream pilot.**

Flowise announced that it is winding down operations. Active development stopped in July 2026, the official GitHub repository was archived in August 2026, packages and images are deprecated, and official core-team support reaches End of Life on 2026-08-31. A new Agent Factory dependency would therefore begin after code freeze and immediately before EOL. This continuity risk is a release blocker regardless of the still-published Cloud pricing or technical feature fit.

The archived source remains useful as a design reference. A future community fork or internally maintained self-hosted derivative would be a different candidate and would require a new change, pinned revision, license review, security ownership, maintenance budget, and separate approval.

## Capability Findings

| Contract area | Official public evidence | Status | Preflight consequence |
|---|---|---|---|
| Vendor continuity | Official sunset notice and archived GitHub repository | **Unsupported** | Blocking; no new pilot |
| Knowledge/RAG | Document Stores, retrievers, metadata, and source-document return are documented | Supported in product design | Does not override EOL |
| `source_id` and section provenance | Metadata can be preserved and passed to prompts; source documents can be returned | Partial | Exact immutable citation path remains unverified without Runtime |
| Hebrew behavior | General LLM workflow support exists | Unknown | Hebrew quality and fallback determinism remain unverified |
| External-action suppression | Tool, HTTP, MCP, custom-code, and agent nodes exist | Partial | A dedicated flow allow-list would be required; absence cannot be proven publicly |
| Logs and usage | Execution traces and prediction quotas are advertised | Partial | Per-run cost evidence and combined provider-model accounting remain unverified |
| Hard cost stop | Monthly prediction/storage quotas are published | Unknown | No official evidence of a combined monetary hard stop across Flowise and model provider |
| Export/reconstruction | Cloud migration guide documents JSON Export/Import, stable IDs, and exclusion of credentials | Partial | Helpful for portability; provider-managed state completeness remains unverified |
| Deletion | APIs exist for stores, chunks, loaders, and vector data | Partial | Loader deletion does not delete vector data; vector deletion is conditional on Record Manager; backups/logs remain undefined |
| Tenant isolation | Workspaces and RBAC are documented; Pro advertises unlimited workspaces and admin roles | Plan-dependent | Free-tier dedicated tenant boundary is not established publicly |
| Credential protection | Encrypted credentials and secret-manager options are documented | Supported for configured deployments | No credentials are authorized by this gate |
| Data location/retention | Cloud privacy policy names US East 1, PostHog, and purpose-based retention | Partial | Exact service-data retention and full deletion SLA are not specified |

## Published Cost Snapshot

Pricing was read from the official public page on 2026-08-21. It remains published despite the official sunset notice and MUST NOT be treated as evidence of future service availability.

| Option | Published platform price | Published allowance | Indicative annual platform price | Excluded or unknown TCO |
|---|---:|---|---:|---|
| Free | USD 0/month | 2 flows/assistants, 100 predictions/month, 5 MB | USD 0 | Model usage, migration, continuity, support |
| Starter | USD 35/month | Unlimited flows/assistants, 10,000 predictions/month, 1 GB | USD 420 | Model usage, taxes, migration, continuity, support |
| Pro | USD 65/month | 50,000 predictions/month, 10 GB, workspaces/admin features | USD 780 base | User-charge semantics, model usage, taxes, migration, continuity |
| Archived self-hosted source | No upstream license fee for Apache-licensed portions | Owner-operated | Unknown | Hosting, backups, monitoring, patching, security response, fork maintenance, commercial-license portions |

Because upstream support is ending, any apparently low license price understates the operational and exit cost. A reliable one-year or three-year TCO cannot be established from the public evidence.

## Risk Assessment

| Risk | Likelihood | Impact | Control or disposition |
|---|---|---|---|
| Official EOL and archived upstream | High | High | Reject new official Flowise pilot |
| Cloud availability or support after EOL is undefined | High | High | Do not register or upload data |
| No upstream security fixes after archive/EOL | High | High | Treat a fork as a separately governed software product |
| Prompt-mediated rather than deterministic citations | Medium | High | Require adapter evidence and negative tests in any future fork evaluation |
| Incomplete deletion across loaders, vectors, logs, and backups | High | High | Fail closed until end-to-end deletion is proven |
| Free-plan isolation insufficiently evidenced | High | High | Never use it for multiple clients |
| Combined platform/model spend stop not evidenced | Medium | High | Require independent hard caps before any live candidate |
| US East 1 and analytics/retention exposure | Medium | High | Synthetic data only; privacy review before any personal data |
| Mixed Apache/commercial licensing areas | Medium | Medium | Pin revision and perform component-level license review before forking |

## Official Sources Reviewed

- Flowise sunset and EOL: https://flowiseai.com/sunset
- Official archived repository: https://github.com/FlowiseAI/Flowise
- Official license file: https://github.com/FlowiseAI/Flowise/blob/main/LICENSE.md
- Cloud pricing: https://flowiseai.com/
- Privacy, region, analytics, retention, and deletion rights: https://flowiseai.com/privacy
- Cloud Export/Import and credential exclusion: https://docs.flowiseai.com/migration-guide/cloud-migration
- Workspaces and RBAC: https://docs.flowiseai.com/using-flowise/workspaces
- Metadata and retrieval: https://docs.flowiseai.com/using-flowise/agentflowv2
- Custom Retriever citation path: https://docs.flowiseai.com/integrations/langchain/retrievers/custom-retriever
- Document Store deletion API: https://docs.flowiseai.com/api-reference/document-store
- Credential encryption and security controls: https://docs.flowiseai.com/configuration/environment-variables

## Stop Record

The authorized public preflight is complete. No provider account or resource was created, and no data, credential, payment method, or request was sent to Flowise Cloud. Flowise is blocked from a runtime pilot under this change.
