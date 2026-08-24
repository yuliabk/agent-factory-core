# K4.0 Capacity and 25-Question Evaluation Plan

## Metadata

- `plan_id`: `af-ka-01-k4-0-capacity`
- `version`: `1.0.0`
- `date`: `2026-08-20`
- `status`: `local_plan_complete_owner_gate_required`
- `data_scope`: `af-demo-services-he@1.0.0` synthetic only
- `evaluation_set`: `ka-prototype-he-v1`
- `current_authorized_stage`: `none`
- `current_committed_spend`: `0 ILS`
- `requirements`: `KA-109, KA-110, KA-111`

## Authorization Boundary

K4.0 is a local planning record only. It does not authorize a Dify inspection or change, Runtime request, Indexing, Payment, Upgrade, Subscription, API key, Credential, Publish, Commit or Push. Every future provider action requires a new approval naming one bounded stage.

## Frozen Facts and Capacity Calculation

Four observed generation paths each reduced the Dify Sandbox balance by six Credits. This aligns operationally with one Retrieval query using `text-embedding-3-small` plus one `gpt-4.1-mini` response, but the measured six-Credit delta—not the public component rates—is the planning basis.

| Item | Calculation | Credits |
|---|---:|---:|
| Frozen scored questions | `25 × 6` | 150 |
| Technical retry reserve | `5 × 6` | 30 |
| Safe run envelope | `30 × 6` | 180 |
| Current available balance | observed after D3T | 36 |
| Deficit for 25 questions without retries | `150 - 36` | 114 |
| Deficit for safe run envelope | `180 - 36` | 144 |
| Expected balance after a fresh 200-Credit allowance and safe envelope | `200 - 180` | 20 |

Thirty attempts are ceilings, not targets. A wrong content answer is recorded as a failure and is not retried. Only a documented technical failure may consume one of the five retry slots.

## Current Public Pricing Basis

Verified on `2026-08-20` against official public sources:

- Dify lists Sandbox as free with 200 monthly message Credits, Professional as USD 59 monthly or USD 590 annually with 5,000 monthly Credits, and Team as USD 159 monthly or USD 1,590 annually with 10,000 monthly Credits.
- Dify lists `gpt-4.1-mini` as one Credit per AI response. The repository's measured end-to-end workflow delta remains six Credits per question because Retrieval also consumes capacity.
- OpenAI lists `gpt-4.1-mini` at USD 0.40 per million input tokens and USD 1.60 per million output tokens, and `text-embedding-3-small` at USD 0.02 per million input tokens.
- The latest available Bank of Israel representative rate used for this plan is `1 USD = 2.9860 ILS`. The representative rate is indicative and must be refreshed at any Payment gate.

Official references:

- https://dify.ai/pricing/dify-cloud
- https://dify.ai/blog/try-openai-claude-gemini-grok-free-on-dify-cloud
- https://developers.openai.com/api/docs/models/gpt-4.1-mini
- https://developers.openai.com/api/docs/models/text-embedding-3-small
- https://www.boi.org.il/roles/markets/exchangerates/

## Alternatives

| Option | Capacity and estimated cost | Advantages | Risks and constraints | K4.0 decision |
|---|---|---|---|---|
| A. Wait for Sandbox monthly renewal | A fresh 200-Credit allowance covers the 180-Credit safe envelope and leaves 20; monetary cost 0 ILS | No Payment, Credential or architecture change; preserves the already smoke-tested configuration | Renewal timing and fresh balance must be verified read-only; any balance below 180 blocks the run; no spare capacity for unrelated testing | **Selected primary path** |
| B. Dify Professional | 5,000 Credits/month; USD 59 monthly ≈ 176.17 ILS, or USD 590 annually ≈ 1,761.74 ILS at the recorded rate | Large capacity margin; no new model-provider Credential required when using included Credits | Monthly price exceeds the approved 100 ILS prototype sub-cap; Upgrade, Payment and possible auto-renewal require separate review and approval | Rejected under current cap |
| C. OpenAI BYOK in Dify | Token-based. Planning formula: `0.40 × input_Mtokens + 1.60 × output_Mtokens + 0.02 × embedding_Mtokens` USD. Exact total is unknown until token ceilings and one calibration request are approved | Likely materially cheaper than a Dify subscription for 30 bounded attempts; direct token measurement | Requires OpenAI billing, secret creation/storage, Dify Credential configuration, usage limits, incident/rotation plan and separate security review; may change the observed runtime cost model | Deferred; not authorized |
| D. Reduced five-question diagnostic | `5 × 6 = 30` Credits, leaving 6 and no retry reserve | Can sample the remaining four safety categories quickly | Does not satisfy the frozen 25-question evaluation; nearly exhausts Sandbox; creates selection bias and delays the scored run | Rejected as K4 evaluation; may be proposed later only as a separately named diagnostic |
| E. Self-host Dify or change runtime | Software may be open source; infrastructure and Owner operations are not yet priced | Maximum portability and control | Largest architecture, security, backup, monitoring and maintenance expansion; breaks comparability with the current Dify smoke evidence | Deferred beyond V1 |

