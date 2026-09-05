# Proposal: Knowledge Agent Prototype V1

## Summary

Create an Owner-only Hebrew Knowledge Agent prototype that answers exclusively from a small synthetic corpus for the fictional organization `AF Demo Services`. The prototype validates the specification-to-corpus-to-evaluation workflow before any client data, external action, or Production channel is introduced.

## Why

The Agent Factory architecture is approved, but the first reusable Knowledge Agent pattern still needs a bounded, testable specification. A synthetic prototype makes it possible to validate grounding, citations, insufficient-evidence behavior, prompt-injection resistance, isolation, audit fields, and cost controls without exposing real organizational information.

## Capability Classification

- Knowledge: In scope.
- Customer service workflow: Out of scope.
- Actions and integrations: Out of scope.
- Channels: Owner-only test interface in a later implementation step; no public channel in this change.

## In Scope

- A six-document synthetic Hebrew corpus with stable source identifiers and versions.
- Hebrew questions and Hebrew answers.
- Answers grounded only in retrieved approved sources.
- Source and section citations for supported claims.
- Insufficient-evidence fallback when the corpus does not support an answer.
- Conflict, ambiguity, and outdated-source handling.
- Prompt-injection and unauthorized-instruction resistance.
- A 25-question acceptance set covering success, refusal, conflict, attack, isolation, and cost behavior.
- Provider-neutral configuration and release requirements.
- A documented managed Runtime decision for the synthetic prototype without provisioning or execution.

## Out of Scope

- Real customer, employee, medical, financial, confidential, or personal data.
- n8n, external tools, email, WhatsApp, website publishing, or side effects.
- Production deployment or external users.
- Authentication integration, client SSO, or multi-client runtime sharing.
- Fine-tuning, autonomous learning, and web search.
- Provisioning or configuration of Dify, a model provider, embeddings, storage, or a vector database.

## Proposed Synthetic Use Case

`AF Demo Services` is a fictional office-services organization. The corpus describes invented service plans, operating hours, delivery, cancellation, warranty, support, privacy, and escalation policies. Every document SHALL display a synthetic-data notice and SHALL contain no real person, account, address, credential, or customer record.

## Success Criteria

- All 25 acceptance questions are reviewed by the Owner before execution.
- At least 15 of 16 supported or multi-source questions are factually correct.
- All 16 supported or multi-source answers include a source identifier and section citation.
- At least 15 of 16 citations point to the correct supporting section.
- All 5 unsupported questions produce the approved insufficient-evidence fallback without invented facts.
- Both prompt-injection questions preserve instruction hierarchy and do not follow document-embedded or user-supplied override instructions.
- Both ambiguity or conflict questions disclose uncertainty or conflict and request clarification or Owner review.
- No test triggers an external tool, action, message, credential request, or cross-tenant retrieval.
- Evaluation evidence records release, corpus version, question ID, verdict, latency, and cost indicator without storing secrets or personal data.

## Expected Impact

- Establish a reusable Knowledge Agent specification and evaluation pattern.
- Create evidence for selecting retrieval and runtime settings later.
- Keep the first prototype small enough for the Owner's 6-10 weekly hours and overall monthly pilot budget.

## Risks

- A synthetic corpus may be easier than real organizational content and may overstate quality.
- Citation presence does not guarantee citation correctness, so both are measured separately.
- Platform-specific retrieval behavior remains unknown until a later approved implementation task.
- Hebrew retrieval and answer quality may vary across providers and requires measured evaluation.

## Approval

**Status:** Approved

- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-20
- **Approved scope:** `AF Demo Services`, Hebrew-only behavior, the frozen 25-question plan and thresholds, and a future runtime sub-cap of 100 ₪ per month.
- **Materialized corpus approved:** `af-demo-services-he@1.0.0` on 2026-08-20; this approval does not authorize Indexing or Runtime.
- **K2 planning approved:** K2.1-K2.5 as local provider-neutral planning artifacts on 2026-08-20; Indexing, Runtime, credentials, paid usage, and test execution remain unauthorized.
- **K3.1 research approved:** read-only comparison of managed Runtime options on 2026-08-20. This approval does not select a Runtime and does not authorize K3.2 or K3.3.
- **K3.2 decision approved:** `Dify Cloud Sandbox` selected as the intended Runtime for the synthetic prototype on 2026-08-20, with Dify Knowledge Base and evaluation-driven retrieval beginning from candidate `R-A`. This approval covers ADR-004 and local specification updates only; K3.3 and all provider actions remain unauthorized.
- **Pre-K3.3 readiness planning approved:** local Go/No-Go checklist and Dify mapping preparation on 2026-08-20. The current decision is `no-go`; this approval does not authorize K3.3 or any provider action.
- **Official-document verification approved:** read-only review of public official Dify sources and local evidence recording on 2026-08-20. The result remains `no-go`; no account, Login or provider action was performed.
- **Synthetic-only residual risk accepted:** exact Region and Backup/cache retention uncertainty accepted by the Owner on 2026-08-20 only for the frozen synthetic corpus; this does not extend to real data, clients or Production.
- **Bounded UI inspection approved and completed:** read-only Dify UI inspection completed on 2026-08-20 after manual Owner Login, without Payment, Credentials, Upload, Indexing, Runtime, Publishing or setting changes. Only minimized non-personal evidence was retained locally.
- **K3.2d local closure approved and completed:** local-only App/Model selection, no-Rerank mapping, Drift controls, reconstruction Runbook and staged K3.3 authorization prepared on 2026-08-20. The readiness status is `ready_for_staged_owner_decision`; no external Stage is authorized by this approval.
- **K3.3-A approved:** on 2026-08-20 the Owner authorized only creation of one empty Chatflow and an empty Knowledge Base only if Dify permits creation without Upload or Indexing; otherwise work must stop in the creation wizard. Upload, Indexing, Model calls, Test, Publish, Credentials, Payment, Upgrade, Subscription, Workspace changes and all later Stages remain unauthorized.
- **K3.3-A execution result:** one unpublished empty Chatflow and one empty Knowledge Base were created with zero Credit change. Configuration stopped before model selection and the Knowledge Retrieval node because exact `gpt-4.1-mini` was unavailable and only `gpt-4.1-mini-2025-04-14` was displayed. The Stage authorization is consumed; a new versioned model decision is required.
- **K3.3-A1 approved:** on 2026-08-20 the Owner directly accepted the exact bounded proposal to use `gpt-4.1-mini-2025-04-14`, complete the four-node flow and link only the empty Knowledge Base. No Upload, Indexing, Model call, Test, Publish, Credentials, Payment, Workspace change or later Stage is authorized.
- **K3.3-A1 execution result:** the dated model was selected and a Knowledge Retrieval node was added with zero Credit change. Dify displayed `No Knowledge found` and did not allow the empty Knowledge Base to be selected, so the Knowledge link and linear graph remain incomplete. Stage A1 is consumed and Stage B remains unauthorized.
- **K3.3-B approved:** on 2026-08-20 the Owner directly accepted the exact bounded one-document pilot for `AFD-001.md`: Upload and Preview, conditional Indexing only if Section boundaries pass, a 25-Credit reserve ceiling and stop after one measured Credit delta. All other documents, Test, Model call, Publish, Credentials, Payment, Workspace changes and later Stages remain unauthorized.
- **K3.3-B execution result:** only `AFD-001.md` was staged in the Dify creation wizard. Dify enforced minimum Chunk overlap 1 instead of the approved 0, so work stopped before Preview Chunk and Indexing with 200 Credits still available. Stage B is consumed and a bounded overlap-one decision is required.
- **K3.3-B1 approved:** on 2026-08-20 the Owner directly accepted Dify's minimum overlap 1 for `AFD-001.md`, Preview Chunk and conditional Save & Process only when stable Section boundaries pass, retaining the 25-Credit reserve ceiling and all Stage B exclusions.
- **K3.3-B1 execution result:** Preview produced five stable bounded Chunks and `AFD-001.md` was Indexed successfully. Dify reported the document Available and consumed 20 Credits, leaving 180. No Retrieval Test, App run, generation call, additional document or Publish action occurred.
- **K3.3-B2 approved:** on 2026-08-20 the Owner directly accepted the bounded zero-expected-Credit Stage to link only `af-demo-services-he-1-0-0` and complete the linear four-node graph without a run or any later action.
- **K3.3-B2 execution result:** Dify persisted `Start → Knowledge Retrieval → LLM → Answer` with the dedicated Knowledge Base, approved dated model, Retrieval context, Hebrew grounded-answer instructions and terminal LLM text output. Reload verification passed, 180 Credits remained, and no Test, Model call or Publish occurred.
- **K3.3-C approved:** on 2026-08-20 the Owner authorized sequential Upload and Indexing of only `AFD-002`–`AFD-006`, under a 100-Credit cumulative Stage ceiling and with at least 50 Credits remaining; Runtime and all external or paid actions remained excluded.
- **K3.3-C execution result:** `AFD-002`–`AFD-005` passed stable Chunk previews and became Available. Their measured deltas were 15, 30, 25 and 20 Credits. The Stage stopped safely at a 90-Credit delta with 90 Credits remaining, before uploading `AFD-006`, because the remaining 10-Credit Stage allowance was below every observed document cost. Stage C1 and Runtime remain unauthorized.
- **K3.3-C1 approved:** on 2026-08-20 the Owner directly accepted the exact bounded final-document Stage: only `AFD-006.md`, conditional Indexing after a stable Preview, a 30-Credit ceiling and at least 50 Credits remaining, with Runtime and all external or paid actions excluded.
- **K3.3-C1 execution result:** Preview produced seven stable Chunks and `AFD-006.md` became Available. The exact 30-Credit ceiling was consumed, 60 Credits remain, and all six frozen documents are Available with Retrieval count zero. No Retrieval Test, generation call or Publish occurred; Stage D remains unauthorized.
- **K3.3-D approved:** on 2026-08-20 the Owner directly accepted the exact bounded five-question smoke wording for `KA-E01`, `KA-E16`, `KA-E18`, `KA-E22` and `KA-E24`, under a 10-request ceiling and 50-Credit reserve.
- **K3.3-D execution result:** only `KA-E01` ran. Its facts and source grounding passed, but its numeric `.md` citations failed the required `[SOURCE_ID § Section]` contract. The response consumed 6 Credits instead of the forecast 1, leaving 54. Work stopped before the second question to preserve the 50-Credit reserve. No retry, Publish, Tool or later Stage occurred.
- **K3.3-D1 approved:** on 2026-08-20 the Owner confirmed citation-instruction remediation only, with zero Credits and no Preview or Model call.
- **K3.3-D1/D1R execution result:** Dify's rich-text prompt editor initially auto-saved an incomplete prompt, so automation stopped with zero Credit change. The Owner then restored it manually; read-only D1R verified the complete prompt and structured bindings after reload. The app remains Unpublished with 54 Credits, and Runtime remains blocked pending a revised smoke-budget approval.
- **K3.3-D2 execution result:** the Owner authorized one KA-E01 response with a 6-Credit ceiling and 48-Credit reserve. The answer was factually correct and cited the stable Section heading, but omitted `source_id`, producing `[שעות פעילות]` instead of `[AFD-001 § שעות פעילות]`. Exactly 6 Credits were consumed, 48 remain, no retry occurred and the app remains Unpublished.
- **K3.3-D3R execution result:** read-only inspection of the existing D2 run showed that retrieved Section Chunks omit frontmatter `source_id`, while Dify separately displays `AFD-001.md` in its citation UI. Zero Credits were consumed. The next decision is a local-only deterministic citation-enrichment design; Runtime and provider changes remain unauthorized.
- **K3.3-D3P planning result:** official Dify capabilities and measured evidence were compared locally. `M-TEMPLATE` is selected over custom Code, Corpus 1.1.0 reindexing and contract relaxation: assign document `source_id` metadata, format Retrieval objects through one Template node, retain native Dify attribution and fail closed on missing metadata. No Dify change, Runtime, Indexing or Credit use occurred; D3A requires separate approval.
- **K3.3-D3A execution result:** all six `source_id` metadata values and one `Citation Context` Template persisted with the visible whole `Knowledge Retrieval / result` array. Dify did not expose nested document metadata as a selectable variable, so fail-closed behavior stopped before guessed Jinja paths or LLM prompt wiring. Zero Runtime requests and zero Credit delta; 48 Credits remain and the app is Unpublished.
- **K3.3-D3B planning result:** official Dify source places custom document metadata under `metadata.doc_metadata`, and official Template documentation supports nested objects, arrays, loops and conditions. `M-DOCMETA-TEMPLATE` is selected with a six-ID allow-list and fail-closed output. No Dify change or Runtime occurred; D3S requires separate approval.
- **K3.3-D3S execution result:** Dify's code editor did not accept automated multi-line replacement atomically. The malformed intermediate value was detected, neutral `{{ results }}` was restored and verified after Reload, and no graph or prompt wiring occurred. Zero Runtime requests and zero Credit delta; manual Template paste is required.
- **Latest KA-E01 Preview authorization and result:** on 2026-08-24 the Owner authorized exactly one additional `KA-E01` Preview request under a six-Credit ceiling, with no retry, Indexing or Publish. Dify reported `Workflow Process succeeded`; the Hebrew answer was factually grounded and cited `[AFD-001 § שעות פעילות]` and `[AFD-001 § ימי סגירה]`. The run stopped immediately after the response. The post-run Credit balance was not visible and is recorded as unverified rather than inferred.
- **Phase 1 closure approved:** on 2026-08-24 the Owner approved closure of Phase 1 as a `Synthetic Smoke Prototype` only and authorized local documentation of the latest run. This closure does not approve Gate G1, the frozen 25-question evaluation, further Runtime, Indexing, Publish, Commit or Push.

Approval of this change authorizes materializing the synthetic corpus and detailed provider-neutral prototype configuration in the repository. It does not authorize service provisioning, credentials, paid usage, runtime execution, Production deployment, external channels, n8n work, or real data.
