import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from agent_factory_core.compiler import CompilationError, compile_effective_release
from agent_factory_core.contracts.agent_manifest import AgentManifest
from agent_factory_core.contracts.client_instance_config import ClientInstanceConfig
from agent_factory_core.contracts.effective_release_config import EffectiveReleaseConfig
from agent_factory_core.contracts.platform_policy import PlatformPolicy
from agent_factory_core.registry import CapabilityImplementation, CapabilityRecord, CapabilityRegistry


ROOT = Path(__file__).resolve().parents[2]


MANIFEST = AgentManifest.model_validate(
    {
        "apiVersion": "agentfactory.io/v1alpha1",
        "kind": "AgentManifest",
        "metadata": {
            "name": "research-agent",
            "version": "0.1.0",
            "description": "Reusable research agent",
        },
        "spec": {
            "template": {"name": "general-agent", "version": 1},
            "capabilities": {
                "provides": [{"ref": "research.lookup", "version": "1"}],
                "requires": [{"ref": "web.search", "version": "1", "optional": False}],
            },
            "tools": {"required": ["web.search"]},
            "permissions": {"requested": ["web.search"]},
            "memoryProfile": "session-only",
            "budgetProfile": "balanced",
            "evalProfile": "standard-agent",
        },
    }
)

CLIENT = ClientInstanceConfig.model_validate(
    {
        "apiVersion": "agentfactory.io/v1alpha1",
        "kind": "ClientInstanceConfig",
        "metadata": {"name": "acme-research", "environment": "sandbox"},
        "spec": {
            "agentRef": {"name": "research-agent", "version": "0.1.0"},
            "tenant": {"id": "tenant-acme"},
            "variables": {"locale": "en"},
            "trustProfile": "internal",
            "providerProfile": "balanced",
            "secretsRef": {"search": "secret://tenant-acme/search"},
            "memoryConfig": {"profile": "session-only"},
            "budgetOverrides": {"monthlyUsd": 50},
            "permissionOverrides": {"allow": ["web.search"], "deny": []},
            "toolBindings": {"web.search": "tool://web-search/default"},
        },
    }
)

POLICY = PlatformPolicy.model_validate(
    {
        "apiVersion": "agentfactory.io/v1alpha1",
        "kind": "PlatformPolicy",
        "metadata": {"name": "platform-default", "version": "1"},
        "spec": {
            "allowedPermissions": ["web.search"],
            "deniedPermissions": [],
            "allowedProviderProfiles": ["balanced"],
            "allowedBudgetOverrideKeys": ["monthlyUsd"],
            "allowedMemoryConfigKeys": ["profile"],
            "maxTrustProfile": "business",
            "registryMode": "strict",
            "defaultDataClassification": "internal",
            "exceptionAllowances": {
                "permissions": [],
                "providerProfiles": [],
                "budgetOverrideKeys": [],
                "memoryConfigKeys": [],
            },
        },
    }
)

REGISTRY = CapabilityRegistry(
    [
        CapabilityRecord(
            ref="web.search",
            version="1",
            environments=["sandbox"],
            requiredPermissions=["web.search"],
            implementations=[
                CapabilityImplementation(id="web-search:test", environments=["sandbox"])
            ],
        )
    ]
)


class EffectiveReleaseCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.release_schema = json.loads(
            (ROOT / "schemas/effective-release-config.schema.json").read_text(encoding="utf-8")
        )

    def test_compiles_to_effective_release(self) -> None:
        release = compile_effective_release(
            MANIFEST,
            CLIENT,
            POLICY,
            REGISTRY,
            release_id="release-001",
        )
        dumped = release.model_dump(by_alias=True, mode="json")
        Draft202012Validator(self.release_schema).validate(dumped)

        self.assertEqual(release.kind, "EffectiveReleaseConfig")
        self.assertEqual(release.metadata.release_id, "release-001")
        self.assertEqual(release.spec.permissions, ("web.search",))
        self.assertEqual(release.spec.tenant.id, "tenant-acme")
        self.assertEqual(release.spec.trust_profile, "internal")
        self.assertEqual(release.spec.capability_bindings["web.search"], "web-search:test")

        generated = EffectiveReleaseConfig.model_json_schema(by_alias=True)
        self.assertEqual(set(self.release_schema["required"]), set(generated["required"]))
        self.assertEqual(set(self.release_schema["properties"]), set(generated["properties"]))

    def test_rejects_trust_profile_above_platform_ceiling(self) -> None:
        client = CLIENT.model_copy(deep=True)
        client.spec.trust_profile = "privileged"
        with self.assertRaises(CompilationError) as ctx:
            compile_effective_release(
                MANIFEST, client, POLICY, REGISTRY, release_id="release-trust-denied"
            )
        self.assertIn("spec.trustProfile", str(ctx.exception))

    def test_rejects_ungranted_required_permission(self) -> None:
        client = CLIENT.model_copy(deep=True)
        client.spec.permission_overrides.allow = []
        with self.assertRaises(CompilationError) as ctx:
            compile_effective_release(
                MANIFEST, client, POLICY, REGISTRY, release_id="release-002"
            )
        self.assertIn("spec.permissionOverrides.allow", str(ctx.exception))

    def test_rejects_missing_tool_binding(self) -> None:
        client = CLIENT.model_copy(deep=True)
        client.spec.tool_bindings = {}
        with self.assertRaises(CompilationError) as ctx:
            compile_effective_release(
                MANIFEST, client, POLICY, REGISTRY, release_id="release-003"
            )
        self.assertIn("spec.toolBindings", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
