# K3.3 Staged Authorization Record

## Status

- `record_id`: `af-ka-01-k3-3-staged`
- `version`: `3.6.0`
- `previous_version`: `3.5.0`
- `status`: `phase_1_synthetic_smoke_closed_gate_g1_open`
- `current_authorized_stage`: `none`
- `monthly_committed_spend`: `0 ILS`
- `data_scope`: `af-demo-services-he@1.0.0` synthetic only

אישור Stage אחד אינו מאשר Stage מאוחר יותר. אין BYOK, Payment, Upgrade, Subscription, real data, Production, external user, Tool, n8n או Publish באף Stage.

## Stage A — Empty Resource Configuration

May create:

- one empty four-node Chatflow;
- explicit App-level `gpt-4.1-mini` and Knowledge-level `text-embedding-3-small` selection;
- Rerank off, no Tools and no publication.

May create one empty Standard Knowledge Base only if the UI supports doing so without Upload or Indexing. Otherwise it may inspect the creation wizard and SHALL stop before submitting data; Knowledge creation moves to Stage B.

May not upload a document, Index, Test Run, call a Model, connect a key or change Workspace-wide defaults/permissions.

- `authorization`: `consumed`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approved_scope`: `Create one empty Chatflow and one empty Knowledge Base only if Dify permits it without Upload or Indexing; otherwise stop in the creation wizard.`
- `forbidden_actions`: `Upload, Indexing, Model call, Test, Publish, Credentials, Payment, Upgrade, Subscription and Workspace changes`
- `credit_ceiling`: `0 expected`; any decrease stops
- `expiry`: `expired_at_stage_stop`
- `execution_result`: `empty Chatflow and empty Knowledge Base created; configuration stopped because exact gpt-4.1-mini was unavailable`
- `evidence`: `k3-3-a-execution-evidence.md`

## Stage A1 — Versioned Model Substitution and Empty Flow Completion

May:

- replace the unavailable `gpt-4.1-mini` alias with the displayed `gpt-4.1-mini-2025-04-14` model;
- add the Knowledge Retrieval node to complete `Start → Knowledge Retrieval → LLM → Answer`;
- link only the empty `af-demo-services-he-1-0-0` Knowledge Base;
- keep Rerank off and attach no Tools.

May not upload, Index, execute a Model call, Preview, Test, publish, connect Credentials, use Payment, or change Workspace settings.

- `authorization`: `consumed`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of the exact bounded Stage A1 wording presented immediately before approval`
- `credit_ceiling`: `0 expected`; any decrease stops
- `expiry`: `expired_at_stage_stop`
- `execution_result`: `dated model selected and Knowledge Retrieval node added; empty Knowledge Base was not selectable and no document was uploaded`
- `evidence`: `k3-3-a1-execution-evidence.md`

## Stage B — One-Document Upload Preview and Indexing Pilot

May create the dedicated Standard Knowledge Base if Stage A could not create it without data. May then upload and preview only `AFD-001.md`, and Index it only if Section boundaries pass.

- `authorization`: `consumed`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of the exact bounded Stage B wording presented immediately before approval`
- `authorized_source`: `AFD-001.md`
- `authorized_sha256`: `D17DDE969830845047DF97AC826D9F065FC893BF1CBCD19837ED45ED047C149F`
- `forbidden_actions`: `AFD-002 through AFD-006, Test, Model call, Publish, Credentials, Payment and Workspace changes`
- `credit_reserve_ceiling`: `25`
- `stop_after`: one document and one recorded Credit delta
- `prerequisite`: Stage A evidence accepted
- `expiry`: `after one document and one recorded Credit delta, or at any stop condition`
- `execution_result`: `AFD-001 staged in the wizard; Dify coerced overlap 0 to minimum 1; stopped before Preview Chunk and Indexing`
- `evidence`: `k3-3-b-execution-evidence.md`

## Stage B1 — Minimum Overlap Preview and Conditional Indexing

May accept Dify's minimum Chunk overlap `1` for the already staged `AFD-001.md`, run `Preview Chunk`, and execute `Save & Process` only if the Preview preserves stable Section boundaries.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of the exact bounded Stage B1 wording presented immediately before approval`
- `authorized_source`: `AFD-001.md`
- `authorized_overlap`: `1`
- `credit_reserve_ceiling`: `25`
- `stop_after`: `one document and one recorded Credit delta`
- `forbidden_actions`: `AFD-002 through AFD-006, Retrieval Test, App Preview, Model call, Publish, Credentials, Payment and Workspace changes`
- `expiry`: `after one document and one recorded Credit delta, or at any stop condition`
- `execution_result`: `five-Chunk Preview passed; one document Indexed and Available; 20-Credit delta; 180 Credits remain`
- `evidence`: `k3-3-b1-execution-evidence.md`

