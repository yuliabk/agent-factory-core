# Tasks: Agent Factory V1

## 0. Architecture Baseline

- [x] T0.1 Create repository-level `AGENTS.md` rules. Requirements: AF-GOV-001, AF-GOV-002, AF-GOV-003.
- [x] T0.2 Document control-plane and client-data-plane architecture. Requirements: AF-105, AF-109.
- [x] T0.3 Document security classification and Production gates. Requirements: AF-104, AF-105, AF-110.
- [x] T0.4 Create roadmap, cost envelope, templates, and skill registry. Requirements: AF-107, AF-108, AF-109.
- [ ] T0.5 Obtain Owner approval for Gate G0. Blocks every implementation task.

## 1. Prototype Environment

- [ ] T1.1 Decide Dify and n8n hosting mode. Requirements: AF-101, AF-105, AF-108.
- [ ] T1.2 Create non-production projects with synthetic data. Requirements: AF-102, AF-105, AF-110.
- [ ] T1.3 Configure model access with usage caps and secret management. Requirements: AF-101, AF-108.

## 2. Knowledge Agent

- [ ] T2.1 Select an approved synthetic document set. Requirements: AF-103, AF-110.
- [ ] T2.2 Configure retrieval, citations, and insufficient-evidence fallback. Requirements: AF-103.
- [ ] T2.3 Create and run 20-30 acceptance questions. Requirements: AF-103, AF-107.

## 3. Service and Action Agent

- [ ] T3.1 Select one reversible internal action. Requirements: AF-104.
- [ ] T3.2 Define n8n workflow schema, authorization, idempotency, and rollback. Requirements: AF-104, AF-107.
- [ ] T3.3 Add human approval and escalation. Requirements: AF-104, AF-106.
- [ ] T3.4 Connect website chat and email draft channel. Requirements: AF-106.

## 4. Hardening and Packaging

- [ ] T4.1 Run tenant-isolation and prompt-injection tests. Requirements: AF-105, AF-110.
- [ ] T4.2 Add audit, cost, latency, error, and quality metrics. Requirements: AF-107, AF-108.
- [ ] T4.3 Run clone rehearsal for a synthetic second client. Requirements: AF-109.
- [ ] T4.4 Complete runbook, rollback, retention, and deletion tests. Requirements: AF-107, AF-110.

## 5. Deferred Channel

- [ ] T5.1 Create a separate OpenSpec change for WhatsApp. Requirements: AF-106.

