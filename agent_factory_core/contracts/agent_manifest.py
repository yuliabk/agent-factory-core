from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


CAPABILITY_REF_PATTERN = r"^[a-z][a-z0-9_-]*(\.[a-z][a-z0-9_-]*)+$"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ManifestMetadata(StrictModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    description: str = Field(min_length=1)


class TemplateRef(StrictModel):
    name: str = Field(min_length=1)
    version: str | int


class CapabilityRef(StrictModel):
    """Lightweight reference into the Capability Registry.

    Registry metadata remains the source of truth. `overrides` is intentionally
    opaque here; the compiler must reject keys not marked overrideable by the
    resolved registry record.
    """

    ref: str = Field(pattern=CAPABILITY_REF_PATTERN)
    version: str = Field(min_length=1)
    overrides: dict[str, Any] = Field(default_factory=dict)


class RequiredCapabilityRef(CapabilityRef):
    optional: bool = False


class Capabilities(StrictModel):
    provides: list[CapabilityRef] = Field(default_factory=list)
    requires: list[RequiredCapabilityRef] = Field(default_factory=list)


class ToolRequirements(StrictModel):
    required: list[str] = Field(default_factory=list)


class PermissionRequirements(StrictModel):
    requested: list[str] = Field(default_factory=list)


class AgentSpec(StrictModel):
    template: TemplateRef
    capabilities: Capabilities
    tools: ToolRequirements
    permissions: PermissionRequirements
    memory_profile: str = Field(alias="memoryProfile", min_length=1)
    budget_profile: str = Field(alias="budgetProfile", min_length=1)
    eval_profile: str = Field(alias="evalProfile", min_length=1)


class AgentManifest(StrictModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["AgentManifest"]
    metadata: ManifestMetadata
    spec: AgentSpec
