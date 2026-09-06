from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Literal, Mapping

from jsonschema import Draft202012Validator, ValidationError

from .contracts.execution_context import ExecutionContext
from .contracts.runtime_audit_event import RuntimeAuditEvent
from .contracts.trust import TrustProfile
from .runtime.audit import build_audit_event
from .runtime.policy import evaluate_request_authority


SideEffectClass = Literal[
    "read_only",
    "reversible_write",
    "external_message",
    "financial",
    "permission_change",
    "irreversible_write",
    "sensitive_domain_action",
]


@dataclass(frozen=True)
class ToolSpec:
    tool_ref: str
    binding_id: str
    version: str
    required_permission: str
    minimum_trust_profile: TrustProfile
    allowed_data_classifications: tuple[str, ...]
    side_effect_class: SideEffectClass
    input_schema: Mapping[str, Any]
    output_schema: Mapping[str, Any]
    estimated_cost: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if not self.tool_ref or not self.binding_id or not self.version or not self.required_permission:
            raise ValueError("tool_ref, binding_id, version and required_permission are required")
        if not self.allowed_data_classifications:
            raise ValueError("allowed_data_classifications must not be empty")
        if self.estimated_cost < 0:
            raise ValueError("estimated_cost must be non-negative")


ToolHandler = Callable[[Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class ToolRegistration:
    spec: ToolSpec
    handler: ToolHandler


@dataclass(frozen=True)
class ToolExecutionResult:
    allowed: bool
    rule: str
    reason: str
    output: Mapping[str, Any] | None
    audit_event: RuntimeAuditEvent


class ToolGateway:
    """Governed in-process Tool Gateway for the first read-only vertical slice."""

    def __init__(self, registrations: tuple[ToolRegistration, ...] = ()) -> None:
        self._by_binding = {registration.spec.binding_id: registration for registration in registrations}
        if len(self._by_binding) != len(registrations):
            raise ValueError("duplicate tool binding_id")

    def execute(
        self,
        context: ExecutionContext,
        *,
        tool_ref: str,
        tenant_id: str,
        data_classification: str,
        payload: Mapping[str, Any],
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...] = (),
        approval_ref: str | None = None,
        now: datetime | None = None,
    ) -> ToolExecutionResult:
        binding_id = context.tool_bindings.get(tool_ref)
        if binding_id is None:
            return self._deny(
                context,
                tool_ref=tool_ref,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="tool_binding",
                reason="tool is not bound by trusted ExecutionContext",
                now=now,
            )

        registration = self._by_binding.get(binding_id)
        if registration is None or registration.spec.tool_ref != tool_ref:
            return self._deny(
                context,
                tool_ref=binding_id,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="tool_registration",
                reason="trusted binding does not resolve to a registered compatible tool",
                now=now,
            )

        spec = registration.spec
        if spec.side_effect_class != "read_only":
            return self._deny(
                context,
                tool_ref=binding_id,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="side_effect_class",
                reason="first Tool Gateway slice permits read_only tools only",
                now=now,
            )

        if spec.estimated_cost > 0:
            return self._deny(
                context,
                tool_ref=binding_id,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="budget_preflight",
                reason="costed tools remain blocked until runtime budget accounting state is attached",
                now=now,
            )

        authority = evaluate_request_authority(
            context,
            tenant_id=tenant_id,
            permission=spec.required_permission,
            data_classification=data_classification,
            required_trust_profile=spec.minimum_trust_profile,
            now=now,
        )
        if not authority.allowed:
            return self._deny(
                context,
                tool_ref=binding_id,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule=authority.rule,
                reason=authority.reason,
                now=now,
            )

        if data_classification not in spec.allowed_data_classifications:
            return self._deny(
                context,
                tool_ref=binding_id,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="tool_data_classification",
                reason="tool does not accept the effective data classification",
                now=now,
            )

        try:
            Draft202012Validator(spec.input_schema).validate(dict(payload))
        except ValidationError as exc:
            return self._deny(
                context,
                tool_ref=binding_id,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="input_schema",
                reason=f"tool input failed schema validation: {exc.message}",
                now=now,
            )

        output = dict(registration.handler(dict(payload)))
        try:
            Draft202012Validator(spec.output_schema).validate(output)
        except ValidationError as exc:
            return self._deny(
                context,
                tool_ref=binding_id,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                rule="output_schema",
                reason=f"tool output failed schema validation: {exc.message}",
                now=now,
            )

        audit_event = build_audit_event(
            context,
            platform_policy_ref=platform_policy_ref,
            exception_policy_refs=exception_policy_refs,
            approval_ref=approval_ref,
            operation="tool.execute",
            target_ref=binding_id,
            decision="allow",
            result="success",
            timestamp=now,
        )
        return ToolExecutionResult(
            allowed=True,
            rule="tool_gateway",
            reason="governed read-only tool execution completed",
            output=output,
            audit_event=audit_event,
        )

    def _deny(
        self,
        context: ExecutionContext,
        *,
        tool_ref: str,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...],
        approval_ref: str | None,
        rule: str,
        reason: str,
        now: datetime | None,
    ) -> ToolExecutionResult:
        audit_event = build_audit_event(
            context,
            platform_policy_ref=platform_policy_ref,
            exception_policy_refs=exception_policy_refs,
            approval_ref=approval_ref,
            operation="tool.execute",
            target_ref=tool_ref,
            decision="deny",
            result=rule,
            timestamp=now,
        )
        return ToolExecutionResult(
            allowed=False,
            rule=rule,
            reason=reason,
            output=None,
            audit_event=audit_event,
        )
