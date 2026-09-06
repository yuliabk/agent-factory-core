import unittest

from agent_factory_core.contracts import EffectiveReleaseConfig
from agent_factory_core.contracts.release_strategy import resolve_release_strategy
from agent_factory_core.eval_policy import EvalGateSummary
from agent_factory_core.release_kernel import ReleaseStrategyError, decide_release_action


def release(strategy: str, *, release_id: str = "release-1") -> EffectiveReleaseConfig:
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


def gate(*, eligible: bool, release_id: str = "release-1") -> EvalGateSummary:
    return EvalGateSummary(
        release_id=release_id,
        eligible=eligible,
        mapped=(),
        blocking_failures=() if eligible else ("security.blocking",),
        warnings=(),
        advisories=(),
    )


class ReleaseStrategyTests(unittest.TestCase):
    def test_requested_strategy_resolves_without_weakening(self) -> None:
        self.assertEqual(resolve_release_strategy("policy-auto", "policy-auto"), "policy-auto")
        self.assertEqual(resolve_release_strategy("policy-auto", "human-required"), "human-required")
        self.assertEqual(resolve_release_strategy("human-required", "policy-auto"), "human-required")
        self.assertEqual(resolve_release_strategy("human-required", "human-required"), "human-required")
        self.assertEqual(resolve_release_strategy("policy", "policy-auto"), "policy-auto")
        self.assertEqual(resolve_release_strategy("policy", "human-required"), "human-required")

    def test_blocking_eval_failure_blocks_every_strategy(self) -> None:
        for strategy in ("policy-auto", "human-required"):
            decision = decide_release_action(release(strategy), gate(eligible=False))
            self.assertEqual(decision.action, "block")
            self.assertEqual(decision.strategy, strategy)

    def test_policy_auto_releases_only_after_blocking_gates_pass(self) -> None:
        decision = decide_release_action(release("policy-auto"), gate(eligible=True))
        self.assertEqual(decision.action, "auto-release")

    def test_human_required_never_auto_releases(self) -> None:
        decision = decide_release_action(release("human-required"), gate(eligible=True))
        self.assertEqual(decision.action, "require-human")

    def test_gate_for_different_release_is_rejected(self) -> None:
        with self.assertRaises(ReleaseStrategyError):
            decide_release_action(
                release("policy-auto", release_id="release-a"),
                gate(eligible=True, release_id="release-b"),
            )


if __name__ == "__main__":
    unittest.main()
