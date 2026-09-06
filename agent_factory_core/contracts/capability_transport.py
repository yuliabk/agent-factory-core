from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class HttpJsonTransportDescriptor(FrozenModel):
    type: Literal["http-json"]
    endpoint_ref: str = Field(alias="endpointRef", min_length=1)
    path: str = Field(min_length=1, pattern=r"^/")
    auth: Literal["bearer"]
    timeout_seconds: int = Field(alias="timeoutSeconds", ge=1, le=30)


class CapabilityInvocationEnvelope(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["CapabilityInvocationEnvelope"]
    invocation_id: str = Field(alias="invocationId", min_length=1)
    request_id: str = Field(alias="requestId", min_length=1)
    trace_id: str = Field(alias="traceId", min_length=1)
    caller_agent_id: str = Field(alias="callerAgentId", min_length=1)
    caller_agent_release_id: str = Field(alias="callerAgentReleaseId", min_length=1)
    tenant_id: str = Field(alias="tenantId", min_length=1)
    environment: str = Field(min_length=1)
    capability_ref: str = Field(alias="capabilityRef", min_length=1)
    implementation_id: str = Field(alias="implementationId", min_length=1)
    data_classification: str = Field(alias="dataClassification", min_length=1)
    delegated_permissions: tuple[str, ...] = Field(alias="delegatedPermissions", min_length=1)
    deadline: datetime
    hop_count: int = Field(alias="hopCount", ge=0)
    max_hops: int = Field(alias="maxHops", ge=1, le=64)
    budget_context: dict[str, Any] = Field(alias="budgetContext", default_factory=dict)
    payload: dict[str, Any]

    @model_validator(mode="after")
    def validate_bounds(self) -> "CapabilityInvocationEnvelope":
        if self.hop_count >= self.max_hops:
            raise ValueError("hopCount must be lower than maxHops")
        if len(set(self.delegated_permissions)) != len(self.delegated_permissions):
            raise ValueError("delegatedPermissions must be unique")
        return self


class CapabilityInvocationResponse(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["CapabilityInvocationResponse"]
    invocation_id: str = Field(alias="invocationId", min_length=1)
    request_id: str = Field(alias="requestId", min_length=1)
    trace_id: str = Field(alias="traceId", min_length=1)
    capability_ref: str = Field(alias="capabilityRef", min_length=1)
    implementation_id: str = Field(alias="implementationId", min_length=1)
    status: Literal["success", "error"]
    output: dict[str, Any] | None = None
    error_code: str | None = Field(alias="errorCode", default=None, min_length=1)
    limitations: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_status(self) -> "CapabilityInvocationResponse":
        if self.status == "success":
            if self.output is None:
                raise ValueError("success response requires output")
            if self.error_code is not None:
                raise ValueError("success response cannot include errorCode")
        else:
            if self.error_code is None:
                raise ValueError("error response requires errorCode")
            if self.output is not None:
                raise ValueError("error response cannot include output")
        if len(set(self.limitations)) != len(self.limitations):
            raise ValueError("limitations must be unique")
        return self
