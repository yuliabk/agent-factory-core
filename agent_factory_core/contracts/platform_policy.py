from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from .release_strategy import EffectiveReleaseStrategy
from .trust import TrustProfile


NonEmptyString = Annotated[str, Field(min_length=1)]
GateClassification = Literal["blocking", "warning", "advisory"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class PolicyMetadata(StrictModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)


class ExceptionAllowances(StrictModel):
    permissions: list[str] = Field(default_factory=list)
    provider_profiles: list[str] = Field(alias="providerProfiles", default_factory=list)
    budget_override_keys: list[str] = Field(alias="budgetOverrideKeys", default_factory=list)
    memory_config_keys: list[str] = Field(alias="memoryConfigKeys", default_factory=list)


class EvalRule(StrictModel):
    check_id: str = Field(alias="checkId", min_length=1)
    classification: GateClassification


class PlatformPolicySpec(StrictModel):
    allowed_permissions: list[str] = Field(alias="allowedPermissions", default_factory=list)
    denied_permissions: list[str] = Field(alias="deniedPermissions", default_factory=list)
    allowed_provider_profiles: list[str] = Field(alias="allowedProviderProfiles", default_factory=list)
    allowed_budget_override_keys: list[str] = Field(alias="allowedBudgetOverrideKeys", default_factory=list)
    allowed_memory_config_keys: list[str] = Field(alias="allowedMemoryConfigKeys", default_factory=list)
    max_trust_profile: TrustProfile = Field(alias="maxTrustProfile")
    minimum_release_strategy: EffectiveReleaseStrategy = Field(alias="minimumReleaseStrategy")
    registry_mode: Literal["soft", "strict"] = Field(alias="registryMode")
    default_data_classification: str = Field(alias="defaultDataClassification", min_length=1)
    eval_rules: list[EvalRule] = Field(alias="evalRules")
    security_invariant_checks: list[NonEmptyString] = Field(alias="securityInvariantChecks")
    exception_allowances: ExceptionAllowances = Field(alias="exceptionAllowances")


class PlatformPolicy(StrictModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["PlatformPolicy"]
    metadata: PolicyMetadata
    spec: PlatformPolicySpec
