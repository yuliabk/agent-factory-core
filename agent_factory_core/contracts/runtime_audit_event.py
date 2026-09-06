from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class RuntimeAuditEvent(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["RuntimeAuditEvent"]
    timestamp: datetime
    tenant_id: str = Field(alias="tenantId", min_length=1)
    request_id: str = Field(alias="requestId", min_length=1)
    trace_id: str = Field(alias="traceId", min_length=1)
    actor_id: str = Field(alias="actorId", min_length=1)
    actor_type: str = Field(alias="actorType", min_length=1)
    agent_release_id: str = Field(alias="agentReleaseId", min_length=1)
    platform_policy_ref: str = Field(alias="platformPolicyRef", min_length=1)
    exception_policy_refs: tuple[str, ...] = Field(alias="exceptionPolicyRefs")
    approval_ref: str | None = Field(alias="approvalRef")
    operation: str = Field(min_length=1)
    target_ref: str | None = Field(alias="targetRef")
    decision: str = Field(min_length=1)
    result: str = Field(min_length=1)
    cost_amount: str | None = Field(alias="costAmount", pattern=r"^[0-9]+(?:\.[0-9]+)?$")
    cost_currency: str | None = Field(alias="costCurrency")

    @model_validator(mode="after")
    def validate_cost_pair(self) -> "RuntimeAuditEvent":
        if (self.cost_amount is None) != (self.cost_currency is None):
            raise ValueError("costAmount and costCurrency must either both be set or both be null")
        return self
