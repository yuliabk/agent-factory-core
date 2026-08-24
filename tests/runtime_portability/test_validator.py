from __future__ import annotations

import json
import socket
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from tools.runtime_portability.validator import run_dry_validation


FIXTURE_ROOT = Path(__file__).parents[1] / "fixtures" / "runtime_portability"


def load_fixture(name: str):
    with (FIXTURE_ROOT / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class DryValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = load_fixture("adapter.valid.json")
        self.question_set = load_fixture("question-set.json")
        self.fixtures = load_fixture("evidence-fixtures.valid.json")

    def run_report(self, adapter=None, question_set=None, fixtures=None):
        return run_dry_validation(
            self.adapter if adapter is None else adapter,
            self.question_set if question_set is None else question_set,
            self.fixtures if fixtures is None else fixtures,
        )

    def test_valid_dry_run_passes_without_executing_questions(self):
        report = self.run_report()

        self.assertEqual("pass", report["overall_verdict"])
        self.assertEqual("preflight_passed", report["lifecycle_state"])
        self.assertEqual(0, report["external_calls"])
        self.assertEqual(0, report["runtime_questions_executed"])
        self.assertEqual(25, len(report["questions"]))
        self.assertTrue(all(item["runtime_status"] == "not_run" for item in report["questions"]))

    def test_report_is_deterministic(self):
        self.assertEqual(self.run_report(), self.run_report())

    def test_unknown_capability_blocks_preflight(self):
        adapter = deepcopy(self.adapter)
        adapter["capabilities"]["source_provenance"]["supported"] = "unknown"

        report = self.run_report(adapter=adapter)

        self.assertEqual("blocked", report["overall_verdict"])
        self.assertIn(
            "capabilities.source_provenance.supported must be true",
            report["adapter_validation"]["errors"],
        )

    def test_duplicate_question_blocks_preflight(self):
        question_set = deepcopy(self.question_set)
        question_set["questions"][1]["question_id"] = "KA-E01"

        report = self.run_report(question_set=question_set)

        self.assertEqual("blocked", report["overall_verdict"])
        self.assertIn("duplicate question_id: KA-E01", report["question_set_validation"]["errors"])

    def test_unresolved_citation_fails_fixture(self):
        fixtures = deepcopy(self.fixtures)
        fixtures[0]["response"]["citations"][0]["section_id"] = "מקור לא קיים"

        report = self.run_report(fixtures=fixtures)

        self.assertEqual("fail", report["overall_verdict"])
        self.assertTrue(
            any("unresolved citation" in error for error in report["fixture_validation"][0]["errors"])
        )

    def test_non_empty_tool_calls_fail_fixture(self):
        fixtures = deepcopy(self.fixtures)
        fixtures[0]["response"]["tool_calls"] = [{"name": "send_message"}]

        report = self.run_report(fixtures=fixtures)

        self.assertEqual("fail", report["overall_verdict"])
        self.assertIn(
            "fixture.response.tool_calls must be an empty array",
            report["fixture_validation"][0]["errors"],
        )

    def test_unknown_cost_fails_fixture_instead_of_becoming_zero(self):
        fixtures = deepcopy(self.fixtures)
        fixtures[0]["evidence"]["normalized_cost"]["amount_ils"] = None
        fixtures[0]["evidence"]["normalized_cost"]["confidence"] = "unknown"

        report = self.run_report(fixtures=fixtures)

        self.assertEqual("fail", report["overall_verdict"])
        self.assertIn(
            "fixture.evidence.normalized_cost.amount_ils cannot be unknown",
            report["fixture_validation"][0]["errors"],
        )

    def test_provider_options_cannot_weaken_policy(self):
        fixtures = deepcopy(self.fixtures)
        fixtures[0]["request"]["provider_options"] = {"tool_policy": "allow_all"}

        report = self.run_report(fixtures=fixtures)

        self.assertEqual("fail", report["overall_verdict"])
        self.assertIn(
            "fixture.request.provider_options cannot override tool_policy",
            report["fixture_validation"][0]["errors"],
        )

    def test_request_cannot_drift_from_canonical_release(self):
        fixtures = deepcopy(self.fixtures)
        fixtures[0]["request"]["agent_release_id"] = "unapproved@9.9.9"

        report = self.run_report(fixtures=fixtures)

        self.assertEqual("fail", report["overall_verdict"])
        self.assertIn(
            "fixture.request.agent_release_id does not match canonical value",
            report["fixture_validation"][0]["errors"],
        )

    def test_fixture_usage_above_stop_threshold_fails(self):
        adapter = deepcopy(self.adapter)
        adapter["cost_controls"]["native_stop_threshold"] = 2

        report = self.run_report(adapter=adapter)

        self.assertEqual("fail", report["overall_verdict"])
        self.assertIn(
            "synthetic fixture usage exceeds native stop threshold",
            report["cost_validation"]["errors"],
        )

    def test_malformed_drift_is_reported_without_crashing(self):
        fixtures = deepcopy(self.fixtures)
        fixtures[0]["evidence"]["drift"] = "invalid"

        report = self.run_report(fixtures=fixtures)

        self.assertEqual("fail", report["overall_verdict"])
        self.assertIn(
            "fixture.evidence.drift must be an object",
            report["fixture_validation"][0]["errors"],
        )

    def test_secret_bearing_field_blocks_adapter(self):
        adapter = deepcopy(self.adapter)
        adapter["api_key"] = "synthetic-but-prohibited"

        report = self.run_report(adapter=adapter)

        self.assertEqual("blocked", report["overall_verdict"])
        self.assertIn(
            "secret-bearing field is prohibited: $.api_key",
            report["adapter_validation"]["errors"],
        )

    def test_validation_still_passes_when_network_sockets_are_disabled(self):
        with patch.object(socket, "socket", side_effect=AssertionError("network access attempted")):
            report = self.run_report()

        self.assertEqual("pass", report["overall_verdict"])
        self.assertEqual(0, report["external_calls"])


if __name__ == "__main__":
    unittest.main()
