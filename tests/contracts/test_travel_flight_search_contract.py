import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from agent_factory_core.contracts.agent_manifest import RequiredCapabilityRef
from agent_factory_core.registry import CapabilityRecord, CapabilityRegistry


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "schemas" / "capabilities" / "travel.flight.search.input.v1.json"
OUTPUT_PATH = ROOT / "schemas" / "capabilities" / "travel.flight.search.output.v1.json"
RECORD_PATH = ROOT / "registry" / "capabilities" / "travel.flight.search.v1.json"
REGISTRY_SCHEMA_PATH = ROOT / "schemas" / "capability-registry-record.schema.json"
FLIGHT_PROVIDER_RELEASE = (
    "github:yuliabk/agent-factory-flight-provider@"
    "d2f4e18d5e8f5911a4365a48da80617b4304e77a"
)


class TravelFlightSearchContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_schema = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
        cls.output_schema = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        cls.record_data = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
        cls.registry_schema = json.loads(REGISTRY_SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_registry_contract_is_provider_neutral_and_bound_only_in_sandbox(self) -> None:
        Draft202012Validator(self.registry_schema).validate(self.record_data)
        record = CapabilityRecord.model_validate(self.record_data)
        self.assertEqual(record.ref, "travel.flight.search")
        self.assertEqual(record.version, "1")
        self.assertEqual(record.risk_class, "read_only")
        self.assertEqual(record.cost_class, "variable")
        self.assertEqual(record.required_permissions, ["travel.flight.search"])
        self.assertEqual(len(record.implementations), 1)
        implementation = record.implementations[0]
        self.assertEqual(implementation.id, FLIGHT_PROVIDER_RELEASE)
        self.assertEqual(implementation.environments, ["sandbox"])
        self.assertTrue(implementation.enabled)
        self.assertIsNotNone(implementation.transport)
        assert implementation.transport is not None
        self.assertEqual(implementation.transport.type, "http-json")
        self.assertEqual(implementation.transport.endpoint_ref, "flight-provider-sandbox")
        self.assertEqual(implementation.transport.path, "/capabilities/travel.flight.search")
        self.assertEqual(implementation.transport.auth, "bearer")
        self.assertEqual(implementation.transport.timeout_seconds, 12)

        public_contract = json.dumps(
            {
                "inputSchemaRef": self.record_data["inputSchemaRef"],
                "outputSchemaRef": self.record_data["outputSchemaRef"],
                "requiredPermissions": self.record_data["requiredPermissions"],
                "overrideable": self.record_data["overrideable"],
            }
        ).lower()
        self.assertNotIn("serpapi", public_contract)
        self.assertNotIn("google", public_contract)
        self.assertNotIn("fast-flights", public_contract)
        self.assertNotIn("faster-flights", public_contract)

    def test_input_supports_one_way_and_round_trip_without_provider_selector(self) -> None:
        one_way = {
            "originIata": "TLV",
            "destinationIata": "NRT",
            "departureDate": "2026-09-07",
            "returnDate": None,
            "tripType": "one-way",
            "adults": 1,
            "children": 0,
            "cabin": "economy",
            "currency": "USD",
            "maxStops": 1,
            "maxResults": 10,
        }
        Draft202012Validator(self.input_schema).validate(one_way)

        round_trip = dict(one_way)
        round_trip.update(
            {
                "tripType": "round-trip",
                "returnDate": "2026-09-24",
            }
        )
        Draft202012Validator(self.input_schema).validate(round_trip)

        for forbidden in ("provider", "adapter", "scraper", "apiKey", "implementationId"):
            payload = dict(one_way)
            payload[forbidden] = "caller-selected"
            with self.assertRaises(ValidationError):
                Draft202012Validator(self.input_schema).validate(payload)

    def test_round_trip_requires_return_date_and_one_way_rejects_it(self) -> None:
        base = {
            "originIata": "TLV",
            "destinationIata": "NRT",
            "departureDate": "2026-09-07",
            "tripType": "round-trip",
            "adults": 1,
            "children": 0,
            "cabin": "economy",
            "currency": "USD",
            "maxResults": 10,
        }
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.input_schema).validate(base)

        one_way_with_return = dict(base)
        one_way_with_return.update(
            {
                "tripType": "one-way",
                "returnDate": "2026-09-24",
            }
        )
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.input_schema).validate(one_way_with_return)

    def test_observed_output_is_not_misrepresented_as_booking_ready(self) -> None:
        output = {
            "status": "complete",
            "searchId": "flight-search-1",
            "observedAt": "2026-09-06T15:30:00Z",
            "options": [
                {
                    "optionId": "option-1",
                    "carrierText": "Example Air",
                    "departureText": "10:00 AM",
                    "arrivalText": "2:00 PM",
                    "durationText": "4 hr",
                    "stops": 0,
                    "price": {
                        "displayText": "$420",
                        "amount": "420",
                        "currency": "USD",
                    },
                    "isBest": True,
                    "bookingReady": False,
                    "evidenceStatus": "observed",
                    "sourceRef": None,
                }
            ],
            "limitations": ["sandbox observed search; booking availability is not guaranteed"],
        }
        Draft202012Validator(self.output_schema).validate(output)
        self.assertFalse(output["options"][0]["bookingReady"])
        self.assertEqual(output["options"][0]["evidenceStatus"], "observed")

        for forbidden in ("provider", "scraper", "rawHtml", "credentials", "apiKey"):
            payload = copy.deepcopy(output)
            payload[forbidden] = "sensitive-or-provider-specific"
            with self.assertRaises(ValidationError):
                Draft202012Validator(self.output_schema).validate(payload)

    def test_price_amount_and_currency_are_both_present_or_both_null(self) -> None:
        base_option = {
            "optionId": "option-1",
            "carrierText": "Example Air",
            "departureText": "10:00 AM",
            "arrivalText": "2:00 PM",
            "durationText": "4 hr",
            "stops": 0,
            "isBest": False,
            "bookingReady": False,
            "evidenceStatus": "observed",
            "sourceRef": None,
        }
        for amount, currency in ((None, None), ("420", "USD")):
            option = dict(base_option)
            option["price"] = {"displayText": "$420", "amount": amount, "currency": currency}
            response = {
                "status": "complete",
                "searchId": "flight-search-1",
                "observedAt": "2026-09-06T15:30:00Z",
                "options": [option],
                "limitations": [],
            }
            Draft202012Validator(self.output_schema).validate(response)

        invalid = dict(base_option)
        invalid["price"] = {"displayText": "$420", "amount": "420", "currency": None}
        response = {
            "status": "complete",
            "searchId": "flight-search-1",
            "observedAt": "2026-09-06T15:30:00Z",
            "options": [invalid],
            "limitations": [],
        }
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.output_schema).validate(response)

    def test_registry_resolves_exact_sandbox_release_and_production_fails_closed(self) -> None:
        registry = CapabilityRegistry([CapabilityRecord.model_validate(self.record_data)])
        resolved = registry.resolve_required(
            RequiredCapabilityRef(
                ref="travel.flight.search",
                version="1",
                optional=False,
                overrides={},
            ),
            environment="sandbox",
            mode="strict",
        )
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved.implementation_id, FLIGHT_PROVIDER_RELEASE)
        self.assertEqual(resolved.required_permissions, ("travel.flight.search",))
        self.assertEqual(resolved.allowed_data_classifications, ("public", "internal"))
        self.assertIsNotNone(resolved.transport)
        assert resolved.transport is not None
        self.assertEqual(resolved.transport.endpoint_ref, "flight-provider-sandbox")

        with self.assertRaises(ValueError):
            registry.resolve_required(
                RequiredCapabilityRef(
                    ref="travel.flight.search",
                    version="1",
                    optional=False,
                    overrides={},
                ),
                environment="production",
                mode="strict",
            )


if __name__ == "__main__":
    unittest.main()
