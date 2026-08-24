# Corpus Review Evidence: af-demo-services-he@1.0.0

## Review Metadata

- Review date: `2026-08-20`
- Reviewer: `Codex`
- Owner decision: Approved `af-demo-services-he@1.0.0` on `2026-08-20`
- Approval boundary: Corpus version only; Indexing and Runtime not authorized
- Indexing performed: No
- Runtime provisioned: No

## Structural Checks

| Check | Result |
|---|---|
| Source document count is 6 | Pass |
| Synthetic notice appears in all 6 documents | Pass |
| Required metadata appears in all 6 documents | Pass |
| Tenant is fixed to `af-demo-services` | Pass |
| Classification is `synthetic` | Pass |
| Language is `he` | Pass |
| Status is `approved` | Pass |
| Owner field uses non-personal role `agent-factory-owner` | Pass |
| Manifest SHA-256 matches every source file | Pass |

## Safety Scans

| Scan | Result |
|---|---|
| HTTP/HTTPS or `www` URLs | No matches |
| Email-address patterns | No matches |
| Common API token or private-key patterns | No matches |
| Standalone nine-digit identifier patterns | No matches |
| Real contact details | No matches found |

## Intentional Security Fixture

`AFD-006 § דוגמת Injection` contains one quoted attack sentence and the terms `system prompt` and `API key`. This is an intentional, visibly labeled, non-executable safety fixture. The surrounding policy explicitly says not to follow it and not to request secrets. It contains no credential, link, or real identifier.

## Content Review

- Canonical facts match `corpus-plan.md`.
- Unsupported evaluation topics remain absent: international delivery policy, phone number, real-currency plan price, medical advice, and employee salary data.
- No conflict fixture is included in the active corpus.
- No external action, Workflow, web search, contact endpoint, or credential is configured.

## Conclusion

The materialized corpus passes local structural and safety review and is approved as `af-demo-services-he@1.0.0`. Indexing and Runtime remain blocked until the Owner grants the separate authorization required by task K3.3.
