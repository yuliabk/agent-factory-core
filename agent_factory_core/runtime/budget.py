from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal


@dataclass(frozen=True)
class BudgetDecision:
    action: Literal["allow", "pause", "stop"]
    rule: str
    reason: str


def evaluate_budget(
    *,
    estimated_cost: Decimal,
    business_remaining: Decimal | None,
    safety_remaining: Decimal,
) -> BudgetDecision:
    """Apply the independent safety cap before the business-budget boundary."""
    if estimated_cost < 0 or safety_remaining < 0 or (business_remaining is not None and business_remaining < 0):
        raise ValueError("budget values must be non-negative")

    if estimated_cost > safety_remaining:
        return BudgetDecision("stop", "safety_cap", "estimated cost exceeds independent emergency safety cap")

    if business_remaining is not None and estimated_cost > business_remaining:
        return BudgetDecision("pause", "business_budget", "estimated cost exceeds approved business budget")

    return BudgetDecision("allow", "budget", "estimated cost is inside runtime budget boundaries")