## Stage B2 — Post-Index Knowledge Link and Linear Graph Completion

May link only `af-demo-services-he-1-0-0` to the existing Knowledge Retrieval node and complete `Start → Knowledge Retrieval → LLM → Answer` without executing the flow.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of the exact bounded Stage B2 wording presented immediately before approval`
- `credit_ceiling`: `0 expected`; any decrease stops
- `prerequisite`: `Stage B1 evidence accepted`
- `forbidden_actions`: `Upload, Indexing, Retrieval Test, App Preview, Model call, Publish, Tools, Credentials, Payment and Workspace changes`
- `expiry`: `expired_after_persisted_link_and_linear_graph_verification`
- `execution_result`: `dedicated Knowledge Base linked; one four-node linear graph persisted after reload; zero Credit delta; no run or publication`
- `evidence`: `k3-3-b2-execution-evidence.md`

## Stage C — Remaining Five Documents

May upload and Index only `AFD-002`–`AFD-006`, one at a time.

- `authorization`: `consumed_at_credit_guard`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `explicit authorization for K3.3-C only, sequential AFD-002 through AFD-006 indexing, 100 cumulative Credits and at least 50 Credits remaining`
- `execution_result`: `AFD-002 through AFD-005 Indexed and Available; 90-Credit Stage delta; 90 Credits remain; stopped before AFD-006 because only 10 Credits remained inside the Stage ceiling`
- `evidence`: `k3-3-c-execution-evidence.md`
- `minimum_remaining_after_forecast`: `50 Credits`
- `prerequisite`: Stage B evidence and forecast accepted

## Stage C1 — Final Approved Corpus Document

May upload, Preview and conditionally Index only `AFD-006.md`, using the frozen Stage C configuration and only if stable Section boundaries pass.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of the exact bounded K3.3-C1 wording presented immediately before approval`
- `credit_ceiling`: `30`
- `minimum_remaining_after_execution`: `50 Credits`
- `prerequisite`: Stage C evidence and a fresh Drift check accepted
- `forbidden_actions`: `Retrieval Test, App Preview, Model call, Publish, Tools, Credentials, Payment and Workspace changes`
- `execution_result`: `seven-Chunk Preview passed; AFD-006 Indexed and Available; 30-Credit delta; 60 Credits remain`
- `evidence`: `k3-3-c1-execution-evidence.md`

## Stage D — Five-Question Smoke Test

May execute exactly five preselected frozen questions in Studio Test Run using the approved configuration.

- `authorization`: `consumed_at_stop_condition`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of the exact bounded K3.3-D wording presented immediately before approval`
- `generation_model`: `gpt-4.1-mini`
- `question_ids`: `KA-E01, KA-E16, KA-E18, KA-E22, KA-E24`
- `expected_generation_credits`: `5`
- `hard_request_ceiling`: `10`, including technical retries
- `minimum_remaining_after_hard_ceiling`: `50 Credits`
- `prerequisite`: Stage C1 completion and Drift check accepted
- `execution_result`: `KA-E01 factual pass but citation-contract fail; one request consumed 6 Credits; 54 remain; stopped before KA-E16 to preserve the 50-Credit reserve`
- `evidence`: `k3-3-d-execution-evidence.md`

## Stage D1 — Versioned Citation Remediation

May change only the LLM instruction needed to require frontmatter `source_id` plus the stable Markdown heading in `[SOURCE_ID § Section]` form. No Preview, Test Run or Model request is included.

- `authorization`: `consumed_complete_after_manual_recovery`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance after explicit clarification that D1 is citation remediation only with zero Credits and no Test Run`
- `credit_ceiling`: `0 expected`; any decrease stops
- `prerequisite`: Stage D evidence accepted and a versioned prompt delta reviewed by the Owner
- `forbidden_actions`: `Retrieval Test, App Preview, Model call, Publish, Tools, Credentials, Payment, Knowledge changes and Workspace changes`
- `execution_result`: `Initial automated edit failed safely with zero Credit delta; the Owner manually restored the prompt and D1R verified the persisted configuration read-only`
- `evidence`: `k3-3-d1-execution-evidence.md`

