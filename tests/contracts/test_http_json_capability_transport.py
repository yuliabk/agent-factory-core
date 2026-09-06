import json
import threading
import unittest
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from jsonschema import Draft202012Validator

from agent_factory_core.capability_gateway import CapabilityGateway
from agent_factory_core.capability_transport import (
    CapabilityTransportError,
    GovernedCapabilityInvoker,
    HttpJsonEndpointConfig,
    build_http_json_registration,
)
from agent_factory_core.contracts.capability_transport import (
    CapabilityInvocationEnvelope,
    CapabilityInvocationResponse,
    HttpJsonTransportDescriptor,
)
from agent_factory_core.contracts.execution_context import ExecutionContext
from agent_factory_core.registry import ResolvedCapability


ROOT = Path(__file__).resolve().parents[2]
ENVELOPE_SCHEMA = json.loads(
    (ROOT / "schemas/capability-invocation-envelope.schema.json").read_text(encoding="utf-8")
)
RESPONSE_SCHEMA = json.loads(
    (ROOT / "schemas/capability-invocation-response.schema.json").read_text(encoding="utf-8")
)
INPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["query"],
    "properties": {"query": {"type": "string", "minLength": 1}},
}
OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["answer"],
    "properties": {"answer": {"type": "string", "minLength": 1}},
}


class _ServerState:
    token = "sandbox-core-token"
    last_envelope = None
    tamper_trace = False


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        if self.path != "/capabilities/research.lookup":
            self.send_error(404)
            return
        if self.headers.get("Authorization") != f"Bearer {_ServerState.token}":
            self.send_error(401)
            return
        size = int(self.headers.get("Content-Length", "0"))
        envelope_data = json.loads(self.rfile.read(size).decode("utf-8"))
        envelope = CapabilityInvocationEnvelope.model_validate(envelope_data)
        _ServerState.last_envelope = envelope

        trace_id = "tampered" if _ServerState.tamper_trace else envelope.trace_id
        response = CapabilityInvocationResponse(
            apiVersion="agentfactory.io/v1alpha1",
            kind="CapabilityInvocationResponse",
            invocationId=envelope.invocation_id,
            requestId=envelope.request_id,
            traceId=trace_id,
            capabilityRef=envelope.capability_ref,
            implementationId=envelope.implementation_id,
            status="success",
            output={"answer": f"remote:{envelope.payload['query']}"},
            limitations=(),
        )
        body = json.dumps(response.model_dump(by_alias=True, mode="json")).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # noqa: A003
        return


class HttpJsonCapabilityTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self):
        _ServerState.last_envelope = None
        _ServerState.tamper_trace = False

    def _context(self, *, permissions=("research.lookup",), deadline=None):
        return ExecutionContext(
            apiVersion="agentfactory.io/v1alpha1",
            kind="ExecutionContext",
            requestId="req-travel-1",
            traceId="trace-travel-1",
            actorId="actor-1",
            actorType="agent",
            tenantId="travel-sandbox",
            environment="sandbox",
            agentId="travel-agent-research-consumer",
            agentReleaseId="travel-release-1",
            trustProfile="internal",
            permissions=permissions,
            dataClassification="internal",
            capabilityBindings={"research.lookup": "research-http-v1"},
            providerProfile="provider.none",
            toolBindings={},
            memoryConfig={},
            budgetConfig={"profile": "sandbox", "maxCost": 0},
            deadline=deadline or datetime.now(timezone.utc) + timedelta(minutes=2),
        )

    def _resolved(self):
        return ResolvedCapability(
            ref="research.lookup",
            version="1",
            implementation_id="research-http-v1",
            input_schema_ref="input.json",
            output_schema_ref="output.json",
            risk_class="read_only",
            cost_class="variable",
            allowed_data_classifications=("public", "internal"),
            required_permissions=("research.lookup",),
            overrides={"qualityProfile": "balanced"},
            transport=HttpJsonTransportDescriptor(
                type="http-json",
                endpointRef="research-agent-sandbox",
                path="/capabilities/research.lookup",
                auth="bearer",
                timeoutSeconds=5,
            ),
        )

    def _gateway(self):
        registration = build_http_json_registration(
            self._resolved(),
            endpoint=HttpJsonEndpointConfig(
                base_url=self.base_url,
                bearer_token=_ServerState.token,
            ),
            input_schema=INPUT_SCHEMA,
            output_schema=OUTPUT_SCHEMA,
            minimum_trust_profile="internal",
        )
        return CapabilityGateway((registration,))

    def test_schema_and_pydantic_contracts_align(self):
        envelope_schema = CapabilityInvocationEnvelope.model_json_schema(by_alias=True)
        response_schema = CapabilityInvocationResponse.model_json_schema(by_alias=True)
        self.assertEqual(set(ENVELOPE_SCHEMA["required"]), set(envelope_schema["required"]))
        self.assertEqual(set(ENVELOPE_SCHEMA["properties"]), set(envelope_schema["properties"]))
        self.assertEqual(set(RESPONSE_SCHEMA["required"]), set(response_schema["required"]))
        self.assertEqual(set(RESPONSE_SCHEMA["properties"]), set(response_schema["properties"]))
        Draft202012Validator(ENVELOPE_SCHEMA).check_schema(ENVELOPE_SCHEMA)
        Draft202012Validator(RESPONSE_SCHEMA).check_schema(RESPONSE_SCHEMA)

    def test_real_http_call_preserves_trusted_context_and_delegates_only_consumer_permission(self):
        context = self._context()
        invoker = GovernedCapabilityInvoker(
            gateway=self._gateway(),
            context=context,
            platform_policy_ref="policy.travel.v1",
        )
        output = invoker.invoke("research.lookup", {"query": "Rome"})
        self.assertEqual(output, {"answer": "remote:Rome"})

        envelope = _ServerState.last_envelope
        self.assertIsNotNone(envelope)
        assert envelope is not None
        self.assertEqual(envelope.request_id, context.request_id)
        self.assertEqual(envelope.trace_id, context.trace_id)
        self.assertEqual(envelope.tenant_id, context.tenant_id)
        self.assertEqual(envelope.caller_agent_release_id, context.agent_release_id)
        self.assertEqual(envelope.data_classification, context.data_classification)
        self.assertEqual(envelope.delegated_permissions, ("research.lookup",))
        self.assertNotIn("web.search", envelope.delegated_permissions)
        self.assertEqual(envelope.budget_context, context.budget_config)
        self.assertEqual(envelope.hop_count, 1)
        self.assertEqual(envelope.max_hops, 4)

    def test_gateway_denies_before_network_when_consumer_permission_is_missing(self):
        invoker = GovernedCapabilityInvoker(
            gateway=self._gateway(),
            context=self._context(permissions=()),
            platform_policy_ref="policy.travel.v1",
        )
        with self.assertRaises(Exception):
            invoker.invoke("research.lookup", {"query": "Rome"})
        self.assertIsNone(_ServerState.last_envelope)

    def test_expired_deadline_fails_before_network(self):
        invoker = GovernedCapabilityInvoker(
            gateway=self._gateway(),
            context=self._context(deadline=datetime.now(timezone.utc) - timedelta(seconds=1)),
            platform_policy_ref="policy.travel.v1",
        )
        with self.assertRaises(Exception):
            invoker.invoke("research.lookup", {"query": "Rome"})
        self.assertIsNone(_ServerState.last_envelope)

    def test_tampered_response_trace_is_rejected(self):
        _ServerState.tamper_trace = True
        invoker = GovernedCapabilityInvoker(
            gateway=self._gateway(),
            context=self._context(),
            platform_policy_ref="policy.travel.v1",
        )
        with self.assertRaises(CapabilityTransportError):
            invoker.invoke("research.lookup", {"query": "Rome"})

    def test_invalid_input_is_rejected_before_network(self):
        invoker = GovernedCapabilityInvoker(
            gateway=self._gateway(),
            context=self._context(),
            platform_policy_ref="policy.travel.v1",
        )
        with self.assertRaises(Exception):
            invoker.invoke("research.lookup", {"query": ""})
        self.assertIsNone(_ServerState.last_envelope)


if __name__ == "__main__":
    unittest.main()
