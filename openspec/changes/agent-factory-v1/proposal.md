# Proposal: Agent Factory V1

## Summary

Create a reusable low-code foundation for knowledge, customer-service, and action agents. Use OpenSpec as the approval contract, Dify as the proposed agent runtime, n8n as the proposed action orchestrator, and isolated client data planes for deployment.

## Why

Building each client agent from a blank project repeats discovery, architecture, safety, testing, and delivery work. A controlled factory shortens delivery time while keeping client-specific requirements and data isolated.

## In Scope

- One reusable architecture and client-cloning model.
- One knowledge-agent prototype with grounded answers.
- One reversible internal action through n8n.
- Website test chat and email-draft integration.
- Human escalation and approval gates.
- Evaluation, audit, cost controls, and delivery templates.

## Out of Scope

- Production medical or financial data.
- Autonomous financial, legal, medical, deletion, or permission-changing decisions.
- Production WhatsApp in the first prototype.
- Shared cross-client knowledge bases or credentials.
- Fine-tuning and complex multi-agent orchestration.

## Expected Impact

- Reduce repeated specification and setup work for future client projects.
- Make scope, risk, cost, and acceptance criteria reviewable before code.
- Support a one-person delivery model with explicit approval gates.

## Success Criteria

- A new client specification can be created from templates in under two working sessions.
- The knowledge agent passes an approved grounded-answer evaluation set.
- The action agent cannot execute a protected action without authorization.
- No data, credentials, retrieval index, or audit record is shared between clients.
- Monthly pilot spend can be capped within 200-500 ₪.
- Every deployed client version can be traced to an approved OpenSpec change, evaluation evidence, and rollback target without storing secrets in Git.
- Client onboarding and decommissioning can be completed from a checklist with evidence that access, data, indexes, credentials, and audit boundaries are isolated.
- Authorization and approval decisions are made by policy controls outside the language model and are covered by negative acceptance tests.

## Approval

- **Gate:** G0
- **Status:** Approved
- **Approved by:** Owner (Yulush)
- **Approval date:** 2026-08-20

This approval accepts the Architecture Baseline and authorizes detailed prototype planning. It does not authorize implementation, service configuration, credential connection, Production deployment, or use of confidential, personal, medical, financial, or other sensitive data.

ADR-001, ADR-002, and ADR-003 were accepted before Gate G0 approval. Every later implementation task group still requires explicit Owner authorization under the repository workflow.

