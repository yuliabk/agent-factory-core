from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ExceptionMetadata(StrictModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)


class PlatformPolicyRef(StrictModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)


class ExceptionScope(StrictModel):
    tenant_id: str = Field(alias="tenantId", min_length=1)
    environment: str = Field(min_length=1)
    agent_name: str | None = Field(alias="agentName", default=None, min_length=1)
    agent_version: str | None = Field(alias="agentVersion", default=None, min_length=1)


class ExceptionAllow(StrictModel):
    permissions: list[str] = Field(default_factory=list)
    provider_profiles: list[str] = Field(alias="providerProfiles", default_factory=list)
    budget_override_keys: list[str] = Field(alias="budgetOverrideKeys", default_factory=list)
    memory_config_keys: list[str] = Field(alias="memoryConfigKeys", default_factory=list)


class ExceptionPolicySpec(StrictModel):
    platform_policy_ref: PlatformPolicyRef = Field(alias="platformPolicyRef")
    scope: ExceptionScope
    reason: str = Field(min_length=1)
    approver: str = Field(min_length=1)
    expires_at: datetime = Field(alias="expiresAt")
    allow: ExceptionAllow


class ExceptionPolicy(StrictModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["ExceptionPolicy"]
    metadata: ExceptionMetadata
    spec: ExceptionPolicySpec
