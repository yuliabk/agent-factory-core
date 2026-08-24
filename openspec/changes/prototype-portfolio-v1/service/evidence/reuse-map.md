# PF-S Canonical Factory Reuse Map

## Measurement Rule

Reuse is counted only when the PF-S artifact points to an existing canonical control or template and preserves its boundary. Copied prose, policy content and PF-S-specific schemas are deltas and are not counted as shared reuse.

## Referenced Canonical Assets

| Reuse ID | Canonical source | Preserved contract | PF-S application | Counted |
|---|---|---|---|---:|
| `REUSE-01` | `templates/client-intake.md` | Client Intake fields | `service/intake.md` | 1 |
| `REUSE-02` | `docs/adr-003-versioned-release-manifest.md` | versioned release identity | `service/manifest.md` | 1 |
| `REUSE-03` | `docs/security-model.md` § Tenant Isolation | tenant-specific data and audit boundary | all PF-S artifacts use `af-demo-retail` | 1 |
| `REUSE-04` | `docs/security-model.md` § Audit, Retention ומחיקה | minimized audit fields | `service/contracts/service-audit.schema.json` | 1 |
| `REUSE-05` | `docs/security-model.md` § פעולות המחייבות אישור אנושי | human review before protected actions | routing contract and `CS-E09` | 1 |
| `REUSE-06` | `docs/tooling-and-costs.md` § עקרון תקציבי | explicit cost boundary | zero provider requests and `0 ILS` | 1 |
| `REUSE-07` | `openspec/changes/portable-runtime-adapters-v1/evaluation-runner-plan.md` | deterministic local evidence and fail-closed ceilings | frozen scenarios and local validation | 1 |
| `REUSE-08` | `openspec/changes/prototype-portfolio-v1/design.md` § Incident/Drift rule | stop before execution on missing dependency or drift | `CS-E11` and routing failure rules | 1 |

- `canonical_references_count`: `8`
- `copied_canonical_assets_count`: `0`
- `pf_s_specific_deltas`: policies, business cases, Service request/response schemas and Hebrew expected drafts.
- `measurement_status`: `measured_local_artifact_references`

This count measures design reuse, not Runtime portability, code reuse, build time reduction or production readiness.
