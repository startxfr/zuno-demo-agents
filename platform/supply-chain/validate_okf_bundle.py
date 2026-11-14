#!/usr/bin/env python3
"""Bundle structure and corp policy references, independent of signature verification.

Checks per agent bundle (agents/<name>/) and experience client (experience-clients/<name>/):

1. **Structure.** The version of `agent.okf.md` follows zuno-demo ADR-0615 clause 5 (profile 1.0, or legacy
   v0.2/v0.3 until 2026-12-01). It has `type: agent`, and `zuno.name` matches the directory name. Every task it
   declares has a `tasks/<task>.md` file with `type: task`.
2. **Policy references.** Every tool a task declares in `zuno.allowed_tools` is a name of
   `policies/tools/tool-policy.yaml` (its `tool` or `capability` name). Every knowledge domain is a domain of
   `policies/knowledge/knowledge-policy.yaml`.
3. **Content notes.** Every `*.md` under `rag/`, `tools/` and `policies/` has the right `type`, and its
   cross-reference back to the bundle's tasks resolves. These notes are documentation: they never grant anything.
4. **Profile 1.0 rules** (ADR-0615 clauses 3, 4, 9, 10), for a bundle whose agent is on profile 1.0:
   - one profile per bundle;
   - `resource` is the document's URL on the main branch;
   - published text is platform-neutral;
   - a root `index.md` exists (`generate_index.py --check` checks its content);
   - every task has a prompt;
   - the upstream `status` agrees with `zuno.status`;
   - a tool note's `capability` is in the tool policy;
   - `used_by_tasks` lists every task that declares the item;
   - a prompt or a skill names a tool by its `capability`, the name the model is offered, never by a legacy
     `tool` name.

   A `stale_after` in the past is a warning, never a failure.

Fails closed: an unreadable bundle, an unknown reference or a missing task file is a finding.

Run from the repository root:

    python3 platform/supply-chain/validate_okf_bundle.py [agents/<name> ...]
"""
from __future__ import annotations

import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "platform" / "okf"))
sys.path.insert(0, str(REPO_ROOT / "platform" / "release"))
from okf_profile import UnsupportedVersion, document_version, is_profile  # noqa: E402
import okf_release  # noqa: E402

AGENTS_DIR = REPO_ROOT / "agents"
CLIENTS_DIR = REPO_ROOT / "experience-clients"
TOOL_POLICY_PATH = REPO_ROOT / "policies" / "tools" / "tool-policy.yaml"
KNOWLEDGE_POLICY_PATH = REPO_ROOT / "policies" / "knowledge" / "knowledge-policy.yaml"


# Profile 1.0 rules (zuno-demo ADR-0615 clauses 4, 9 and 10). A legacy (v0.2/v0.3) bundle is checked as before.
RESOURCE_BASE = "https://github.com/startxfr/zuno-demo-agents/blob/main/"
# Published text names no component, path or version of one particular platform (ADR-0615 clause 10).
PLATFORM_SPECIFIC = re.compile(r"Agent Runtime|agent-runtime|agent-frontend|agent-bff|components/|evaluations/|"
                               r"gitops/|MEMORY\.md|docs/agents|platform/ai-gateway|\bv0\b")
STATUS_FOR = {"active": {"stable"}, "placeholder": {"draft"}, "deprecated": {"deprecated"}, "retired": {"deprecated"}}


@dataclass
class Finding:
    bundle: str
    message: str


def _split_frontmatter(path: pathlib.Path) -> Dict:
    if not path.is_file():
        raise ValueError(f"{path} does not exist")
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: expected a leading '---' YAML frontmatter block")
    return yaml.safe_load(parts[1]) or {}


def _known_tool_names() -> Set[str]:
    """Every name policies/tools/tool-policy.yaml answers to - legacy
    `tool` names and ADR-0116 canonical `capability` names alike (mirrors
    components/mcp-gateway/app/policy.py's own dual-indexing)."""
    if not TOOL_POLICY_PATH.is_file():
        return set()
    doc = yaml.safe_load(TOOL_POLICY_PATH.read_text()) or {}
    names: Set[str] = set()
    for entry in doc.get("tools", []):
        if "tool" in entry:
            names.add(entry["tool"])
        if "capability" in entry:
            names.add(entry["capability"])
    return names


