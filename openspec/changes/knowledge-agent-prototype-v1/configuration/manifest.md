# Configuration Planning Manifest

## Status

- `configuration_set_id`: `af-ka-01-planning`
- `configuration_version`: `4.0.0`
- `previous_configuration_version`: `3.9.0`
- `change_id`: `knowledge-agent-prototype-v1`
- `corpus`: `af-demo-services-he@1.0.0`
- `evaluation_set`: `ka-prototype-he-v1`
- `status`: `partially_materialized_synthetic_prototype`
- `approved_by`: `Owner (Yulush)`
- `approval_date`: `2026-08-20`
- `indexing_status`: `all_six_documents_indexed_available`
- `runtime_status`: `d3t_smoke_pass_36_remaining_full_evaluation_blocked_unpublished`
- `credentials_status`: `not_connected`
- `paid_execution_status`: `not_authorized`
- `intended_runtime`: `Dify Cloud Sandbox`
- `runtime_decision_status`: `selected_partially_materialized`
- `runtime_decision_reference`: `docs/adr-004-dify-cloud-sandbox-runtime.md`
- `k3_3_readiness_status`: `k4_0_capacity_plan_complete_k4_1c_not_granted`
- `k3_3_readiness_reference`: `configuration/k3-3-readiness-checklist.md`
- `k4_1c_status`: `gate_request_drafted_pending_owner_approval`
- `k4_1c_reference`: `configuration/k4-1c-capacity-verification-request.md`
- `dify_evidence_status`: `official_partial_ui_complete_residual_bounded`
- `dify_evidence_reference`: `configuration/dify-official-evidence.md`
- `residual_region_retention_risk`: `accepted_synthetic_only`
- `ui_inspection_status`: `complete_read_only`
- `ui_inspection_reference`: `configuration/dify-ui-inspection-evidence.md`
- `k3_2d_status`: `complete_local_only`
- `k3_3_current_authorized_stage`: `none`
- `k3_3_stage_a_status`: `consumed_partial_blocked_model_drift`
- `k3_3_stage_a1_status`: `consumed_partial_blocked_empty_knowledge_not_selectable`
- `k3_3_stage_b_status`: `consumed_partial_blocked_minimum_overlap_drift`
- `k3_3_stage_b1_status`: `complete_20_credit_delta`
- `k3_3_stage_b2_status`: `complete_zero_credit_delta`
- `k3_3_stage_c_status`: `stopped_safely_90_credit_delta_before_AFD-006`
- `k3_3_stage_c1_status`: `complete_30_credit_delta_60_remaining`
- `k3_3_stage_d_status`: `stopped_after_one_request_6_credit_delta_citation_fail_54_remaining`
- `k3_3_stage_d1_status`: `complete_after_manual_recovery_zero_credit_delta`
- `k3_3_stage_d1r_status`: `complete_read_only_verified_54_remaining`
- `k3_3_stage_d2_status`: `complete_one_request_6_credit_delta_citation_fail_48_remaining`
- `k3_3_stage_d3r_status`: `complete_zero_credit_metadata_boundary_identified_48_remaining`
- `k3_3_stage_d3p_status`: `complete_local_only_m_template_selected`
- `k3_3_stage_d3a_status`: `partial_safe_stop_metadata_values_and_template_persisted_nested_path_unavailable_zero_credit`
- `k3_3_stage_d3b_status`: `complete_local_only_source_backed_doc_metadata_path_selected`
- `k3_3_stage_d3s_status`: `partial_safe_stop_neutral_template_restored_zero_credit`
- `k3_3_stage_d3sr_status`: `complete_read_only_template_verified_42_remaining`
- `k3_3_stage_d3w_status`: `complete_five_node_graph_prompt_variable_zero_credit_42_remaining`
- `k3_3_stage_d3t_status`: `complete_one_request_citation_pass_6_credit_delta_36_remaining`
- `k3_3_stage_d3c_status`: `complete_local_evidence_closure_no_provider_action`
- `k4_0_status`: `complete_local_capacity_plan_owner_gate_required`
- `k4_0_reference`: `configuration/k4-0-capacity-evaluation-plan.md`
- `provider_resource_status`: `one_unpublished_five_node_chatflow_and_one_knowledge_base_with_all_six_documents_indexed`

## Authorized Planning Scope

The provider-neutral artifacts cover K2.1-K2.5. ADR-004 selected Dify Cloud Sandbox for K3.2. Version `3.9.0` added the local K4.0 capacity decision to the completed D3SR, D3W and D3T record. Version `4.0.0` drafts the bounded `K4.1C` gate-approval request text so the Owner can grant a read-only Credit-balance/Drift verification before any K4.1 provisioning; the gate itself remains `not_granted` and no provider action was performed to produce it. The persisted flow is `User Input → Knowledge Retrieval → Citation Context → LLM 2 → Answer 2`; KA-E01 passed factual, Hebrew and citation checks. The app remains Unpublished with 36 Credits. K4.0 selects waiting for a fresh monthly Sandbox allowance, followed by a separately approved read-only K4.1C gate. Further Runtime and the 25-question evaluation remain unauthorized.

