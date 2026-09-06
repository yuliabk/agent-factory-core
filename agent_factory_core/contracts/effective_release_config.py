from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .agent_manifest import Capabilities
from .client_instance_config import AgentRef, TenantRef


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class EffectiveReleaseMetadata(FrozenModel):
    release_id: str = Field(alias="releaseId", min_length=1)
    environment: str = Field(min_length=1)


class PolicySnapshot(FrozenModel):
    platform_policy_version: str = Field(alias="platformPolicyVersion", min_length=1)
    exception_policy_refs: tuple[str, ...] = Field(alias="exceptionPolicyRefs", default_factory=tuple)


class EffectiveReleaseSpec(FrozenModel):
    agent_ref: AgentRef = Field(alias="agentRef")
    tenant: TenantRef
    variables: dict[str, Any]
    capabilities: Capabilities
    provider_profile: str = Field(alias="providerProfile", min_length=1)
    secrets_ref: dict[str, str] = Field(alias="secretsRef")
    memory_config: dict[str, Any] = Field(alias="memoryConfig")
    budget_config: dict[str, Any] = Field(alias="budgetConfig")
    permissions: tuple[str, ...]
    tool_bindings: dict[str, str] = Field(alias="toolBindings")
    eval_profile: str = Field(alias="evalProfile", min_length=1)


class EffectiveReleaseConfig(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["EffectiveReleaseConfig"]
    metadata: EffectiveReleaseMetadata
    policy: PolicySnapshot
    spec: EffectiveReleaseSpec
