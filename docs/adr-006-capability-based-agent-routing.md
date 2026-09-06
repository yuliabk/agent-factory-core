# ADR-006: Capability-based Agent Routing

**Status:** Proposed  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

Agents עתידיים יצטרכו להשתמש ביכולות של Agents אחרים. Direct calls לפי שם/URL יוצרים Coupling, מקשים על החלפה, Policy, Cost control ו-Audit.

## Decision

Agent יכריז ב-Manifest על Capabilities שהוא `provides` ו-`requires`. כל Agent-to-Agent invocation יעבור דרך Core Capability Registry ו-Orchestrator.

Consumer אינו יודע מי ה-Provider הקונקרטי.

## Consequences

- ניתן להחליף Research Agent ללא שינוי Travel Agent.
- אפשר fallback בין implementations תואמים.
- כל delegation עובר permission, budget ו-audit checks.
- נדרש contract versioning ו-hop limit.

## Rejected default

Direct Agent-to-Agent URLs אינם ברירת מחדל מותרת. Exception דורש ADR/Policy מפורש.
