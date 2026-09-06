from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .release_strategy import EffectiveReleaseStrategy


NonEmptyString = Annotated[str, Field(min_length=1)]


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class ReleaseDecisionRecord(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["ReleaseDecisionRecord"]
    release_decision_id: str = Field(alias="releaseDecisionId", min_length=1)
    release_id: str = Field(alias="releaseId", min_length=1)
    platform_policy_ref: str = Field(alias="platformPolicyRef", min_length=1)
    exception_policy_refs: tuple[NonEmptyString, ...] = Field(alias="exceptionPolicyRefs")
    strategy: EffectiveReleaseStrategy
    result: Literal["released", "blocked", "pending-approval"]
    blocking_check_refs: tuple[NonEmptyString, ...] = Field(alias="blockingCheckRefs")
    warning_check_refs: tuple[NonEmptyString, ...] = Field(alias="warningCheckRefs")
    advisory_check_refs: tuple[NonEmptyString, ...] = Field(alias="advisoryCheckRefs")
    eval_result_refs: tuple[NonEmptyString, ...] = Field(alias="evalResultRefs")
    approval_ref: Annotated[str, Field(min_length=1)] | None = Field(alias="approvalRef")
    reason: str = Field(min_length=1)
    timestamp: datetime

    @model_validator(mode="after")
    def validate_record(self) -> "ReleaseDecisionRecord":
        for label, values in (
            ("exceptionPolicyRefs", self.exception_policy_refs),
            ("blockingCheckRefs", self.blocking_check_refs),
            ("warningCheckRefs", self.warning_check_refs),
            ("advisoryCheckRefs", self.advisory_check_refs),
            ("evalResultRefs", self.eval_result_refs),
        ):
            if len(set(values)) != len(values):
                raise ValueError(f"{label} must be unique")
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        if self.strategy == "policy-auto" and self.approval_ref is not None:
            raise ValueError("policy-auto release decisions must not carry approvalRef")
        if self.strategy == "human-required" and self.result == "released" and self.approval_ref is None:
            raise ValueError("released human-required decisions require approvalRef")
        if self.result == "pending-approval" and self.strategy != "human-required":
            raise ValueError("pending-approval is only valid for human-required strategy")
        return self
