# Client Experience and Conversational Intake

**Status:** Accepted direction after Owner Review

## 1. Principle: technical black box, business transparency

The client should not need to understand MCP, API, Vector DB, Model Router, prompt-injection controls or Runtime adapters.

They should be able to say:

> "I want an Agent that sells for me and answers customers."

The platform translates that into a technical specification behind the scenes.

Black box does **not** mean opaque. The client should see material business facts: scope, assumptions, connected business services, expected cost, data-use summary, limitations and actions requiring approval.

## 2. UX target

Initial intake target:

- usually under 10 minutes;
- one free-form description first;
- typically 5-6 critical follow-up questions;
- additional questions only when needed for safe scope, cost, data or consequential-action decisions.

This is a UX target, not a hard technical limit.

## 3. Progressive clarification

The system does not try to collect 100% of information up front.

Information is divided into:

1. **Blocking** - must be known now.
2. **Inferable** - Factory may infer and show as an assumption.
3. **Deferred** - can be resolved during Build/Onboarding.

For ambiguous requests the default pattern is:

`infer -> show assumptions -> client confirms/corrects`

## 4. Progressive complexity

The Factory initially proposes the simplest Agent architecture that can deliver the requested outcome.

Extra autonomy, integrations, persistent memory, premium models or channels are added only when they materially improve the approved outcome or are required by policy.

## 5. Critical question areas

Questions are business-oriented, not technical. Typical areas:

- desired business outcome;
- who the Agent serves/communicates with;
- where work happens today;
- information required;
- actions that should never happen without approval;
- budget/range;
- data sensitivity or regulatory constraints when relevant.

Not every Agent receives every question.

## 6. Handling "I don't know"

When the client does not know, the Factory recommends a default or 2-3 understandable options.

Instead of asking which MCP server/provider/model they want, explain the business consequence and ask about the desired outcome/permission.

## 7. Assumption confirmation

The platform summarizes the inferred solution in plain language, especially assumptions affecting:

- scope;
- cost;
- security/data use;
- side effects;
- approval boundaries.

Low-impact technical assumptions do not need separate confirmation one by one.

## 8. Budget early, jargon late

Budget/range is collected early because it affects solution architecture and routing policy.

Technical detail is surfaced only when it materially affects price, privacy, business limitations, responsibility or a required client action.

The client can choose business-level options such as economical, balanced/recommended or advanced rather than provider/model brands.

## 9. Intake output

The client does not write the Spec. The Factory produces, behind the scenes:

```text
ClientIntent
Assumptions
Risk/Trust recommendation
Budget/Optimization Profile
Capability Requirements
Channel Requirements
Data Requirements
Consequential Action Boundaries
Success Metrics
Release/Eval Requirements
```

Spec Compiler then creates/updates the versioned Spec, AgentManifest and ClientInstanceConfig drafts.

## 10. Client-facing completion

At build/release time, the client sees:

- what the Agent does and does not do;
- material assumptions;
- allowed actions and approval points;
- business services/accounts that need connection;
- expected cost/range and budget-overage behavior;
- material data-use/retention summary;
- known limitations;
- how to pause/change/decommission the Agent.

Backend implementation remains hidden unless requested or necessary for an informed decision.