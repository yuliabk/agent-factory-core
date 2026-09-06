import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from agent_factory_core.contracts import ExecutionContext
from agent_factory_core.synthetic_readonly_tool import build_synthetic_lookup_tool
from agent_factory_core.tool_gateway import ToolGateway, ToolRegistration, ToolSpec


def context() -> ExecutionContext:
    return ExecutionContext(
        apiVersion="agentfactory.io/v1alpha1",
        kind="ExecutionContext",
        requestId="req-tool-1",
        traceId="trace-tool-1",
        actorId="user-1",
        actorType="user",
        tenantId="tenant-a",
        environment="sandbox",
        agentId="test-agent",
        agentReleaseId="release-tool-1",
        trustProfile="internal",
        permissions=("synthetic.lookup",),
        dataClassification="internal",
        capabilityBindings={},
        providerProfile="balanced",
        toolBindings={"synthetic.lookup": "tool.synthetic.lookup.v1"},
        memoryConfig={},
        budgetConfig={},
        deadline=datetime.now(timezone.utc) + timedelta(minutes=2),
    )


class ToolGatewayContractTests(unittest.TestCase):
    def test_read_only_bound_tool_executes_and_audits(self) -> None:
        ctx = context()
        gateway = ToolGateway((build_synthetic_lookup_tool(),))

        result = gateway.execute(
            ctx,
            tool_ref="synthetic.lookup",
            tenant_id="tenant-a",
            data_classification="internal",
            payload={"key": "alpha"},
            platform_policy_ref="platform-default@1",
        )

        self.assertTrue(result.allowed)
        self.assertEqual(result.output, {"found": True, "value": "A"})
        self.assertEqual(result.audit_event.decision, "allow")
        self.assertEqual(result.audit_event.target_ref, "tool.synthetic.lookup.v1")
        self.assertEqual(ctx.permissions, ("synthetic.lookup",))

    def test_unbound_tool_is_denied_before_execution(self) -> None:
        gateway = ToolGateway((build_synthetic_lookup_tool(),))
        ctx = context().model_copy(update={"tool_bindings": {}})

        result = gateway.execute(
            ctx,
            tool_ref="synthetic.lookup",
            tenant_id="tenant-a",
            data_classification="internal",
            payload={"key": "alpha"},
            platform_policy_ref="platform-default@1",
        )

        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "tool_binding")
        self.assertEqual(result.audit_event.decision, "deny")

    def test_wrong_tenant_is_denied(self) -> None:
        gateway = ToolGateway((build_synthetic_lookup_tool(),))
        result = gateway.execute(
            context(),
            tool_ref="synthetic.lookup",
            tenant_id="tenant-b",
            data_classification="internal",
            payload={"key": "alpha"},
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "tenant")

    def test_tool_minimum_trust_cannot_exceed_execution_context(self) -> None:
        base = build_synthetic_lookup_tool()
        elevated = ToolRegistration(
            spec=ToolSpec(
                tool_ref=base.spec.tool_ref,
                binding_id=base.spec.binding_id,
                version=base.spec.version,
                required_permission=base.spec.required_permission,
                minimum_trust_profile="business",
                allowed_data_classifications=base.spec.allowed_data_classifications,
                side_effect_class="read_only",
                input_schema=base.spec.input_schema,
                output_schema=base.spec.output_schema,
            ),
            handler=base.handler,
        )
        result = ToolGateway((elevated,)).execute(
            context(),
            tool_ref="synthetic.lookup",
            tenant_id="tenant-a",
            data_classification="internal",
            payload={"key": "alpha"},
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "trust_profile")

    def test_costed_tool_is_blocked_until_budget_state_is_attached(self) -> None:
        base = build_synthetic_lookup_tool()
        costed = ToolRegistration(
            spec=ToolSpec(
                tool_ref=base.spec.tool_ref,
                binding_id=base.spec.binding_id,
                version=base.spec.version,
                required_permission=base.spec.required_permission,
                minimum_trust_profile=base.spec.minimum_trust_profile,
                allowed_data_classifications=base.spec.allowed_data_classifications,
                side_effect_class="read_only",
                input_schema=base.spec.input_schema,
                output_schema=base.spec.output_schema,
                estimated_cost=Decimal("0.01"),
            ),
            handler=base.handler,
        )
        result = ToolGateway((costed,)).execute(
            context(),
            tool_ref="synthetic.lookup",
            tenant_id="tenant-a",
            data_classification="internal",
            payload={"key": "alpha"},
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "budget_preflight")

    def test_invalid_input_is_denied_before_handler(self) -> None:
        gateway = ToolGateway((build_synthetic_lookup_tool(),))
        result = gateway.execute(
            context(),
            tool_ref="synthetic.lookup",
            tenant_id="tenant-a",
            data_classification="internal",
            payload={"wrong": "shape"},
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "input_schema")

    def test_non_read_only_registration_is_blocked_in_first_slice(self) -> None:
        base = build_synthetic_lookup_tool()
        write_like = ToolRegistration(
            spec=ToolSpec(
                tool_ref=base.spec.tool_ref,
                binding_id=base.spec.binding_id,
                version=base.spec.version,
                required_permission=base.spec.required_permission,
                minimum_trust_profile=base.spec.minimum_trust_profile,
                allowed_data_classifications=base.spec.allowed_data_classifications,
                side_effect_class="reversible_write",
                input_schema=base.spec.input_schema,
                output_schema=base.spec.output_schema,
            ),
            handler=base.handler,
        )
        result = ToolGateway((write_like,)).execute(
            context(),
            tool_ref="synthetic.lookup",
            tenant_id="tenant-a",
            data_classification="internal",
            payload={"key": "alpha"},
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "side_effect_class")


if __name__ == "__main__":
    unittest.main()
