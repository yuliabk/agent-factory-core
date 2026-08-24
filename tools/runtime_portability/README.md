# Offline Runtime-Portability Validator

This PR-G1 tool validates only local JSON declarations and synthetic fixtures. It has no provider adapter, network client, model call, credential handling, indexing, payment, publication, or live-execution mode.

## Run

From the repository root:

```powershell
python -B -m tools.runtime_portability.cli `
  --adapter tests/fixtures/runtime_portability/adapter.valid.json `
  --question-set tests/fixtures/runtime_portability/question-set.json `
  --fixtures tests/fixtures/runtime_portability/evidence-fixtures.valid.json
```

The command writes the deterministic JSON report to standard output only. Exit code `0` means all local preflight and fixture checks passed. Exit code `2` means the result is `fail` or `blocked`.

## Test

```powershell
python -B -m unittest discover -s tests -v
```

The test suite includes a socket-denial test to confirm the successful path does not require network access.

## Safety Boundary

- Input paths must be local files; URL-like paths are rejected.
- Unknown required capabilities, costs, citations, or isolation controls fail closed.
- Secret-bearing fields are rejected.
- Every dry-run question remains `not_run`.
- Provider-specific preflight or execution remains blocked until separate PR-G2 approval.
