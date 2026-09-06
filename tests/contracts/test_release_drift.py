import unittest
from datetime import datetime, timedelta, timezone

from agent_factory_core.contracts import EffectiveReleaseConfig, build_execution_context
from agent_factory_core.eval_policy import EvalGateSummary, MappedEvalResult
from agent_factory_core.provenance import check_release_drift, effective_release_fingerprint
from agent_factory_core.release_evidence import build_evidence_pack, build_release_decision_record


def release(*, provider_profile: str = "balanced", release_id: str = "release-1") -> EffectiveReleaseConfig:
    return EffectiveReleaseConfig.model_validate(
        {
            "apiVersion": "agentfactory.io/v1alpha1",
            "kind": "EffectiveReleaseConfig",
            "metadata": {"releaseId": release_id, "environment": "sandbox"},
            "policy": {
                "platformPolicyName": "platform-default",
                "platformPolicyVersion": "1",
                "exceptionPolicyRefs": [],
            },
            "spec": {
                "agentRef": {"name": "synthetic-agent", "version": "0.1.0"},
                "tenant": {"id": "tenant-a"},
                "variables": {},
                "capabilities": {"provides": [], "requires": []},
                "capabilityBindings": {"synthetic.lookup": "cap.synthetic.lookup.v1"},
                "trustProfile": "internal",
                "releaseStrategy": "policy-auto",
                "providerProfile": provider_profile,
                "secretsRef": {},
                "memoryConfig": {"readEnabled": True},
                "budgetConfig": {"monthlyLimit": 10},
                "permissions": ["model.invoke", "synthetic.lookup"],
                "dataClassification": "internal",
                "toolBindings": {"synthetic.lookup": "tool.synthetic.lookup.v1"},
                "evalProfile": "standard-agent",
            },
        }
    )


def gate(release_id: str = "release-1") -> EvalGateSummary:
    return EvalGateSummary(
        release_id=release_id,
        eligible=True,
        mapped=(
            MappedEvalResult(
                eval_id="eval-1",
                check_id="security.synthetic",
                status="PASS",
                classification="blocking",
                effect="pass",
            ),
        ),
        blocking_failures=(),
        warnings=(),
        advisories=(),
    )


def evidence(rel: EffectiveReleaseConfig, *, spec_ref: str = "spec://approved/synthetic@1"):
    decision = build_release_decision_record(
        rel,
        gate(rel.metadata.release_id),
        release_decision_id="decision-1",
    )
    return build_evidence_pack(
        rel,
        decision,
        evidence_pack_id="evidence-1",
        spec_ref=spec_ref,
        agent_manifest_ref="artifact://manifest/synthetic@0.1.0",
        client_instance_config_ref="artifact://client/tenant-a",
        template_module_refs=("template://general-agent@1",),
        config_diff_ref="artifact://diff/release-1",
        capability_tool_contract_refs=("contract://synthetic.lookup@1",),
    )


def context(rel: EffectiveReleaseConfig):
    return build_execution_context(
        rel,
        request_id="req-1",
        trace_id="trace-1",
        actor_id="user-1",
        actor_type="user",
        deadline=datetime.now(timezone.utc) + timedelta(minutes=5),
    )


class ReleaseDriftTests(unittest.TestCase):
    def test_exact_release_context_and_approved_spec_are_managed(self) -> None:
        rel = release()
        result = check_release_drift(
            rel,
            context(rel),
            evidence(rel),
            approved_spec_ref="spec://approved/synthetic@1",
        )
        self.assertTrue(result.managed)
        self.assertEqual(result.mismatches, ())
        self.assertEqual(result.release_fingerprint, effective_release_fingerprint(rel))

    def test_material_release_change_changes_fingerprint(self) -> None:
        balanced = release(provider_profile="balanced")
        premium = release(provider_profile="premium")
        self.assertNotEqual(
            effective_release_fingerprint(balanced),
            effective_release_fingerprint(premium),
        )
        self.assertEqual(
            effective_release_fingerprint(balanced),
            effective_release_fingerprint(balanced),
        )

    def test_tampered_runtime_context_is_flagged(self) -> None:
        rel = release()
        ctx = context(rel).model_copy(
            update={
                "tenant_id": "tenant-b",
                "provider_profile": "premium",
                "permissions": ("model.invoke", "admin.write"),
            }
        )
        result = check_release_drift(
            rel,
            ctx,
            evidence(rel),
            approved_spec_ref="spec://approved/synthetic@1",
        )
        self.assertFalse(result.managed)
        self.assertIn("runtime.tenantId", result.mismatches)
        self.assertIn("runtime.providerProfile", result.mismatches)
        self.assertIn("runtime.permissions", result.mismatches)

    def test_wrong_spec_or_release_fingerprint_is_flagged(self) -> None:
        rel = release()
        pack = evidence(rel)
        wrong_fingerprint = pack.model_copy(
            update={"effective_release_config_ref": "sha256:" + "0" * 64}
        )
        result = check_release_drift(
            rel,
            context(rel),
            wrong_fingerprint,
            approved_spec_ref="spec://approved/other@1",
        )
        self.assertFalse(result.managed)
        self.assertIn("evidence.specRef", result.mismatches)
        self.assertIn("evidence.effectiveReleaseConfigRef", result.mismatches)

    def test_evidence_from_another_release_is_flagged(self) -> None:
        rel = release()
        other = release(release_id="release-other")
        result = check_release_drift(
            rel,
            context(rel),
            evidence(other),
            approved_spec_ref="spec://approved/synthetic@1",
        )
        self.assertFalse(result.managed)
        self.assertIn("evidence.releaseId", result.mismatches)
        self.assertIn("evidence.effectiveReleaseConfigRef", result.mismatches)


if __name__ == "__main__":
    unittest.main()
