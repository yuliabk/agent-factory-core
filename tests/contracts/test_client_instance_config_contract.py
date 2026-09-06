import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from pydantic import ValidationError as PydanticValidationError

from agent_factory_core.contracts.client_instance_config import ClientInstanceConfig


SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "client-instance-config.schema.json"


VALID_CONFIG = {
    "apiVersion": "agentfactory.io/v1alpha1",
    "kind": "ClientInstanceConfig",
    "metadata": {"name": "acme-research", "environment": "sandbox"},
    "spec": {
        "agentRef": {"name": "research-agent", "version": "0.1.0"},
        "tenant": {"id": "tenant-acme"},
        "variables": {"locale": "en"},
        "trustProfile": "internal",
        "releaseStrategy": "policy",
        "providerProfile": "balanced",
        "secretsRef": {"search": "secret://tenant-acme/search"},
        "memoryConfig": {"profile": "session-only"},
        "budgetOverrides": {"monthlyUsd": 50},
        "permissionOverrides": {"allow": ["web.search"], "deny": []},
        "toolBindings": {"web.search": "tool://web-search/default"},
    },
}


class ClientInstanceConfigContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_valid_config_passes_json_schema_and_pydantic(self) -> None:
        self.validator.validate(VALID_CONFIG)
        parsed = ClientInstanceConfig.model_validate(VALID_CONFIG)
        self.assertEqual(parsed.spec.agent_ref.name, "research-agent")
        self.assertEqual(parsed.spec.trust_profile, "internal")
        self.assertEqual(parsed.spec.release_strategy, "policy")
        self.assertEqual(parsed.model_dump(by_alias=True)["kind"], "ClientInstanceConfig")

    def test_business_logic_field_is_rejected(self) -> None:
        config = json.loads(json.dumps(VALID_CONFIG))
        config["spec"]["businessLogic"] = {"prompt": "do sales"}
        with self.assertRaises(ValidationError):
            self.validator.validate(config)
        with self.assertRaises(PydanticValidationError):
            ClientInstanceConfig.model_validate(config)

    def test_missing_trust_profile_is_rejected(self) -> None:
        config = json.loads(json.dumps(VALID_CONFIG))
        del config["spec"]["trustProfile"]
        with self.assertRaises(ValidationError):
            self.validator.validate(config)
        with self.assertRaises(PydanticValidationError):
            ClientInstanceConfig.model_validate(config)

    def test_missing_or_unknown_release_strategy_is_rejected(self) -> None:
        config = json.loads(json.dumps(VALID_CONFIG))
        del config["spec"]["releaseStrategy"]
        with self.assertRaises(ValidationError):
            self.validator.validate(config)
        with self.assertRaises(PydanticValidationError):
            ClientInstanceConfig.model_validate(config)

        config = json.loads(json.dumps(VALID_CONFIG))
        config["spec"]["releaseStrategy"] = "always-auto"
        with self.assertRaises(ValidationError):
            self.validator.validate(config)
        with self.assertRaises(PydanticValidationError):
            ClientInstanceConfig.model_validate(config)

    def test_required_top_level_shape_stays_aligned(self) -> None:
        generated = ClientInstanceConfig.model_json_schema(by_alias=True)
        self.assertEqual(set(self.schema["required"]), set(generated["required"]))
        self.assertEqual(set(self.schema["properties"]), set(generated["properties"]))


if __name__ == "__main__":
    unittest.main()
