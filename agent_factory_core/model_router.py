from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Callable, Mapping

from .contracts.execution_context import ExecutionContext
from .contracts.runtime_audit_event import RuntimeAuditEvent
from .contracts.trust import TrustProfile
from .runtime.audit import build_audit_event
from .runtime.policy import evaluate_request_authority


@dataclass(frozen=True)
class ModelRequest:
    input_text: str
    data_classification: str


@dataclass(frozen=True)
class ModelAdapterOutput:
    text: str
    input_units: int
    output_units: int


@dataclass(frozen=True)
class ModelAdapterSpec:
    implementation_id: str
    version: str
    supported_profiles: tuple[str, ...]
    allowed_data_classifications: tuple[str, ...]
    minimum_trust_profile: TrustProfile
    estimated_cost: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if not self.implementation_id or not self.version:
            raise ValueError("implementation_id and version are required")
        if not self.supported_profiles:
            raise ValueError("supported_profiles must not be empty")
        if not self.allowed_data_classifications:
            raise ValueError("allowed_data_classifications must not be empty")
        if self.estimated_cost < 0:
            raise ValueError("estimated_cost must be non-negative")


ModelHandler = Callable[[ModelRequest], ModelAdapterOutput]


@dataclass(frozen=True)
class ModelRegistration:
    spec: ModelAdapterSpec
    handler: ModelHandler


@dataclass(frozen=True)
class ModelInvocationResult:
    allowed: bool
    rule: str
    reason: str
    output: ModelAdapterOutput | None
    implementation_id: str | None
    audit_event: RuntimeAuditEvent


class ModelAdapterUnavailable(RuntimeError):
    pass


class ModelRouter:
    """Provider-neutral router for the first zero-cost synthetic model slice."""

    def __init__(
        self,
        registrations: tuple[ModelRegistration, ...],
        *,
        routes: Mapping[str, tuple[str, ...]],
    ) -> None:
        self._registrations = {item.spec.implementation_id: item for item in registrations}
        if len(self._registrations) != len(registrations):
            raise ValueError("duplicate model implementation_id")
        self._routes = {profile: tuple(implementations) for profile, implementations in routes.items()}

    def invoke(
        self,
        context: ExecutionContext,
        *,
        request: ModelRequest,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...] = (),
        approval_ref: str | None = None,
        now: datetime | None = None,
    ) -> ModelInvocationResult:
        if not request.input_text:
            return self._deny(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="model_request",
                reason="input_text is required",
                now=now,
            )

        candidates = self._routes.get(context.provider_profile, ())
        if not candidates:
            return self._deny(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="model_route",
                reason="trusted provider profile has no registered model route",
                now=now,
            )

        last_reason = "no compatible model implementation"
        for implementation_id in candidates:
            registration = self._registrations.get(implementation_id)
            if registration is None:
                last_reason = "configured model route references an unregistered implementation"
                continue

            spec = registration.spec
            if context.provider_profile not in spec.supported_profiles:
                last_reason = "model implementation does not support the trusted provider profile"
                continue
            if request.data_classification not in spec.allowed_data_classifications:
                last_reason = "model implementation does not allow the effective data classification"
                continue
            if spec.estimated_cost > 0:
                last_reason = "costed model adapters remain blocked until runtime budget accounting state is attached"
                continue

            authority = evaluate_request_authority(
                context,
                tenant_id=context.tenant_id,
                permission="model.invoke",
                data_classification=request.data_classification,
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

            try:
                output = registration.handler(request)
            except ModelAdapterUnavailable:
                last_reason = f"model implementation {implementation_id} unavailable"
                continue

            if output.input_units < 0 or output.output_units < 0:
                return self._deny(
                    context,
                    platform_policy_ref=platform_policy_ref,
                    exception_policy_refs=exception_policy_refs,
                    approval_ref=approval_ref,
                    rule="model_output",
                    reason="model adapter returned invalid usage units",
                    now=now,
                )

            return ModelInvocationResult(
                allowed=True,
                rule="model_router",
                reason="provider-neutral model invocation completed",
                output=output,
                implementation_id=implementation_id,
                audit_event=build_audit_event(
                    context,
                    platform_policy_ref=platform_policy_ref,
                    exception_policy_refs=exception_policy_refs,
                    approval_ref=approval_ref,
                    operation="model.invoke",
                    target_ref=implementation_id,
                    decision="allow",
                    result="success",
                    timestamp=now,
                ),
            )

        return self._deny(
            context,
            platform_policy_ref=platform_policy_ref,
            exception_policy_refs=exception_policy_refs,
            approval_ref=approval_ref,
            rule="model_route",
            reason=last_reason,
            now=now,
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
    ) -> ModelInvocationResult:
        return ModelInvocationResult(
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
                operation="model.invoke",
                target_ref=None,
                decision="deny",
                result=rule,
                timestamp=now,
            ),
        )
