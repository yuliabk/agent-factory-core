# Tasks: Knowledge Agent Prototype V1

## 0. Specification and Owner Gate

- [x] K0.1 Draft the bounded Knowledge Agent proposal and exclusions. Requirements: KA-101, KA-107, KA-108.
- [x] K0.2 Define provider-neutral retrieval, answer, citation, fallback, security, audit, cost, and rollback design. Requirements: KA-102, KA-103, KA-104, KA-105, KA-106, KA-110, KA-111.
- [x] K0.3 Define the six-document synthetic corpus plan and version rules. Requirements: KA-101, KA-105.
- [x] K0.4 Freeze the proposed 25-question evaluation plan and thresholds. Requirements: KA-109.
- [x] K0.5 Obtain Owner approval for the proposed use case, corpus, Hebrew-only scope, thresholds, and 100 ₪ runtime sub-cap. Approval permits local corpus materialization only; runtime remains separately gated. Requirements: KA-101, KA-109, KA-111.

## 1. Synthetic Corpus Materialization

- [x] K1.1 Create `AFD-001` through `AFD-006` from the approved canonical facts, with stable headings and synthetic-data notices. Requirements: KA-101.
- [x] K1.2 Create the corpus manifest with source, document, status, language, tenant, classification, and version metadata. Requirements: KA-101, KA-105.
- [x] K1.3 Review the corpus for accidental real names, contact details, personal data, sensitive data, credentials, URLs, and hidden instructions. Requirements: KA-101, KA-106, KA-110.
- [x] K1.4 Record corpus version evidence and obtain Owner approval of `af-demo-services-he@1.0.0`. Approval covers the corpus version only; Indexing and Runtime remain unauthorized. Requirements: KA-101, KA-109.

## 2. Provider-neutral Prototype Configuration

- [x] K2.1 Define versioned request, answer, citation, fallback, and refusal configuration artifacts without credentials. Requirements: KA-102, KA-103, KA-104, KA-107, KA-108.
- [x] K2.2 Define candidate retrieval parameters and an experiment matrix rather than selecting them without evidence. Requirements: KA-102, KA-103, KA-109.
- [x] K2.3 Define fixed tenant, Owner actor, source-status filter, and cross-tenant negative checks. Requirements: KA-101, KA-108.
- [x] K2.4 Define minimized evaluation record schema and retention behavior. Requirements: KA-110.
- [x] K2.5 Define request limits, measurable cost indicators, stop policy, and approved runtime budget cap. Requirements: KA-111.

## 3. Runtime Decision and Separate Authorization

