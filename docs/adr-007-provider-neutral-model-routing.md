# ADR-007: Provider-neutral Model Routing

**Status:** Proposed  
**Date:** 2026-09-06  
**Decider:** Owner

## Context

מחירים, זמינות, יכולות ומדיניות פרטיות של Model providers משתנים. לקוחות שונים גם מחזיקים תקציבים והעדפות שונות.

## Decision

Business Agents יבקשו Model Profile ולא Provider/Model קונקרטי. Core Model Router ימפה Profile ל-Provider/Model לפי Policy, Data requirements, Cost, Quality, Latency ו-Availability.

Provider change יתבצע דרך configuration/adapter עם Regression evaluation.

## Consequences

- פחות vendor lock-in.
- התאמת פתרון לתקציב.
- fallback מבוקר.
- נדרש adapter contract אחיד.
- נדרש Eval כדי להוכיח ש-provider חלופי שומר על behavior נדרש.

## Exception

Hard-coded Provider מותר רק כאשר Requirement עסקי/רגולטורי מחייב אותו והוא מתועד במפורש.
