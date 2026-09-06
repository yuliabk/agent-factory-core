from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from .capability_gateway import CapabilityGateway
from .contracts.execution_context import ExecutionContext
from .contracts.runtime_audit_event import RuntimeAuditEvent
from .memory_gateway import MemoryGateway, MemoryReadRequest, MemoryWriteRequest
from .model_router import ModelRequest, ModelRouter
from .runtime.audit import build_audit_event
from .runtime.limits import RuntimeLimits, evaluate_limits
from .tool_gateway import ToolGateway


@dataclass(frozen=True)
class ModelPlanStep:
    step_id: str
    input_text: str


@dataclass(frozen=True)
class ToolPlanStep:
    step_id: str
    tool_ref: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class CapabilityPlanStep:
    step_id: str
    capability_ref: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class MemoryWritePlanStep:
    step_id: str
    memory_class: str
    purpose: str
    key: str
    content: Any
    retention_profile: str
    source_reference: str | None = None


@dataclass(frozen=True)
class MemoryReadPlanStep:
    step_id: str
    memory_class: str
    purpose: str
    key: str


PlanStep = (
    ModelPlanStep
    | ToolPlanStep
    | CapabilityPlanStep
    | MemoryWritePlanStep
    | MemoryReadPlanStep
)


@dataclass(frozen=True)
class BoundedPlan:
    steps: tuple[PlanStep, ...]


@dataclass(frozen=True)
class OrchestratorLimits:
    max_steps: int
    max_repeats_per_operation: int

    def __post_init__(self) -> None:
        if self.max_steps < 1:
            raise ValueError("max_steps must be at least 1")
        if self.max_repeats_per_operation < 1:
            raise ValueError("max_repeats_per_operation must be at least 1")


@dataclass(frozen=True)
class OrchestratorStepResult:
    step_id: str
    operation: str
    allowed: bool
    rule: str
    reason: str
    output: Any
    audit_event: RuntimeAuditEvent


@dataclass(frozen=True)
class OrchestrationResult:
    completed: bool
    rule: str
    reason: str
    steps: tuple[OrchestratorStepResult, ...]


