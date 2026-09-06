from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping
from urllib import error as urllib_error
from urllib import request as urllib_request
from uuid import uuid4

from jsonschema import Draft202012Validator

from .capability_gateway import CapabilityGateway, CapabilityRegistration, CapabilitySpec
from .contracts.capability_transport import (
    CapabilityInvocationEnvelope,
    CapabilityInvocationResponse,
    HttpJsonTransportDescriptor,
)
from .contracts.execution_context import ExecutionContext
from .contracts.trust import TrustProfile
from .registry import ResolvedCapability


class CapabilityTransportError(RuntimeError):
    pass


class CapabilityInvocationDenied(RuntimeError):
    pass


@dataclass(frozen=True)
class HttpJsonEndpointConfig:
    base_url: str
    bearer_token: str

    def __post_init__(self) -> None:
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("base_url must use http or https")
        if not self.bearer_token:
            raise ValueError("bearer_token is required")


class HttpJsonRemoteCapabilityHandler:
    def __init__(
        self,
        *,
        capability_ref: str,
        implementation_id: str,
        required_permission: str,
        descriptor: HttpJsonTransportDescriptor,
        endpoint: HttpJsonEndpointConfig,
        input_schema: Mapping[str, Any],
        output_schema: Mapping[str, Any],
        max_hops: int = 4,
    ) -> None:
        if max_hops < 2:
            raise ValueError("max_hops must allow at least one delegated hop")
        self.capability_ref = capability_ref
        self.implementation_id = implementation_id
        self.required_permission = required_permission
        self.descriptor = descriptor
        self.endpoint = endpoint
        self.input_validator = Draft202012Validator(dict(input_schema))
        self.output_validator = Draft202012Validator(dict(output_schema))
        self.max_hops = max_hops

    def __call__(
        self,
        context: ExecutionContext,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        payload_dict = dict(payload)
        self.input_validator.validate(payload_dict)

        now = datetime.now(timezone.utc)
        seconds_until_deadline = (context.deadline - now).total_seconds()
        if seconds_until_deadline <= 0:
            raise CapabilityTransportError("execution deadline expired before remote capability call")

        invocation_id = f"capinv_{uuid4().hex}"
        envelope = CapabilityInvocationEnvelope(
            apiVersion="agentfactory.io/v1alpha1",
            kind="CapabilityInvocationEnvelope",
            invocationId=invocation_id,
            requestId=context.request_id,
            traceId=context.trace_id,
            callerAgentId=context.agent_id,
            callerAgentReleaseId=context.agent_release_id,
            tenantId=context.tenant_id,
            environment=context.environment,
            capabilityRef=self.capability_ref,
            implementationId=self.implementation_id,
            dataClassification=context.data_classification,
            delegatedPermissions=(self.required_permission,),
            deadline=context.deadline,
            hopCount=1,
            maxHops=self.max_hops,
            budgetContext=dict(context.budget_config),
            payload=payload_dict,
        )

        timeout = min(float(self.descriptor.timeout_seconds), seconds_until_deadline)
        url = self.endpoint.base_url.rstrip("/") + self.descriptor.path
        body = json.dumps(
            envelope.model_dump(by_alias=True, mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        req = urllib_request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.endpoint.bearer_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "agent-factory-core/http-json-capability-v1",
            },
        )
        try:
            with urllib_request.urlopen(req, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
        except (urllib_error.URLError, TimeoutError, OSError) as exc:
            raise CapabilityTransportError("remote capability transport failed") from exc

        try:
            response_data = json.loads(raw)
            remote = CapabilityInvocationResponse.model_validate(response_data)
        except Exception as exc:
            raise CapabilityTransportError("remote capability response is not a valid envelope") from exc

        expected = {
            "invocation_id": invocation_id,
            "request_id": context.request_id,
            "trace_id": context.trace_id,
            "capability_ref": self.capability_ref,
            "implementation_id": self.implementation_id,
        }
        for field, value in expected.items():
            if getattr(remote, field) != value:
                raise CapabilityTransportError(f"remote capability response mismatch: {field}")

        if remote.status != "success" or remote.output is None:
            raise CapabilityTransportError(
                f"remote capability returned error: {remote.error_code or 'unknown'}"
            )

        self.output_validator.validate(remote.output)
        return dict(remote.output)


def build_http_json_registration(
    resolved: ResolvedCapability,
    *,
    endpoint: HttpJsonEndpointConfig,
    input_schema: Mapping[str, Any],
    output_schema: Mapping[str, Any],
    minimum_trust_profile: TrustProfile,
    max_hops: int = 4,
) -> CapabilityRegistration:
    if resolved.transport is None:
        raise ValueError("resolved capability has no remote transport descriptor")
    if len(resolved.required_permissions) != 1:
        raise ValueError("HTTP JSON v1 requires exactly one consumer permission")

    spec = CapabilitySpec(
        capability_ref=resolved.ref,
        implementation_id=resolved.implementation_id,
        required_permission=resolved.required_permissions[0],
        minimum_trust_profile=minimum_trust_profile,
        allowed_data_classifications=resolved.allowed_data_classifications,
    )
    handler = HttpJsonRemoteCapabilityHandler(
        capability_ref=resolved.ref,
        implementation_id=resolved.implementation_id,
        required_permission=resolved.required_permissions[0],
        descriptor=resolved.transport,
        endpoint=endpoint,
        input_schema=input_schema,
        output_schema=output_schema,
        max_hops=max_hops,
    )
    return CapabilityRegistration(spec=spec, context_handler=handler)


class GovernedCapabilityInvoker:
    """Small consumer-facing adapter over an already-compiled Core capability gateway."""

    def __init__(
        self,
        *,
        gateway: CapabilityGateway,
        context: ExecutionContext,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...] = (),
        approval_ref: str | None = None,
    ) -> None:
        self.gateway = gateway
        self.context = context
        self.platform_policy_ref = platform_policy_ref
        self.exception_policy_refs = exception_policy_refs
        self.approval_ref = approval_ref

    def invoke(self, capability_ref: str, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        result = self.gateway.invoke(
            self.context,
            capability_ref=capability_ref,
            payload=payload,
            data_classification=self.context.data_classification,
            platform_policy_ref=self.platform_policy_ref,
            exception_policy_refs=self.exception_policy_refs,
            approval_ref=self.approval_ref,
        )
        if not result.allowed or result.output is None:
            raise CapabilityInvocationDenied(f"{result.rule}: {result.reason}")
        return dict(result.output)
