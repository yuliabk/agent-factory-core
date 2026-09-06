from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from agent_factory_core.contracts.execution_context import ExecutionContext


@dataclass(frozen=True)
class AuditEvent:
    timestamp: datetime
    tenant_id: str
    request_id: str
    trace_id: str
    actor_id: str
    agent_release_id: str
    platform_policy_ref: str
    exception_policy_refs: tuple[str, ...]
    operation: str
    decision: str
    result: str
    cost_amount: Decimal | None = None
    cost_currency: str | None = None


def build_audit_event(
    context: ExecutionContext,
    *,
    platform_policy_ref: str,
    operation: str,
    decision: str,
    result: str,
    exception_policy_refs: tuple[str, ...] = (),
    cost_amount: Decimal | None = None,
    cost_currency: str | None = None,
    timestamp: datetime | None = None,
) -> AuditEvent:
    """Build a minimized runtime evidence record without prompts, secrets or payload bodies."""
    if not platform_policy_ref:
        raise ValueError("platform_policy_ref is required")
    if not operation:
        raise ValueError("operation is required")
    if cost_amount is not None and cost_amount < 0:
        raise ValueError("cost_amount must be non-negative")
    if cost_amount is not None and not cost_currency:
        raise ValueError("cost_currency is required when cost_amount is provided")

    return AuditEvent(
        timestamp=timestamp or datetime.now(timezone.utc),
        tenant_id=context.tenant_id,
        request_id=context.request_id,
        trace_id=context.trace_id,
        actor_id=context.actor_id,
        agent_release_id=context.agent_release_id,
        platform_policy_ref=platform_policy_ref,
        exception_policy_refs=exception_policy_refs,
        operation=operation,
        decision=decision,
        result=result,
        cost_amount=cost_amount,
        cost_currency=cost_currency,
    )
