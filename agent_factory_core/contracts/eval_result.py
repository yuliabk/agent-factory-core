from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


NonEmptyString = Annotated[str, Field(min_length=1)]
EvalFamily = Literal[
    "functional_business",
    "security_policy",
    "cost_runtime",
    "contract_portability",
]
EvalStatus = Literal["PASS", "PASS_WITH_WARNINGS", "FAIL"]
MetricValue = str | int | float | bool | None


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, frozen=True)


class EvalResult(FrozenModel):
    api_version: Literal["agentfactory.io/v1alpha1"] = Field(alias="apiVersion")
    kind: Literal["EvalResult"]
    eval_id: str = Field(alias="evalId", min_length=1)
    release_id: str = Field(alias="releaseId", min_length=1)
    check_id: str = Field(alias="checkId", min_length=1)
    check_version: str = Field(alias="checkVersion", min_length=1)
    family: EvalFamily
    status: EvalStatus
    summary: str = Field(min_length=1)
    metrics: dict[str, MetricValue]
    evidence_refs: tuple[NonEmptyString, ...] = Field(alias="evidenceRefs")
    observed_at: datetime = Field(alias="observedAt")

    @model_validator(mode="after")
    def validate_evidence_refs(self) -> "EvalResult":
        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ValueError("evidenceRefs must be unique")
        return self
