# ADR-008: Budget Warning, Approval and Safety Cap

**Status:** Accepted  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

Cost is a primary operational concern for both platform and client. A rigid business hard stop can make an Agent unusable, while silent overrun or runaway spend is unacceptable.

## Decision

The system separates:

1. **Business Budget** - client/Owner budget. Default policy is warn/project/offer alternatives and require explicit overage approval when the effective policy says the next spend crosses the approved envelope.
2. **Emergency Safety Cap** - independent operational guardrail for loops, recursion or anomalous spend.

Build-time expensive work is subject to the effective build-cost policy. Runtime overage approval belongs to the authorized client approver defined in EffectiveReleaseConfig.

Every request performs a lightweight budget check. Expensive/composite operations receive preflight estimation where practical.

Threshold values are policy profiles, not universal hard-coded numbers.

## Consequences

- no silent overspend;
- client can intentionally extend a business budget without rebuilding the Agent;
- cheaper approved alternatives can be offered before asking for more budget;
- extreme failure loops remain protected by a separate safety mechanism;
- cost decisions are auditable.

## Non-override rule

Business-budget approval does not disable or raise the emergency safety cap automatically. Safety-cap changes follow PlatformPolicy and may require separate approval/exception.

## Audit requirement

Budget approval records approver, amount/new limit, currency, period, timestamp, reason and expiration/review date, linked to request/release/policy as appropriate.