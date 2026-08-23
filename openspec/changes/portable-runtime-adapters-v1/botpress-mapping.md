# P2 — Botpress Mapping

## Status

Public official-source preflight completed on 2026-08-21 under `PR-G2-Botpress-Preflight`. Decision: **CONDITIONAL-GO for a later synthetic, non-production pilot only; currently BLOCKED** pending a new authorization and proof of citation, isolation, deny-all behavior, export/reconstruction, deletion, Hebrew fallback, and cost controls. No Botpress account, bot, workspace, knowledge base, credential, payment method, or runtime activity was authorized or created.

## Vendor Continuity Result

No public continuity blocker was found. Official documentation is current, the public status page reports operational services, and Botpress announced a USD 25 million Series B in June 2025. This is a positive signal, not a financial guarantee or Runtime approval.

## Concept Mapping

| Canonical concept | Botpress candidate concept | Planning assessment |
|---|---|---|
| Agent release | Bot configuration/export plus Agent Factory manifest | Must prove immutable reconstruction reference |
| Prompt and policy | Agent instructions, workflow/nodes, and guard logic | Must prove external actions are disabled |
| Approved corpus | Botpress knowledge source/knowledge base | Must preserve corpus version and isolation |
| Retrieval evidence | Knowledge retrieval logs expose query, source name, content preview, token use, and table metadata; Knowledge Agent exposes citations | Exact stable `source_id` and section path remains unproven |
| Answer contract | Generated response plus post-validation | Citation validation may require adapter logic |
| Evaluation run | Emulator/API execution plus event/log evidence | Requires a separately approved live gate |
| Usage and cost | Events, AI Spend, storage, and plan limits | Native units must remain visible |
| Export/deletion | `.bpz` bot export, agent/workspace deletion and data APIs | Proprietary export links hosted source files; retention and backup completion remain incomplete |

## Cost Planning Snapshot

Official pricing reviewed on 2026-08-21 described PAYG at USD 0 plus AI Spend, USD 5 monthly AI credit, one bot, one collaborator, 500 incoming events, 100 MB vector storage, and 100 MB file storage. Botpress documents a custom AI Spend cap and a USD 100 monthly maximum for PAYG/Plus, but also states that reliable AI Spend forecasting is not currently available. Auto Recharge MUST remain disabled in any future pilot.

## Required Preflight Evidence

- The intended plan supports an enforceable AI-spend cap and observable event usage.
- Retrieval metadata reaches the adapter with stable `source_id` and section provenance.
- A bot cannot invoke integrations, actions, or tools outside the approved deny-all policy.
- Workspace, bot, knowledge, logs, and credentials can be isolated for one synthetic prototype.
- Configuration can be exported or reconstructed without exporting secrets.
- Retention and deletion behavior cover knowledge, logs, conversations, indexes, and backups.
- Hebrew answer and fallback behavior can be measured against the frozen set.

## Known Gaps and Risks

- Citation provenance may not be exposed at the granularity required by the canonical contract.
- Platform events and AI Spend are different cost dimensions; both require ceilings.
- `.bpz` export is proprietary, must not be modified, and links knowledge files that remain hosted on Botpress.
- Integrations require manual restoration after import.
- Logs are retained for 30 days; conversations, messages, and events for 90 days; files and other data may persist indefinitely until deletion.
- PAYG has no RBAC or contractual SLA; those controls require higher plans.
- The DPA says the service is not designed for sensitive data.
- Hebrew quality and deterministic fallback behavior are unverified.

## Fail-Closed Decision

Botpress passes public continuity review but remains ineligible for authenticated inspection or Runtime while required evidence is absent. A future pilot may be considered only for one dedicated PAYG workspace, one Owner, synthetic data, disabled Auto Recharge, a low AI Spend cap, no integrations/tools/web search, and separately proven citations and deletion. Exact citations MUST never be fabricated.

## Official Sources

- Pricing: https://botpress.com/en/pricing
- Workspace controls: https://botpress.com/docs/studio/get-started/configure-your-workspace/
- Knowledge and citations: https://botpress.com/docs/studio/concepts/agents/knowledge-agent/
- Export: https://botpress.com/docs/studio/concepts/import-export-bots/
- Retention: https://botpress.com/docs/learn/guides/advanced/retention-period
- Privacy/DPA: https://botpress.com/legal/privacy-statement
- Status: https://status.botpress.com/
- Detailed evidence: `pr-g2-botpress-preflight-evidence.md`
