import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from agent_factory_core.contracts.agent_manifest import RequiredCapabilityRef
from agent_factory_core.registry import (
    CapabilityImplementation,
    CapabilityRecord,
    CapabilityRegistry,
)


ROOT = Path(__file__).resolve().parents[2]
RECORD_PATH = ROOT / "registry" / "capabilities" / "research.lookup.v1.json"
REGISTRY_SCHEMA_PATH = ROOT / "schemas" / "capability-registry-record.schema.json"
INPUT_SCHEMA_PATH = ROOT / "schemas" / "capabilities" / "research.lookup.input.v1.json"
OUTPUT_SCHEMA_PATH = ROOT / "schemas" / "capabilities" / "research.lookup.output.v1.json"


class ResearchLookupContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record_data = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
        cls.registry_schema = json.loads(REGISTRY_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.input_schema = json.loads(INPUT_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.output_schema = json.loads(OUTPUT_SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_authoritative_registry_record_is_valid_and_complete(self) -> None:
        Draft202012Validator(self.registry_schema).validate(self.record_data)
        record = CapabilityRecord.model_validate(self.record_data)

        self.assertEqual(record.ref, "research.lookup")
        self.assertEqual(record.version, "1")
        self.assertEqual(record.risk_class, "read_only")
        self.assertEqual(record.cost_class, "variable")
        self.assertEqual(record.allowed_data_classifications, ["public", "internal"])
        self.assertEqual(record.required_permissions, ["research.lookup"])
        self.assertNotIn("web.search", record.required_permissions)
        self.assertEqual(record.implementations, [])

        generated = CapabilityRecord.model_json_schema(by_alias=True)
        self.assertEqual(set(self.registry_schema["required"]), set(generated["required"]))
        self.assertEqual(set(self.registry_schema["properties"]), set(generated["properties"]))

    def test_registry_resolution_preserves_contract_metadata_without_provider_leakage(self) -> None:
        data = copy.deepcopy(self.record_data)
        data["implementations"] = [
            {
                "id": "agent.research.synthetic.v1",
                "environments": ["sandbox"],
                "enabled": True,
            }
        ]
        registry = CapabilityRegistry([CapabilityRecord.model_validate(data)])
        resolved = registry.resolve_required(
            RequiredCapabilityRef(
                ref="research.lookup",
                version="1",
                optional=False,
                overrides={"qualityProfile": "balanced"},
            ),
            environment="sandbox",
            mode="strict",
        )

        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved.required_permissions, ("research.lookup",))
        self.assertEqual(
            resolved.input_schema_ref,
            "schemas/capabilities/research.lookup.input.v1.json",
        )
        self.assertEqual(
            resolved.output_schema_ref,
            "schemas/capabilities/research.lookup.output.v1.json",
        )
        self.assertEqual(resolved.risk_class, "read_only")
        self.assertEqual(resolved.cost_class, "variable")
        self.assertEqual(resolved.allowed_data_classifications, ("public", "internal"))
        self.assertEqual(resolved.overrides, {"qualityProfile": "balanced"})

    def test_public_input_is_provider_neutral(self) -> None:
        valid = {
            "query": "What changed in the rail schedule?",
            "purpose": "travel planning",
            "freshness": "current",
            "maxEvidenceItems": 6,
        }
        Draft202012Validator(self.input_schema).validate(valid)

        for forbidden_field in ("provider", "model", "tool", "webSearch", "apiKey"):
            payload = dict(valid)
            payload[forbidden_field] = "caller-selected"
            with self.assertRaises(ValidationError):
                Draft202012Validator(self.input_schema).validate(payload)

    def test_output_is_structured_evidence_without_raw_provider_payloads(self) -> None:
        valid = {
            "status": "complete",
            "answer": "The synthetic schedule changed.",
            "findings": [
                {
                    "statement": "A schedule change was published.",
                    "evidenceIds": ["e1"],
                }
            ],
            "evidence": [
                {
                    "id": "e1",
                    "sourceType": "web",
                    "sourceRef": "https://example.test/schedule",
                    "title": "Schedule update",
                    "summary": "Official page reports the change.",
                    "retrievedAt": "2026-09-06T13:00:00Z",
                }
            ],
            "limitations": [],
        }
        Draft202012Validator(self.output_schema).validate(valid)

        for forbidden_field in ("prompt", "providerPayload", "credentials", "apiKey"):
            payload = copy.deepcopy(valid)
            payload[forbidden_field] = "sensitive"
            with self.assertRaises(ValidationError):
                Draft202012Validator(self.output_schema).validate(payload)

    def test_override_surface_is_bounded_to_quality_profile(self) -> None:
        data = copy.deepcopy(self.record_data)
        data["implementations"] = [{"id": "agent.research.synthetic.v1"}]
        registry = CapabilityRegistry([CapabilityRecord.model_validate(data)])

        with self.assertRaises(ValueError):
            registry.resolve_required(
                RequiredCapabilityRef(
                    ref="research.lookup",
                    version="1",
                    optional=False,
                    overrides={"provider": "direct-web"},
                ),
                environment="sandbox",
                mode="strict",
            )


if __name__ == "__main__":
    unittest.main()
