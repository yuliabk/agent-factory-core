from __future__ import annotations

from typing import Literal

TrustProfile = Literal["sandbox", "internal", "business", "privileged"]

TRUST_PROFILE_ORDER: tuple[TrustProfile, ...] = (
    "sandbox",
    "internal",
    "business",
    "privileged",
)


def trust_profile_rank(profile: TrustProfile) -> int:
    return TRUST_PROFILE_ORDER.index(profile)
