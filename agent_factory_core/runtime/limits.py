from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeLimits:
    max_hops: int
    max_repeats_per_capability: int

    def __post_init__(self) -> None:
        if self.max_hops < 0:
            raise ValueError("max_hops must be non-negative")
        if self.max_repeats_per_capability < 1:
            raise ValueError("max_repeats_per_capability must be at least 1")


@dataclass(frozen=True)
class LimitDecision:
    allowed: bool
    rule: str
    reason: str


def evaluate_limits(
    *,
    limits: RuntimeLimits,
    current_hops: int,
    capability_path: tuple[str, ...],
    next_capability: str,
) -> LimitDecision:
    if current_hops >= limits.max_hops:
        return LimitDecision(False, "hop_limit", "maximum delegation hop count reached")

    repeats = capability_path.count(next_capability)
    if repeats >= limits.max_repeats_per_capability:
        return LimitDecision(False, "cycle_limit", "capability repetition limit reached")

    return LimitDecision(True, "runtime_limits", "delegation is inside runtime limits")