def _legacy_tool_names() -> Dict[str, str]:
    """Legacy `tool` name -> its `capability`, for every entry of the tool policy where the two differ. The runtime
    offers a tool to the model under its capability, so a prompt that names the legacy name names a tool the
    model never sees."""
    if not TOOL_POLICY_PATH.is_file():
        return {}
    doc = yaml.safe_load(TOOL_POLICY_PATH.read_text()) or {}
    return {e["tool"]: e["capability"] for e in doc.get("tools", [])
            if e.get("tool") and e.get("capability") and e["tool"] != e["capability"]}


def tool_policy_findings(path: pathlib.Path = TOOL_POLICY_PATH) -> List["Finding"]:
    """Structural checks on the tool policy itself. `access` (zuno-demo ADR-0406
    and ADR-0409) is optional and must be `read` or `write`; absent means `write`."""
    if not path.is_file():
        return []
    label = "policies/tools/tool-policy.yaml"
    findings: List[Finding] = []
    for entry in (yaml.safe_load(path.read_text()) or {}).get("tools", []):
        access = entry.get("access")
        if access is not None and access not in ("read", "write"):
            findings.append(Finding(label, f"tool '{entry.get('tool')}': access must be 'read' or 'write', got {access!r}"))
    return findings


def _known_knowledge_domains() -> Set[str]:
    """ADR-0202/0203 knowledge policy - feature-detected. Returns an empty
    set (meaning "no knowledge references validated yet") until WP-20
    creates this file; callers must treat an empty set as "skip", not
    "everything is unknown"."""
    if not KNOWLEDGE_POLICY_PATH.is_file():
        return set()
    doc = yaml.safe_load(KNOWLEDGE_POLICY_PATH.read_text()) or {}
    return set(doc.get("domains", {}).keys())


def _content_notes(dir_path: pathlib.Path) -> List[pathlib.Path]:
    """Schema-conformant notes under a rag/tools/policies directory - every
    `*.md` except the directory's own index README (ADR-0513 content is
    one file per item, README.md is the human index, not an item)."""
    if not dir_path.is_dir():
        return []
    return sorted(p for p in dir_path.glob("*.md") if p.name != "README.md")


def _validate_content_notes(bundle_dir: pathlib.Path, label: str, declared_tasks: Dict[str, Dict[str, Set[str]]]) -> List[Finding]:
    """ADR-0513 check 3: rag/tools/policies notes cross-reference tasks the
    bundle actually declares, with the tool/domain those tasks actually
    allow. `declared_tasks` maps task_name -> {"tools": set, "knowledge": set},
    built from the same task frontmatter check 1/2 already parsed."""
    findings: List[Finding] = []

    def _resolve_tasks(rel_path: str, used_by_tasks) -> List[str]:
        unknown = [t for t in used_by_tasks if t not in declared_tasks]
        for t in unknown:
            findings.append(Finding(label, f"{rel_path}: used_by_tasks references '{t}', not a declared task"))
        return [t for t in used_by_tasks if t in declared_tasks]

    for note_path in _content_notes(bundle_dir / "rag"):
        rel = f"rag/{note_path.name}"
        try:
            fm = _split_frontmatter(note_path)
        except ValueError as exc:
            findings.append(Finding(label, str(exc)))
            continue
        if not _version_ok(fm, findings, label, rel) or fm.get("type") != "rag":
            if fm.get("type") != "rag":
                findings.append(Finding(label, f"{rel}: expected type rag"))
            continue
        zuno = fm.get("zuno") or {}
        domain = zuno.get("domain")
        for task_name in _resolve_tasks(rel, zuno.get("used_by_tasks") or []):
            if domain not in declared_tasks[task_name]["knowledge"]:
                findings.append(
                    Finding(label, f"{rel}: domain '{domain}' not in task '{task_name}''s allowed_knowledge")
                )

    for note_path in _content_notes(bundle_dir / "tools"):
        rel = f"tools/{note_path.name}"
        try:
            fm = _split_frontmatter(note_path)
        except ValueError as exc:
            findings.append(Finding(label, str(exc)))
            continue
        if not _version_ok(fm, findings, label, rel) or fm.get("type") != "tool":
            if fm.get("type") != "tool":
                findings.append(Finding(label, f"{rel}: expected type tool"))
            continue
        zuno = fm.get("zuno") or {}
        capability = zuno.get("capability")
        for task_name in _resolve_tasks(rel, zuno.get("used_by_tasks") or []):
            if capability not in declared_tasks[task_name]["tools"]:
                findings.append(
                    Finding(label, f"{rel}: capability '{capability}' not in task '{task_name}''s allowed_tools")
                )

    for note_path in _content_notes(bundle_dir / "policies"):
        rel = f"policies/{note_path.name}"
        try:
            fm = _split_frontmatter(note_path)
        except ValueError as exc:
            findings.append(Finding(label, str(exc)))
            continue
        if not _version_ok(fm, findings, label, rel) or fm.get("type") != "policy":
            if fm.get("type") != "policy":
                findings.append(Finding(label, f"{rel}: expected type policy"))
            continue
        zuno = fm.get("zuno") or {}
        applies_to = zuno.get("applies_to") or {}
        tasks_in_scope = _resolve_tasks(rel, applies_to.get("tasks") or [])
        allowed_tools_union: Set[str] = set()
        allowed_knowledge_union: Set[str] = set()
        for task_name in tasks_in_scope:
            allowed_tools_union |= declared_tasks[task_name]["tools"]
            allowed_knowledge_union |= declared_tasks[task_name]["knowledge"]
        for tool_name in applies_to.get("tools") or []:
            if tool_name not in allowed_tools_union:
                findings.append(
                    Finding(label, f"{rel}: applies_to.tools '{tool_name}' not allowed by any task in applies_to.tasks")
                )
        for domain in applies_to.get("knowledge") or []:
            if domain not in allowed_knowledge_union:
                findings.append(
                    Finding(label, f"{rel}: applies_to.knowledge '{domain}' not allowed by any task in applies_to.tasks")
                )

    return findings


