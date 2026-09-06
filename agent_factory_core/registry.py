from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field

from .contracts.agent_manifest import RequiredCapabilityRef


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class CapabilityImplementation(StrictModel):
    id: str = Field(min_length=1)
    environments: list[str] = Field(default_factory=list)
    enabled: bool = True


class CapabilityRecord(StrictModel):
    ref: str = Field(min_length=1)
    version: str = Field(min_length=1)
    environments: list[str] = Field(default_factory=list)
    required_permissions: list[str] = Field(alias="requiredPermissions", default_factory=list)
    overrideable: dict[str, list[Any]] = Field(default_factory=dict)
    implementations: list[CapabilityImplementation] = Field(default_factory=list)


@dataclass(frozen=True)
class ResolvedCapability:
    ref: str
    version: str
    implementation_id: str
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
            required_permissions=tuple(record.required_permissions),
            overrides=dict(requirement.overrides),
        )
