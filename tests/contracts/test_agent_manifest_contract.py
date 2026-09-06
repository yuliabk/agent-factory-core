import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from pydantic import ValidationError as PydanticValidationError

from agent_factory_core.contracts.agent_manifest import AgentManifest


SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "agent-manifest.schema.json"


VALID_MANIFEST = {
    "apiVersion": "agentfactory.io/v1alpha1",
    "kind": "AgentManifest",
    "metadata": {
        "name": "research-agent",
        "version": "0.1.0",
        "description": "Reusable policy-bounded research capability",
    },
    "spec": {
        "template": {"name": "general-agent", "version": 1},
        "capabilities": {
            "provides": [
                {"ref": "research.lookup", "version": "1"},
            ],
            "requires": [
                {
                    "ref": "web.search",
                    "version": "1",
                    "optional": True,
                    "overrides": {"qualityProfile": "balanced"},
                }
            ],
        },
        "tools": {"required": ["web.search"]},
        "permissions": {"requested": ["web.search"]},
        "memoryProfile": "session-plus-client-knowledge",
        "budgetProfile": "balanced",
        "evalProfile": "standard-agent",
    },
}


class AgentManifestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_valid_manifest_passes_json_schema_and_pydantic(self) -> None:
        self.validator.validate(VALID_MANIFEST)
        parsed = AgentManifest.model_validate(VALID_MANIFEST)
        self.assertEqual(parsed.spec.capabilities.provides[0].ref, "research.lookup")
        self.assertEqual(parsed.model_dump(by_alias=True)["apiVersion"], "agentfactory.io/v1alpha1")

    def test_capability_string_shorthand_is_rejected_by_both(self) -> None:
        manifest = json.loads(json.dumps(VALID_MANIFEST))
        manifest["spec"]["capabilities"]["requires"] = ["web.search@v1"]
        with self.assertRaises(ValidationError):
            self.validator.validate(manifest)
        with self.assertRaises(PydanticValidationError):
            AgentManifest.model_validate(manifest)

    def test_capability_metadata_duplication_is_rejected_by_both(self) -> None:
        manifest = json.loads(json.dumps(VALID_MANIFEST))
        manifest["spec"]["capabilities"]["provides"][0]["risk"] = "read-only"
        with self.assertRaises(ValidationError):
            self.validator.validate(manifest)
        with self.assertRaises(PydanticValidationError):
            AgentManifest.model_validate(manifest)

    def test_required_top_level_shape_stays_aligned(self) -> None:
        generated = AgentManifest.model_json_schema(by_alias=True)
        self.assertEqual(set(self.schema["required"]), set(generated["required"]))
        self.assertEqual(set(self.schema["properties"]), set(generated["properties"]))


if __name__ == "__main__":
    unittest.main()