def _version_ok(fm: Dict, findings: List["Finding"], label: str, rel: str) -> Optional[str]:
    """The document's profile version, or None after recording why it is unsupported."""
    try:
        return document_version(fm)
    except UnsupportedVersion as exc:
        findings.append(Finding(label, f"{rel}: {exc}"))
        return None


WARNINGS: List[str] = []


def _profile_documents(label: str, paths: List[pathlib.Path]) -> List["Finding"]:
    """One profile per bundle, the canonical `resource`, platform-neutral text; `stale_after` only warns."""
    import datetime
    findings: List[Finding] = []
    now = datetime.datetime.now(datetime.timezone.utc)
    for path in paths:
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            fm = _split_frontmatter(path)
        except ValueError as exc:
            findings.append(Finding(label, str(exc)))
            continue
        version = _version_ok(fm, findings, label, rel)
        if version is not None and not is_profile(version):
            findings.append(Finding(label, f"{rel}: one profile per bundle - this document is legacy {version}"))
        expected = RESOURCE_BASE + rel
        if fm.get("resource") != expected:
            findings.append(Finding(label, f"{rel}: resource must be {expected}, got {fm.get('resource')!r}"))
        hit = PLATFORM_SPECIFIC.search(path.read_text(encoding="utf-8"))
        if hit:
            findings.append(Finding(label, f"{rel}: names {hit.group(0)!r}, which belongs to one platform "
                                           f"(published text must be platform-neutral, ADR-0615 clause 10)"))
        stale = fm.get("stale_after")
        if isinstance(stale, str):
            try:
                if datetime.datetime.fromisoformat(stale.replace("Z", "+00:00")) < now:
                    WARNINGS.append(f"{rel}: stale_after {stale} is past - review the document")
            except ValueError:
                pass  # the schema reports the format
    return findings


