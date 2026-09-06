import unittest
from datetime import datetime, timedelta, timezone

from agent_factory_core.capability_gateway import (
    CapabilityGateway,
    CapabilityRegistration,
    CapabilitySpec,
)
from agent_factory_core.contracts import ExecutionContext
from agent_factory_core.memory_gateway import MemoryGateway
from agent_factory_core.model_router import ModelRouter
from agent_factory_core.orchestrator import (
    BoundedHybridOrchestrator,
    BoundedPlan,
    CapabilityPlanStep,
    MemoryReadPlanStep,
    MemoryWritePlanStep,
    ModelPlanStep,
    OrchestratorLimits,
    ToolPlanStep,
)
from agent_factory_core.synthetic_model_adapters import (
    build_deterministic_model_adapter,
    build_stub_model_adapter,
)
from agent_factory_core.synthetic_readonly_tool import build_synthetic_lookup_tool
from agent_factory_core.tool_gateway import ToolGateway


def context(
    *,
    tool_bindings: dict[str, str] | None = None,
    capability_bindings: dict[str, str] | None = None,
    deadline: datetime | None = None,
) -> ExecutionContext:
    return ExecutionContext(
        apiVersion="agentfactory.io/v1alpha1",
        kind="ExecutionContext",
        requestId="req-orch-1",
        traceId="trace-orch-1",
        actorId="user-1",
        actorType="user",
        tenantId="tenant-a",
        environment="sandbox",
        agentId="test-agent",
        agentReleaseId="release-orch-1",
        trustProfile="internal",
        permissions=(
            "model.invoke",
            "synthetic.lookup",
            "capability.synthetic.invoke",
            "memory.read",
            "memory.write",
        ),
        dataClassification="internal",
        capabilityBindings=capability_bindings
        if capability_bindings is not None
        else {"synthetic.capability": "cap.synthetic.v1"},
        providerProfile="balanced",
        toolBindings=tool_bindings
        if tool_bindings is not None
        else {"synthetic.lookup": "tool.synthetic.lookup.v1"},
        memoryConfig={
            "allowedClasses": ["session", "task_working"],
            "allowedPurposes": ["conversation", "task"],
            "allowedRetentionProfiles": ["session", "task"],
            "readEnabled": True,
            "writeEnabled": True,
            "minimumTrustProfile": "internal",
        },
        budgetConfig={},
        deadline=deadline or datetime.now(timezone.utc) + timedelta(minutes=2),
    )


def capability_registration() -> CapabilityRegistration:
    spec = CapabilitySpec(
        capability_ref="synthetic.capability",
        implementation_id="cap.synthetic.v1",
        required_permission="capability.synthetic.invoke",
        minimum_trust_profile="internal",
        allowed_data_classifications=("internal",),
    )

    def handler(payload: dict) -> dict:
        return {"capability": payload.get("value")}

    return CapabilityRegistration(spec=spec, handler=handler)


def orchestrator(memory_gateway: MemoryGateway | None = None) -> BoundedHybridOrchestrator:
    primary = build_deterministic_model_adapter()
    stub = build_stub_model_adapter()
    model_router = ModelRouter(
        (primary, stub),
        routes={"balanced": (primary.spec.implementation_id, stub.spec.implementation_id)},
    )
    return BoundedHybridOrchestrator(
        model_router=model_router,
        tool_gateway=ToolGateway((build_synthetic_lookup_tool(),)),
        memory_gateway=memory_gateway or MemoryGateway(),
        capability_gateway=CapabilityGateway((capability_registration(),)),
    )


