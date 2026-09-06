from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Mapping

from .contracts.execution_context import ExecutionContext
from .contracts.runtime_audit_event import RuntimeAuditEvent
from .contracts.trust import TrustProfile
from .runtime.audit import build_audit_event
from .runtime.policy import evaluate_request_authority


@dataclass(frozen=True)
class CapabilitySpec:
    capability_ref: str
    implementation_id: str
    required_permission: str
    minimum_trust_profile: TrustProfile
    allowed_data_classifications: tuple[str, ...]
    estimated_cost: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if not self.capability_ref or not self.implementation_id or not self.required_permission:
            raise ValueError("capability_ref, implementation_id and required_permission are required")
        if not self.allowed_data_classifications:
            raise ValueError("allowed_data_classifications must not be empty")
        if self.estimated_cost < 0:
            raise ValueError("estimated_cost must be non-negative")


CapabilityHandler = Callable[[Mapping[str, Any]], Mapping[str, Any]]
ContextCapabilityHandler = Callable[[ExecutionContext, Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class CapabilityRegistration:
    spec: CapabilitySpec
    handler: CapabilityHandler | None = None
    context_handler: ContextCapabilityHandler | None = None

    def __post_init__(self) -> None:
        if (self.handler is None) == (self.context_handler is None):
            raise ValueError("exactly one of handler or context_handler is required")


@dataclass(frozen=True)
class CapabilityInvocationResult:
    allowed: bool
    rule: str
    reason: str
    output: Mapping[str, Any] | None
    implementation_id: str | None
    audit_event: RuntimeAuditEvent


class CapabilityGateway:
    """Runtime dispatcher for capability bindings already compiled into ExecutionContext."""

    def __init__(self, registrations: tuple[CapabilityRegistration, ...] = ()) -> None:
        self._by_implementation = {
            registration.spec.implementation_id: registration for registration in registrations
        }
        if len(self._by_implementation) != len(registrations):
            raise ValueError("duplicate capability implementation_id")

    def invoke(
        self,
        context: ExecutionContext,
        *,
        capability_ref: str,
        payload: Mapping[str, Any],
        data_classification: str,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...] = (),
        approval_ref: str | None = None,
        now: datetime | None = None,
    ) -> CapabilityInvocationResult:
        implementation_id = context.capability_bindings.get(capability_ref)
        if implementation_id is None:
            return self._deny(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="capability_binding",
                reason="capability is not bound by trusted ExecutionContext",
                now=now,
            )

        registration = self._by_implementation.get(implementation_id)
        if registration is None or registration.spec.capability_ref != capability_ref:
            return self._deny(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="capability_registration",
                reason="compiled capability binding does not resolve to a compatible runtime registration",
                now=now,
            )

        spec = registration.spec
        if spec.estimated_cost > 0:
            return self._deny(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="budget_preflight",
                reason="costed capabilities remain blocked until runtime budget accounting state is attached",
                now=now,
            )

        if data_classification not in spec.allowed_data_classifications:
            return self._deny(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="capability_data_classification",
                reason="capability implementation does not allow the effective data classification",
                now=now,
            )

        authority = evaluate_request_authority(
            context,
            tenant_id=context.tenant_id,
            permission=spec.required_permission,
            data_classification=data_classification,
            required_trust_profile=spec.minimum_trust_profile,
            now=now,
        )
        if not authority.allowed:
            return self._deny(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule=authority.rule,
                reason=authority.reason,
                now=now,
            )

        if registration.context_handler is not None:
            output = dict(registration.context_handler(context, dict(payload)))
        else:
            assert registration.handler is not None
            output = dict(registration.handler(dict(payload)))

        return CapabilityInvocationResult(
            allowed=True,
            rule="capability_gateway",
            reason="compiled capability invocation completed",
            output=output,
            implementation_id=implementation_id,
            audit_event=build_audit_event(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="capability.invoke",
                target_ref=implementation_id,
                decision="allow",
                result="success",
                timestamp=now,
            ),
        )

    @staticmethod
    def _deny(
        context: ExecutionContext,
        *,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...],
        approval_ref: str | None,
        rule: str,
        reason: str,
        now: datetime | None,
    ) -> CapabilityInvocationResult:
        return CapabilityInvocationResult(
            allowed=False,
            rule=rule,
            reason=reason,
            output=None,
            implementation_id=None,
            audit_event=build_audit_event(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="capability.invoke",
                target_ref=None,
                decision="deny",
                result=rule,
                timestamp=now,
            ),
        )
