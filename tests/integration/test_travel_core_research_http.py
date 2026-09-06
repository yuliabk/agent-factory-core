from __future__ import annotations

import json
import os
import sys
import unittest
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from agent_factory_core.capability_gateway import CapabilityGateway
from agent_factory_core.capability_transport import (
    GovernedCapabilityInvoker,
    HttpJsonEndpointConfig,
    build_http_json_registration,
)
from agent_factory_core.compiler import compile_effective_release
from agent_factory_core.contracts import (
    AgentManifest,
    ClientInstanceConfig,
    PlatformPolicy,
    build_execution_context,
)
from agent_factory_core.registry import CapabilityRecord, CapabilityRegistry


ROOT = Path(__file__).resolve().parents[2]
RESEARCH_RECORD_PATH = ROOT / "registry" / "capabilities" / "research.lookup.v1.json"
RESEARCH_INPUT_SCHEMA_PATH = ROOT / "schemas" / "capabilities" / "research.lookup.input.v1.json"
RESEARCH_OUTPUT_SCHEMA_PATH = ROOT / "schemas" / "capabilities" / "research.lookup.output.v1.json"
CORE_TRAVEL_MANIFEST_PATH = ROOT / "examples" / "travel-research-consumer" / "agent-manifest.json"

TRAVEL_COMMIT = "9da84b635d1ea3b1d62f4b4e8652acd22e42ead6"
RESEARCH_COMMIT = "024367572ca001dec385ca0f781495b5fa91d181"
RESEARCH_RELEASE_ID = f"github:yuliabk/agent-factory-research-agent@{RESEARCH_COMMIT}"


class RecordingGateway:
    def __init__(self, inner: CapabilityGateway) -> None:
        self.inner = inner
        self.last_result = None

    def invoke(self, *args, **kwargs):
        self.last_result = self.inner.invoke(*args, **kwargs)
        return self.last_result


class TravelCoreResearchHttpIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        travel_root_value = os.environ.get("TRAVEL_REPO_PATH")
        research_base_url = os.environ.get("RESEARCH_BASE_URL")
        research_token = os.environ.get("RESEARCH_CAPABILITY_TOKEN")
        if not travel_root_value or not research_base_url or not research_token:
            raise unittest.SkipTest("cross-repository HTTP integration environment is not configured")

        cls.travel_root = Path(travel_root_value).resolve()
        cls.research_base_url = research_base_url
        cls.research_token = research_token
        sys.path.insert(0, str(cls.travel_root))

        from src.capabilities.research_lookup_v1 import ResearchLookupConsumerV1
        from src.contracts.travel_v1 import (
            ConsentStatus,
            CreatedByType,
            CustomerContact,
            TravelerParty,
            TripPreferences,
            TripRequest,
        )

        cls.ResearchLookupConsumerV1 = ResearchLookupConsumerV1
        cls.ConsentStatus = ConsentStatus
        cls.CreatedByType = CreatedByType
        cls.CustomerContact = CustomerContact
        cls.TravelerParty = TravelerParty
        cls.TripPreferences = TripPreferences
        cls.TripRequest = TripRequest

    def _client(self) -> ClientInstanceConfig:
        return ClientInstanceConfig.model_validate(
            {
                "apiVersion": "agentfactory.io/v1alpha1",
                "kind": "ClientInstanceConfig",
                "metadata": {"name": "travel-research-sandbox", "environment": "sandbox"},
                "spec": {
                    "agentRef": {"name": "travel-agent-research-consumer", "version": "1.0.0"},
                    "tenant": {"id": "tenant-travel-sandbox"},
                    "variables": {},
                    "trustProfile": "internal",
                    "releaseStrategy": "policy",
                    "providerProfile": "balanced",
                    "secretsRef": {},
                    "memoryConfig": {"profile": "session-only"},
                    "budgetOverrides": {},
                    "permissionOverrides": {"allow": ["research.lookup"], "deny": []},
                    "toolBindings": {},
                },
            }
        )

    def _policy(self) -> PlatformPolicy:
        return PlatformPolicy.model_validate(
            {
                "apiVersion": "agentfactory.io/v1alpha1",
                "kind": "PlatformPolicy",
                "metadata": {"name": "travel-sandbox-policy", "version": "1"},
                "spec": {
                    "allowedPermissions": ["research.lookup"],
                    "deniedPermissions": [],
                    "allowedProviderProfiles": ["balanced"],
                    "allowedBudgetOverrideKeys": [],
                    "allowedMemoryConfigKeys": ["profile"],
                    "maxTrustProfile": "business",
                    "minimumReleaseStrategy": "policy-auto",
                    "registryMode": "strict",
                    "defaultDataClassification": "internal",
                    "evalRules": [],
                    "securityInvariantChecks": [],
                    "exceptionAllowances": {
                        "permissions": [],
                        "providerProfiles": [],
                        "budgetOverrideKeys": [],
                        "memoryConfigKeys": [],
                    },
                },
            }
        )

    def test_real_travel_to_core_to_research_to_wikipedia_path(self) -> None:
        external_manifest_path = (
            self.travel_root / "agent-factory" / "research-consumer-manifest.json"
        )
        external_manifest_data = json.loads(external_manifest_path.read_text(encoding="utf-8"))
        core_manifest_data = json.loads(CORE_TRAVEL_MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(external_manifest_data, core_manifest_data)

        manifest = AgentManifest.model_validate(external_manifest_data)
        record = CapabilityRecord.model_validate_json(
            RESEARCH_RECORD_PATH.read_text(encoding="utf-8")
        )
        registry = CapabilityRegistry([record])
        release = compile_effective_release(
            manifest,
            self._client(),
            self._policy(),
            registry,
            release_id=f"travel-http-integration@{TRAVEL_COMMIT}",
        )
        context = build_execution_context(
            release,
            request_id="req-travel-http-real-1",
            trace_id="trace-travel-http-real-1",
            actor_id="integration-user",
            actor_type="user",
            deadline=datetime.now(timezone.utc) + timedelta(minutes=2),
        )

        self.assertEqual(context.permissions, ("research.lookup",))
        self.assertNotIn("web.search", context.permissions)
        self.assertEqual(context.capability_bindings["research.lookup"], RESEARCH_RELEASE_ID)
        self.assertEqual(context.tool_bindings, {})

        requirement = manifest.spec.capabilities.requires[0]
        resolved = registry.resolve_required(
            requirement,
            environment="sandbox",
            mode="strict",
        )
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved.implementation_id, RESEARCH_RELEASE_ID)
        self.assertIsNotNone(resolved.transport)
        assert resolved.transport is not None
        self.assertEqual(resolved.transport.endpoint_ref, "research-agent-sandbox")

        registration = build_http_json_registration(
            resolved,
            endpoint=HttpJsonEndpointConfig(
                base_url=self.research_base_url,
                bearer_token=self.research_token,
            ),
            input_schema=json.loads(RESEARCH_INPUT_SCHEMA_PATH.read_text(encoding="utf-8")),
            output_schema=json.loads(RESEARCH_OUTPUT_SCHEMA_PATH.read_text(encoding="utf-8")),
            minimum_trust_profile="internal",
            max_hops=4,
        )
        recording_gateway = RecordingGateway(CapabilityGateway((registration,)))
        invoker = GovernedCapabilityInvoker(
            gateway=recording_gateway,
            context=context,
            platform_policy_ref="travel-sandbox-policy@1",
        )

        request = self.TripRequest(
            request_id="req_travel_http_real_1",
            created_by_type=self.CreatedByType.CUSTOMER,
            customer=self.CustomerContact(
                name="Private Integration Customer",
                email="integration-private@example.com",
            ),
            origin="Tel Aviv",
            destination="Rome",
            departure_date=date(2026, 10, 10),
            return_date=date(2026, 10, 15),
            travelers=self.TravelerParty(adults=2),
            budget=Decimal("6000"),
            currency="ILS",
            preferences=self.TripPreferences(),
            consent_status=self.ConsentStatus.GRANTED,
        )

        consumer = self.ResearchLookupConsumerV1(invoker, max_evidence_items=3)
        minimized = consumer.build_request(request).model_dump(by_alias=True, mode="json")
        minimized_text = json.dumps(minimized, ensure_ascii=False)
        self.assertNotIn("Private Integration Customer", minimized_text)
        self.assertNotIn("integration-private@example.com", minimized_text)
        self.assertNotIn("6000", minimized_text)
        self.assertNotIn("provider", minimized)
        self.assertNotIn("model", minimized)
        self.assertNotIn("tool", minimized)

        records = consumer.search_background(request)
        self.assertGreaterEqual(len(records), 1)
        first = records[0]
        self.assertEqual(first.type.value, "PLACE")
        self.assertEqual(first.provider, "research.lookup")
        self.assertIsNone(first.amount)
        self.assertIsNone(first.currency)
        self.assertEqual(first.source_status.value, "unverified")
        self.assertTrue(first.provider_reference)
        self.assertIn("wikipedia.org", first.provider_reference)
        self.assertEqual(first.normalized_data["source_type"], "web")
        self.assertTrue(first.normalized_data["summary"])

        gateway_result = recording_gateway.last_result
        self.assertIsNotNone(gateway_result)
        assert gateway_result is not None
        self.assertTrue(gateway_result.allowed)
        self.assertEqual(gateway_result.implementation_id, RESEARCH_RELEASE_ID)
        self.assertEqual(gateway_result.audit_event.trace_id, context.trace_id)
        self.assertEqual(gateway_result.audit_event.request_id, context.request_id)
        self.assertEqual(gateway_result.audit_event.target_ref, RESEARCH_RELEASE_ID)
        self.assertEqual(gateway_result.audit_event.operation, "capability.invoke")
        self.assertEqual(gateway_result.audit_event.decision, "allow")


if __name__ == "__main__":
    unittest.main()
