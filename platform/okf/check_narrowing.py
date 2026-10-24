#!/usr/bin/env python3
"""OKF v0.3: an agent bundle may only narrow the corp policies (zuno-demo ADR-0579 clause 5).

Runs on every bundle; v0.2 bundles have none of the v0.3 fields and pass
trivially. For a v0.3 bundle, a declaration that would WIDEN what the corp
policies allow is a finding, naming the corp clause it exceeds:

- skills       every skill a task lists exists (agents/<agent>/skills/<name>.md, or
               policies/skills/<name>.md for `corp/<name>`, shipped in the
               corp artifact's policies layer), is a
               `type: skill` document, and needs no tool or knowledge domain
               the task itself does not allow
- models       preferred/forbidden roles exist in policies/models/model-catalog.yaml;
               a preferred role has at least one model eligible for the
               agent's classification; no role is both preferred and forbidden
- guardrails   the mode is at least the corp minimum for the agent's
               classification (policies/guardrails/guardrails-policy.yaml);
               categories are corp categories
- limits       max_tokens and max_concurrent_requests are at most the corp
               ceilings (policies/limits/limits-policy.yaml); quota_class is a
               class of policies/quotas/quota-policy.yaml (agent and task
               level, and the v0.2 task `quota_class`/`max_tokens` aliases);
               limits.delegation.max_depth is at most max_delegation_depth
- delegation   zuno.delegation.targets (zuno-demo ADR-0401) name another agent
               of the release and one of its tasks, never the agent itself;
               delegation is a v0.3 field (a v0.2 bundle declaring it is a finding)

Tool and knowledge references themselves are checked by
platform/supply-chain/validate_okf_bundle.py.

Run from the repository root:
    python3 platform/okf/check_narrowing.py [agents/<name> ...]
"""
from __future__ import annotations

import pathlib
import sys
from typing import Dict, List, Optional, Set

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / "agents"
CORP_SKILLS_DIR = REPO_ROOT / "policies" / "skills"
POLICIES = REPO_ROOT / "policies"
CLASS_ORDER = ["C1", "C2", "C3"]


def frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    return (yaml.safe_load(text[4:end]) or {}) if text.startswith("---\n") and end > 0 else {}


def load(rel: str) -> dict:
    path = POLICIES / rel
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.is_file() else {}


class Corp:
    """The corp policies a bundle is checked against."""

    def __init__(self) -> None:
        catalog = load("models/model-catalog.yaml").get("models") or []
        self.roles: Dict[str, Set[str]] = {}
        for m in catalog:
            self.roles.setdefault(m.get("role", ""), set()).update(m.get("eligible_for") or [])
        guard = load("guardrails/guardrails-policy.yaml")
        self.modes: List[str] = guard.get("modes") or ["off", "observe", "block"]
        self.min_mode: Dict[str, str] = guard.get("minimum_mode_by_classification") or {}
        self.categories: Set[str] = set(guard.get("categories") or [])
        limits = load("limits/limits-policy.yaml")
        self.max_tokens: Optional[int] = limits.get("max_tokens")
        self.max_concurrent: Optional[int] = limits.get("max_concurrent_requests")
        self.max_delegation_depth: Optional[int] = limits.get("max_delegation_depth")
        self.quota_classes: Set[str] = set((load("quotas/quota-policy.yaml").get("classes") or {}).keys())


def _models(where: str, models: dict, classification: str, corp: Corp) -> List[str]:
    out = []
    preferred = list(models.get("preferred") or [])
    forbidden = list(models.get("forbidden") or [])
    for role in preferred + forbidden:
        if role not in corp.roles:
            out.append(f"{where}: model role {role!r} is not a role of policies/models/model-catalog.yaml")
    for role in preferred:
        if role in corp.roles and classification and classification not in corp.roles[role]:
            out.append(f"{where}: no model of role {role!r} is eligible for {classification} "
                       f"(policies/models/model-catalog.yaml eligible_for)")
    for role in sorted(set(preferred) & set(forbidden)):
        out.append(f"{where}: model role {role!r} is both preferred and forbidden")
    return out


def _limits(where: str, limits: dict, corp: Corp) -> List[str]:
    out = []
    if corp.max_tokens is not None and (limits.get("max_tokens") or 0) > corp.max_tokens:
        out.append(f"{where}: max_tokens {limits['max_tokens']} exceeds the corp ceiling {corp.max_tokens} "
                   f"(policies/limits/limits-policy.yaml)")
    if corp.max_concurrent is not None and (limits.get("max_concurrent_requests") or 0) > corp.max_concurrent:
        out.append(f"{where}: max_concurrent_requests {limits['max_concurrent_requests']} exceeds the corp "
                   f"ceiling {corp.max_concurrent} (policies/limits/limits-policy.yaml)")
    depth = (limits.get("delegation") or {}).get("max_depth")
    if corp.max_delegation_depth is not None and depth is not None and depth > corp.max_delegation_depth:
        out.append(f"{where}: delegation max_depth {depth} exceeds the corp ceiling {corp.max_delegation_depth} "
                   f"(policies/limits/limits-policy.yaml)")
    qc = limits.get("quota_class")
    if qc is not None and qc not in corp.quota_classes:
        out.append(f"{where}: quota_class {qc!r} is not a class of policies/quotas/quota-policy.yaml")
    return out