- [x] K3.1 Compare eligible managed runtime options against Hebrew retrieval quality, isolation, export, deletion, region, cost controls, and Owner effort. Research artifact: `runtime-options-comparison.md`. No Runtime was selected during K3.1 and no provider action was performed; the later selection is recorded in K3.2. Requirements: KA-101, KA-108, KA-110, KA-111.
- [x] K3.2 Record `Dify Cloud Sandbox` and Dify Knowledge Base with evaluation-driven `R-A` first mapping in ADR-004. The decision is local only and does not authorize provider action. Requirements: KA-109, KA-111.
- [x] K3.2a Prepare the local Dify mapping and K3.3 Go/No-Go readiness checklist. Current decision remains `no-go`; no provider action was performed. Requirements: KA-101, KA-107, KA-108, KA-109, KA-110, KA-111.
- [x] K3.2b Verify public official Dify documentation and record provider-specific evidence locally. The result is partial evidence and `no-go`; no account, Login or provider action was performed. Evidence: `configuration/dify-official-evidence.md`. Requirements: KA-101, KA-108, KA-110, KA-111.
- [x] K3.2c Complete the authorized read-only Dify UI inspection after manual Owner Login. Evidence confirms one Owner, Sandbox, zero Apps/Documents/usage, no visible BYOK or external integrations, and records default-model/tool Drift risks without retaining account data. No setting, Payment, Credential, Upload, Indexing, Runtime or Publishing action was performed. Evidence: `configuration/dify-ui-inspection-evidence.md`. Requirements: KA-108, KA-110, KA-111.
- [x] K3.2d Prepare the local closure package for Chatflow + `gpt-4.1-mini` + `text-embedding-3-small`, no-Rerank mapping, Provider Drift controls, manual reconstruction and staged K3.3 authorization. No Dify action was performed or authorized. Evidence: `configuration/k3-2d-closure-package.md`. Requirements: KA-107, KA-108, KA-109, KA-110, KA-111.
- [x] K3.3 Obtain explicit Owner approval for exactly one Stage before each provider action. Separate approvals were recorded through K3.3-D3T; every later provider action remains separately gated. Requirements: KA-101, KA-111.
- [ ] K3.3-A Create and configure the bounded empty resources. One unpublished empty Chatflow and one empty Knowledge Base were created with zero Credit change; configuration stopped before model selection and the Knowledge Retrieval node because exact `gpt-4.1-mini` was unavailable. Evidence: `configuration/k3-3-a-execution-evidence.md`. Requirements: KA-107, KA-108, KA-111.
- [ ] K3.3-A1 Apply the Owner-approved dated model substitution, complete the four-node empty flow and link only the empty Knowledge Base. The model and node were configured with zero Credit change, but Dify did not expose the empty Knowledge Base and the linear flow remains incomplete. Evidence: `configuration/k3-3-a1-execution-evidence.md`. Requirements: KA-107, KA-108, KA-111.
- [ ] K3.3-B Upload and Preview only `AFD-001.md`; Index only if stable Section boundaries pass, reserve no more than 25 Credits, then stop after one recorded Credit delta. The file was staged, but Dify forced minimum overlap 1 and work stopped before Preview/Indexing. Evidence: `configuration/k3-3-b-execution-evidence.md`. Requirements: KA-101, KA-105, KA-108, KA-111.
- [x] K3.3-B1 Accept overlap 1 for the staged `AFD-001.md`, verify the five-Chunk Preview and Index one document under the 25-Credit reserve ceiling. Actual delta: 20 Credits; 180 remain. Evidence: `configuration/k3-3-b1-execution-evidence.md`. Requirements: KA-101, KA-105, KA-108, KA-111.
- [x] K3.3-B2 Link the Indexed Knowledge Base and persist one linear `Start → Knowledge Retrieval → LLM → Answer` graph without a run. Zero Credit delta; 180 remain. Evidence: `configuration/k3-3-b2-execution-evidence.md`. Requirements: KA-107, KA-108, KA-111.
- [x] K3.3-C Upload and Index sequentially under the 100-Credit Stage ceiling and 50-Credit reserve rule. `AFD-002`–`AFD-005` passed Preview and became Available; actual Stage delta was 90 Credits and work stopped before `AFD-006`. Evidence: `configuration/k3-3-c-execution-evidence.md`. Requirements: KA-101, KA-105, KA-108, KA-111.
- [x] K3.3-C1 Preview and conditionally Index only `AFD-006.md` under a 30-Credit ceiling and 50-Credit reserve. Seven stable Chunks passed; the document is Available, 30 Credits were consumed and 60 remain. Evidence: `configuration/k3-3-c1-execution-evidence.md`. Requirements: KA-101, KA-105, KA-108, KA-111.
- [ ] K3.3-D Run exactly five frozen-question Studio smoke tests under the approved guard. The Stage stopped after KA-E01: factual pass, citation-contract fail, 6-Credit delta and 54 remaining. KA-E16, KA-E18, KA-E22 and KA-E24 were not run. Evidence: `configuration/k3-3-d-execution-evidence.md`. Requirements: KA-102, KA-103, KA-104, KA-105, KA-106, KA-107, KA-108, KA-109, KA-110, KA-111.
- [x] K3.3-D1 Apply the approved versioned citation-instruction remediation with zero expected Credits and no Test Run. The initial edit failed safely; manual recovery completed the remediation. Evidence: `configuration/k3-3-d1-execution-evidence.md`, `configuration/k3-3-d1r-execution-evidence.md`. Requirements: KA-103, KA-109, KA-111.
- [x] K3.3-D1R Manually restore the approved System instruction plus `Knowledge Retrieval / result` and `User Input / query`, then perform read-only reload verification. Evidence: `configuration/k3-3-d1r-execution-evidence.md`. Requirements: KA-102, KA-103, KA-104, KA-106, KA-107, KA-109, KA-111.
- [x] K3.3-D2 Retest only KA-E01 under one request, 6-Credit ceiling and 48-Credit reserve. Factual/Hebrew pass; citation contract failed with `[שעות פעילות]`; 48 Credits remain and no retry occurred. Evidence: `configuration/k3-3-d2-execution-evidence.md`. Requirements: KA-102, KA-103, KA-104, KA-106, KA-107, KA-109, KA-111.
- [x] K3.3-D3R Inspect the existing D2 Last Run and visible Retrieval evidence read-only. Section Chunks omit `source_id`; Dify separately displays `AFD-001.md`; zero Credit delta and 48 remain. Evidence: `configuration/k3-3-d3r-execution-evidence.md`. Requirements: KA-103, KA-107, KA-109, KA-111.
- [x] K3.3-D3P Compare deterministic Retrieval-metadata enrichment with Corpus 1.1.0 locally only. Select `M-TEMPLATE`, define fail-closed behavior, cost and rollback. Evidence: `configuration/citation-remediation-plan.md`. Requirements: KA-103, KA-104, KA-107, KA-109, KA-111.
- [ ] K3.3-D3A After separate approval only, add six `source_id` metadata values and one `Citation Context` Template node, bind visible Retrieval fields, reload-verify and stop with zero Runtime requests. Partial safe stop: six values and the whole visible `result` array persisted, but nested document metadata was not selectable and no LLM wiring was attempted. Evidence: `configuration/k3-3-d3a-execution-evidence.md`. Requirements: KA-103, KA-104, KA-107, KA-109, KA-111.
- [x] K3.3-D3B Research the opaque Retrieval metadata object locally against official Dify documentation and source. Select the source-backed `metadata.doc_metadata.source_id` path, allow-list and fail-closed Template without provider changes. Evidence: `configuration/citation-metadata-path-plan.md`. Requirements: KA-103, KA-104, KA-107, KA-111.
- [ ] K3.3-D3S After separate approval only, replace the neutral Template with `M-DOCMETA-TEMPLATE`, manually rewire `Citation Context` between Retrieval and LLM, add only verified variable chips, reload-verify and stop without Runtime. Partial safe stop: automated editor replacement was non-atomic; `{{ results }}` was restored and reload-verified before any wiring. Evidence: `configuration/k3-3-d3s-execution-evidence.md`. Requirements: KA-103, KA-104, KA-106, KA-107, KA-111.
- [x] K3.3-D3SR After the Owner manually pasted the reviewed Template, perform read-only Reload verification and stop. The allow-list, `metadata.doc_metadata.source_id`, evidence blocks, fallback and Retrieval binding persisted; no graph, prompt or Runtime change occurred. Requirements: KA-103, KA-104, KA-107, KA-111.
- [x] K3.3-D3W Rewire the persisted Template between Retrieval and LLM, preserve Retrieval Context for native attribution, insert `Citation Context / output` in the System prompt, reload-verify and stop without Runtime. Evidence: `configuration/k3-3-d3w-execution-evidence.md`. Requirements: KA-103, KA-104, KA-106, KA-107, KA-111.
- [x] K3.3-D3T Run only KA-E01 once under a six-Credit ceiling with no retry. Factual grounding, Hebrew and both inline citations passed; six Credits were consumed and 36 remain. Evidence: `configuration/k3-3-d3t-execution-evidence.md`. Requirements: KA-102, KA-103, KA-104, KA-107, KA-109, KA-111.
- [x] K3.3-D3C Record D3W and D3T evidence and close the local status package without Dify, Runtime, Indexing, Publish, Commit or Push. Requirements: KA-103, KA-109, KA-110, KA-111.

