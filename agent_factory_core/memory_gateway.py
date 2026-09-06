from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Mapping

from .contracts.execution_context import ExecutionContext
from .contracts.runtime_audit_event import RuntimeAuditEvent
from .contracts.trust import TrustProfile
from .runtime.audit import build_audit_event
from .runtime.policy import evaluate_request_authority


MemoryClass = Literal["session", "task_working"]


@dataclass(frozen=True)
class MemoryWriteRequest:
    memory_class: MemoryClass
    purpose: str
    data_classification: str
    key: str
    content: Any
    retention_profile: str
    source_reference: str | None = None


@dataclass(frozen=True)
class MemoryReadRequest:
    memory_class: MemoryClass
    purpose: str
    data_classification: str
    key: str


@dataclass(frozen=True)
class MemoryEntry:
    memory_class: MemoryClass
    purpose: str
    data_classification: str
    key: str
    content: Any
    retention_profile: str
    source_reference: str | None
    tenant_id: str
    agent_release_id: str
    scope_id: str


@dataclass(frozen=True)
class MemoryOperationResult:
    allowed: bool
    rule: str
    reason: str
    entry: MemoryEntry | None
    audit_event: RuntimeAuditEvent


@dataclass(frozen=True)
class _MemoryPolicy:
    allowed_classes: tuple[MemoryClass, ...]
    allowed_purposes: tuple[str, ...]
    allowed_retention_profiles: tuple[str, ...]
    read_enabled: bool
    write_enabled: bool
    minimum_trust_profile: TrustProfile


class InMemorySessionTaskStore:
    """Ephemeral tenant/release/request-scoped store for the first memory slice."""

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str, str, str, str], MemoryEntry] = {}

    def put(self, entry: MemoryEntry) -> None:
        self._entries[self._storage_key(entry)] = entry

    def get(
        self,
        *,
        tenant_id: str,
        agent_release_id: str,
        memory_class: MemoryClass,
        scope_id: str,
        key: str,
    ) -> MemoryEntry | None:
        return self._entries.get((tenant_id, agent_release_id, memory_class, scope_id, key))

    @staticmethod
    def _storage_key(entry: MemoryEntry) -> tuple[str, str, str, str, str]:
        return (
            entry.tenant_id,
            entry.agent_release_id,
            entry.memory_class,
            entry.scope_id,
            entry.key,
        )


