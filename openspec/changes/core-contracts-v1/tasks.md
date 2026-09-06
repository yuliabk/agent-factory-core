# Tasks: Core Contracts v1

All implementation tasks remain blocked until Owner approval of the contracts.

## C1 - Documentation and contract review

- [ ] C1.1 Review platform vision, architecture and Core boundaries. Maps: CORE-201, CORE-210, CORE-211.
- [ ] C1.2 Review Agent Manifest and ExecutionContext contract. Maps: CORE-202, CORE-203.
- [ ] C1.3 Review security, governance, tool and memory contracts. Maps: CORE-206, CORE-207, CORE-212.
- [ ] C1.4 Review capability/orchestration contract. Maps: CORE-204.
- [ ] C1.5 Review provider/cost policy. Maps: CORE-205, CORE-208.
- [ ] C1.6 Review lifecycle, evidence, eval and approval contract. Maps: CORE-209, CORE-212.
- [ ] C1.7 Accept/modify ADR-005 through ADR-008.

## C2 - Schema skeleton after approval

- [ ] C2.1 Define JSON/YAML schema for Agent Manifest. Maps: CORE-202.
- [ ] C2.2 Define ExecutionContext schema. Maps: CORE-203.
- [ ] C2.3 Define minimal audit event schema. Maps: CORE-212.
- [ ] C2.4 Define capability registration/delegation schema. Maps: CORE-204.
- [ ] C2.5 Define tool and memory adapter interfaces. Maps: CORE-206, CORE-207.
- [ ] C2.6 Define budget policy schema with business limit and emergency cap. Maps: CORE-208.

## C3 - Deterministic validation after C2 approval

- [ ] C3.1 Manifest validator with default-deny tests. Maps: CORE-202.
- [ ] C3.2 ExecutionContext and permission enforcement tests. Maps: CORE-203, CORE-206.
- [ ] C3.3 Agent-hop/cycle limit tests. Maps: CORE-204.
- [ ] C3.4 Budget preflight and safety-cap tests. Maps: CORE-208.
- [ ] C3.5 Cross-tenant memory negative tests. Maps: CORE-207.

## C4 - Portability skeleton after C3 approval

- [ ] C4.1 Model profile/provider adapter interface with at least two test adapters. Maps: CORE-205.
- [ ] C4.2 Capability registry with two contract-compatible test providers. Maps: CORE-204.
- [ ] C4.3 Template registry/build-plan prototype. Maps: CORE-210.
- [ ] C4.4 Regression eval harness for provider/template swaps. Maps: CORE-209.

## C5 - Next-agent gate

- [ ] C5.1 Approve `research.lookup` capability contract.
- [ ] C5.2 Create Research/Brain Agent in a separate repository only after the required Core skeleton/evals are approved.