def _delegation(label: str, bundle: pathlib.Path, z: dict) -> List[str]:
    out: List[str] = []
    name = z.get("name", bundle.name)
    for target in (z.get("delegation") or {}).get("targets") or []:
        agent, task = target.get("agent"), target.get("task")
        if agent == name:
            out.append(f"{label}/agent.okf.md: delegation target {agent!r} is the agent itself")
        elif not (bundle.parent / str(agent) / "agent.okf.md").is_file():
            out.append(f"{label}/agent.okf.md: delegation target agent {agent!r} is not in the release")
        elif not (bundle.parent / str(agent) / "tasks" / f"{task}.md").is_file():
            out.append(f"{label}/agent.okf.md: delegation target task {agent}/{task} does not exist")
    return out


def _skill_path(bundle: pathlib.Path, ref: str) -> pathlib.Path:
    if ref.startswith("corp/"):
        return CORP_SKILLS_DIR / f"{ref[len('corp/'):]}.md"
    return bundle / "skills" / f"{ref}.md"


def check_bundle(bundle: pathlib.Path, corp: Corp) -> List[str]:
    label = bundle.relative_to(REPO_ROOT).as_posix()
    agent = frontmatter(bundle / "agent.okf.md")
    z = agent.get("zuno") or {}
    if agent.get("okf_version") != "v0.3":
        if z.get("delegation") or (z.get("limits") or {}).get("delegation"):
            return [f"{label}/agent.okf.md: delegation is an OKF v0.3 field; this bundle declares "
                    f"okf_version {agent.get('okf_version')!r}"]
        return []
    classification = (z.get("model") or {}).get("preferred_classification", "")
    findings: List[str] = []

    findings += _models(f"{label}/agent.okf.md", z.get("models") or {}, classification, corp)
    findings += _limits(f"{label}/agent.okf.md", z.get("limits") or {}, corp)
    findings += _delegation(label, bundle, z)

    guard = z.get("guardrails") or {}
    mode = guard.get("mode")
    floor = corp.min_mode.get(classification)
    if mode and floor and corp.modes.index(mode) < corp.modes.index(floor):
        findings.append(f"{label}/agent.okf.md: guardrails mode {mode!r} is weaker than the corp minimum "
                        f"{floor!r} for {classification} (policies/guardrails/guardrails-policy.yaml)")
    for cat in guard.get("categories") or []:
        if cat not in corp.categories:
            findings.append(f"{label}/agent.okf.md: guardrails category {cat!r} is not a corp category "
                            f"(policies/guardrails/guardrails-policy.yaml)")

    for task in z.get("tasks") or []:
        task_path = bundle / "tasks" / f"{task}.md"
        if not task_path.is_file():
            continue  # reported by validate_okf_bundle.py
        where = f"{label}/tasks/{task}.md"
        tz = frontmatter(task_path).get("zuno") or {}
        findings += _models(where, tz.get("models") or {}, classification, corp)
        task_limits = dict(tz.get("limits") or {})
        for alias in ("max_tokens", "quota_class"):
            if alias in tz:
                task_limits.setdefault(alias, tz[alias])
        findings += _limits(where, task_limits, corp)
        tools, domains = set(tz.get("allowed_tools") or []), set(tz.get("allowed_knowledge") or [])
        for ref in tz.get("skills") or []:
            path = _skill_path(bundle, ref)
            if not path.is_file():
                findings.append(f"{where}: skill {ref!r} not found ({path.relative_to(REPO_ROOT).as_posix()})")
                continue
            skill = frontmatter(path)
            if skill.get("type") != "skill":
                findings.append(f"{where}: {path.relative_to(REPO_ROOT).as_posix()} is not a type: skill document")
                continue
            sz = skill.get("zuno") or {}
            for tool in sorted(set(sz.get("allowed_tools") or []) - tools):
                findings.append(f"{where}: skill {ref!r} needs tool {tool!r}, which the task does not allow")
            for domain in sorted(set(sz.get("allowed_knowledge") or []) - domains):
                findings.append(f"{where}: skill {ref!r} needs knowledge domain {domain!r}, "
                                f"which the task does not allow")
    return findings


def main(argv: List[str]) -> int:
    bundles = [REPO_ROOT / a for a in argv] if argv else sorted(p.parent for p in AGENTS_DIR.glob("*/agent.okf.md"))
    corp = Corp()
    findings: List[str] = []
    for bundle in bundles:
        findings += check_bundle(bundle, corp)
    if findings:
        print(f"{len(findings)} widening(s) of the corp policies:")
        for f in findings:
            print(f"  ✗ {f}")
        print("\nRESULT: FAIL - a bundle may only narrow the corp policies (ADR-0579 clause 5).")
        return 1
    v03 = sum(1 for b in bundles if frontmatter(b / "agent.okf.md").get("okf_version") == "v0.3")
    print(f"Checked {len(bundles)} bundle(s), {v03} in OKF v0.3.")
    print("\nRESULT: PASS - no bundle widens the corp policies.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
