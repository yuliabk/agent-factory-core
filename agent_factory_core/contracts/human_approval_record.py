from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


NonEmptyString = Annotated[str, Field(min_length=1)]


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class HumanApprovalRecord(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["HumanApprovalRecord"]
    approval_id: str = Field(alias="approvalId", min_length=1)
    approver_id: str = Field(alias="approverId", min_length=1)
    approver_role: str = Field(alias="approverRole", min_length=1)
    scope: Literal["release"]
    release_id: str = Field(alias="releaseId", min_length=1)
    platform_policy_ref: str = Field(alias="platformPolicyRef", min_length=1)
    exception_policy_refs: tuple[NonEmptyString, ...] = Field(alias="exceptionPolicyRefs")
    decision: Literal["approve", "reject"]
    timestamp: datetime
    expires_at: datetime = Field(alias="expiresAt")
    comment: str | None

    @model_validator(mode="after")
    def validate_record(self) -> "HumanApprovalRecord":
        if len(set(self.exception_policy_refs)) != len(self.exception_policy_refs):
            raise ValueError("exceptionPolicyRefs must be unique")
        if self.timestamp.tzinfo is None or self.expires_at.tzinfo is None:
            raise ValueError("timestamp and expiresAt must be timezone-aware")
        if self.expires_at <= self.timestamp:
            raise ValueError("expiresAt must be after timestamp")
        return self
