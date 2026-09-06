import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

from agent_factory_core.capability_gateway import (
    CapabilityGateway,
    CapabilityRegistration,
    CapabilitySpec,
)
from agent_factory_core.compiler import compile_effective_release
from agent_factory_core.contracts import (
    AgentManifest,
    ClientInstanceConfig,
    EvalResult,
    PlatformPolicy,
    build_execution_context,
)
from agent_factory_core.eval_policy import map_eval_results
from agent_factory_core.memory_gateway import MemoryGateway
from agent_factory_core.model_router import ModelRouter
from agent_factory_core.orchestrator import (
    BoundedHybridOrchestrator,
    BoundedPlan,
    CapabilityPlanStep,
    MemoryReadPlanStep,
    MemoryWritePlanStep,
    ModelPlanStep,
    OrchestratorLimits,
    ToolPlanStep,
)
from agent_factory_core.provenance import check_release_drift
from agent_factory_core.registry import (
    CapabilityImplementation,
    CapabilityRecord,
    CapabilityRegistry,
)
from agent_factory_core.release_evidence import (
    build_evidence_pack,
    build_release_decision_record,
)
from agent_factory_core.synthetic_model_adapters import (
    build_deterministic_model_adapter,
    build_stub_model_adapter,
)
from agent_factory_core.synthetic_readonly_tool import build_synthetic_lookup_tool
from agent_factory_core.tool_gateway import ToolGateway


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "examples" / "synthetic-reference-agent"
APPROVED_SPEC_REF = "spec://core-contracts/synthetic-reference-agent@1"
RELEASE_ID = "release-synthetic-e2e-1"
PLATFORM_POLICY_REF = "synthetic-platform-policy@1"


def load_json(name: str) -> dict:
    return json.loads((REFERENCE / name).read_text(encoding="utf-8"))


def capability_registry() -> CapabilityRegistry:
    return CapabilityRegistry(
        [
            CapabilityRecord(
                ref="synthetic.capability",
                version="1",
                environments=["sandbox"],
                requiredPermissions=["capability.synthetic.invoke"],
                implementations=[
                    CapabilityImplementation(
                        id="cap.synthetic.v1",
                        environments=["sandbox"],
                    )
                ],
            )
        ]
    )


def runtime_capability() -> CapabilityRegistration:
    spec = CapabilitySpec(
        capability_ref="synthetic.capability",
        implementation_id="cap.synthetic.v1",
        required_permission="capability.synthetic.invoke",
        minimum_trust_profile="internal",
        allowed_data_classifications=("internal",),
    )

    def handler(payload: dict) -> dict:
        return {"capability": payload.get("value")}

    return CapabilityRegistration(spec=spec, handler=handler)


def runtime_orchestrator() -> BoundedHybridOrchestrator:
    primary = build_deterministic_model_adapter()
    stub = build_stub_model_adapter()
    return BoundedHybridOrchestrator(
        model_router=ModelRouter(
            (primary, stub),
            routes={
                "balanced": (
                    primary.spec.implementation_id,
                    stub.spec.implementation_id,
                )
            },
        ),
        tool_gateway=ToolGateway((build_synthetic_lookup_tool(),)),
        memory_gateway=MemoryGateway(),
        capability_gateway=CapabilityGateway((runtime_capability(),)),
    )


def synthetic_plan() -> BoundedPlan:
    return BoundedPlan(
        steps=(
            CapabilityPlanStep(
                "capability",
                "synthetic.capability",
                {"value": "compiled-binding-ok"},
            ),
            ModelPlanStep("model", "hello synthetic core"),
            ToolPlanStep("tool", "synthetic.lookup", {"key": "alpha"}),
            MemoryWritePlanStep(
                "memory-write",
                memory_class="task_working",
                purpose="task",
                key="synthetic-result",
                content={"status": "saved"},
                retention_profile="task",
                source_reference="synthetic:c6",
            ),
            MemoryReadPlanStep(
                "memory-read",
                memory_class="task_working",
                purpose="task",
                key="synthetic-result",
            ),
        )
    )


class SyntheticEndToEndGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest_data = load_json("agent-manifest.json")
        cls.client_data = load_json("client-instance-config.json")
        cls.policy_data = load_json("platform-policy.json")

        cls.manifest_schema = json.loads(
            (ROOT / "schemas" / "agent-manifest.schema.json").read_text(encoding="utf-8")
        )
        cls.client_schema = json.loads(
            (ROOT / "schemas" / "client-instance-config.schema.json").read_text(encoding="utf-8")
        )
        cls.policy_schema = json.loads(
            (ROOT / "schemas" / "platform-policy.schema.json").read_text(encoding="utf-8")
        )

    def test_complete_synthetic_reference_agent_path(self) -> None:
        # C6.1 - the checked-in reference definition is a valid external contract.
        Draft202012Validator(self.manifest_schema).validate(self.manifest_data)
        Draft202012Validator(self.client_schema).validate(self.client_data)
        Draft202012Validator(self.policy_schema).validate(self.policy_data)

        manifest = AgentManifest.model_validate(self.manifest_data)
        client = ClientInstanceConfig.model_validate(self.client_data)
        policy = PlatformPolicy.model_validate(self.policy_data)

        # C6.2 - compile the same checked-in definition through Registry resolution.
        release = compile_effective_release(
            manifest,
            client,
            policy,
            capability_registry(),
            release_id=RELEASE_ID,
        )
        self.assertEqual(
            release.spec.capability_bindings,
            {"synthetic.capability": "cap.synthetic.v1"},
        )
        self.assertEqual(
            release.spec.tool_bindings,
            {"synthetic.lookup": "tool.synthetic.lookup.v1"},
        )
        self.assertEqual(release.spec.release_strategy, "policy-auto")

        # C6.3 - derive trusted runtime authority and execute a bounded mixed plan.
        now = datetime.now(timezone.utc)
        context = build_execution_context(
            release,
            request_id="req-synthetic-e2e-1",
            trace_id="trace-synthetic-e2e-1",
            actor_id="synthetic-user",
            actor_type="user",
            deadline=now + timedelta(minutes=2),
        )
        execution = runtime_orchestrator().execute(
            context,
            plan=synthetic_plan(),
            limits=OrchestratorLimits(max_steps=5, max_repeats_per_operation=2),
            platform_policy_ref=PLATFORM_POLICY_REF,
            exception_policy_refs=release.policy.exception_policy_refs,
            now=now,
        )
        self.assertTrue(execution.completed)
        self.assertEqual(len(execution.steps), 5)
        self.assertEqual(
            execution.steps[0].output,
            {"capability": "compiled-binding-ok"},
        )
        self.assertEqual(execution.steps[1].output, "primary:hello synthetic core")
        self.assertEqual(execution.steps[2].output, {"found": True, "value": "A"})
        self.assertEqual(execution.steps[3].output, {"key": "synthetic-result"})
        self.assertEqual(execution.steps[4].output, {"status": "saved"})

        audit_events = tuple(step.audit_event for step in execution.steps)
        self.assertTrue(all(item.trace_id == context.trace_id for item in audit_events))
        self.assertTrue(all(item.tenant_id == "tenant-synthetic" for item in audit_events))
        self.assertTrue(all(item.agent_release_id == RELEASE_ID for item in audit_events))
        self.assertTrue(all(item.platform_policy_ref == PLATFORM_POLICY_REF for item in audit_events))
        self.assertTrue(all(item.decision == "allow" for item in audit_events))

        # C6.4 - produce all required eval families and map them through policy.
        eval_specs = (
            (
                "eval-functional",
                "functional.synthetic-plan",
                "functional_business",
                {"completed": execution.completed, "steps": len(execution.steps)},
            ),
            (
                "eval-security",
                "security.synthetic-authority",
                "security_policy",
                {"allStepsAudited": len(audit_events) == len(execution.steps)},
            ),
            (
                "eval-cost",
                "cost.synthetic-zero-cost",
                "cost_runtime",
                {"estimatedCost": 0},
            ),
            (
                "eval-portability",
                "contract.synthetic-portability",
                "contract_portability",
                {"providerProfile": release.spec.provider_profile},
            ),
        )
        eval_results = tuple(
            EvalResult(
                apiVersion="agentfactory.io/v1alpha1",
                kind="EvalResult",
                evalId=eval_id,
                releaseId=RELEASE_ID,
                checkId=check_id,
                checkVersion="1",
                family=family,
                status="PASS",
                summary="synthetic C6 gate passed",
                metrics=metrics,
                evidenceRefs=(f"trace://{context.trace_id}",),
                observedAt=now,
            )
            for eval_id, check_id, family, metrics in eval_specs
        )
        gate = map_eval_results(eval_results, policy)
        self.assertTrue(gate.eligible)
        self.assertEqual(gate.blocking_failures, ())
        self.assertEqual(len(gate.mapped), 4)

        decision = build_release_decision_record(
            release,
            gate,
            release_decision_id="decision-synthetic-e2e-1",
            timestamp=now,
        )
        self.assertEqual(decision.result, "released")
        self.assertEqual(decision.strategy, "policy-auto")
        self.assertEqual(
            set(decision.eval_result_refs),
            {item.eval_id for item in eval_results},
        )

        # C6.5 - reconstruct release evidence and verify exact provenance/drift.
        evidence = build_evidence_pack(
            release,
            decision,
            evidence_pack_id="evidence-synthetic-e2e-1",
            spec_ref=APPROVED_SPEC_REF,
            agent_manifest_ref="repo://examples/synthetic-reference-agent/agent-manifest.json",
            client_instance_config_ref="repo://examples/synthetic-reference-agent/client-instance-config.json",
            template_module_refs=("template://general-agent@1",),
            config_diff_ref="diff://synthetic-reference-agent/release-1",
            capability_tool_contract_refs=(
                "capability://synthetic.capability@1",
                "tool://synthetic.lookup@1",
                "model://synthetic-provider-neutral@1",
                "memory://session-task@1",
            ),
            known_limitations=(
                "synthetic adapters only",
                "zero-cost read-only/ephemeral slice",
            ),
            created_at=now,
        )
        self.assertEqual(evidence.release_decision_ref, decision.release_decision_id)
        self.assertEqual(set(evidence.eval_result_refs), {item.eval_id for item in eval_results})

        drift = check_release_drift(
            release,
            context,
            evidence,
            approved_spec_ref=APPROVED_SPEC_REF,
        )
        self.assertTrue(drift.managed)
        self.assertEqual(drift.mismatches, ())
        self.assertTrue(drift.release_fingerprint.startswith("sha256:"))

        # Evidence is minimized: raw prompts, memory content and secrets are not release artifacts.
        evidence_dump = evidence.model_dump(by_alias=True, mode="json")
        self.assertNotIn("prompt", evidence_dump)
        self.assertNotIn("payload", evidence_dump)
        self.assertNotIn("secrets", evidence_dump)


if __name__ == "__main__":
    unittest.main()
