from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from agent_factory_core.contracts.execution_context import ExecutionContext
from agent_factory_core.contracts.runtime_audit_event import RuntimeAuditEvent


def build_audit_event(
    context: ExecutionContext,
    *,
    platform_policy_ref: str,
    operation: str,
    decision: str,
    result: str,
    exception_policy_refs: tuple[str, ...] = (),
    approval_ref: str | None = None,
    target_ref: str | None = None,
    cost_amount: Decimal | None = None,
    cost_currency: str | None = None,
    timestamp: datetime | None = None,
) -> RuntimeAuditEvent:
    """Build minimized runtime evidence without prompts, secrets or payload bodies."""
    if not platform_policy_ref:
        raise ValueError("platform_policy_ref is required")
    if not operation:
        raise ValueError("operation is required")
    if not decision:
        raise ValueError("decision is required")
    if not result:
        raise ValueError("result is required")
    if cost_amount is not None and cost_amount < 0:
        raise ValueError("cost_amount must be non-negative")
    if (cost_amount is None) != (cost_currency is None):
        raise ValueError("cost_amount and cost_currency must either both be set or both be null")

    return RuntimeAuditEvent(
        apiVersion="agentfactory.io/v1alpha1",
        kind="RuntimeAuditEvent",
        timestamp=timestamp or datetime.now(timezone.utc),
        tenantId=context.tenant_id,
        requestId=context.request_id,
        traceId=context.trace_id,
        actorId=context.actor_id,
        actorType=context.actor_type,
        agentReleaseId=context.agent_release_id,
        platformPolicyRef=platform_policy_ref,
        exceptionPolicyRefs=exception_policy_refs,
        approvalRef=approval_ref,
        operation=operation,
        targetRef=target_ref,
        decision=decision,
        result=result,
        costAmount=str(cost_amount) if cost_amount is not None else None,
        costCurrency=cost_currency,
    )
