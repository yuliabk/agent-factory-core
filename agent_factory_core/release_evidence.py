from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence

from .contracts.effective_release_config import EffectiveReleaseConfig
from .contracts.evidence_pack import EvidencePack
from .contracts.human_approval_record import HumanApprovalRecord
from .contracts.release_decision_record import ReleaseDecisionRecord
from .eval_policy import EvalGateSummary
from .release_kernel import decide_release_action


class ReleaseEvidenceError(ValueError):
    pass


def _platform_policy_ref(release: EffectiveReleaseConfig) -> str:
    return (
        f"{release.policy.platform_policy_name}@"
        f"{release.policy.platform_policy_version}"
    )


def _same_refs(left: Sequence[str], right: Sequence[str]) -> bool:
    return len(left) == len(right) and set(left) == set(right)


def validate_human_approval(
    release: EffectiveReleaseConfig,
    approval: HumanApprovalRecord,
    *,
    now: datetime,
) -> None:
    if now.tzinfo is None:
        raise ReleaseEvidenceError("approval validation time must be timezone-aware")
    if approval.release_id != release.metadata.release_id:
        raise ReleaseEvidenceError("approval releaseId does not match EffectiveReleaseConfig")
    if approval.platform_policy_ref != _platform_policy_ref(release):
        raise ReleaseEvidenceError("approval platformPolicyRef does not match effective release policy")
    if not _same_refs(
        approval.exception_policy_refs,
        release.policy.exception_policy_refs,
    ):
        raise ReleaseEvidenceError("approval exceptionPolicyRefs do not match effective release")
    if approval.timestamp > now:
        raise ReleaseEvidenceError("approval timestamp is in the future")
    if now >= approval.expires_at:
        raise ReleaseEvidenceError("approval is expired")


def build_release_decision_record(
    release: EffectiveReleaseConfig,
    gate: EvalGateSummary,
    *,
    release_decision_id: str,
    approval: HumanApprovalRecord | None = None,
    timestamp: datetime | None = None,
) -> ReleaseDecisionRecord:
    current_time = timestamp or datetime.now(timezone.utc)
    if current_time.tzinfo is None:
        raise ReleaseEvidenceError("release decision timestamp must be timezone-aware")
    if not gate.mapped:
        raise ReleaseEvidenceError("release decision requires at least one mapped EvalResult")

    action = decide_release_action(release, gate)
    approval_ref: str | None = None

    if action.action == "block":
        if approval is not None:
            raise ReleaseEvidenceError("approval is not applicable to an eval-blocked release")
        result = "blocked"
        reason = action.reason
    elif action.action == "auto-release":
        if approval is not None:
            raise ReleaseEvidenceError("policy-auto release must not depend on human approval")
        result = "released"
        reason = action.reason
    else:
        if approval is None:
            result = "pending-approval"
            reason = action.reason
        else:
            validate_human_approval(release, approval, now=current_time)
            approval_ref = approval.approval_id
            if approval.decision == "approve":
                result = "released"
                reason = "valid human approval authorizes the exact release"
            else:
                result = "blocked"
                reason = "human approver rejected the exact release"

    return ReleaseDecisionRecord(
        apiVersion="agentfactory.io/v1alpha1",
        kind="ReleaseDecisionRecord",
        releaseDecisionId=release_decision_id,
        releaseId=release.metadata.release_id,
        platformPolicyRef=_platform_policy_ref(release),
        exceptionPolicyRefs=release.policy.exception_policy_refs,
        strategy=release.spec.release_strategy,
        result=result,
        blockingCheckRefs=gate.blocking_failures,
        warningCheckRefs=gate.warnings,
        advisoryCheckRefs=gate.advisories,
        evalResultRefs=tuple(item.eval_id for item in gate.mapped),
        approvalRef=approval_ref,
        reason=reason,
        timestamp=current_time,
    )


def build_evidence_pack(
    release: EffectiveReleaseConfig,
    decision: ReleaseDecisionRecord,
    *,
    evidence_pack_id: str,
    spec_ref: str,
    agent_manifest_ref: str,
    client_instance_config_ref: str,
    effective_release_config_ref: str,
    template_module_refs: Sequence[str],
    config_diff_ref: str,
    capability_tool_contract_refs: Sequence[str] = (),
    known_limitations: Sequence[str] = (),
    rollback_ref: str | None = None,
    created_at: datetime | None = None,
) -> EvidencePack:
    if decision.release_id != release.metadata.release_id:
        raise ReleaseEvidenceError("release decision does not belong to EffectiveReleaseConfig")
    if decision.platform_policy_ref != _platform_policy_ref(release):
        raise ReleaseEvidenceError("release decision policy reference does not match effective release")
    if not _same_refs(
        decision.exception_policy_refs,
        release.policy.exception_policy_refs,
    ):
        raise ReleaseEvidenceError("release decision exception refs do not match effective release")

    timestamp = created_at or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        raise ReleaseEvidenceError("EvidencePack createdAt must be timezone-aware")

    return EvidencePack(
        apiVersion="agentfactory.io/v1alpha1",
        kind="EvidencePack",
        evidencePackId=evidence_pack_id,
        releaseId=release.metadata.release_id,
        specRef=spec_ref,
        agentManifestRef=agent_manifest_ref,
        clientInstanceConfigRef=client_instance_config_ref,
        effectiveReleaseConfigRef=effective_release_config_ref,
        platformPolicyRef=_platform_policy_ref(release),
        exceptionPolicyRefs=release.policy.exception_policy_refs,
        templateModuleRefs=tuple(template_module_refs),
        configDiffRef=config_diff_ref,
        providerProfile=release.spec.provider_profile,
        capabilityToolContractRefs=tuple(capability_tool_contract_refs),
        evalResultRefs=decision.eval_result_refs,
        releaseDecisionRef=decision.release_decision_id,
        knownLimitations=tuple(known_limitations),
        rollbackRef=rollback_ref,
        createdAt=timestamp,
    )
