# Security and Platform Governance

**Status:** Proposed

## Policy hierarchy

From highest to lowest authority:

1. Platform security invariants.
2. Legal/privacy and tenant isolation policy.
3. Owner-approved Core policy profiles.
4. Agent Manifest permissions and limits.
5. Agent-specific behavior/specification.
6. Runtime/model output.

A lower layer cannot weaken a higher layer.

## Approval authorities

### Build time

The Platform Owner approves material changes to:

- permissions;
- data classification;
- budget profile;
- model/provider privacy profile;
- tools with side effects;
- runtime profile;
- templates and release gates.

### Runtime

The authorized client approver handles business-budget overages and client-owned consequential actions according to policy.

### Elevated domains

Sensitive personal, medical, financial or legal use requires the designated Security/Privacy/Domain approval path before production.

## Change classes

- **Documentation only:** no runtime effect; normal review.
- **Contract compatible:** regression eval required.
- **Permission/data/cost expansion:** OpenSpec change and explicit approval required.
- **Breaking contract:** major version, migration plan and rollback required.
- **Emergency security change:** may suspend capability immediately; retrospective documentation follows.

## Required records

Material decisions are preserved as:

- OpenSpec change;
- ADR when architectural;
- Manifest diff;
- evaluation evidence;
- approval record;
- release reference;
- audit events for consequential runtime actions.

## Supply chain governance

External skills, plugins, MCP servers, packages, providers and templates require source verification, pinning, license review, permission inventory and security review before approval.
