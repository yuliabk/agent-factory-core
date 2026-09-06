from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .effective_release_config import EffectiveReleaseConfig
from .trust import TrustProfile


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class ExecutionContext(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["ExecutionContext"]
    request_id: str = Field(alias="requestId", min_length=1)
    trace_id: str = Field(alias="traceId", min_length=1)
    actor_id: str = Field(alias="actorId", min_length=1)
    actor_type: str = Field(alias="actorType", min_length=1)
    tenant_id: str = Field(alias="tenantId", min_length=1)
    environment: str = Field(min_length=1)
    agent_id: str = Field(alias="agentId", min_length=1)
    agent_release_id: str = Field(alias="agentReleaseId", min_length=1)
    trust_profile: TrustProfile = Field(alias="trustProfile")
    permissions: tuple[str, ...]
    data_classification: str = Field(alias="dataClassification", min_length=1)
    capability_bindings: dict[str, str] = Field(alias="capabilityBindings")
    provider_profile: str = Field(alias="providerProfile", min_length=1)
    tool_bindings: dict[str, str] = Field(alias="toolBindings")
    memory_config: dict[str, Any] = Field(alias="memoryConfig")
    budget_config: dict[str, Any] = Field(alias="budgetConfig")
    deadline: datetime


def build_execution_context(
    release: EffectiveReleaseConfig,
    *,
    request_id: str,
    trace_id: str,
    actor_id: str,
    actor_type: str,
    deadline: datetime,
) -> ExecutionContext:
    return ExecutionContext(
        apiVersion="agentfactory.io/v1alpha1",
        kind="ExecutionContext",
        requestId=request_id,
        traceId=trace_id,
        actorId=actor_id,
        actorType=actor_type,
        tenantId=release.spec.tenant.id,
        environment=release.metadata.environment,
        agentId=release.spec.agent_ref.name,
        agentReleaseId=release.metadata.release_id,
        trustProfile=release.spec.trust_profile,
        permissions=release.spec.permissions,
        dataClassification=release.spec.data_classification,
        capabilityBindings=dict(release.spec.capability_bindings),
        providerProfile=release.spec.provider_profile,
        toolBindings=dict(release.spec.tool_bindings),
        memoryConfig=dict(release.spec.memory_config),
        budgetConfig=dict(release.spec.budget_config),
        deadline=deadline,
    )
