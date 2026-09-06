import json
import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from agent_factory_core.contracts import ExecutionContext, RuntimeAuditEvent
from agent_factory_core.runtime import (
    RuntimeLimits,
    build_audit_event,
    evaluate_budget,
    evaluate_limits,
    evaluate_request_authority,
)


ROOT = Path(__file__).resolve().parents[2]


def context() -> ExecutionContext:
    return ExecutionContext(
        apiVersion="agentfactory.io/v1alpha1",
        kind="ExecutionContext",
        requestId="req-1",
        traceId="trace-1",
        actorId="user-1",
        actorType="user",
        tenantId="tenant-a",
        environment="sandbox",
        agentId="research-agent",
        agentReleaseId="release-1",
        trustProfile="internal",
        permissions=("web.search",),
        dataClassification="internal",
        capabilityBindings={"web.search": "web-search:test"},
        providerProfile="balanced",
        toolBindings={"web.search": "tool.web-search.default"},
        memoryConfig={"retention": "short"},
        budgetConfig={"monthlyLimit": 25},
        deadline=datetime.now(timezone.utc) + timedelta(minutes=2),
    )


class RuntimeGovernanceKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit_schema = json.loads((ROOT / "schemas/runtime-audit-event.schema.json").read_text())

    def test_request_authority_allows_only_trusted_scope(self) -> None:
        ctx = context()
        allowed = evaluate_request_authority(
            ctx,
            tenant_id="tenant-a",
            permission="web.search",
            data_classification="internal",
            required_trust_profile="sandbox",
        )
        self.assertTrue(allowed.allowed)

        denied = evaluate_request_authority(ctx, tenant_id="tenant-b", permission="web.search")
        self.assertFalse(denied.allowed)
        self.assertEqual(denied.rule, "tenant")

        denied = evaluate_request_authority(ctx, tenant_id="tenant-a", permission="crm.write")
        self.assertFalse(denied.allowed)
        self.assertEqual(denied.rule, "permission")

        denied = evaluate_request_authority(
            ctx,
            tenant_id="tenant-a",
            permission="web.search",
            data_classification="confidential",
        )
        self.assertFalse(denied.allowed)
        self.assertEqual(denied.rule, "data_classification")

    def test_request_authority_rejects_trust_escalation(self) -> None:
        decision = evaluate_request_authority(
            context(),
            tenant_id="tenant-a",
            permission="web.search",
            required_trust_profile="business",
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.rule, "trust_profile")

    def test_request_authority_rejects_expired_deadline(self) -> None:
        ctx = context()
        decision = evaluate_request_authority(
            ctx,
            tenant_id="tenant-a",
            permission="web.search",
            now=ctx.deadline,
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.rule, "deadline")

    def test_runtime_limits_stop_hops_and_cycles(self) -> None:
        limits = RuntimeLimits(max_hops=2, max_repeats_per_capability=2)

        hop = evaluate_limits(
            limits=limits,
            current_hops=2,
            capability_path=("research.lookup",),
            next_capability="web.search",
        )
        self.assertFalse(hop.allowed)
        self.assertEqual(hop.rule, "hop_limit")

        cycle = evaluate_limits(
            limits=limits,
            current_hops=1,
            capability_path=("web.search", "web.search"),
            next_capability="web.search",
        )
        self.assertFalse(cycle.allowed)
        self.assertEqual(cycle.rule, "cycle_limit")

    def test_safety_cap_is_independent_from_business_budget(self) -> None:
        stop = evaluate_budget(
            estimated_cost=Decimal("12"),
            business_remaining=Decimal("100"),
            safety_remaining=Decimal("10"),
        )
        self.assertEqual(stop.action, "stop")
        self.assertEqual(stop.rule, "safety_cap")

        pause = evaluate_budget(
            estimated_cost=Decimal("12"),
            business_remaining=Decimal("10"),
            safety_remaining=Decimal("100"),
        )
        self.assertEqual(pause.action, "pause")
        self.assertEqual(pause.rule, "business_budget")

        allowed = evaluate_budget(
            estimated_cost=Decimal("5"),
            business_remaining=Decimal("10"),
            safety_remaining=Decimal("20"),
        )
        self.assertEqual(allowed.action, "allow")

    def test_audit_event_validates_against_canonical_schema(self) -> None:
        event = build_audit_event(
            context(),
            platform_policy_ref="platform-default@1",
            exception_policy_refs=("tenant-a-exception@1",),
            approval_ref="approval-123",
            operation="tool.execute",
            target_ref="tool:web.search",
            decision="allow",
            result="success",
            cost_amount=Decimal("0.02"),
            cost_currency="USD",
        )
        dumped = event.model_dump(by_alias=True, mode="json")
        Draft202012Validator(self.audit_schema).validate(dumped)

        generated = RuntimeAuditEvent.model_json_schema(by_alias=True)
        self.assertEqual(set(self.audit_schema["required"]), set(generated["required"]))
        self.assertEqual(set(self.audit_schema["properties"]), set(generated["properties"]))

        self.assertEqual(event.tenant_id, "tenant-a")
        self.assertEqual(event.agent_release_id, "release-1")
        self.assertEqual(event.platform_policy_ref, "platform-default@1")
        self.assertEqual(event.target_ref, "tool:web.search")
        self.assertFalse(hasattr(event, "prompt"))
        self.assertFalse(hasattr(event, "payload"))


if __name__ == "__main__":
    unittest.main()