class MemoryGateway:
    """Governed session/task memory gateway backed by ephemeral in-process storage."""

    def __init__(self, store: InMemorySessionTaskStore | None = None) -> None:
        self._store = store or InMemorySessionTaskStore()

    def write(
        self,
        context: ExecutionContext,
        *,
        request: MemoryWriteRequest,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...] = (),
        approval_ref: str | None = None,
        now: datetime | None = None,
    ) -> MemoryOperationResult:
        policy, error = self._policy_from_context(context)
        if error is not None:
            return self._deny(
                context,
                target_ref=f"memory:{request.memory_class}:{request.key}",
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.write",
                rule="memory_config",
                reason=error,
                now=now,
            )
        assert policy is not None

        decision = self._evaluate(
            context,
            memory_class=request.memory_class,
            purpose=request.purpose,
            data_classification=request.data_classification,
            permission="memory.write",
            retention_profile=request.retention_profile,
            policy=policy,
            now=now,
        )
        if decision is not None:
            rule, reason = decision
            return self._deny(
                context,
                target_ref=f"memory:{request.memory_class}:{request.key}",
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.write",
                rule=rule,
                reason=reason,
                now=now,
            )

        if not policy.write_enabled:
            return self._deny(
                context,
                target_ref=f"memory:{request.memory_class}:{request.key}",
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.write",
                rule="memory_write_disabled",
                reason="memory writes are disabled by trusted memory configuration",
                now=now,
            )

        if not request.key or not request.purpose or not request.retention_profile:
            return self._deny(
                context,
                target_ref=f"memory:{request.memory_class}:{request.key}",
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.write",
                rule="memory_request",
                reason="key, purpose and retention_profile are required",
                now=now,
            )

        entry = MemoryEntry(
            memory_class=request.memory_class,
            purpose=request.purpose,
            data_classification=request.data_classification,
            key=request.key,
            content=request.content,
            retention_profile=request.retention_profile,
            source_reference=request.source_reference,
            tenant_id=context.tenant_id,
            agent_release_id=context.agent_release_id,
            scope_id=self._scope_id(context, request.memory_class),
        )
        self._store.put(entry)

        return MemoryOperationResult(
            allowed=True,
            rule="memory_gateway",
            reason="governed ephemeral memory write completed",
            entry=entry,
            audit_event=build_audit_event(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.write",
                target_ref=f"memory:{request.memory_class}:{request.key}",
                decision="allow",
                result="success",
                timestamp=now,
            ),
        )

    def read(
        self,
        context: ExecutionContext,
        *,
        request: MemoryReadRequest,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...] = (),
        approval_ref: str | None = None,
        now: datetime | None = None,
    ) -> MemoryOperationResult:
        policy, error = self._policy_from_context(context)
        if error is not None:
            return self._deny(
                context,
                target_ref=f"memory:{request.memory_class}:{request.key}",
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.read",
                rule="memory_config",
                reason=error,
                now=now,
            )
        assert policy is not None

        decision = self._evaluate(
            context,
            memory_class=request.memory_class,
            purpose=request.purpose,
            data_classification=request.data_classification,
            permission="memory.read",
            retention_profile=None,
            policy=policy,
            now=now,
        )
        if decision is not None:
            rule, reason = decision
            return self._deny(
                context,
                target_ref=f"memory:{request.memory_class}:{request.key}",
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.read",
                rule=rule,
                reason=reason,
                now=now,
            )

        if not policy.read_enabled:
            return self._deny(
                context,
                target_ref=f"memory:{request.memory_class}:{request.key}",
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.read",
                rule="memory_read_disabled",
                reason="memory reads are disabled by trusted memory configuration",
                now=now,
            )

        entry = self._store.get(
            tenant_id=context.tenant_id,
            agent_release_id=context.agent_release_id,
            memory_class=request.memory_class,
            scope_id=self._scope_id(context, request.memory_class),
            key=request.key,
        )
        if entry is not None and (
            entry.purpose != request.purpose
            or entry.data_classification != request.data_classification
        ):
            entry = None

        return MemoryOperationResult(
            allowed=True,
            rule="memory_gateway",
            reason="governed ephemeral memory read completed",
            entry=entry,
            audit_event=build_audit_event(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation="memory.read",
                target_ref=f"memory:{request.memory_class}:{request.key}",
                decision="allow",
                result="found" if entry is not None else "not_found",
                timestamp=now,
            ),
        )

    def _evaluate(
        self,
        context: ExecutionContext,
        *,
        memory_class: MemoryClass,
        purpose: str,
        data_classification: str,
        permission: str,
        retention_profile: str | None,
        policy: _MemoryPolicy,
        now: datetime | None,
    ) -> tuple[str, str] | None:
        authority = evaluate_request_authority(
            context,
            tenant_id=context.tenant_id,
            permission=permission,
            data_classification=data_classification,
            required_trust_profile=policy.minimum_trust_profile,
            now=now,
        )
        if not authority.allowed:
            return authority.rule, authority.reason
        if memory_class not in policy.allowed_classes:
            return "memory_class", "memory class is not allowed by trusted memory configuration"
        if purpose not in policy.allowed_purposes:
            return "memory_purpose", "memory purpose is not allowed by trusted memory configuration"
        if retention_profile is not None and retention_profile not in policy.allowed_retention_profiles:
            return "memory_retention", "retention profile is not allowed by trusted memory configuration"
        return None

    @staticmethod
    def _scope_id(context: ExecutionContext, memory_class: MemoryClass) -> str:
        if memory_class == "session":
            return context.request_id
        return context.trace_id

    @staticmethod
    def _policy_from_context(context: ExecutionContext) -> tuple[_MemoryPolicy | None, str | None]:
        config: Mapping[str, Any] = context.memory_config
        classes = tuple(config.get("allowedClasses", ()))
        purposes = tuple(config.get("allowedPurposes", ()))
        retention = tuple(config.get("allowedRetentionProfiles", ()))
        minimum_trust = config.get("minimumTrustProfile")

        supported = {"session", "task_working"}
        if not classes or any(item not in supported for item in classes):
            return None, "memoryConfig.allowedClasses must contain only session/task_working"
        if not purposes:
            return None, "memoryConfig.allowedPurposes must not be empty"
        if not retention:
            return None, "memoryConfig.allowedRetentionProfiles must not be empty"
        if minimum_trust not in {"sandbox", "internal", "business", "privileged"}:
            return None, "memoryConfig.minimumTrustProfile must be a supported trust profile"

        return (
            _MemoryPolicy(
                allowed_classes=classes,  # type: ignore[arg-type]
                allowed_purposes=purposes,
                allowed_retention_profiles=retention,
                read_enabled=config.get("readEnabled") is True,
                write_enabled=config.get("writeEnabled") is True,
                minimum_trust_profile=minimum_trust,
            ),
            None,
        )

    @staticmethod
    def _deny(
        context: ExecutionContext,
        *,
        target_ref: str,
        platform_policy_ref: str,
        exception_policy_refs: tuple[str, ...],
        approval_ref: str | None,
        operation: str,
        rule: str,
        reason: str,
        now: datetime | None,
    ) -> MemoryOperationResult:
        return MemoryOperationResult(
            allowed=False,
            rule=rule,
            reason=reason,
            entry=None,
            audit_event=build_audit_event(
                context,
                platform_policy_ref=platform_policy_ref,
                exception_policy_refs=exception_policy_refs,
                approval_ref=approval_ref,
                operation=operation,
                target_ref=target_ref,
                decision="deny",
                result=rule,
                timestamp=now,
            ),
        )
