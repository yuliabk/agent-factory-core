# Prototype Cost Control Plan

## Metadata

- Plan ID: `ka-cost-control`
- Version: `1.7.0`
- Previous version: `1.6.0`
- Status: K4.0 capacity plan complete; waiting for Sandbox renewal and separate read-only gate
- Approved future monthly sub-cap: 100 ₪
- Requirements: KA-111

## Authorization Boundary

The 100 ₪ cap is a maximum for a later authorized Runtime, not authorization to spend. No paid request, Indexing, embedding, model call, subscription, or credential connection may occur before K3.3 approval.

## Required Cost Indicators

A candidate provider must expose or permit calculation of:

- Indexing or ingestion cost;
- Retrieval cost when separately charged;
- generation input and output usage;
- model or request cost;
- storage or platform cost attributable to the prototype;
- cumulative monthly cost in ILS or source currency with conversion date and rate recorded;
- remaining amount before warning and hard-stop thresholds.

An estimate is labeled `forecast`; provider-reported or invoice-derived cost is labeled `actual`. They are never mixed silently.

## Request Limits

- Frozen questions per scored candidate run: 25.
- Maximum documented technical retries per candidate: 5.
- Maximum billable question attempts per candidate: 30.
- Maximum candidates in one approved comparison round: 3.
- Maximum billable question attempts in that round: 90.
- A failed content answer is recorded as a failure and is not retried as a technical error.

These are ceilings, not execution authorization.

## Budget Thresholds

| Threshold | Action |
|---|---|
| Forecast exceeds 60 ₪ for the planned round | Stop planning the run and reduce scope or request Owner review |
| Actual or committed monthly cost reaches 60 ₪ | Warn Owner; no additional candidate starts automatically |
| Actual or committed monthly cost reaches 80 ₪ | Freeze new experiments; allow no action without explicit Owner review |
| Actual or committed monthly cost reaches 100 ₪ | Hard stop all prototype requests and Indexing |
| Cost cannot be measured or capped | Block execution before the first paid request |

## Stop Policy

The default degraded policy is `stop`, not silent model substitution. A provider, model, Retrieval method or quality setting is not changed solely to continue spending. Any proposed change creates a new configuration version and requires comparable evaluation evidence.

## Pre-run Checklist

- [ ] K3.3 approval is recorded.
- [ ] Provider prices and free-tier rules are verified at the time of execution.
- [ ] Cost measurement and hard-stop mechanism are tested with no real data.
- [ ] Monthly spend to date is recorded.
- [ ] Forecast for Indexing and the full round is below 60 ₪ or separately approved.
- [ ] Request limits are configured.
- [ ] No auto-renewing plan or paid add-on is enabled without explicit Owner approval.

## Dify Sandbox Credit Plan

- Current observed state on `2026-08-20`: Sandbox, `164 / 200` AI Credits used and 36 remaining after all approved stages, no visible BYOK or paid quota, disabled Billing management.
- Selected generation candidate: `gpt-4.1-mini`, listed by Dify at 1 Credit per AI response.
- Selected embedding candidate: `text-embedding-3-small`, listed by Dify at 5 Credits per applicable AI response.
- Rerank: disabled; no `qwen3-rerank` consumption is authorized.
- Measured end-to-end forecast for 25 questions: 150 Credits.
- Safe capacity target for 25 questions plus 5 technical retries: 180 Credits.
- Measured `AFD-001.md` Indexing delta: 20 Credits under the 25-Credit reserve ceiling.
- Linear remaining-Indexing forecast: five documents × 20 Credits = 100 Credits, leaving an estimated 80 Credits. This clears the 50-Credit reserve rule but does not authorize Stage C.
- Current monetary commitment and authorized spend: 0 ₪.
- The operational hard stop is absence of Paid plan/BYOK plus request ceilings. Any account-state Drift blocks the next request.

The original one-Credit generation-only forecast is superseded by the measured six-Credit end-to-end workflow rate. A fresh 200-Credit monthly Sandbox allowance would cover the 180-Credit envelope and leave 20; the current balance is 144 Credits short. The selected K4.0 strategy is to wait for renewal, then request a separate read-only capacity/Drift gate. Pricing evidence: https://dify.ai/pricing/dify-cloud and https://dify.ai/blog/try-openai-claude-gemini-grok-free-on-dify-cloud, verified `2026-08-20`.

## Run Record

K3.3-B1 recorded 200 Credits before, 180 Credits after, one document Indexed, five Preview Chunks and no generation request.

K3.3-B2 recorded 180 Credits before and after linking the dedicated Knowledge Base and persisting the linear four-node graph. No Retrieval Test, generation request or paid action occurred.

K3.3-C recorded these sequential deltas: `AFD-002` 15, `AFD-003` 30, `AFD-004` 25 and `AFD-005` 20 Credits. The Stage delta reached 90 Credits and 90 of 200 Credits remained. Processing stopped before `AFD-006` because only 10 Credits remained inside the approved 100-Credit Stage ceiling and observed per-document consumption was 15–30 Credits.

K3.3-C1 recorded a 30-Credit delta for `AFD-006`, leaving 60 of 200 Credits. The separately approved C1 ceiling was fully consumed and the 50-Credit reserve was preserved. Total full-corpus Indexing consumption is 140 Credits. No generation request occurred.

K3.3-D measured 6 Credits for the first successful question, not the forecast 1. The run stopped with 54 Credits remaining because another comparable response could breach the approved 50-Credit reserve. At the measured rate, the original five-question smoke forecast is 30 Credits and cannot be completed while preserving 50 from a 60-Credit starting balance.

An authorized run records forecast, actual cost when available, source currency, conversion date and rate, request counts, technical retries, threshold events and stop decision. It contains no credential or payment-card information.

## Planning Boundary

K4.0 performed a read-only public pricing lookup and recorded it locally. It performed no purchase, subscription, provider call, Dify account inspection or change, Indexing or Runtime execution. The detailed decision, alternatives and Gate K4.1C are in `k4-0-capacity-evaluation-plan.md`.
