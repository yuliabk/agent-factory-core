from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


NonEmptyString = Annotated[str, Field(min_length=1)]
Sha256Fingerprint = Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")]


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class EvidencePack(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["EvidencePack"]
    evidence_pack_id: str = Field(alias="evidencePackId", min_length=1)
    release_id: str = Field(alias="releaseId", min_length=1)
    spec_ref: str = Field(alias="specRef", min_length=1)
    agent_manifest_ref: str = Field(alias="agentManifestRef", min_length=1)
    client_instance_config_ref: str = Field(alias="clientInstanceConfigRef", min_length=1)
    effective_release_config_ref: Sha256Fingerprint = Field(alias="effectiveReleaseConfigRef")
    platform_policy_ref: str = Field(alias="platformPolicyRef", min_length=1)
    exception_policy_refs: tuple[NonEmptyString, ...] = Field(alias="exceptionPolicyRefs")
    template_module_refs: tuple[NonEmptyString, ...] = Field(alias="templateModuleRefs", min_length=1)
    config_diff_ref: str = Field(alias="configDiffRef", min_length=1)
    provider_profile: str = Field(alias="providerProfile", min_length=1)
    capability_tool_contract_refs: tuple[NonEmptyString, ...] = Field(alias="capabilityToolContractRefs")
    eval_result_refs: tuple[NonEmptyString, ...] = Field(alias="evalResultRefs", min_length=1)
    release_decision_ref: str = Field(alias="releaseDecisionRef", min_length=1)
    known_limitations: tuple[NonEmptyString, ...] = Field(alias="knownLimitations")
    rollback_ref: Annotated[str, Field(min_length=1)] | None = Field(alias="rollbackRef")
    created_at: datetime = Field(alias="createdAt")

    @model_validator(mode="after")
    def validate_pack(self) -> "EvidencePack":
        for label, values in (
            ("exceptionPolicyRefs", self.exception_policy_refs),
            ("templateModuleRefs", self.template_module_refs),
            ("capabilityToolContractRefs", self.capability_tool_contract_refs),
            ("evalResultRefs", self.eval_result_refs),
            ("knownLimitations", self.known_limitations),
        ):
            if len(set(values)) != len(values):
                raise ValueError(f"{label} must be unique")
        if self.created_at.tzinfo is None:
            raise ValueError("createdAt must be timezone-aware")
        return self
