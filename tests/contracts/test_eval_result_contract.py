import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from pydantic import ValidationError as PydanticValidationError

from agent_factory_core.contracts import EvalResult


ROOT = Path(__file__).resolve().parents[2]


VALID_RESULT = {
    "apiVersion": "agentfactory.io/v1alpha1",
    "kind": "EvalResult",
    "evalId": "eval-security-001",
    "releaseId": "release-001",
    "checkId": "security.cross-tenant-isolation",
    "checkVersion": "1",
    "family": "security_policy",
    "status": "PASS",
    "summary": "Cross-tenant isolation checks passed",
    "metrics": {"cases": 12, "violations": 0, "coverage": 1.0},
    "evidenceRefs": ["artifact://evals/security/cross-tenant-001"],
    "observedAt": datetime.now(timezone.utc).isoformat(),
}


class EvalResultContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((ROOT / "schemas/eval-result.schema.json").read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_valid_result_passes_json_schema_and_pydantic(self) -> None:
        self.validator.validate(VALID_RESULT)
        parsed = EvalResult.model_validate(VALID_RESULT)
        self.assertEqual(parsed.family, "security_policy")
        self.assertEqual(parsed.status, "PASS")
        self.assertEqual(parsed.release_id, "release-001")

    def test_all_four_eval_families_are_supported(self) -> None:
        for family in (
            "functional_business",
            "security_policy",
            "cost_runtime",
            "contract_portability",
        ):
            result = dict(VALID_RESULT)
            result["family"] = family
            self.validator.validate(result)
            self.assertEqual(EvalResult.model_validate(result).family, family)

    def test_status_vocabulary_is_raw_eval_result_only(self) -> None:
        for status in ("PASS", "PASS_WITH_WARNINGS", "FAIL"):
            result = dict(VALID_RESULT)
            result["status"] = status
            self.validator.validate(result)
            self.assertEqual(EvalResult.model_validate(result).status, status)

        invalid = dict(VALID_RESULT)
        invalid["status"] = "BLOCKING"
        with self.assertRaises(ValidationError):
            self.validator.validate(invalid)
        with self.assertRaises(PydanticValidationError):
            EvalResult.model_validate(invalid)

    def test_policy_and_release_decision_fields_are_rejected(self) -> None:
        for field, value in (
            ("blocking", True),
            ("severity", "blocking"),
            ("releaseDecision", "approve"),
        ):
            result = dict(VALID_RESULT)
            result[field] = value
            with self.assertRaises(ValidationError):
                self.validator.validate(result)
            with self.assertRaises(PydanticValidationError):
                EvalResult.model_validate(result)

    def test_duplicate_evidence_refs_are_rejected(self) -> None:
        result = dict(VALID_RESULT)
        result["evidenceRefs"] = ["artifact://same", "artifact://same"]
        with self.assertRaises(ValidationError):
            self.validator.validate(result)
        with self.assertRaises(PydanticValidationError):
            EvalResult.model_validate(result)

    def test_external_and_internal_top_level_shapes_stay_aligned(self) -> None:
        generated = EvalResult.model_json_schema(by_alias=True)
        self.assertEqual(set(self.schema["required"]), set(generated["required"]))
        self.assertEqual(set(self.schema["properties"]), set(generated["properties"]))


if __name__ == "__main__":
    unittest.main()
