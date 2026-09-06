from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

from .contracts.eval_result import EvalResult
from .contracts.platform_policy import GateClassification, PlatformPolicy


MappedEffect = Literal["pass", "warning", "advisory", "block"]


class EvalPolicyError(ValueError):
    pass


@dataclass(frozen=True)
class MappedEvalResult:
    eval_id: str
    check_id: str
    status: str
    classification: GateClassification
    effect: MappedEffect


@dataclass(frozen=True)
class EvalGateSummary:
    release_id: str
    eligible: bool
    mapped: tuple[MappedEvalResult, ...]
    blocking_failures: tuple[str, ...]
    warnings: tuple[str, ...]
    advisories: tuple[str, ...]


def map_eval_results(
    results: Sequence[EvalResult],
    policy: PlatformPolicy,
) -> EvalGateSummary:
    if not results:
        raise EvalPolicyError("at least one EvalResult is required")

    rule_ids = [rule.check_id for rule in policy.spec.eval_rules]
    if len(set(rule_ids)) != len(rule_ids):
        raise EvalPolicyError("PlatformPolicy evalRules contains duplicate checkId values")

    rules = {rule.check_id: rule.classification for rule in policy.spec.eval_rules}
    for check_id in policy.spec.security_invariant_checks:
        classification = rules.get(check_id)
        if classification is None:
            raise EvalPolicyError(
                f"security invariant check {check_id!r} is missing from evalRules"
            )
        if classification != "blocking":
            raise EvalPolicyError(
                f"security invariant check {check_id!r} must be classified blocking"
            )

    release_ids = {result.release_id for result in results}
    if len(release_ids) != 1:
        raise EvalPolicyError("EvalResults from different releaseId values cannot share one gate")
    release_id = next(iter(release_ids))

    mapped: list[MappedEvalResult] = []
    blocking_failures: list[str] = []
    warnings: list[str] = []
    advisories: list[str] = []

    invariant_ids = set(policy.spec.security_invariant_checks)

    for result in results:
        classification = rules.get(result.check_id)
        if classification is None:
            raise EvalPolicyError(
                f"EvalResult check {result.check_id!r} is not mapped by PlatformPolicy"
            )
        if result.check_id in invariant_ids and result.family != "security_policy":
            raise EvalPolicyError(
                f"security invariant check {result.check_id!r} must use security_policy family"
            )

        if result.status == "PASS":
            effect: MappedEffect = "pass"
        elif result.status == "PASS_WITH_WARNINGS":
            if classification == "advisory":
                effect = "advisory"
                advisories.append(result.check_id)
            else:
                effect = "warning"
                warnings.append(result.check_id)
        elif classification == "blocking":
            effect = "block"
            blocking_failures.append(result.check_id)
        elif classification == "warning":
            effect = "warning"
            warnings.append(result.check_id)
        else:
            effect = "advisory"
            advisories.append(result.check_id)

        mapped.append(
            MappedEvalResult(
                eval_id=result.eval_id,
                check_id=result.check_id,
                status=result.status,
                classification=classification,
                effect=effect,
            )
        )

    return EvalGateSummary(
        release_id=release_id,
        eligible=not blocking_failures,
        mapped=tuple(mapped),
        blocking_failures=tuple(blocking_failures),
        warnings=tuple(warnings),
        advisories=tuple(advisories),
    )
