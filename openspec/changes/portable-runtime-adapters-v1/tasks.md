# Tasks: Portable Runtime Adapters v1

## P0 — Adapter Contract Planning

- [x] P0.1 Define versioned adapter identity and canonical release linkage (RP-101, RP-102).
- [x] P0.2 Define normalized request, response, citation, evidence, policy, usage, and cost records (RP-103, RP-104, RP-107).
- [x] P0.3 Define capability declarations, drift detection, isolation, export, deletion, and fail-closed controls (RP-106, RP-108, RP-112).

## P1 — Evaluation Runner Planning

- [x] P1.1 Define a network-free local dry-runner scope and lifecycle (RP-104).
- [x] P1.2 Map the frozen 25-question set, technical retries, citation/fallback checks, and immutable run evidence (RP-104, RP-105).
- [x] P1.3 Define separate future gates for implementation and live execution (RP-111).

## P2 — Botpress Mapping Planning

- [x] P2.1 Map Botpress concepts to the adapter contract (RP-109).
- [x] P2.2 Record citation, isolation, export, retention, Hebrew-quality, and cost-control gaps (RP-108, RP-109).
- [x] P2.3 Define Botpress preflight blockers and stop conditions (RP-107, RP-109, RP-111).

## P3 — Flowise Mapping Planning

- [x] P3.1 Map Flowise concepts to the adapter contract (RP-110).
- [x] P3.2 Record metadata, citation, isolation, export, deletion, retention, and cost-control gaps (RP-108, RP-110).
- [x] P3.3 Define Flowise preflight blockers and stop conditions (RP-107, RP-110, RP-111).

## Approval Gates and Separately Gated Future Work

- [x] PR-G0 Owner approval of this planning package only. Approved 2026-08-21; no implementation or external action is authorized.
- [x] PR-G1 Implement the local network-free adapter validator and dry evaluation runner. Completed 2026-08-21.
- [x] PR-G1 Validate implementation against synthetic fixtures without model or provider calls. Thirteen tests and the valid CLI fixture run passed on 2026-08-21.
- [x] PR-G2 Select exactly one candidate for a public read-only preflight. Flowise selected and reviewed on 2026-08-21 (RP-110, RP-111).
- [x] PR-G2-Flowise-Preflight review official public evidence for continuity, cost, citation, isolation, export, deletion, privacy, and security. Result: `NO-GO`; no provider-side action occurred (RP-107, RP-108, RP-110, RP-112).
- [x] PR-G2-Botpress-Preflight review official public evidence for continuity, cost, citation, isolation, export, deletion, privacy, and security. Result: `CONDITIONAL-GO`, currently blocked; no provider-side action occurred (RP-107, RP-108, RP-109, RP-112).
- [x] PR-G2-Botpress-A0 open the official registration page and guide the Owner through one Free-account registration without reading personal or authentication data and without creating an additional workspace or Bot (RP-109, RP-111).
- [x] PR-G2-Botpress-A1 inspect the existing default workspace, Free-plan usage, and billing summary read-only. Result: allowances verified, usage zero, hard-stop enforcement unproven, and `CONDITIONAL-GO` remains blocked (RP-107, RP-108, RP-109, RP-111).
- [x] PR-G2-Botpress-A1-Doc record the separately approved A0/A1 boundary and findings in the planning package only; no provider-side action, Commit, or Push (RP-107, RP-108, RP-109, RP-111).
- [x] PR-G2-Botpress-A2 inspect workspace cost, membership, audit, deletion, and workspace-level export controls read-only. Result: auto-recharge disabled, hard cap not visible, destructive and financial controls untouched, and two uninspected Bot routes recorded as drift (RP-107, RP-108, RP-109, RP-111, RP-112).
- [x] PR-G2-Botpress-A2-Doc record the separately approved A2 boundary, control findings, and configuration drift in the planning package only; no provider-side action, Commit, or Push (RP-107, RP-108, RP-109, RP-111, RP-112).
- [x] PR-G2-Botpress-A3 reconcile drift read-only by counting non-personal Bot inventory and checking available audit categories and timestamps without opening Bot or Studio. Result: two routes confirmed, no attributable audit evidence, and origin/configuration remain unknown (RP-108, RP-109, RP-111).
- [x] PR-G2-Botpress-A3-Doc record the separately approved A3 boundary, missing audit evidence, rejected weak signal, and unresolved drift in the planning package only; no provider-side action, Commit, or Push (RP-108, RP-109, RP-111).
- [x] PR-G2-Botpress-IR-A0 perform read-only incident triage after the Owner disclaimed Bot creation. Result: two Bot routes persisted, file storage increased to 1 MB, usage remained zero, auto-recharge remained disabled, and safe account-security routes were unavailable (RP-107, RP-108, RP-109, RP-111).
- [x] PR-G2-Botpress-IR-A0-Doc record the provisional `SEV3`, `Investigating`, `INCIDENT-HOLD`, minimized evidence, and containment boundary only; no provider-side action, Commit, or Push (RP-108, RP-109, RP-111).
- [x] PR-G2-Botpress-IR-A1 re-verify the incident surfaces read-only before containment confirmation. Result: no additional drift relative to IR-A0, no new audit evidence, and incident status unchanged (RP-107, RP-108, RP-109, RP-111).
- [x] PR-G2-Botpress-IR-A1-Doc record the stable-but-unresolved snapshot and unverified containment state only; no provider-side action, Commit, or Push (RP-108, RP-109, RP-111).
- [ ] Owner secure the identity provider and review or revoke unknown sessions without sharing authentication or personal data with Codex.
- [ ] After Owner confirms containment, separately approve a post-containment read-only incident re-verification (RP-108, RP-109, RP-111).
- [ ] PR-G2 Authorize credentials, data upload/indexing, runtime, payment, provider-native limits, or any additional provider resource explicitly.
- [ ] PR-G2 Execute a bounded pilot and preserve normalized and provider-native evidence.
- [ ] Approve migration, publication, or production use through a later change.