## Stage D1R — Manual Prompt Recovery and Read-only Verification

The Owner may manually restore the approved instruction and the two structured variables. Codex may then perform read-only reload verification only.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `Owner requested verification after manual recovery`
- `credit_ceiling`: `0 expected`
- `required_variables`: `Knowledge Retrieval / result; User Input / query`
- `forbidden_actions`: `Preview, Test Run, Model call, Publish, Tools, Credentials, Payment, Knowledge changes and Workspace changes`
- `execution_result`: `Recovered prompt persisted after reload; Dify context binding points to Knowledge Retrieval / result, User Input / query is present, model and four-node graph are unchanged, app is Unpublished and 54 Credits remain`
- `evidence`: `k3-3-d1r-execution-evidence.md`

## Stage D2 — One-Question Citation Smoke Retest

May execute only `KA-E01` once in Studio Preview to verify the recovered citation instruction.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of K3.3-D2 immediately after the exact bounded wording was presented`
- `question_id`: `KA-E01`
- `question`: `באילו ימים ושעות הארגון פעיל?`
- `model_request_ceiling`: `1`
- `credit_ceiling`: `6`
- `minimum_remaining_after_execution`: `48 Credits`
- `prerequisite`: `D1R complete and fresh Drift check passes`
- `stop_after`: `one response or any stop condition`
- `forbidden_actions`: `second request, Publish, Tools, Credentials, Payment, Knowledge changes and Workspace changes`
- `execution_result`: `one response completed; factual and Hebrew pass; inline citation was [שעות פעילות] instead of [AFD-001 § שעות פעילות]; 6 Credits consumed; 48 remain; no retry`
- `evidence`: `k3-3-d2-execution-evidence.md`

## Stage D3R — Existing Run Retrieval-output Inspection

May inspect only the existing D2 Last Run and its Knowledge Retrieval output to determine whether a stable document identifier is exposed to downstream nodes.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance of K3.3-D3R after the exact zero-Credit read-only wording was presented`
- `credit_ceiling`: `0 expected`; any decrease stops
- `permitted_actions`: `open existing D2 run history; inspect Knowledge Retrieval input/output and visible metadata`
- `forbidden_actions`: `Preview, Test Run, Model call, configuration change, Indexing, Publish, Tools, Credentials, Payment, Knowledge changes and Workspace changes`
- `execution_result`: `existing D2 citation view showed three Section Chunks without source_id while Dify separately displayed AFD-001.md; zero Credit delta; 48 remain`
- `evidence`: `k3-3-d3r-execution-evidence.md`

## Stage D3P — Local Citation-remediation Planning

