from __future__ import annotations

from typing import Literal


RequestedReleaseStrategy = Literal["human-required", "policy-auto", "policy"]
EffectiveReleaseStrategy = Literal["human-required", "policy-auto"]


def resolve_release_strategy(
    requested: RequestedReleaseStrategy,
    minimum: EffectiveReleaseStrategy,
) -> EffectiveReleaseStrategy:
    """Resolve a concrete strategy without allowing policy to become less strict."""
    if requested == "human-required":
        return "human-required"
    if requested == "policy":
        return minimum
    if minimum == "human-required":
        return "human-required"
    return "policy-auto"
