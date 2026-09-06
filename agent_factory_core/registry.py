from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any, Iterable

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .contracts.agent_manifest import RequiredCapabilityRef


NonEmptyString = Annotated[str, Field(min_length=1)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class CapabilityImplementation(StrictModel):
    id: str = Field(min_length=1)
    environments: list[NonEmptyString] = Field(default_factory=list)
    enabled: bool = True

    @model_validator(mode="after")
    def validate_environments(self) -> "CapabilityImplementation":
        if len(set(self.environments)) != len(self.environments):
            raise ValueError("environments must be unique")
        return self


class CapabilityRecord(StrictModel):
    ref: str = Field(min_length=1)
    version: str = Field(min_length=1)
    input_schema_ref: str = Field(alias="inputSchemaRef", min_length=1)
    output_schema_ref: str = Field(alias="outputSchemaRef", min_length=1)
    risk_class: str = Field(alias="riskClass", min_length=1)
    cost_class: str = Field(alias="costClass", min_length=1)
    allowed_data_classifications: list[NonEmptyString] = Field(
        alias="allowedDataClassifications",
        min_length=1,
    )
    environments: list[NonEmptyString] = Field(default_factory=list)
    required_permissions: list[NonEmptyString] = Field(
        alias="requiredPermissions",
        default_factory=list,
    )
    overrideable: dict[str, list[Any]] = Field(default_factory=dict)
    implementations: list[CapabilityImplementation] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_metadata(self) -> "CapabilityRecord":
        for label, values in (
            ("allowedDataClassifications", self.allowed_data_classifications),
            ("environments", self.environments),
            ("requiredPermissions", self.required_permissions),
        ):
            if len(set(values)) != len(values):
                raise ValueError(f"{label} must be unique")
        implementation_ids = [item.id for item in self.implementations]
        if len(set(implementation_ids)) != len(implementation_ids):
            raise ValueError("implementation ids must be unique")
        return self


@dataclass(frozen=True)
class ResolvedCapability:
    ref: str
    version: str
    implementation_id: str
    input_schema_ref: str
    output_schema_ref: str
    risk_class: str
    cost_class: str
    allowed_data_classifications: tuple[str, ...]
    required_permissions: tuple[str, ...]
    overrides: dict[str, Any]


class CapabilityResolutionError(ValueError):
    pass


class CapabilityRegistry:
    def __init__(self, records: Iterable[CapabilityRecord] = ()) -> None:
        self._records = {(r.ref, r.version): r for r in records}

    def register(self, record: CapabilityRecord) -> None:
        self._records[(record.ref, record.version)] = record

    def resolve_required(
        self,
        requirement: RequiredCapabilityRef,
        *,
        environment: str,
        mode: str,
    ) -> ResolvedCapability | None:
        record = self._records.get((requirement.ref, requirement.version))
        if record is None:
            if requirement.optional and mode == "soft":
                return None
            raise CapabilityResolutionError(
                f"No registry record for {requirement.ref}@{requirement.version}"
            )

        if record.environments and environment not in record.environments:
            if requirement.optional and mode == "soft":
                return None
            raise CapabilityResolutionError(
                f"{requirement.ref}@{requirement.version} is not enabled for {environment}"
            )

        unknown = set(requirement.overrides) - set(record.overrideable)
        if unknown:
            raise CapabilityResolutionError(
                f"Non-overrideable keys for {requirement.ref}: {', '.join(sorted(unknown))}"
            )
        for key, value in requirement.overrides.items():
            allowed = record.overrideable.get(key, [])
            if allowed and value not in allowed:
                raise CapabilityResolutionError(
                    f"Override {key}={value!r} is not allowed for {requirement.ref}"
                )

        implementation = next(
            (
                item
                for item in record.implementations
                if item.enabled and (not item.environments or environment in item.environments)
            ),
            None,
        )
        if implementation is None:
            if requirement.optional and mode == "soft":
                return None
            raise CapabilityResolutionError(
                f"No enabled implementation for {requirement.ref}@{requirement.version} in {environment}"
            )

        return ResolvedCapability(
            ref=requirement.ref,
            version=requirement.version,
            implementation_id=implementation.id,
            input_schema_ref=record.input_schema_ref,
            output_schema_ref=record.output_schema_ref,
            risk_class=record.risk_class,
            cost_class=record.cost_class,
            allowed_data_classifications=tuple(record.allowed_data_classifications),
            required_permissions=tuple(record.required_permissions),
            overrides=dict(requirement.overrides),
        )
