from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ClientMetadata(StrictModel):
    name: str = Field(min_length=1)
    environment: str = Field(min_length=1)


class AgentRef(StrictModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)


class TenantRef(StrictModel):
    id: str = Field(min_length=1)


class PermissionOverrides(StrictModel):
    allow: list[str] = Field(default_factory=list)
    deny: list[str] = Field(default_factory=list)


class ClientInstanceSpec(StrictModel):
    agent_ref: AgentRef = Field(alias="agentRef")
    tenant: TenantRef
    variables: dict[str, Any] = Field(default_factory=dict)
    provider_profile: str = Field(alias="providerProfile", min_length=1)
    secrets_ref: dict[str, str] = Field(alias="secretsRef", default_factory=dict)
    memory_config: dict[str, Any] = Field(alias="memoryConfig", default_factory=dict)
    budget_overrides: dict[str, Any] = Field(alias="budgetOverrides", default_factory=dict)
    permission_overrides: PermissionOverrides = Field(alias="permissionOverrides")
    tool_bindings: dict[str, str] = Field(alias="toolBindings", default_factory=dict)


class ClientInstanceConfig(StrictModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["ClientInstanceConfig"]
    metadata: ClientMetadata
    spec: ClientInstanceSpec
