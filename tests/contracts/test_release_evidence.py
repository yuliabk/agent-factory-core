import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from pydantic import ValidationError as PydanticValidationError

from agent_factory_core.contracts import (
    EffectiveReleaseConfig,
    EvidencePack,
    HumanApprovalRecord,
    ReleaseDecisionRecord,
)
from agent_factory_core.eval_policy import EvalGateSummary, MappedEvalResult
from agent_factory_core.provenance import effective_release_fingerprint
from agent_factory_core.release_evidence import (
    ReleaseEvidenceError,
    build_evidence_pack,
    build_release_decision_record,
)


ROOT = Path(__file__).resolve().parents[2]


def release(strategy: str = "policy-auto", *, release_id: str = "release-1") -> EffectiveReleaseConfig:
    return EffectiveReleaseConfig.model_validate(
        {
            "apiVersion": "agentfactory.io/v1alpha1",
            "kind": "EffectiveReleaseConfig",
            "metadata": {"releaseId": release_id, "environment": "sandbox"},
            "policy": {
                "platformPolicyName": "platform-default",
                "platformPolicyVersion": "1",
                "exceptionPolicyRefs": ["exception-a@1"],
            },
            "spec": {
                "agentRef": {"name": "synthetic-agent", "version": "0.1.0"},
                "tenant": {"id": "tenant-a"},
                "variables": {},
                "capabilities": {"provides": [], "requires": []},
                "capabilityBindings": {},
                "trustProfile": "internal",
                "releaseStrategy": strategy,
                "providerProfile": "balanced",
                "secretsRef": {},
                "memoryConfig": {},
                "budgetConfig": {},
                "permissions": [],
                "dataClassification": "internal",
                "toolBindings": {},
                "evalProfile": "standard-agent",
            },
        }
    )


def gate(*, eligible: bool = True, release_id: str = "release-1") -> EvalGateSummary:
    mapped = MappedEvalResult(
        eval_id="eval-security-1",
        check_id="security.cross-tenant",
        status="PASS" if eligible else "FAIL",
        classification="blocking",
        effect="pass" if eligible else "block",
    )
    return EvalGateSummary(
        release_id=release_id,
        eligible=eligible,
        mapped=(mapped,),
        blocking_failures=() if eligible else ("security.cross-tenant",),
        warnings=("business.quality",) if eligible else (),
        advisories=(),
    )


def approval(
    *,
    decision: str = "approve",
    release_id: str = "release-1",
    policy_ref: str = "platform-default@1",
    exception_refs=("exception-a@1",),
    timestamp: datetime | None = None,
    expires_at: datetime | None = None,
) -> HumanApprovalRecord:
    approved_at = timestamp or datetime.now(timezone.utc)
    expiry = expires_at or approved_at + timedelta(hours=1)
    return HumanApprovalRecord.model_validate(
        {
            "apiVersion": "agentfactory.io/v1alpha1",
            "kind": "HumanApprovalRecord",
            "approvalId": "approval-1",
            "approverId": "owner-1",
            "approverRole": "platform-owner",
            "scope": "release",
            "releaseId": release_id,
            "platformPolicyRef": policy_ref,
            "exceptionPolicyRefs": list(exception_refs),
            "decision": decision,
            "timestamp": approved_at.isoformat(),
            "expiresAt": expiry.isoformat(),
            "comment": "synthetic approval",
        }
    )


class ReleaseEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.approval_schema = json.loads(
            (ROOT / "schemas/human-approval-record.schema.json").read_text(encoding="utf-8")
        )
        cls.decision_schema = json.loads(
            (ROOT / "schemas/release-decision-record.schema.json").read_text(encoding="utf-8")
        )
        cls.evidence_schema = json.loads(
            (ROOT / "schemas/evidence-pack.schema.json").read_text(encoding="utf-8")
        )

    def test_auto_release_creates_released_decision_without_approval(self) -> None:
        decision = build_release_decision_record(
            release(),
            gate(),
            release_decision_id="decision-auto-1",
        )
        self.assertEqual(decision.result, "released")
        self.assertEqual(decision.strategy, "policy-auto")
        self.assertIsNone(decision.approval_ref)
        Draft202012Validator(self.decision_schema).validate(
            decision.model_dump(by_alias=True, mode="json")
        )

    def test_human_required_without_approval_is_pending(self) -> None:
        decision = build_release_decision_record(
            release("human-required"),
            gate(),
            release_decision_id="decision-human-pending",
        )
        self.assertEqual(decision.result, "pending-approval")
        self.assertIsNone(decision.approval_ref)

    def test_valid_human_approval_releases_exact_release(self) -> None:
        now = datetime.now(timezone.utc)
        approved = approval(timestamp=now - timedelta(minutes=1), expires_at=now + timedelta(hours=1))
        decision = build_release_decision_record(
            release("human-required"),
            gate(),
            release_decision_id="decision-human-approved",
            approval=approved,
            timestamp=now,
        )
        self.assertEqual(decision.result, "released")
        self.assertEqual(decision.approval_ref, "approval-1")
        Draft202012Validator(self.approval_schema).validate(
            approved.model_dump(by_alias=True, mode="json")
        )

    def test_human_rejection_blocks_release(self) -> None:
        now = datetime.now(timezone.utc)
        rejected = approval(
            decision="reject",
            timestamp=now - timedelta(minutes=1),
            expires_at=now + timedelta(hours=1),
        )
        decision = build_release_decision_record(
            release("human-required"),
            gate(),
            release_decision_id="decision-human-rejected",
            approval=rejected,
            timestamp=now,
        )
        self.assertEqual(decision.result, "blocked")
        self.assertEqual(decision.approval_ref, "approval-1")

    def test_expired_or_mismatched_approval_is_rejected(self) -> None:
        now = datetime.now(timezone.utc)
        expired = approval(
            timestamp=now - timedelta(hours=2),
            expires_at=now - timedelta(hours=1),
        )
        with self.assertRaises(ReleaseEvidenceError):
            build_release_decision_record(
                release("human-required"),
                gate(),
                release_decision_id="decision-expired",
                approval=expired,
                timestamp=now,
            )

        for bad in (
            approval(release_id="other-release"),
            approval(policy_ref="other-policy@1"),
            approval(exception_refs=()),
        ):
            with self.assertRaises(ReleaseEvidenceError):
                build_release_decision_record(
                    release("human-required"),
                    gate(),
                    release_decision_id="decision-mismatch",
                    approval=bad,
                    timestamp=datetime.now(timezone.utc),
                )

    def test_blocking_eval_failure_cannot_be_overridden_by_approval(self) -> None:
        decision = build_release_decision_record(
            release("human-required"),
            gate(eligible=False),
            release_decision_id="decision-blocked",
        )
        self.assertEqual(decision.result, "blocked")
        self.assertEqual(decision.blocking_check_refs, ("security.cross-tenant",))

        with self.assertRaises(ReleaseEvidenceError):
            build_release_decision_record(
                release("human-required"),
                gate(eligible=False),
                release_decision_id="decision-blocked-with-approval",
                approval=approval(),
            )

    def test_evidence_pack_links_exact_release_decision_and_eval_refs(self) -> None:
        rel = release()
        decision = build_release_decision_record(
            rel,
            gate(),
            release_decision_id="decision-auto-1",
        )
        pack = build_evidence_pack(
            rel,
            decision,
            evidence_pack_id="evidence-1",
            spec_ref="spec://core-contracts/synthetic-agent@1",
            agent_manifest_ref="artifact://agent-manifest/synthetic-agent@0.1.0",
            client_instance_config_ref="artifact://client/tenant-a/synthetic-agent",
            template_module_refs=("template://general-agent@1",),
            config_diff_ref="artifact://diff/release-1",
            capability_tool_contract_refs=("contract://tool/synthetic.lookup@1",),
            known_limitations=("synthetic adapters only",),
            rollback_ref="release://previous",
        )
        self.assertEqual(pack.release_id, "release-1")
        self.assertEqual(pack.eval_result_refs, ("eval-security-1",))
        self.assertEqual(pack.release_decision_ref, "decision-auto-1")
        self.assertEqual(pack.provider_profile, "balanced")
        self.assertEqual(pack.effective_release_config_ref, effective_release_fingerprint(rel))
        Draft202012Validator(self.evidence_schema).validate(
            pack.model_dump(by_alias=True, mode="json")
        )

    def test_evidence_pack_rejects_decision_from_other_release(self) -> None:
        other_decision = build_release_decision_record(
            release(release_id="release-other"),
            gate(release_id="release-other"),
            release_decision_id="decision-other",
        )
        with self.assertRaises(ReleaseEvidenceError):
            build_evidence_pack(
                release(),
                other_decision,
                evidence_pack_id="evidence-bad",
                spec_ref="spec://one",
                agent_manifest_ref="artifact://manifest",
                client_instance_config_ref="artifact://client",
                template_module_refs=("template://one",),
                config_diff_ref="artifact://diff",
            )

    def test_contract_shapes_stay_aligned_and_reject_sensitive_extras(self) -> None:
        for schema, model in (
            (self.approval_schema, HumanApprovalRecord),
            (self.decision_schema, ReleaseDecisionRecord),
            (self.evidence_schema, EvidencePack),
        ):
            generated = model.model_json_schema(by_alias=True)
            self.assertEqual(set(schema["required"]), set(generated["required"]))
            self.assertEqual(set(schema["properties"]), set(generated["properties"]))

        decision = build_release_decision_record(
            release(), gate(), release_decision_id="decision-extra"
        ).model_dump(by_alias=True, mode="json")
        decision["prompt"] = "secret raw prompt"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.decision_schema).validate(decision)
        with self.assertRaises(PydanticValidationError):
            ReleaseDecisionRecord.model_validate(decision)

        bad_pack = build_evidence_pack(
            release(),
            build_release_decision_record(release(), gate(), release_decision_id="decision-fp"),
            evidence_pack_id="evidence-fp",
            spec_ref="spec://one",
            agent_manifest_ref="artifact://manifest",
            client_instance_config_ref="artifact://client",
            template_module_refs=("template://one",),
            config_diff_ref="artifact://diff",
        ).model_dump(by_alias=True, mode="json")
        bad_pack["effectiveReleaseConfigRef"] = "artifact://not-a-fingerprint"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.evidence_schema).validate(bad_pack)
        with self.assertRaises(PydanticValidationError):
            EvidencePack.model_validate(bad_pack)


if __name__ == "__main__":
    unittest.main()