## Artifact Set

| Artifact | Version | Purpose |
|---|---|---|
| `request-answer-contract.md` | `1.0.0` | Request, response, citation, fallback and refusal contracts |
| `retrieval-experiment-matrix.md` | `1.2.0` | Candidate retrieval configurations and measured Dify R-A mapping |
| `access-policy.md` | `1.0.0` | Fixed tenant, Owner actor and source-eligibility policy |
| `evaluation-record-contract.md` | `1.0.0` | Minimized evidence schema and retention rules |
| `cost-control-plan.md` | `1.7.0` | 180-Credit safe capacity target and renewal strategy |
| `k4-0-capacity-evaluation-plan.md` | `1.0.0` | 25-question capacity, alternatives, costs, risks and future gates |
| `k4-1c-capacity-verification-request.md` | `1.0.0` | Bounded K4.1C gate-approval text, forbidden actions and evidence fields; not yet granted |
| `citation-remediation-plan.md` | `1.0.0` | Candidate comparison, selected M-TEMPLATE design and fail-closed contract |
| `citation-metadata-path-plan.md` | `1.0.0` | Source-backed doc_metadata path, reviewed Template candidate and D3S gate |
| `k3-3-readiness-checklist.md` | `3.6.0` | K4.0 capacity strategy and ungranted K4.1C gate |
| `dify-official-evidence.md` | `1.1.0` | Official evidence, unauthenticated UI checkpoint, gaps and local constraints |
| `dify-ui-inspection-evidence.md` | `1.0.0` | Minimized authenticated UI evidence without account data or screenshots |
| `k3-2d-closure-package.md` | `2.3.0` | D3S editor safe stop and manual recovery boundary |
| `dify-reconstruction-runbook.md` | `1.1.0` | Manual reconstruction, measured R3 settings, rollback and deletion sequence |
| `k3-3-staged-authorization.md` | `3.6.0` | D3 closure, K4.0 capacity prerequisite and drafted K4.1C gate; no current stage |
| `k3-3-a-execution-evidence.md` | `1.0.0` | Minimized empty-resource evidence and model Drift stop |
| `k3-3-a1-execution-evidence.md` | `1.0.0` | Dated-model, empty Retrieval node and platform-constraint evidence |
| `k3-3-b-execution-evidence.md` | `1.0.0` | One-document staging and minimum-overlap Drift evidence |
| `k3-3-b1-execution-evidence.md` | `1.0.0` | Five-Chunk Preview, one-document Indexing and measured Credit evidence |
| `k3-3-b2-execution-evidence.md` | `1.0.0` | Persisted Knowledge link, four-node graph and zero-Credit evidence |
| `k3-3-c-execution-evidence.md` | `1.0.0` | Four sequential Indexing results, measured Credits and safe guard stop |
| `k3-3-c1-execution-evidence.md` | `1.0.0` | Final document Preview, Indexing, Credits and full-corpus verification |
| `k3-3-d-execution-evidence.md` | `1.0.0` | One-question smoke result, citation failure and Credit guard stop |
| `k3-3-d1-execution-evidence.md` | `1.0.0` | Zero-Credit editor failure and manual prompt recovery requirement |
| `k3-3-d1r-execution-evidence.md` | `1.0.0` | Persisted manual recovery, binding checks and zero-Credit read-only verification |
| `k3-3-d2-execution-evidence.md` | `1.0.0` | One-question citation retest, six-Credit delta and safe stop |
| `k3-3-d3r-execution-evidence.md` | `1.0.0` | Existing-run Retrieval inspection and metadata-boundary finding |
| `k3-3-d3a-execution-evidence.md` | `1.0.0` | Six metadata values, Citation Context binding, reload verification and safe stop |
| `k3-3-d3s-execution-evidence.md` | `1.0.0` | Template editor failure, neutral recovery, Reload and zero-Credit evidence |
| `k3-3-d3w-execution-evidence.md` | `1.0.0` | Persisted five-node graph, structured prompt variable and zero-Credit verification |
| `k3-3-d3t-execution-evidence.md` | `1.0.0` | One-question factual and citation pass, six-Credit delta and safe stop |

## Invariants

- Tenant remains `af-demo-services`.
- Corpus remains `af-demo-services-he@1.0.0`.
- Language remains Hebrew.
- External tools and side effects remain disabled.
- No artifact contains a secret, credential, provider account, endpoint, or real user data.
- Any later provider mapping receives a new configuration version and separate approval.
