from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from agent_factory_core.contracts.execution_context import ExecutionContext


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    rule: str
    reason: str


def evaluate_request_authority(
    context: ExecutionContext,
    *,
    tenant_id: str,
    permission: str,
    data_classification: str | None = None,
    now: datetime | None = None,
) -> PolicyDecision:
    """Evaluate request-time authority only from trusted ExecutionContext fields."""
    current_time = now or datetime.now(timezone.utc)

    if current_time >= context.deadline:
        return PolicyDecision(False, "deadline", "execution deadline has expired")

    if tenant_id != context.tenant_id:
        return PolicyDecision(False, "tenant", "request tenant does not match trusted context")

    if permission not in context.permissions:
        return PolicyDecision(False, "permission", "permission is not granted by effective runtime authority")

    if data_classification is not None and data_classification != context.data_classification:
        return PolicyDecision(False, "data_classification", "request classification does not match trusted context")

    return PolicyDecision(True, "authority", "request is inside trusted runtime authority")
