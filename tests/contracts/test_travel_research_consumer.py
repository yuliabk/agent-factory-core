import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

from agent_factory_core.compiler import compile_effective_release
from agent_factory_core.contracts import (
    AgentManifest,
    ClientInstanceConfig,
    PlatformPolicy,
    build_execution_context,
)
from agent_factory_core.registry import CapabilityRecord, CapabilityRegistry


ROOT = Path(__file__).resolve().parents[2]
TRAVEL_MANIFEST_PATH = ROOT / "examples" / "travel-research-consumer" / "agent-manifest.json"
TRAVEL_SOURCE_LOCK_PATH = ROOT / "examples" / "travel-research-consumer" / "source-lock.json"
AGENT_MANIFEST_SCHEMA_PATH = ROOT / "schemas" / "agent-manifest.schema.json"
RESEARCH_RECORD_PATH = ROOT / "registry" / "capabilities" / "research.lookup.v1.json"

TRAVEL_COMMIT = "9da84b635d1ea3b1d62f4b4e8652acd22e42ead6"
RESEARCH_RELEASE_ID = "github:yuliabk/agent-factory-research-agent@4a8b308aeaf22228c6a03d438509b0717e6daf8b"


class TravelResearchConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest_data = json.loads(TRAVEL_MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.source_lock = json.loads(TRAVEL_SOURCE_LOCK_PATH.read_text(encoding="utf-8"))
        cls.manifest_schema = json.loads(AGENT_MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.research_record = CapabilityRecord.model_validate_json(
            RESEARCH_RECORD_PATH.read_text(encoding="utf-8")
        )

    def client(self) -> ClientInstanceConfig:
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

    def policy(self) -> PlatformPolicy:
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

    def test_external_travel_manifest_is_locked_and_valid(self) -> None:
        Draft202012Validator(self.manifest_schema).validate(self.manifest_data)
        manifest = AgentManifest.model_validate(self.manifest_data)

        self.assertEqual(self.source_lock["repository"], "yuliabk/travel-agent-bot")
        self.assertEqual(self.source_lock["commit"], TRAVEL_COMMIT)
        self.assertEqual(
            self.source_lock["path"],
            "agent-factory/research-consumer-manifest.json",
        )
        self.assertEqual(manifest.spec.permissions.requested, ["research.lookup"])
        self.assertEqual(len(manifest.spec.capabilities.requires), 1)
        self.assertEqual(manifest.spec.capabilities.requires[0].ref, "research.lookup")
        self.assertNotIn("web.search", manifest.spec.permissions.requested)

    def test_travel_compiles_to_exact_research_provider_without_permission_leakage(self) -> None:
        manifest = AgentManifest.model_validate(self.manifest_data)
        registry = CapabilityRegistry([self.research_record])

        release = compile_effective_release(
            manifest,
            self.client(),
            self.policy(),
            registry,
            release_id="travel-research-sandbox-release-1",
        )

        self.assertEqual(
            release.spec.capability_bindings,
            {"research.lookup": RESEARCH_RELEASE_ID},
        )
        self.assertEqual(release.spec.permissions, ("research.lookup",))
        self.assertNotIn("web.search", release.spec.permissions)
        self.assertEqual(release.spec.tool_bindings, {})
        self.assertEqual(release.spec.data_classification, "internal")

        context = build_execution_context(
            release,
            request_id="req-travel-research-1",
            trace_id="trace-travel-research-1",
            actor_id="travel-sandbox-user",
            actor_type="user",
            deadline=datetime.now(timezone.utc) + timedelta(minutes=2),
        )

        self.assertEqual(context.permissions, ("research.lookup",))
        self.assertNotIn("web.search", context.permissions)
        self.assertEqual(
            context.capability_bindings,
            {"research.lookup": RESEARCH_RELEASE_ID},
        )
        self.assertEqual(context.tool_bindings, {})


if __name__ == "__main__":
    unittest.main()
