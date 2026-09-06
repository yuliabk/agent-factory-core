import unittest
from datetime import datetime, timezone

from agent_factory_core.contracts import EvalResult, PlatformPolicy
from agent_factory_core.eval_policy import EvalPolicyError, map_eval_results


def policy(*, rules=None, invariants=None) -> PlatformPolicy:
    default_rules = [
        {"checkId": "security.cross-tenant", "classification": "blocking"},
        {"checkId": "business.quality", "classification": "warning"},
        {"checkId": "contract.portability", "classification": "advisory"},
    ]
    return PlatformPolicy.model_validate(
        {
            "apiVersion": "agentfactory.io/v1alpha1",
            "kind": "PlatformPolicy",
            "metadata": {"name": "platform-default", "version": "1"},
            "spec": {
                "allowedPermissions": [],
                "deniedPermissions": [],
                "allowedProviderProfiles": ["balanced"],
                "allowedBudgetOverrideKeys": [],
                "allowedMemoryConfigKeys": [],
                "maxTrustProfile": "business",
                "minimumReleaseStrategy": "policy-auto",
                "registryMode": "strict",
                "defaultDataClassification": "internal",
                "evalRules": rules if rules is not None else default_rules,
                "securityInvariantChecks": invariants
                if invariants is not None
                else ["security.cross-tenant"],
                "exceptionAllowances": {
                    "permissions": [],
                    "providerProfiles": [],
                    "budgetOverrideKeys": [],
                    "memoryConfigKeys": [],
                },
            },
        }
    )


def result(
    check_id: str,
    *,
    family: str,
    status: str,
    release_id: str = "release-1",
) -> EvalResult:
    return EvalResult.model_validate(
        {
            "apiVersion": "agentfactory.io/v1alpha1",
            "kind": "EvalResult",
            "evalId": f"eval:{check_id}:{status}",
            "releaseId": release_id,
            "checkId": check_id,
            "checkVersion": "1",
            "family": family,
            "status": status,
            "summary": "synthetic eval",
            "metrics": {},
            "evidenceRefs": [],
            "observedAt": datetime.now(timezone.utc).isoformat(),
        }
    )


class EvalPolicyMappingTests(unittest.TestCase):
    def test_blocking_failure_makes_release_ineligible(self) -> None:
        summary = map_eval_results(
            [result("security.cross-tenant", family="security_policy", status="FAIL")],
            policy(),
        )
        self.assertFalse(summary.eligible)
        self.assertEqual(summary.blocking_failures, ("security.cross-tenant",))
        self.assertEqual(summary.mapped[0].effect, "block")

    def test_warning_and_advisory_failures_do_not_block(self) -> None:
        summary = map_eval_results(
            [
                result("business.quality", family="functional_business", status="FAIL"),
                result("contract.portability", family="contract_portability", status="FAIL"),
            ],
            policy(),
        )
        self.assertTrue(summary.eligible)
        self.assertEqual(summary.warnings, ("business.quality",))
        self.assertEqual(summary.advisories, ("contract.portability",))

    def test_pass_with_warnings_on_blocking_check_warns_but_does_not_block(self) -> None:
        summary = map_eval_results(
            [
                result(
                    "security.cross-tenant",
                    family="security_policy",
                    status="PASS_WITH_WARNINGS",
                )
            ],
            policy(),
        )
        self.assertTrue(summary.eligible)
        self.assertEqual(summary.warnings, ("security.cross-tenant",))
        self.assertEqual(summary.blocking_failures, ())

    def test_unmapped_check_fails_closed(self) -> None:
        with self.assertRaises(EvalPolicyError):
            map_eval_results(
                [result("cost.unmapped", family="cost_runtime", status="PASS")],
                policy(),
            )

    def test_duplicate_rule_ids_fail_closed(self) -> None:
        duplicate_policy = policy(
            rules=[
                {"checkId": "business.quality", "classification": "warning"},
                {"checkId": "business.quality", "classification": "advisory"},
            ],
            invariants=[],
        )
        with self.assertRaises(EvalPolicyError):
            map_eval_results(
                [result("business.quality", family="functional_business", status="PASS")],
                duplicate_policy,
            )

    def test_security_invariant_cannot_be_downgraded(self) -> None:
        downgraded = policy(
            rules=[{"checkId": "security.cross-tenant", "classification": "warning"}],
            invariants=["security.cross-tenant"],
        )
        with self.assertRaises(EvalPolicyError):
            map_eval_results(
                [result("security.cross-tenant", family="security_policy", status="PASS")],
                downgraded,
            )

    def test_security_invariant_must_be_mapped_and_use_security_family(self) -> None:
        missing = policy(rules=[], invariants=["security.cross-tenant"])
        with self.assertRaises(EvalPolicyError):
            map_eval_results(
                [result("business.quality", family="functional_business", status="PASS")],
                missing,
            )

        with self.assertRaises(EvalPolicyError):
            map_eval_results(
                [result("security.cross-tenant", family="functional_business", status="PASS")],
                policy(),
            )

    def test_mixed_release_ids_are_rejected(self) -> None:
        with self.assertRaises(EvalPolicyError):
            map_eval_results(
                [
                    result("business.quality", family="functional_business", status="PASS", release_id="r1"),
                    result("contract.portability", family="contract_portability", status="PASS", release_id="r2"),
                ],
                policy(),
            )


if __name__ == "__main__":
    unittest.main()
