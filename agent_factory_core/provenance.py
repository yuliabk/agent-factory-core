from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .contracts.effective_release_config import EffectiveReleaseConfig
from .contracts.evidence_pack import EvidencePack
from .contracts.execution_context import ExecutionContext


@dataclass(frozen=True)
class DriftCheckResult:
    managed: bool
    release_fingerprint: str
    approved_spec_ref: str
    mismatches: tuple[str, ...]


def effective_release_fingerprint(release: EffectiveReleaseConfig) -> str:
    payload = json.dumps(
        release.model_dump(by_alias=True, mode="json"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _policy_ref(release: EffectiveReleaseConfig) -> str:
    return f"{release.policy.platform_policy_name}@{release.policy.platform_policy_version}"


def _same_refs(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    return len(left) == len(right) and set(left) == set(right)


def check_release_drift(
    release: EffectiveReleaseConfig,
    context: ExecutionContext,
    evidence_pack: EvidencePack,
    *,
    approved_spec_ref: str,
) -> DriftCheckResult:
    fingerprint = effective_release_fingerprint(release)
    mismatches: list[str] = []

    if evidence_pack.release_id != release.metadata.release_id:
        mismatches.append("evidence.releaseId")
    if evidence_pack.spec_ref != approved_spec_ref:
        mismatches.append("evidence.specRef")
    if evidence_pack.effective_release_config_ref != fingerprint:
        mismatches.append("evidence.effectiveReleaseConfigRef")
    if evidence_pack.platform_policy_ref != _policy_ref(release):
        mismatches.append("evidence.platformPolicyRef")
    if not _same_refs(
        evidence_pack.exception_policy_refs,
        release.policy.exception_policy_refs,
    ):
        mismatches.append("evidence.exceptionPolicyRefs")
    if evidence_pack.provider_profile != release.spec.provider_profile:
        mismatches.append("evidence.providerProfile")

    checks = (
        ("runtime.agentReleaseId", context.agent_release_id, release.metadata.release_id),
        ("runtime.environment", context.environment, release.metadata.environment),
        ("runtime.agentId", context.agent_id, release.spec.agent_ref.name),
        ("runtime.tenantId", context.tenant_id, release.spec.tenant.id),
        ("runtime.trustProfile", context.trust_profile, release.spec.trust_profile),
        ("runtime.permissions", context.permissions, release.spec.permissions),
        (
            "runtime.dataClassification",
            context.data_classification,
            release.spec.data_classification,
        ),
        (
            "runtime.capabilityBindings",
            context.capability_bindings,
            release.spec.capability_bindings,
        ),
        ("runtime.providerProfile", context.provider_profile, release.spec.provider_profile),
        ("runtime.toolBindings", context.tool_bindings, release.spec.tool_bindings),
        ("runtime.memoryConfig", context.memory_config, release.spec.memory_config),
        ("runtime.budgetConfig", context.budget_config, release.spec.budget_config),
    )
    for field, observed, expected in checks:
        if observed != expected:
            mismatches.append(field)

    return DriftCheckResult(
        managed=not mismatches,
        release_fingerprint=fingerprint,
        approved_spec_ref=approved_spec_ref,
        mismatches=tuple(mismatches),
    )
