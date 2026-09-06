import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from agent_factory_core.contracts import ExecutionContext
from agent_factory_core.model_router import (
    ModelAdapterOutput,
    ModelAdapterSpec,
    ModelAdapterUnavailable,
    ModelRegistration,
    ModelRequest,
    ModelRouter,
)
from agent_factory_core.synthetic_model_adapters import (
    build_deterministic_model_adapter,
    build_stub_model_adapter,
)


def context(
    *,
    permissions: tuple[str, ...] = ("model.invoke",),
    trust_profile: str = "internal",
    provider_profile: str = "balanced",
) -> ExecutionContext:
    return ExecutionContext(
        apiVersion="agentfactory.io/v1alpha1",
        kind="ExecutionContext",
        requestId="req-model-1",
        traceId="trace-model-1",
        actorId="user-1",
        actorType="user",
        tenantId="tenant-a",
        environment="sandbox",
        agentId="test-agent",
        agentReleaseId="release-model-1",
        trustProfile=trust_profile,
        permissions=permissions,
        dataClassification="internal",
        capabilityBindings={},
        providerProfile=provider_profile,
        toolBindings={},
        memoryConfig={},
        budgetConfig={},
        deadline=datetime.now(timezone.utc) + timedelta(minutes=2),
    )


def request(classification: str = "internal") -> ModelRequest:
    return ModelRequest(input_text="hello model", data_classification=classification)


class ModelRouterContractTests(unittest.TestCase):
    def test_compiled_provider_profile_routes_to_primary_adapter(self) -> None:
        primary = build_deterministic_model_adapter()
        stub = build_stub_model_adapter()
        router = ModelRouter(
            (primary, stub),
            routes={"balanced": (primary.spec.implementation_id, stub.spec.implementation_id)},
        )
        result = router.invoke(
            context(),
            request=request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.implementation_id, "model.synthetic.primary.v1")
        self.assertEqual(result.output.text, "primary:hello model")
        self.assertEqual(result.audit_event.target_ref, "model.synthetic.primary.v1")

    def test_same_agent_request_can_switch_adapter_without_provider_hard_code(self) -> None:
        primary = build_deterministic_model_adapter()
        stub = build_stub_model_adapter()
        ctx = context()
        req = request()

        first = ModelRouter(
            (primary, stub),
            routes={"balanced": (primary.spec.implementation_id,)},
        ).invoke(ctx, request=req, platform_policy_ref="platform-default@1")

        second = ModelRouter(
            (primary, stub),
            routes={"balanced": (stub.spec.implementation_id,)},
        ).invoke(ctx, request=req, platform_policy_ref="platform-default@1")

        self.assertEqual(first.output.text, "primary:hello model")
        self.assertEqual(second.output.text, "stub:hello model")
        self.assertEqual(ctx.provider_profile, "balanced")

    def test_unavailable_primary_falls_back_to_compatible_stub(self) -> None:
        primary = build_deterministic_model_adapter()
        stub = build_stub_model_adapter()

        def unavailable(_: ModelRequest) -> ModelAdapterOutput:
            raise ModelAdapterUnavailable("synthetic outage")

        unavailable_primary = ModelRegistration(spec=primary.spec, handler=unavailable)
        router = ModelRouter(
            (unavailable_primary, stub),
            routes={"balanced": (primary.spec.implementation_id, stub.spec.implementation_id)},
        )
        result = router.invoke(
            context(),
            request=request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.implementation_id, stub.spec.implementation_id)
        self.assertEqual(result.output.text, "stub:hello model")

    def test_missing_model_permission_is_denied(self) -> None:
        primary = build_deterministic_model_adapter()
        result = ModelRouter(
            (primary,), routes={"balanced": (primary.spec.implementation_id,)}
        ).invoke(
            context(permissions=()),
            request=request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "permission")

    def test_trust_escalation_is_denied(self) -> None:
        primary = build_deterministic_model_adapter()
        elevated = ModelRegistration(
            spec=ModelAdapterSpec(
                implementation_id=primary.spec.implementation_id,
                version=primary.spec.version,
                supported_profiles=primary.spec.supported_profiles,
                allowed_data_classifications=primary.spec.allowed_data_classifications,
                minimum_trust_profile="business",
            ),
            handler=primary.handler,
        )
        result = ModelRouter(
            (elevated,), routes={"balanced": (elevated.spec.implementation_id,)}
        ).invoke(
            context(trust_profile="internal"),
            request=request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "trust_profile")

    def test_data_classification_cannot_be_changed_by_model_request(self) -> None:
        primary = build_deterministic_model_adapter()
        expanded = ModelRegistration(
            spec=ModelAdapterSpec(
                implementation_id=primary.spec.implementation_id,
                version=primary.spec.version,
                supported_profiles=primary.spec.supported_profiles,
                allowed_data_classifications=("internal", "confidential"),
                minimum_trust_profile="internal",
            ),
            handler=primary.handler,
        )
        result = ModelRouter(
            (expanded,), routes={"balanced": (expanded.spec.implementation_id,)}
        ).invoke(
            context(),
            request=request("confidential"),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "data_classification")

    def test_costed_adapter_is_blocked_until_budget_state_is_attached(self) -> None:
        primary = build_deterministic_model_adapter()
        costed = ModelRegistration(
            spec=ModelAdapterSpec(
                implementation_id=primary.spec.implementation_id,
                version=primary.spec.version,
                supported_profiles=primary.spec.supported_profiles,
                allowed_data_classifications=primary.spec.allowed_data_classifications,
                minimum_trust_profile=primary.spec.minimum_trust_profile,
                estimated_cost=Decimal("0.01"),
            ),
            handler=primary.handler,
        )
        result = ModelRouter(
            (costed,), routes={"balanced": (costed.spec.implementation_id,)}
        ).invoke(
            context(),
            request=request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "model_route")
        self.assertIn("costed model adapters remain blocked", result.reason)

    def test_unknown_provider_profile_is_denied(self) -> None:
        primary = build_deterministic_model_adapter()
        result = ModelRouter(
            (primary,), routes={"balanced": (primary.spec.implementation_id,)}
        ).invoke(
            context(provider_profile="premium"),
            request=request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "model_route")


if __name__ == "__main__":
    unittest.main()