class BoundedHybridOrchestratorTests(unittest.TestCase):
    def test_executes_one_bounded_capability_model_tool_memory_plan(self) -> None:
        plan = BoundedPlan(
            steps=(
                CapabilityPlanStep("cap", "synthetic.capability", {"value": "ok"}),
                ModelPlanStep("model", "hello model"),
                ToolPlanStep("tool", "synthetic.lookup", {"key": "alpha"}),
                MemoryWritePlanStep(
                    "write",
                    memory_class="task_working",
                    purpose="task",
                    key="result",
                    content={"status": "saved"},
                    retention_profile="task",
                    source_reference="synthetic:orchestrator",
                ),
                MemoryReadPlanStep(
                    "read",
                    memory_class="task_working",
                    purpose="task",
                    key="result",
                ),
            )
        )
        result = orchestrator().execute(
            context(),
            plan=plan,
            limits=OrchestratorLimits(max_steps=5, max_repeats_per_operation=2),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(result.completed)
        self.assertEqual(len(result.steps), 5)
        self.assertEqual(result.steps[0].output, {"capability": "ok"})
        self.assertEqual(result.steps[1].output, "primary:hello model")
        self.assertEqual(result.steps[2].output, {"found": True, "value": "A"})
        self.assertEqual(result.steps[3].output, {"key": "result"})
        self.assertEqual(result.steps[4].output, {"status": "saved"})
        self.assertTrue(all(step.audit_event.trace_id == "trace-orch-1" for step in result.steps))

    def test_plan_stops_on_first_denied_gateway_step(self) -> None:
        memory = MemoryGateway()
        orch = orchestrator(memory)
        ctx = context(tool_bindings={})
        plan = BoundedPlan(
            steps=(
                ToolPlanStep("tool", "synthetic.lookup", {"key": "alpha"}),
                MemoryWritePlanStep(
                    "write",
                    memory_class="session",
                    purpose="conversation",
                    key="should-not-exist",
                    content="blocked",
                    retention_profile="session",
                ),
            )
        )
        result = orch.execute(
            ctx,
            plan=plan,
            limits=OrchestratorLimits(max_steps=2, max_repeats_per_operation=2),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.completed)
        self.assertEqual(result.rule, "tool_binding")
        self.assertEqual(len(result.steps), 1)

        read = memory.read(
            ctx,
            request=__import__("agent_factory_core.memory_gateway", fromlist=["MemoryReadRequest"]).MemoryReadRequest(
                memory_class="session",
                purpose="conversation",
                data_classification="internal",
                key="should-not-exist",
            ),
            platform_policy_ref="platform-default@1",
        )
        self.assertIsNone(read.entry)

    def test_max_step_limit_stops_new_work(self) -> None:
        plan = BoundedPlan(
            steps=(
                ModelPlanStep("m1", "one"),
                ModelPlanStep("m2", "two"),
            )
        )
        result = orchestrator().execute(
            context(),
            plan=plan,
            limits=OrchestratorLimits(max_steps=1, max_repeats_per_operation=2),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.completed)
        self.assertEqual(result.rule, "hop_limit")
        self.assertEqual(len(result.steps), 2)
        self.assertTrue(result.steps[0].allowed)
        self.assertFalse(result.steps[1].allowed)

    def test_cycle_limit_stops_repeated_operation(self) -> None:
        plan = BoundedPlan(
            steps=(
                ToolPlanStep("t1", "synthetic.lookup", {"key": "alpha"}),
                ToolPlanStep("t2", "synthetic.lookup", {"key": "beta"}),
            )
        )
        result = orchestrator().execute(
            context(),
            plan=plan,
            limits=OrchestratorLimits(max_steps=2, max_repeats_per_operation=1),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.completed)
        self.assertEqual(result.rule, "cycle_limit")
        self.assertEqual(len(result.steps), 2)

    def test_deadline_is_rechecked_by_gateway_during_plan(self) -> None:
        deadline = datetime.now(timezone.utc)
        result = orchestrator().execute(
            context(deadline=deadline),
            plan=BoundedPlan(steps=(ModelPlanStep("model", "hello"),)),
            limits=OrchestratorLimits(max_steps=1, max_repeats_per_operation=1),
            platform_policy_ref="platform-default@1",
            now=deadline,
        )
        self.assertFalse(result.completed)
        self.assertEqual(result.rule, "deadline")

    def test_unbound_capability_is_denied_without_runtime_reresolution(self) -> None:
        result = orchestrator().execute(
            context(capability_bindings={}),
            plan=BoundedPlan(
                steps=(CapabilityPlanStep("cap", "synthetic.capability", {"value": "x"}),)
            ),
            limits=OrchestratorLimits(max_steps=1, max_repeats_per_operation=1),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.completed)
        self.assertEqual(result.rule, "capability_binding")


if __name__ == "__main__":
    unittest.main()
