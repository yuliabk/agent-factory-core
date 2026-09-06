from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from .contracts.agent_manifest import AgentManifest
from .contracts.client_instance_config import ClientInstanceConfig
from .contracts.effective_release_config import (
    EffectiveReleaseConfig,
    EffectiveReleaseMetadata,
    EffectiveReleaseSpec,
    PolicySnapshot,
)
from .contracts.exception_policy import ExceptionPolicy
from .contracts.platform_policy import PlatformPolicy
from .contracts.trust import trust_profile_rank
from .registry import CapabilityRegistry, CapabilityResolutionError


@dataclass(frozen=True)
class CompilationError(ValueError):
    path: str
    rule: str
    remediation: str

    def __str__(self) -> str:
        return f"{self.path}: {self.rule}. {self.remediation}"


def _validate_exception(
    exception: ExceptionPolicy,
    *,
    platform_policy: PlatformPolicy,
    client: ClientInstanceConfig,
    manifest: AgentManifest,
    now: datetime,
) -> None:
    ref = exception.spec.platform_policy_ref
    if (ref.name, ref.version) != (
        platform_policy.metadata.name,
        platform_policy.metadata.version,
    ):
        raise CompilationError(
            path=f"exceptionPolicy[{exception.metadata.name}].spec.platformPolicyRef",
            rule="must reference the PlatformPolicy being compiled",
            remediation="Update or remove the exception before compiling",
        )

    scope = exception.spec.scope
    if scope.tenant_id != client.spec.tenant.id or scope.environment != client.metadata.environment:
        raise CompilationError(
            path=f"exceptionPolicy[{exception.metadata.name}].spec.scope",
            rule="does not match tenant/environment",
            remediation="Use an exception scoped to this client instance",
        )
    if scope.agent_name is not None and scope.agent_name != manifest.metadata.name:
        raise CompilationError(
            path=f"exceptionPolicy[{exception.metadata.name}].spec.scope.agentName",
            rule="does not match the Agent",
            remediation="Use an exception scoped to this Agent",
        )
    if scope.agent_version is not None and scope.agent_version != manifest.metadata.version:
        raise CompilationError(
            path=f"exceptionPolicy[{exception.metadata.name}].spec.scope.agentVersion",
            rule="does not match the Agent version",
            remediation="Use an exception scoped to this Agent version",
        )

    expiry = exception.spec.expires_at
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    if expiry <= now:
        raise CompilationError(
            path=f"exceptionPolicy[{exception.metadata.name}].spec.expiresAt",
            rule="exception is expired",
            remediation="Renew through the approved exception process or remove it",
        )

    allowed = platform_policy.spec.exception_allowances
    checks = (
        (set(exception.spec.allow.permissions), set(allowed.permissions), "permissions"),
        (set(exception.spec.allow.provider_profiles), set(allowed.provider_profiles), "providerProfiles"),
        (set(exception.spec.allow.budget_override_keys), set(allowed.budget_override_keys), "budgetOverrideKeys"),
        (set(exception.spec.allow.memory_config_keys), set(allowed.memory_config_keys), "memoryConfigKeys"),
    )
    for requested, permitted, field in checks:
        invalid = requested - permitted
        if invalid:
            raise CompilationError(
                path=f"exceptionPolicy[{exception.metadata.name}].spec.allow.{field}",
                rule=f"contains non-overridable values: {', '.join(sorted(invalid))}",
                remediation="Remove values not declared overrideable by PlatformPolicy",
            )