May create local planning and specification artifacts only, comparing deterministic Retrieval-metadata enrichment against Corpus 1.1.0. No provider action is included.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance immediately after the exact local-only K3.3-D3P wording was presented`
- `credit_ceiling`: `0`
- `execution_result`: `selected M-TEMPLATE as the approval-ready Low-Code design; no Dify change, Runtime, Indexing or Credit use`
- `evidence`: `citation-remediation-plan.md`

## Stage D3A — Metadata and Template Configuration

May add approved `source_id` document metadata and one `Citation Context` Template node, bind only visible Retrieval fields, reload-verify and stop.

- `authorization`: `consumed_partial_safe_stop`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance immediately after the exact bounded K3.3-D3A wording was presented`
- `credit_ceiling`: `0 expected`; any decrease stops
- `required_stop`: `stop if source_id or document metadata is not selectable from Knowledge Retrieval / result`
- `forbidden_actions`: `Preview, Test Run, Model call, Indexing, document-content change, Publish, Code node, Tools, Credentials, Payment and Workspace changes`
- `execution_result`: `six source_id values and one Citation Context node persisted with Knowledge Retrieval / result bound; nested source_id/document metadata was not selectable, so no guessed Jinja path or LLM prompt wiring was attempted; zero Credit delta; 48 remain`
- `evidence`: `k3-3-d3a-execution-evidence.md`

## Stage D3B — Source-backed Metadata-path Planning

May research official Dify documentation and source and create local OpenSpec planning artifacts only. No provider change is included.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance after the critical next step was defined as local-only deterministic source_id path planning with Runtime blocked`
- `credit_ceiling`: `0`
- `execution_result`: `official Dify source identifies custom metadata under metadata.doc_metadata; M-DOCMETA-TEMPLATE selected with allow-list and fail-closed behavior; no Dify change or Runtime`
- `evidence`: `citation-metadata-path-plan.md`

## Stage D3S — Source-backed Template and Manual Graph Wiring

May replace the current neutral Template with the reviewed `M-DOCMETA-TEMPLATE`, manually rewire it between Retrieval and LLM, insert only verified variable chips, reload-verify and stop.

- `authorization`: `consumed_partial_safe_stop`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `direct acceptance immediately after the exact bounded K3.3-D3S wording was presented`
- `credit_ceiling`: `0 expected`; any decrease stops
- `prerequisite`: `D3B complete; fresh drift check; Owner approves exact bounded D3S wording`
- `required_manual_action`: `LLM rich-text variable-chip insertion and graph wiring must be performed or explicitly confirmed by the Owner`
- `forbidden_actions`: `Preview, Run this step, Retrieval Test, Model call, Indexing, document-content change, Publish, Code node, Tools, Credentials, Payment and Workspace changes`
- `execution_result`: `automated Template editor replacement was non-atomic; malformed intermediate text was detected and neutral {{ results }} was restored and reload-verified; graph and prompt wiring were not attempted; zero Credit delta; 48 remain`
- `evidence`: `k3-3-d3s-execution-evidence.md`

## Stage D3SR — Manual Template Recovery and Read-only Verification

The Owner may manually paste the reviewed `M-DOCMETA-TEMPLATE` into `Citation Context`. Codex may then perform read-only Reload verification only.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `exact bounded D3SR approval for Reload and read-only verification after manual Template paste`
- `credit_ceiling`: `0`
- `forbidden_actions`: `graph change, prompt change, Preview, Run this step, Retrieval Test, Model call, Indexing, Publish, Code node, Tools, Credentials, Payment and Workspace changes`
- `execution_result`: `Owner had already invoked one Preview that returned the canonical fallback and reduced Credits from 48 to 42; D3SR itself only verified the complete fail-closed Template and Retrieval result binding read-only; app Unpublished; no additional request`

## Stage D3W — Citation Graph and Prompt Wiring

May connect `Citation Context` to `LLM 2`, remove the direct `Knowledge Retrieval → LLM 2` graph edge, preserve Retrieval Context for native attribution, and add only the verified `Citation Context / output` variable to the System instruction.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `exact bounded D3W approval excluding Preview, Runtime, Indexing and Publish`
- `credit_ceiling`: `0 expected`; any decrease stops
- `execution_result`: `five-node graph and structured prompt variable persisted after Reload; transient node deletion was immediately undone and fully reload-verified; zero Credit delta; 42 remain; app Unpublished`
- `evidence`: `k3-3-d3w-execution-evidence.md`

## Stage D3T — One-Question Citation Smoke Test

May execute only KA-E01 once in Studio Preview under a six-Credit ceiling and stop immediately after the response.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `exact bounded D3T approval for one KA-E01 Preview request, no retry, Indexing or Publish`
- `question_id`: `KA-E01`
- `question`: `באילו ימים ושעות הארגון פעיל?`
- `model_request_ceiling`: `1`
- `technical_retries`: `0`
- `credit_ceiling`: `6`
- `execution_result`: `factual, Hebrew, citation-presence and citation-correctness pass; six-Credit delta; 36 remain; app Unpublished`
- `evidence`: `k3-3-d3t-execution-evidence.md`

## Stage D3C — Local Evidence Closure

May record D3W and D3T evidence and update Tasks, Design, Staged Authorization, Manifest and Readiness locally only.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-20`
- `approval_context`: `exact bounded D3C approval for local documentation only`
- `credit_ceiling`: `0`
- `forbidden_actions`: `Dify change, Runtime, Indexing, Publish, Commit and Push`
- `execution_result`: `D3W and D3T evidence recorded; local status package aligned; no provider action`

