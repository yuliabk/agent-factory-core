from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .contracts.effective_release_config import EffectiveReleaseConfig
from .contracts.release_strategy import EffectiveReleaseStrategy
from .eval_policy import EvalGateSummary


ReleaseAction = Literal["block", "auto-release", "require-human"]


class ReleaseStrategyError(ValueError):
    pass


@dataclass(frozen=True)
class ReleaseStrategyDecision:
    release_id: str
    strategy: EffectiveReleaseStrategy
    action: ReleaseAction
    reason: str


def decide_release_action(
    release: EffectiveReleaseConfig,
    gate: EvalGateSummary,
) -> ReleaseStrategyDecision:
    if gate.release_id != release.metadata.release_id:
        raise ReleaseStrategyError(
            "EvalGateSummary release_id does not match EffectiveReleaseConfig releaseId"
        )

    strategy = release.spec.release_strategy
    if not gate.eligible:
        return ReleaseStrategyDecision(
            release_id=release.metadata.release_id,
            strategy=strategy,
            action="block",
            reason="one or more blocking evaluation gates failed",
        )

    if strategy == "human-required":
        return ReleaseStrategyDecision(
            release_id=release.metadata.release_id,
            strategy=strategy,
            action="require-human",
            reason="effective release strategy requires human approval",
        )

    return ReleaseStrategyDecision(
        release_id=release.metadata.release_id,
        strategy=strategy,
        action="auto-release",
        reason="all blocking gates passed and effective policy permits automatic release",
    )