## 4. Authorized Prototype and Evaluation

- [x] K4.0 Prepare the local capacity and 25-question evaluation plan, including measured capacity, alternatives, costs, risks, stop controls and a separate approval gate. No Dify action, Runtime, Payment, Credential, Commit or Push was authorized or performed. Evidence: `configuration/k4-0-capacity-evaluation-plan.md`. Requirements: KA-109, KA-110, KA-111.
- [ ] K4.1 Provision only the approved non-production synthetic tenant and disable external tools and actions. Requirements: KA-107, KA-108.
- [ ] K4.2 Index only the approved corpus version and verify that superseded, withdrawn, conflict-fixture, and foreign-tenant sources are excluded by default. Requirements: KA-101, KA-105, KA-108.
- [ ] K4.3 Run the frozen 25-question set and preserve per-question evidence. Requirements: KA-102, KA-103, KA-104, KA-105, KA-106, KA-107, KA-108, KA-109, KA-110, KA-111.
- [ ] K4.4 Record failures without deleting them; version any configuration change and rerun the complete relevant set. Requirements: KA-109.

## 5. Review and Release Gate G1

- [ ] K5.1 Verify all mandatory safety thresholds and quality minimums. Requirements: KA-103, KA-104, KA-105, KA-106, KA-107, KA-108, KA-109.
- [ ] K5.2 Review actual cost, latency, failure, citation, and fallback evidence with the Owner. Requirements: KA-109, KA-110, KA-111.
- [ ] K5.3 Create a versioned release manifest and rollback target without secrets or client content. Requirements: KA-109, KA-110.
- [ ] K5.4 Obtain Owner approval for Gate G1. This does not authorize Production, external users, real data, n8n, or external actions. Requirements: KA-109, KA-111.