class BoundedHybridOrchestrator:
    """Executes an Agent-provided bounded plan while preserving per-gateway authority checks."""

    def __init__(
        self,
        *,
        model_router: ModelRouter,
        tool_gateway: ToolGateway,
        memory_gateway: MemoryGateway,
        capability_gateway: CapabilityGateway,
    ) -> None:
        self._model_router = model_router
        self._tool_gateway = tool_gateway
        self._memory_gateway = memory_gateway
        self._capability_gateway = capability_gateway

    def execute(
        self,
        context: ExecutionContext,
        *,
        plan: BoundedPlan,
        limits: OrchestratorLimits,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...] = (),
        approval_ref: str | None = None,
        now: datetime | None = None,
    ) -> OrchestrationResult:
        if not plan.steps:
            return OrchestrationResult(
                completed=True,
                rule="orchestrator",
                reason="empty plan completed",
                steps=(),
            )

        runtime_limits = RuntimeLimits(
            max_hops=limits.max_steps,
            max_repeats_per_capability=limits.max_repeats_per_operation,
        )
        operation_path: list[str] = []
        results: list[OrchestratorStepResult] = []

        for index, step in enumerate(plan.steps):
            operation = self._operation_key(step)
            limit = evaluate_limits(
                limits=runtime_limits,
                current_hops=index,
                capability_path=tuple(operation_path),
                next_capability=operation,
            )
            if not limit.allowed:
                audit = build_audit_event(
                    context,
                    platform_policy_ref=platform_policy_ref,
                    exception_policy_refs=exception_policy_refs,
                    approval_ref=approval_ref,
                    operation="orchestrator.step",
                    target_ref=step.step_id,
                    decision="deny",
                    result=limit.rule,
                    timestamp=now,
                )
                results.append(
                    OrchestratorStepResult(
                        step_id=step.step_id,
                        operation=operation,
                        allowed=False,
                        rule=limit.rule,
                        reason=limit.reason,
                        output=None,
                        audit_event=audit,
                    )
                )
                return OrchestrationResult(
                    completed=False,
                    rule=limit.rule,
                    reason=limit.reason,
                    steps=tuple(results),
                )

            operation_path.append(operation)
            step_result = self._execute_step(
                context,
                step=step,
                operation=operation,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                now=now,
            )
            results.append(step_result)
            if not step_result.allowed:
                return OrchestrationResult(
                    completed=False,
                    rule=step_result.rule,
                    reason=step_result.reason,
                    steps=tuple(results),
                )

        return OrchestrationResult(
            completed=True,
            rule="orchestrator",
            reason="bounded plan completed",
            steps=tuple(results),
        )

    def _execute_step(
        self,
        context: ExecutionContext,
        *,
        step: PlanStep,
        operation: str,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...],
        approval_ref: str | None,
        now: datetime | None,
    ) -> OrchestratorStepResult:
        if isinstance(step, ModelPlanStep):
            result = self._model_router.invoke(
                context,
                request=ModelRequest(
                    input_text=step.input_text,
                    data_classification=context.data_classification,
                ),
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                now=now,
            )
            output = None if result.output is None else result.output.text
            return self._result(step.step_id, operation, result, output)

        if isinstance(step, ToolPlanStep):
            result = self._tool_gateway.execute(
                context,
                tool_ref=step.tool_ref,
                tenant_id=context.tenant_id,
                data_classification=context.data_classification,
                payload=step.payload,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                now=now,
            )
            return self._result(step.step_id, operation, result, result.output)

        if isinstance(step, CapabilityPlanStep):
            result = self._capability_gateway.invoke(
                context,
                capability_ref=step.capability_ref,
                payload=step.payload,
                data_classification=context.data_classification,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                now=now,
            )
            return self._result(step.step_id, operation, result, result.output)

        if isinstance(step, MemoryWritePlanStep):
            result = self._memory_gateway.write(
                context,
                request=MemoryWriteRequest(
                    memory_class=step.memory_class,  # type: ignore[arg-type]
                    purpose=step.purpose,
                    data_classification=context.data_classification,
                    key=step.key,
                    content=step.content,
                    retention_profile=step.retention_profile,
                    source_reference=step.source_reference,
                ),
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                now=now,
            )
            output = None if result.entry is None else {"key": result.entry.key}
            return self._result(step.step_id, operation, result, output)

        if isinstance(step, MemoryReadPlanStep):
            result = self._memory_gateway.read(
                context,
                request=MemoryReadRequest(
                    memory_class=step.memory_class,  # type: ignore[arg-type]
                    purpose=step.purpose,
                    data_classification=context.data_classification,
                    key=step.key,
                ),
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                now=now,
            )
            output = None if result.entry is None else result.entry.content
            return self._result(step.step_id, operation, result, output)

        raise TypeError(f"unsupported plan step: {type(step)!r}")

    @staticmethod
    def _result(step_id: str, operation: str, result: Any, output: Any) -> OrchestratorStepResult:
        return OrchestratorStepResult(
            step_id=step_id,
            operation=operation,
            allowed=result.allowed,
            rule=result.rule,
            reason=result.reason,
            output=output,
            audit_event=result.audit_event,
        )

    @staticmethod
    def _operation_key(step: PlanStep) -> str:
        if isinstance(step, ModelPlanStep):
            return "model.invoke"
        if isinstance(step, ToolPlanStep):
            return f"tool:{step.tool_ref}"
        if isinstance(step, CapabilityPlanStep):
            return f"capability:{step.capability_ref}"
        if isinstance(step, MemoryWritePlanStep):
            return f"memory.write:{step.memory_class}"
        if isinstance(step, MemoryReadPlanStep):
            return f"memory.read:{step.memory_class}"
        raise TypeError(f"unsupported plan step: {type(step)!r}")