def compile_effective_release(
    manifest: AgentManifest,
    client: ClientInstanceConfig,
    platform_policy: PlatformPolicy,
    registry: CapabilityRegistry,
    *,
    release_id: str,
    exceptions: Sequence[ExceptionPolicy] = (),
    now: datetime | None = None,
) -> EffectiveReleaseConfig:
    if client.spec.agent_ref.name != manifest.metadata.name:
        raise CompilationError(
            path="spec.agentRef.name",
            rule="must match AgentManifest metadata.name",
            remediation=f"Set agentRef.name to {manifest.metadata.name!r}",
        )
    if client.spec.agent_ref.version != manifest.metadata.version:
        raise CompilationError(
            path="spec.agentRef.version",
            rule="must match AgentManifest metadata.version",
            remediation=f"Set agentRef.version to {manifest.metadata.version!r}",
        )

    now = now or datetime.now(timezone.utc)
    platform_allow = set(platform_policy.spec.allowed_permissions)
    platform_deny = set(platform_policy.spec.denied_permissions)
    allowed_provider_profiles = set(platform_policy.spec.allowed_provider_profiles)
    allowed_budget_keys = set(platform_policy.spec.allowed_budget_override_keys)
    allowed_memory_keys = set(platform_policy.spec.allowed_memory_config_keys)

    exception_refs: list[str] = []
    for exception in exceptions:
        _validate_exception(
            exception,
            platform_policy=platform_policy,
            client=client,
            manifest=manifest,
            now=now,
        )
        exception_refs.append(f"{exception.metadata.name}@{exception.metadata.version}")
        platform_allow.update(exception.spec.allow.permissions)
        allowed_provider_profiles.update(exception.spec.allow.provider_profiles)
        allowed_budget_keys.update(exception.spec.allow.budget_override_keys)
        allowed_memory_keys.update(exception.spec.allow.memory_config_keys)

    requested = set(manifest.spec.permissions.requested)
    client_allow = set(client.spec.permission_overrides.allow)
    client_deny = set(client.spec.permission_overrides.deny)

    missing_client_grants = requested - client_allow
    if missing_client_grants:
        raise CompilationError(
            path="spec.permissionOverrides.allow",
            rule=f"does not grant required Agent permissions: {', '.join(sorted(missing_client_grants))}",
            remediation="Grant the required permissions or choose a different Agent definition",
        )

    denied = requested & (client_deny | platform_deny)
    if denied:
        raise CompilationError(
            path="spec.permissionOverrides",
            rule=f"required Agent permissions are explicitly denied: {', '.join(sorted(denied))}",
            remediation="Remove the conflict; PlatformPolicy deniedPermissions are non-overridable in this skeleton",
        )

    outside_platform = requested - platform_allow
    if outside_platform:
        raise CompilationError(
            path="platformPolicy.spec.allowedPermissions",
            rule=f"does not permit required Agent permissions: {', '.join(sorted(outside_platform))}",
            remediation="Use an allowed configuration or a valid scoped ExceptionPolicy",
        )

    if trust_profile_rank(client.spec.trust_profile) > trust_profile_rank(platform_policy.spec.max_trust_profile):
        raise CompilationError(
            path="spec.trustProfile",
            rule=(
                f"trust profile {client.spec.trust_profile!r} exceeds PlatformPolicy ceiling "
                f"{platform_policy.spec.max_trust_profile!r}"
            ),
            remediation="Choose a trust profile at or below the PlatformPolicy ceiling",
        )

    if client.spec.provider_profile not in allowed_provider_profiles:
        raise CompilationError(
            path="spec.providerProfile",
            rule=f"profile {client.spec.provider_profile!r} is not allowed by effective policy",
            remediation="Choose an allowed provider profile or valid exception",
        )

    required_tools = set(manifest.spec.tools.required)
    missing_tool_bindings = required_tools - set(client.spec.tool_bindings)
    if missing_tool_bindings:
        raise CompilationError(
            path="spec.toolBindings",
            rule=f"missing bindings for required tools: {', '.join(sorted(missing_tool_bindings))}",
            remediation="Bind every required tool before compiling the release",
        )

    unknown_budget_keys = set(client.spec.budget_overrides) - allowed_budget_keys
    if unknown_budget_keys:
        raise CompilationError(
            path="spec.budgetOverrides",
            rule=f"contains policy-disallowed override keys: {', '.join(sorted(unknown_budget_keys))}",
            remediation="Remove them or use a valid scoped exception",
        )

    unknown_memory_keys = set(client.spec.memory_config) - allowed_memory_keys
    if unknown_memory_keys:
        raise CompilationError(
            path="spec.memoryConfig",
            rule=f"contains policy-disallowed config keys: {', '.join(sorted(unknown_memory_keys))}",
            remediation="Remove them or use a valid scoped exception",
        )

    capability_bindings: dict[str, str] = {}
    for requirement in manifest.spec.capabilities.requires:
        try:
            resolved = registry.resolve_required(
                requirement,
                environment=client.metadata.environment,
                mode=platform_policy.spec.registry_mode,
            )
        except CapabilityResolutionError as exc:
            raise CompilationError(
                path=f"spec.capabilities.requires[{requirement.ref}]",
                rule=str(exc),
                remediation="Register a compatible implementation, change the reference, or mark an eligible dependency optional in soft mode",
            ) from exc
        if resolved is None:
            continue
        missing_capability_permissions = set(resolved.required_permissions) - requested
        if missing_capability_permissions:
            raise CompilationError(
                path=f"spec.capabilities.requires[{requirement.ref}]",
                rule=f"registry requires undeclared permissions: {', '.join(sorted(missing_capability_permissions))}",
                remediation="Declare the required permissions in AgentManifest and grant them through client/policy",
            )
        capability_bindings[resolved.ref] = resolved.implementation_id

    effective_permissions = tuple(sorted(requested))

    return EffectiveReleaseConfig(
        apiVersion="agentfactory.io/v1alpha1",
        kind="EffectiveReleaseConfig",
        metadata=EffectiveReleaseMetadata(
            releaseId=release_id,
            environment=client.metadata.environment,
        ),
        policy=PolicySnapshot(
            platformPolicyName=platform_policy.metadata.name,
            platformPolicyVersion=platform_policy.metadata.version,
            exceptionPolicyRefs=tuple(exception_refs),
        ),
        spec=EffectiveReleaseSpec(
            agentRef=client.spec.agent_ref,
            tenant=client.spec.tenant,
            variables=dict(client.spec.variables),
            capabilities=manifest.spec.capabilities,
            capabilityBindings=capability_bindings,
            trustProfile=client.spec.trust_profile,
            providerProfile=client.spec.provider_profile,
            secretsRef=dict(client.spec.secrets_ref),
            memoryConfig=dict(client.spec.memory_config),
            budgetConfig=dict(client.spec.budget_overrides),
            permissions=effective_permissions,
            dataClassification=platform_policy.spec.default_data_classification,
            toolBindings=dict(client.spec.tool_bindings),
            evalProfile=manifest.spec.eval_profile,
        ),
    )