def _profile_rules(bundle_dir: pathlib.Path, label: str, agent: Dict,
                   declared_tasks: Dict[str, Dict[str, Set[str]]], known_tools: Set[str]) -> List["Finding"]:
    """Rules a profile 1.0 bundle adds (ADR-0615 clauses 3, 4, 9, 10)."""
    findings: List[Finding] = []
    docs = [p for p in okf_release.runtime_files(bundle_dir) if p.suffix == ".md" and p.name != "index.md"]
    findings += _profile_documents(label, docs)
    if not (bundle_dir / "index.md").is_file():
        findings.append(Finding(label, "index.md is missing: run python3 platform/okf/generate_index.py"))
    zuno = agent.get("zuno") or {}
    status = agent.get("status")
    if status is not None and status not in STATUS_FOR.get(zuno.get("status"), set()):
        findings.append(Finding(label, f"agent.okf.md: status {status!r} disagrees with zuno.status "
                                       f"{zuno.get('status')!r}"))
    for task in declared_tasks:
        if not (bundle_dir / "prompts" / f"{task}.md").is_file():
            findings.append(Finding(label, f"task {task!r} has no prompts/{task}.md (every task has a prompt)"))
    legacy = _legacy_tool_names()
    for doc in docs:
        rel = doc.relative_to(bundle_dir).as_posix()
        if not rel.startswith(("prompts/", "skills/")):
            continue
        for name in sorted(set(re.findall(r"`([A-Za-z0-9_.]+)`", doc.read_text(encoding="utf-8"))) & set(legacy)):
            findings.append(Finding(label, f"{rel}: names the tool {name!r}; the model is offered it as "
                                           f"{legacy[name]!r}, write that"))
    # Notes: a known capability, and used_by_tasks lists every task that declares it (both directions).
    for kind, key, field in (("tools", "capability", "tools"), ("rag", "domain", "knowledge")):
        for note in _content_notes(bundle_dir / kind):
            try:
                nz = _split_frontmatter(note).get("zuno") or {}
            except ValueError:
                continue
            item = nz.get(key)
            if kind == "tools" and known_tools and item not in known_tools:
                findings.append(Finding(label, f"{kind}/{note.name}: capability {item!r} is not in tool-policy.yaml"))
            users = {t for t, d in declared_tasks.items() if item in d[field]}
            missing = sorted(users - set(nz.get("used_by_tasks") or []))
            if missing:
                findings.append(Finding(label, f"{kind}/{note.name}: used_by_tasks misses {missing}, which declare "
                                               f"{item!r}"))
    return findings


def validate_bundle(bundle_dir: pathlib.Path, known_tools: Set[str], known_domains: Set[str]) -> List[Finding]:
    label = str(bundle_dir.relative_to(REPO_ROOT))
    findings: List[Finding] = []
    index_path = bundle_dir / "agent.okf.md"

    try:
        frontmatter = _split_frontmatter(index_path)
    except ValueError as exc:
        return [Finding(label, str(exc))]

    # Profile 1.0 (zuno-demo ADR-0615), or legacy v0.2/v0.3 until 2026-12-01.
    # platform/okf/check_narrowing.py checks the v0.3-and-above fields against the corp policies.
    version = _version_ok(frontmatter, findings, label, "agent.okf.md")
    if frontmatter.get("type") != "agent":
        findings.append(Finding(label, f"type must be 'agent', got {frontmatter.get('type')!r}"))

    zuno = frontmatter.get("zuno") or {}
    if zuno.get("name") != bundle_dir.name:
        findings.append(
            Finding(label, f"zuno.name {zuno.get('name')!r} does not match directory name {bundle_dir.name!r}")
        )

    declared_tasks: Dict[str, Dict[str, Set[str]]] = {}
    for task_name in zuno.get("tasks", []):
        task_path = bundle_dir / "tasks" / f"{task_name}.md"
        try:
            task_frontmatter = _split_frontmatter(task_path)
        except ValueError as exc:
            findings.append(Finding(label, str(exc)))
            continue

        if task_frontmatter.get("type") != "task":
            findings.append(Finding(label, f"{task_path.name}: expected type task"))

        task_zuno = task_frontmatter.get("zuno") or {}
        task_tools = set(task_zuno.get("allowed_tools", []))
        task_knowledge = set(task_zuno.get("allowed_knowledge", []))
        declared_tasks[task_name] = {"tools": task_tools, "knowledge": task_knowledge}

        for tool_name in task_tools:
            if known_tools and tool_name not in known_tools:
                findings.append(
                    Finding(label, f"{task_path.name}: unknown tool '{tool_name}' (not in tool-policy.yaml)")
                )
        for domain in task_knowledge:
            if known_domains and domain not in known_domains:
                findings.append(
                    Finding(label, f"{task_path.name}: unknown knowledge domain '{domain}' (not in knowledge-policy.yaml)")
                )

    findings.extend(_validate_content_notes(bundle_dir, label, declared_tasks))
    if version and is_profile(version):
        findings.extend(_profile_rules(bundle_dir, label, frontmatter, declared_tasks, known_tools))

    return findings


CLASSIFICATION_RANK = {"C1": 1, "C2": 2, "C3": 3}


def _tool_min_classification() -> Dict[str, str]:
    """tool or capability name -> min_classification in tool-policy.yaml."""
    if not TOOL_POLICY_PATH.is_file():
        return {}
    doc = yaml.safe_load(TOOL_POLICY_PATH.read_text()) or {}
    out: Dict[str, str] = {}
    for entry in doc.get("tools", []):
        for key in ("tool", "capability"):
            if key in entry:
                out[entry[key]] = entry.get("min_classification", "C1")
    return out


