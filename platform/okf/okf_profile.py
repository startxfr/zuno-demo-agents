"""Which version of the Zuno OKF profile a document follows (zuno-demo ADR-0615 clause 5).

Every tool of this repository that reads a document's frontmatter dispatches through `document_version`, so
the rule is written once here. Consumers (zuno-demo's reader hooks, unifai-operator) implement the same table
in their own code; the conformance cases under `conformance/cases/` keep them aligned.

| okf_version            | zuno.profile            | version     |
|------------------------|-------------------------|-------------|
| "v0.2" or "v0.3"       | absent                  | that legacy version (transition, until operator line 0.2) |
| "0.2"                  | "1.0"                   | "1.0"       |
| "0.2"                  | absent or another value | refused: unsupported zuno.profile |
| anything else          | -                       | refused: unsupported okf_version |

`okf_version` must be a YAML string: an unquoted `0.2` is a number and is refused.
"""
from __future__ import annotations

from typing import Any, Mapping

UPSTREAM_OKF_VERSION = "0.2"
LEGACY_VERSIONS = ("v0.2", "v0.3")
PROFILES = ("1.0",)
CURRENT_PROFILE = "1.0"
# Narrowing applies from v0.3 up (ADR-0615 clause 6): compare levels, never versions.
LEVEL = {"v0.2": 2, "v0.3": 3, "1.0": 4}


class UnsupportedVersion(ValueError):
    """A document whose okf_version / zuno.profile pair no reader accepts."""


def document_version(doc: Mapping[str, Any]) -> str:
    """Return "v0.2", "v0.3" or "1.0" for a document's frontmatter, or raise UnsupportedVersion."""
    version = doc.get("okf_version")
    zuno = doc.get("zuno")
    profile = zuno.get("profile") if isinstance(zuno, Mapping) else None
    if isinstance(version, str) and version in LEGACY_VERSIONS:
        if profile is not None:
            raise UnsupportedVersion(f"zuno.profile is only valid with okf_version \"{UPSTREAM_OKF_VERSION}\" "
                                     f"(this document says okf_version {version!r})")
        return version
    if isinstance(version, str) and version == UPSTREAM_OKF_VERSION:
        if isinstance(profile, str) and profile in PROFILES:
            return profile
        raise UnsupportedVersion(f"unsupported zuno.profile {profile!r} (supported: {', '.join(PROFILES)})")
    raise UnsupportedVersion(f"unsupported okf_version {version!r} "
                             f"(supported: \"{UPSTREAM_OKF_VERSION}\" with zuno.profile, or legacy "
                             f"{', '.join(LEGACY_VERSIONS)})")


def level(version: str) -> int:
    return LEVEL[version]


def at_least_v03(version: str) -> bool:
    """True when the v0.3 rules (skills, models, guardrails, limits, delegation) apply."""
    return LEVEL.get(version, 0) >= LEVEL["v0.3"]


def is_profile(version: str) -> bool:
    return version in PROFILES