The ILS conversions are forecasts only: `USD amount × 2.9860`. Taxes, card-provider spreads and later exchange-rate changes are excluded. No paid cost is committed by this plan.

## Selected Execution Design After Capacity Approval

The primary path is to wait for the next monthly Sandbox allowance and then request a separate read-only capacity/Drift gate. No question is run until all preconditions pass.

### Phase 1 — Read-only capacity and Drift verification

Required evidence before Runtime:

- Workspace remains Sandbox, one Owner, App Unpublished, no paid quota, BYOK, Tool, Trigger or external integration.
- Available Credits are at least 180.
- The persisted five-node graph, model snapshot, Knowledge Base, six documents, metadata, Prompt and corpus hashes match the approved configuration.
- The 25 questions and expected verdicts remain frozen.
- A local evaluation record exists for every question before the first request.

Failure of any check stops before Runtime.

### Phase 2 — One bounded scored run

- Run IDs: one new `evaluation_run_id` and one request ID per attempt.
- Question order: `KA-E01` through `KA-E25`; do not skip or replace failures.
- Maximum primary attempts: 25.
- Maximum technical retries: 5 total; zero automatic retries.
- Hard request ceiling: 30.
- Hard Credit ceiling: 180.
- Warning checkpoint: after question 10 or 60 Credits, whichever comes first.
- Mandatory checkpoint: after question 20 or 120 Credits, whichever comes first.
- Stop immediately on any global safety condition, unexpected Credit rate, missing evidence record, publication, Provider/Model Drift, cross-tenant retrieval, Tool call, secret/PII exposure or paid-state change.

### Phase 3 — Local scoring and Gate G1 preparation

After the last permitted response, stop Runtime. Record all results locally, apply the frozen thresholds, preserve failures, calculate actual Credits/request and total Credits, and request a separate Owner decision. No configuration remediation or rerun is included.

## Cost and Risk Controls

- `safe_capacity_floor_before_start`: `180 Credits`
- `hard_attempt_ceiling`: `30`
- `hard_credit_ceiling`: `180`
- `monetary_commitment_ceiling`: `0 ILS` for the selected Sandbox path
- `monthly_prototype_sub_cap`: `100 ILS`, still not spending authorization
- `automatic_retry`: `disabled`
- `automatic_model_substitution`: `disabled`
- `paid_overage_or_upgrade`: `disabled/not authorized`
- `credential_connection`: `disabled/not authorized`
- `publish`: `disabled/not authorized`

Residual risks:

1. Dify's public Credit schedule can change between planning and execution.
2. The six-Credit rate can drift with model, plugin, Retrieval or provider changes.
3. A monthly allowance may renew later than expected or not appear as a full 200-Credit balance.
4. One supported-question citation pass does not predict unsupported, injection, ambiguity or conflict behavior.
5. Manual Studio execution can introduce transcription or evidence-capture errors.

These risks are controlled through a fresh read-only gate, fixed question IDs, two checkpoints, per-question evidence and immediate stop conditions.

## Gate K4.1C — Capacity Strategy and Read-only Verification

`K4.1C` is the next proposed gate; it is **not granted** by K4.0.

To approve it, the Owner must explicitly authorize only a read-only Dify reload/inspection to verify the renewed balance and frozen configuration. It must forbid Runtime, Preview, Indexing, Payment, Upgrade, Subscription, Credentials, graph or Prompt changes, Publish and external tools. A passing result may prepare—but does not authorize—the scored run.

Only after K4.1C passes may a separate `K4.3E` scored-run gate be proposed with the exact 25-question set, 30-attempt/180-Credit ceilings, checkpoints, stop conditions and zero paid commitment.

## Decision Record

- `selected_option`: `wait_for_sandbox_monthly_renewal_then_read_only_gate`
- `reason`: `zero monetary cost, no Credential expansion, and a fresh 200-Credit allowance fits the 180-Credit safe envelope`
- `not_selected`: `Professional exceeds the 100 ILS cap; BYOK expands Payment/Credential/security scope; reduced diagnostic is not a scored evaluation; self-hosting expands architecture and operations`
- `next_action`: `Owner may approve K4.1C only after a renewed Sandbox balance is expected`
- `runtime_authorization`: `not_granted`