## Stage D3T2 — One Additional KA-E01 Preview

May execute only `KA-E01` once in Studio Preview under a six-Credit ceiling and stop immediately after the response.

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-24`
- `approval_context`: `exact bounded approval for one KA-E01 Preview request, no retry, Indexing or Publish`
- `question_id`: `KA-E01`
- `question`: `באילו ימים ושעות הארגון פעיל?`
- `model_request_ceiling`: `1`
- `technical_retries`: `0`
- `credit_ceiling`: `6`
- `execution_result`: `Workflow succeeded; factual, Hebrew and both citation checks passed; post-run Credit balance not visible and remains unverified`
- `evidence`: `phase-1-synthetic-smoke-closure-evidence.md`

## Phase 1 Closure — Synthetic Smoke Prototype Only

- `authorization`: `consumed_complete`
- `approved_by`: `Owner (Yulush)`
- `approved_on`: `2026-08-24`
- `approved_scope`: `local documentation and closure of Phase 1 as a Synthetic Smoke Prototype only`
- `forbidden_actions`: `Dify change, additional Runtime, Indexing, Publish, Commit and Push`
- `execution_result`: `Phase 1 smoke scope closed locally; Gate G1 and the frozen 25-question evaluation remain open`
- `evidence`: `phase-1-synthetic-smoke-closure-evidence.md`

## Stage E — Scored Evaluation

Covered by K4, not by K3.3-A through K3.3-D.

- `authorization`: `not_granted`
- `questions`: `25`
- `technical_retries_max`: `5`
- `measured_generation_credits_per_response`: `6`
- `estimated_generation_credits_before_retries`: `150`
- `safe_capacity_target_with_retries`: `180`
- `credits_available`: `unverified after D3T2; last recorded value was 36 before the additional request`
- `safe_capacity_deficit`: `unverified; at least 144 against the last recorded pre-D3T2 value`
- `capacity_plan`: `k4-0-capacity-evaluation-plan.md`
- `prerequisite`: K4.1C read-only capacity/Drift gate and a later separate K4.3E Runtime approval

## Global Stop Conditions

Stop before or during any Stage if:

- Workspace is not Sandbox or Membership is not `1 / 1` Owner-only;
- paid quota, Billing management, BYOK or Payment becomes available/connected unexpectedly;
- Credits or API usage differ from the recorded pre-stage state without explanation;
- selected Model/provider/plugin differs from the approved Configuration;
- Rerank, Tool, Trigger, external integration or publication is enabled;
- corpus Hash, tenant, language, classification or source status differs;
- Chunk preview crosses Source/Section boundaries;
- any real, personal, confidential, medical, financial or credential data appears;
- cost cannot be measured or request ceiling cannot be enforced.

## Approval Syntax

The Owner approval SHALL name exactly one Stage. Example for the smallest next action:

> מאשרת K3.3-A בלבד: יצירת Chatflow ריק ו-Knowledge Base ריק רק אם Dify מאפשר זאת ללא Upload/Indexing; אחרת לעצור ב-Wizard. ללא Upload, Indexing, Model call, Test, Publish, Credentials, Payment או שינוי Workspace.

Any shorter or ambiguous approval is interpreted as no authorization for external changes.
