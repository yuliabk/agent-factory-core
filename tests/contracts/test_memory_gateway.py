import unittest
from datetime import datetime, timedelta, timezone

from agent_factory_core.contracts import ExecutionContext
from agent_factory_core.memory_gateway import (
    InMemorySessionTaskStore,
    MemoryGateway,
    MemoryReadRequest,
    MemoryWriteRequest,
)


DEFAULT_MEMORY_CONFIG = {
    "allowedClasses": ["session", "task_working"],
    "allowedPurposes": ["conversation", "task"],
    "allowedRetentionProfiles": ["session", "task"],
    "readEnabled": True,
    "writeEnabled": True,
    "minimumTrustProfile": "internal",
}


def context(
    *,
    tenant_id: str = "tenant-a",
    request_id: str = "req-memory-1",
    trace_id: str = "trace-memory-1",
    permissions: tuple[str, ...] = ("memory.read", "memory.write"),
    trust_profile: str = "internal",
    memory_config: dict | None = None,
) -> ExecutionContext:
    return ExecutionContext(
        apiVersion="agentfactory.io/v1alpha1",
        kind="ExecutionContext",
        requestId=request_id,
        traceId=trace_id,
        actorId="user-1",
        actorType="user",
        tenantId=tenant_id,
        environment="sandbox",
        agentId="test-agent",
        agentReleaseId="release-memory-1",
        trustProfile=trust_profile,
        permissions=permissions,
        dataClassification="internal",
        capabilityBindings={},
        providerProfile="balanced",
        toolBindings={},
        memoryConfig=DEFAULT_MEMORY_CONFIG if memory_config is None else memory_config,
        budgetConfig={},
        deadline=datetime.now(timezone.utc) + timedelta(minutes=2),
    )


def write_request(
    *,
    memory_class: str = "session",
    purpose: str = "conversation",
    classification: str = "internal",
    key: str = "alpha",
    retention: str = "session",
) -> MemoryWriteRequest:
    return MemoryWriteRequest(
        memory_class=memory_class,  # type: ignore[arg-type]
        purpose=purpose,
        data_classification=classification,
        key=key,
        content={"value": "synthetic"},
        retention_profile=retention,
        source_reference="synthetic:test",
    )


def read_request(
    *,
    memory_class: str = "session",
    purpose: str = "conversation",
    classification: str = "internal",
    key: str = "alpha",
) -> MemoryReadRequest:
    return MemoryReadRequest(
        memory_class=memory_class,  # type: ignore[arg-type]
        purpose=purpose,
        data_classification=classification,
        key=key,
    )


class MemoryGatewayContractTests(unittest.TestCase):
    def test_session_write_read_is_governed_and_audited(self) -> None:
        gateway = MemoryGateway()
        ctx = context()

        written = gateway.write(
            ctx,
            request=write_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(written.allowed)
        self.assertEqual(written.entry.tenant_id, "tenant-a")
        self.assertEqual(written.entry.scope_id, "req-memory-1")
        self.assertEqual(written.audit_event.operation, "memory.write")
        self.assertFalse(hasattr(written.audit_event, "content"))

        read = gateway.read(
            ctx,
            request=read_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(read.allowed)
        self.assertIsNotNone(read.entry)
        self.assertEqual(read.entry.content, {"value": "synthetic"})
        self.assertEqual(read.audit_event.result, "found")

    def test_task_working_memory_is_trace_scoped_across_requests(self) -> None:
        gateway = MemoryGateway()
        first = context(request_id="req-1", trace_id="trace-task")
        second = context(request_id="req-2", trace_id="trace-task")

        written = gateway.write(
            first,
            request=write_request(memory_class="task_working", purpose="task", retention="task"),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(written.allowed)
        self.assertEqual(written.entry.scope_id, "trace-task")

        read = gateway.read(
            second,
            request=read_request(memory_class="task_working", purpose="task"),
            platform_policy_ref="platform-default@1",
        )
        self.assertIsNotNone(read.entry)

    def test_session_memory_does_not_cross_request_scope(self) -> None:
        gateway = MemoryGateway()
        gateway.write(
            context(request_id="req-1"),
            request=write_request(),
            platform_policy_ref="platform-default@1",
        )
        read = gateway.read(
            context(request_id="req-2"),
            request=read_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(read.allowed)
        self.assertIsNone(read.entry)

    def test_cross_tenant_memory_is_not_visible(self) -> None:
        store = InMemorySessionTaskStore()
        gateway = MemoryGateway(store)
        tenant_b = context(tenant_id="tenant-b", request_id="shared-request")
        tenant_a = context(tenant_id="tenant-a", request_id="shared-request")

        gateway.write(
            tenant_b,
            request=write_request(),
            platform_policy_ref="platform-default@1",
        )
        read = gateway.read(
            tenant_a,
            request=read_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertTrue(read.allowed)
        self.assertIsNone(read.entry)

    def test_missing_memory_permission_is_denied(self) -> None:
        gateway = MemoryGateway()
        result = gateway.write(
            context(permissions=("memory.read",)),
            request=write_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "permission")

    def test_trust_escalation_is_denied(self) -> None:
        gateway = MemoryGateway()
        result = gateway.write(
            context(trust_profile="sandbox"),
            request=write_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.rule, "trust_profile")

    def test_classification_and_purpose_are_enforced(self) -> None:
        gateway = MemoryGateway()
        classification = gateway.write(
            context(),
            request=write_request(classification="confidential"),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(classification.allowed)
        self.assertEqual(classification.rule, "data_classification")

        purpose = gateway.write(
            context(),
            request=write_request(purpose="marketing"),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(purpose.allowed)
        self.assertEqual(purpose.rule, "memory_purpose")

    def test_persistent_class_and_unapproved_retention_are_blocked(self) -> None:
        gateway = MemoryGateway()
        persistent = gateway.write(
            context(),
            request=write_request(memory_class="user_persistent"),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(persistent.allowed)
        self.assertEqual(persistent.rule, "memory_class")

        retention = gateway.write(
            context(),
            request=write_request(retention="forever"),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(retention.allowed)
        self.assertEqual(retention.rule, "memory_retention")

    def test_memory_config_is_default_deny_and_can_disable_write(self) -> None:
        gateway = MemoryGateway()
        missing = gateway.write(
            context(memory_config={"readEnabled": True}),
            request=write_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(missing.allowed)
        self.assertEqual(missing.rule, "memory_config")

        config = {
            "allowedClasses": ["session"],
            "allowedPurposes": ["conversation"],
            "allowedRetentionProfiles": ["session"],
            "readEnabled": True,
            "writeEnabled": False,
            "minimumTrustProfile": "internal",
        }
        disabled = gateway.write(
            context(memory_config=config),
            request=write_request(),
            platform_policy_ref="platform-default@1",
        )
        self.assertFalse(disabled.allowed)
        self.assertEqual(disabled.rule, "memory_write_disabled")


if __name__ == "__main__":
    unittest.main()
