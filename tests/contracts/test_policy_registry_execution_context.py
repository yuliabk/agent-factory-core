import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

from agent_factory_core.compiler import CompilationError, compile_effective_release
from agent_factory_core.contracts import (
    AgentManifest,
    ClientInstanceConfig,
    ExceptionPolicy,
    ExecutionContext,
    PlatformPolicy,
    build_execution_context,
)
from agent_factory_core.registry import (
    CapabilityImplementation,
    CapabilityRecord,
    CapabilityRegistry,
)


ROOT = Path(__file__).resolve().parents[2]


MANIFEST = {
    "apiVersion": "agentfactory.io/v1alpha1",
    "kind": "AgentManifest",
    "metadata": {"name": "research-agent", "version": "0.1.0", "description": "test"},
    "spec": {
        "template": {"name": "general-agent", "version": 1},
        "capabilities": {
            "provides": [],
            "requires": [{"ref": "web.search", "version": "1", "overrides": {"qualityProfile": "balanced"}}],
        },
        "tools": {"required": ["web.search"]},
        "permissions": {"requested": ["web.search"]},
        "memoryProfile": "session-only",
        "budgetProfile": "balanced",
        "evalProfile": "standard-agent",
    },
}

CLIENT = {
    "apiVersion": "agentfactory.io/v1alpha1",
    "kind": "ClientInstanceConfig",
    "metadata": {"name": "tenant-a-research", "environment": "sandbox"},
    "spec": {
        "agentRef": {"name": "research-agent", "version": "0.1.0"},
        "tenant": {"id": "tenant-a"},
        "variables": {},
        "providerProfile": "balanced",
        "secretsRef": {},
        "memoryConfig": {"retention": "short"},
        "budgetOverrides": {"monthlyLimit": 25},
        "permissionOverrides": {"allow": ["web.search"], "deny": []},
        "toolBindings": {"web.search": "tool.web-search.default"},
    },
}

POLICY = {
    "apiVersion": "agentfactory.io/v1alpha1",
    "kind": "PlatformPolicy",
    "metadata": {"name": "platform-default", "version": "1"},
    "spec": {
        "allowedPermissions": ["web.search"],
        "deniedPermissions": [],
        "allowedProviderProfiles": ["balanced"],
        "allowedBudgetOverrideKeys": ["monthlyLimit"],
        "allowedMemoryConfigKeys": ["retention"],
        "registryMode": "strict",
        "defaultDataClassification": "internal",
        "exceptionAllowances": {
            "permissions": ["crm.read"],
            "providerProfiles": ["premium"],
            "budgetOverrideKeys": ["burstLimit"],
            "memoryConfigKeys": ["longRetention"],
        },
    },
}


class PolicyRegistryExecutionContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy_schema = json.loads((ROOT / "schemas/platform-policy.schema.json").read_text())
        cls.exception_schema = json.loads((ROOT / "schemas/exception-policy.schema.json").read_text())
        cls.context_schema = json.loads((ROOT / "schemas/execution-context.schema.json").read_text())

    def registry(self) -> CapabilityRegistry:
        return CapabilityRegistry([
            CapabilityRecord(
                ref="web.search",
                version="1",
                environments=["sandbox", "production"],
                requiredPermissions=["web.search"],
                overrideable={"qualityProfile": ["economy", "balanced", "high"]},
                implementations=[CapabilityImplementation(id="web-search:test", environments=["sandbox"])],
            )
        ])

    def test_platform_policy_validates_in_json_schema_and_pydantic(self) -> None:
        Draft202012Validator(self.policy_schema).validate(POLICY)
        parsed = PlatformPolicy.model_validate(POLICY)
        self.assertEqual(parsed.spec.registry_mode, "strict")

    def test_external_and_internal_top_level_shapes_stay_aligned(self) -> None:
        for schema, model in (
            (self.policy_schema, PlatformPolicy),
            (self.exception_schema, ExceptionPolicy),
            (self.context_schema, ExecutionContext),
        ):
            generated = model.model_json_schema(by_alias=True)
            self.assertEqual(set(schema["required"]), set(generated["required"]))
            self.assertEqual(set(schema["properties"]), set(generated["properties"]))

    def test_compiler_resolves_required_capability(self) -> None:
        release = compile_effective_release(
            AgentManifest.model_validate(MANIFEST),
            ClientInstanceConfig.model_validate(CLIENT),
            PlatformPolicy.model_validate(POLICY),
            self.registry(),
            release_id="release-1",
        )
        self.assertEqual(release.spec.capability_bindings["web.search"], "web-search:test")
        self.assertEqual(release.spec.data_classification, "internal")

    def test_registry_rejects_non_overrideable_key(self) -> None:
        manifest = json.loads(json.dumps(MANIFEST))
        manifest["spec"]["capabilities"]["requires"][0]["overrides"] = {"providerAgent": "evil"}
        with self.assertRaises(CompilationError):
            compile_effective_release(
                AgentManifest.model_validate(manifest),
                ClientInstanceConfig.model_validate(CLIENT),
                PlatformPolicy.model_validate(POLICY),
                self.registry(),
                release_id="release-2",
            )

    def test_valid_exception_can_expand_declared_policy_dimension(self) -> None:
        client = json.loads(json.dumps(CLIENT))
        client["spec"]["providerProfile"] = "premium"
        exception = {
            "apiVersion": "agentfactory.io/v1alpha1",
            "kind": "ExceptionPolicy",
            "metadata": {"name": "premium-for-tenant-a", "version": "1"},
            "spec": {
                "platformPolicyRef": {"name": "platform-default", "version": "1"},
                "scope": {"tenantId": "tenant-a", "environment": "sandbox", "agentName": "research-agent", "agentVersion": "0.1.0"},
                "reason": "approved test",
                "approver": "platform-owner",
                "expiresAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
                "allow": {"permissions": [], "providerProfiles": ["premium"], "budgetOverrideKeys": [], "memoryConfigKeys": []},
            },
        }
        Draft202012Validator(self.exception_schema).validate(exception)
        release = compile_effective_release(
            AgentManifest.model_validate(MANIFEST),
            ClientInstanceConfig.model_validate(client),
            PlatformPolicy.model_validate(POLICY),
            self.registry(),
            release_id="release-3",
            exceptions=[ExceptionPolicy.model_validate(exception)],
        )
        self.assertEqual(release.spec.provider_profile, "premium")
        self.assertEqual(release.policy.exception_policy_refs, ("premium-for-tenant-a@1",))

    def test_execution_context_is_derived_from_effective_release(self) -> None:
        release = compile_effective_release(
            AgentManifest.model_validate(MANIFEST),
            ClientInstanceConfig.model_validate(CLIENT),
            PlatformPolicy.model_validate(POLICY),
            self.registry(),
            release_id="release-4",
        )
        context = build_execution_context(
            release,
            request_id="req-1",
            trace_id="trace-1",
            actor_id="user-1",
            actor_type="user",
            deadline=datetime.now(timezone.utc) + timedelta(minutes=2),
        )
        dumped = context.model_dump(by_alias=True, mode="json")
        Draft202012Validator(self.context_schema).validate(dumped)
        self.assertEqual(dumped["agentReleaseId"], "release-4")
        self.assertEqual(dumped["tenantId"], "tenant-a")


if __name__ == "__main__":
    unittest.main()