def validate_client(client_dir: pathlib.Path, known_tools: Set[str], agent_names: Set[str]) -> List[Finding]:
    """zuno-demo ADR-0592: an experience client (experience-clients/<name>).

    Same task rules as an agent (each task exists, is a task, and allows only
    tools of tool-policy.yaml), plus what keeps it from being mistaken for an
    agent: its name is no agent's name, and it allows no tool its declared
    classification cannot reach (a C1 client cannot use a C2 tool)."""
    label = str(client_dir.relative_to(REPO_ROOT))
    findings: List[Finding] = []
    try:
        frontmatter = _split_frontmatter(client_dir / "client.okf.md")
    except ValueError as exc:
        return [Finding(label, str(exc))]

    client_version = _version_ok(frontmatter, findings, label, "client.okf.md")
    if client_version == "v0.2":
        findings.append(Finding(label, "an experience client needs OKF v0.3 or profile 1.0, got v0.2"))
    if client_version and is_profile(client_version):
        docs = [client_dir / "client.okf.md"] + sorted((client_dir / "tasks").glob("*.md"))
        findings.extend(_profile_documents(label, [d for d in docs if d.name not in ("README.md",)]))
    if frontmatter.get("type") != "experience-client":
        findings.append(Finding(label, f"type must be 'experience-client', got {frontmatter.get('type')!r}"))

    zuno = frontmatter.get("zuno") or {}
    name = zuno.get("name")
    if name != client_dir.name:
        findings.append(Finding(label, f"zuno.name {name!r} does not match directory name {client_dir.name!r}"))
    if name in agent_names:
        findings.append(Finding(label, f"zuno.name {name!r} is also an agent: a logical name is either an agent or a client"))

    ceiling = zuno.get("classification")
    min_class = _tool_min_classification()
    for task_name in zuno.get("tasks", []):
        task_path = client_dir / "tasks" / f"{task_name}.md"
        try:
            task_frontmatter = _split_frontmatter(task_path)
        except ValueError as exc:
            findings.append(Finding(label, str(exc)))
            continue
        if task_frontmatter.get("type") != "task":
            findings.append(Finding(label, f"{task_path.name}: expected type task"))
        task_zuno = task_frontmatter.get("zuno") or {}
        if task_zuno.get("allowed_knowledge"):
            findings.append(Finding(label, f"{task_path.name}: an experience client has no RAG, allowed_knowledge must be empty"))
        for tool_name in task_zuno.get("allowed_tools", []):
            if known_tools and tool_name not in known_tools:
                findings.append(Finding(label, f"{task_path.name}: unknown tool '{tool_name}' (not in tool-policy.yaml)"))
                continue
            needed = min_class.get(tool_name, "C1")
            if ceiling and CLASSIFICATION_RANK[needed] > CLASSIFICATION_RANK[ceiling]:
                findings.append(
                    Finding(label, f"{task_path.name}: tool '{tool_name}' needs {needed}, above the client's classification {ceiling}")
                )
    return findings


def main() -> int:
    args = sys.argv[1:]
    if args:
        bundle_dirs = [REPO_ROOT / arg for arg in args]
    else:
        bundle_dirs = sorted(p for p in AGENTS_DIR.iterdir() if p.is_dir())

    known_tools = _known_tool_names()
    known_domains = _known_knowledge_domains()

    all_findings: List[Finding] = list(tool_policy_findings())
    for bundle_dir in bundle_dirs:
        all_findings.extend(validate_bundle(bundle_dir, known_tools, known_domains))

    client_dirs = [] if args else sorted(p for p in CLIENTS_DIR.iterdir() if p.is_dir()) if CLIENTS_DIR.is_dir() else []
    agent_names = {p.name for p in AGENTS_DIR.iterdir() if p.is_dir()}
    for client_dir in client_dirs:
        all_findings.extend(validate_client(client_dir, known_tools, agent_names))

    print(f"Validated {len(bundle_dirs)} OKF bundle(s) under agents/ and {len(client_dirs)} under experience-clients/.")
    for warning in WARNINGS:
        print(f"  ! warning: {warning}")
    if not all_findings:
        print("\nRESULT: PASS - every bundle is structurally valid and every policy reference resolves.")
        return 0

    print(f"\n{len(all_findings)} finding(s):")
    for f in all_findings:
        print(f"  ✗ {f.bundle}: {f.message}")
    print("\nRESULT: FAIL - fix the bundle(s) above (ADR-0106).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
