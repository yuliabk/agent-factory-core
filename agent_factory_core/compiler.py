from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .contracts.agent_manifest import AgentManifest
from .contracts.client_instance_config import ClientInstanceConfig
from .contracts.effective_release_config import (
    EffectiveReleaseConfig,
    EffectiveReleaseMetadata,
    EffectiveReleaseSpec,
    PolicySnapshot,
)


@dataclass(frozen=True)
class CompilationError(ValueError):
    path: str
    rule: str
    remediation: str

    def __str__(self) -> str:
        return f"{self.path}: {self.rule}. {self.remediation}"


def _require_policy_list(policy: Mapping[str, Any], key: str) -> set[str]:
    value = policy.get(key)
    if not isinstance(value, (list, tuple, set)) or not all(isinstance(item, str) for item in value):
        raise CompilationError(
            path=f"platformPolicy.{key}",
            rule="must be an explicit list of strings in the first compiler skeleton",
            remediation=f"Add {key} to PlatformPolicy before compiling this release",
        )
    return set(value)


def compile_effective_release(
    manifest: AgentManifest,
    client: ClientInstanceConfig,
    platform_policy: Mapping[str, Any],
    *,
    release_id: str,
    exception_policy_refs: Sequence[str] = (),
) -> EffectiveReleaseConfig:
    """Compile reusable Agent requirements and client configuration into runtime authority.

    This is intentionally a narrow first compiler. It enforces only rules whose
    semantics are already accepted. Full PlatformPolicy/ExceptionPolicy models
    will replace the temporary mapping boundary in the next Core Skeleton step.
    """

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

    policy_version = platform_policy.get("version")
    if not isinstance(policy_version, str) or not policy_version:
        raise CompilationError(
            path="platformPolicy.version",
            rule="is required",
            remediation="Provide the version of the PlatformPolicy used to compile the release",
        )

    requested = set(manifest.spec.permissions.requested)
    client_allow = set(client.spec.permission_overrides.allow)
    client_deny = set(client.spec.permission_overrides.deny)
    platform_allow = _require_policy_list(platform_policy, "allowedPermissions")
    platform_deny = set(platform_policy.get("deniedPermissions", []))

    missing_client_grants = requested - client_allow
    if missing_client_grants:
        missing = ", ".join(sorted(missing_client_grants))
        raise CompilationError(
            path="spec.permissionOverrides.allow",
            rule=f"does not grant required Agent permissions: {missing}",
            remediation="Grant the required permissions for this tenant or choose a different Agent definition",
        )

    denied = requested & (client_deny | platform_deny)
    if denied:
        values = ", ".join(sorted(denied))
        raise CompilationError(
            path="spec.permissionOverrides",
            rule=f"required Agent permissions are explicitly denied: {values}",
            remediation="Remove the conflicting grant/deny combination or use a compatible Agent definition",
        )

    outside_platform = requested - platform_allow
    if outside_platform:
        values = ", ".join(sorted(outside_platform))
        raise CompilationError(
            path="platformPolicy.allowedPermissions",
            rule=f"does not permit required Agent permissions: {values}",
            remediation="Use an allowed Agent configuration or a separately validated ExceptionPolicy path",
        )

    allowed_provider_profiles = _require_policy_list(platform_policy, "allowedProviderProfiles")
    if client.spec.provider_profile not in allowed_provider_profiles:
        raise CompilationError(
            path="spec.providerProfile",
            rule=f"profile {client.spec.provider_profile!r} is not allowed by PlatformPolicy",
            remediation="Choose an allowed provider profile",
        )

    required_tools = set(manifest.spec.tools.required)
    missing_tool_bindings = required_tools - set(client.spec.tool_bindings)
    if missing_tool_bindings:
        values = ", ".join(sorted(missing_tool_bindings))
        raise CompilationError(
            path="spec.toolBindings",
            rule=f"missing bindings for required tools: {values}",
            remediation="Bind every required tool before compiling the release",
        )

    allowed_budget_keys = _require_policy_list(platform_policy, "allowedBudgetOverrideKeys")
    unknown_budget_keys = set(client.spec.budget_overrides) - allowed_budget_keys
    if unknown_budget_keys:
        values = ", ".join(sorted(unknown_budget_keys))
        raise CompilationError(
            path="spec.budgetOverrides",
            rule=f"contains policy-disallowed override keys: {values}",
            remediation="Remove the keys or add them through an approved policy change/exception",
        )

    allowed_memory_keys = _require_policy_list(platform_policy, "allowedMemoryConfigKeys")
    unknown_memory_keys = set(client.spec.memory_config) - allowed_memory_keys
    if unknown_memory_keys:
        values = ", ".join(sorted(unknown_memory_keys))
        raise CompilationError(
            path="spec.memoryConfig",
            rule=f"contains policy-disallowed config keys: {values}",
            remediation="Remove the keys or add them through an approved policy change/exception",
        )

    effective_permissions = tuple(sorted(requested))

    return EffectiveReleaseConfig(
        apiVersion="agentfactory.io/v1alpha1",
        kind="EffectiveReleaseConfig",
        metadata=EffectiveReleaseMetadata(
            releaseId=release_id,
            environment=client.metadata.environment,
        ),
        policy=PolicySnapshot(
            platformPolicyVersion=policy_version,
            exceptionPolicyRefs=tuple(exception_policy_refs),
        ),
        spec=EffectiveReleaseSpec(
            agentRef=client.spec.agent_ref,
            tenant=client.spec.tenant,
            variables=dict(client.spec.variables),
            capabilities=manifest.spec.capabilities,
            providerProfile=client.spec.provider_profile,
            secretsRef=dict(client.spec.secrets_ref),
            memoryConfig=dict(client.spec.memory_config),
            budgetConfig=dict(client.spec.budget_overrides),
            permissions=effective_permissions,
            toolBindings=dict(client.spec.tool_bindings),
            evalProfile=manifest.spec.eval_profile,
        ),
    )
