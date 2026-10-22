#!/usr/bin/env python3
"""Build, version-check and publish OKF releases (ADR-0577).

One OCI artifact per agent, holding only the files a consumer reads, plus one
corp artifact holding the corp policies and an index of the agent digests.
The corp artifact is the release: consumers pin its digest and reach the
agents through it.

    agent artifact  <registry>/okf-<agent>
        type        application/vnd.zuno.okf.bundle.v2
        layer       application/vnd.zuno.okf.bundle.v2.tar+gzip
                    agent.okf.md, tasks/, prompts/, skills/, tools/, rag/,
                    policies/ - never tests/ nor README.md files
    corp artifact   <registry>/okf-corp
        type        application/vnd.zuno.okf.corp.v1
        layers      application/vnd.zuno.okf.policies.v1.tar+gzip (policies/)
                    application/vnd.zuno.okf.index.v1+json (agent digests)

Layers are deterministic (sorted entries, mtime 0, uid/gid 0, mode 0644) and
an agent manifest's annotations depend only on that agent's own history, so
an agent whose files did not change keeps its digest from one release to the
next, whatever else changed.

Versions: `VERSION` at the root is the release version; `agents/<name>/VERSION`
is each agent's own version. Both are bumped by hand on `devel`;
`check-versions` refuses a merge to `main` that would reuse a released
version or change an agent's files without bumping its version.

Commands, run from the repository root:
    okf_release.py check-versions
    okf_release.py build --out DIR
    okf_release.py publish --registry quay.io/zuno --channel release --sha SHA
    okf_release.py publish --registry quay.io/zuno --channel devel --sha SHA
    okf_release.py publish --oci-layout DIR --channel release --sha SHA   (local test)
    okf_release.py changelog --previous v0.1.0
"""
from __future__ import annotations

import argparse
import dataclasses
import gzip
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from typing import Dict, List, Optional, Sequence, Tuple

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / "agents"
POLICIES_DIR = REPO_ROOT / "policies"
SOURCE_URL = "https://github.com/startxfr/zuno-demo-agents"

AGENT_ARTIFACT_TYPE = "application/vnd.zuno.okf.bundle.v2"
AGENT_LAYER_TYPE = "application/vnd.zuno.okf.bundle.v2.tar+gzip"
CORP_ARTIFACT_TYPE = "application/vnd.zuno.okf.corp.v1"
POLICIES_LAYER_TYPE = "application/vnd.zuno.okf.policies.v1.tar+gzip"
INDEX_LAYER_TYPE = "application/vnd.zuno.okf.index.v1+json"

RUNTIME_FILES = ("agent.okf.md",)
RUNTIME_DIRS = ("tasks", "prompts", "skills", "tools", "rag", "policies")
EXCLUDED_NAMES = {"README.md"}
CHANNELS = ("release", "devel", "main")

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ReleaseError(RuntimeError):
    pass


# --- versions -----------------------------------------------------------------

def parse_semver(text: str, where: str) -> Tuple[int, int, int]:
    m = SEMVER_RE.match(text.strip())
    if not m:
        raise ReleaseError(f"{where}: {text.strip()!r} is not a MAJOR.MINOR.PATCH version")
    return tuple(int(x) for x in m.groups())  # type: ignore[return-value]


def read_version(path: pathlib.Path) -> str:
    if not path.is_file():
        raise ReleaseError(f"{path.relative_to(REPO_ROOT)} is missing")
    text = path.read_text(encoding="utf-8").strip()
    parse_semver(text, str(path.relative_to(REPO_ROOT)))
    return text


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise ReleaseError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.strip()


def latest_tag(prefix: str) -> Optional[Tuple[str, Tuple[int, int, int]]]:
    """Highest `<prefix>MAJOR.MINOR.PATCH` tag, or None."""
    best: Optional[Tuple[str, Tuple[int, int, int]]] = None
    for tag in git("tag", "--list", f"{prefix}*").splitlines():
        rest = tag[len(prefix):]
        if SEMVER_RE.match(rest):
            version = parse_semver(rest, tag)
            if best is None or version > best[1]:
                best = (tag, version)
    return best


def agent_dirs() -> List[pathlib.Path]:
    return sorted(p.parent for p in AGENTS_DIR.glob("*/agent.okf.md"))


def runtime_files(agent_dir: pathlib.Path) -> List[pathlib.Path]:
    files = [agent_dir / name for name in RUNTIME_FILES if (agent_dir / name).is_file()]
    for name in RUNTIME_DIRS:
        root = agent_dir / name
        if root.is_dir():
            files += [p for p in root.rglob("*") if p.is_file() and p.name not in EXCLUDED_NAMES]
    return sorted(files, key=lambda p: p.relative_to(agent_dir).as_posix())


def policy_files() -> List[pathlib.Path]:
    return sorted((p for p in POLICIES_DIR.rglob("*") if p.is_file() and p.name not in EXCLUDED_NAMES),
                  key=lambda p: p.relative_to(POLICIES_DIR).as_posix())


def runtime_changed_since(tag: str, agent_dir: pathlib.Path) -> bool:
    paths = [p.relative_to(REPO_ROOT).as_posix() for p in runtime_files(agent_dir)]
    old = git("ls-tree", "-r", "--name-only", tag, "--", agent_dir.relative_to(REPO_ROOT).as_posix())
    old_runtime = {line for line in old.splitlines()
                   if _is_runtime(pathlib.PurePosixPath(line).relative_to(agent_dir.relative_to(REPO_ROOT).as_posix()))}
    if old_runtime != set(paths):
        return True
    result = subprocess.run(["git", "diff", "--quiet", tag, "--", *paths], cwd=REPO_ROOT)
    return result.returncode != 0


def _is_runtime(rel: pathlib.PurePosixPath) -> bool:
    if rel.name in EXCLUDED_NAMES:
        return False
    if len(rel.parts) == 1:
        return rel.name in RUNTIME_FILES
    return rel.parts[0] in RUNTIME_DIRS


def check_versions() -> List[str]:
    """Problems that must block a merge to main; empty when releasable."""
    problems: List[str] = []
    try:
        version = read_version(REPO_ROOT / "VERSION")
        last = latest_tag("v")
        if last and parse_semver(version, "VERSION") <= last[1]:
            problems.append(f"VERSION {version} is not greater than the last release {last[0]}: bump it")
    except ReleaseError as exc:
        problems.append(str(exc))
    for agent_dir in agent_dirs():
        name = agent_dir.name
        try:
            agent_version = read_version(agent_dir / "VERSION")
        except ReleaseError as exc:
            problems.append(str(exc))
            continue
        last = latest_tag(f"{name}-v")
        if last is None:
            continue
        current = parse_semver(agent_version, f"agents/{name}/VERSION")
        if current < last[1]:
            problems.append(f"agents/{name}/VERSION {agent_version} is lower than the released {last[0]}")
        elif current == last[1] and runtime_changed_since(last[0], agent_dir):
            problems.append(f"agents/{name} changed since {last[0]} but agents/{name}/VERSION "
                            f"is still {agent_version}: bump it")
    return problems


# --- layers -------------------------------------------------------------------

def build_layer(root: pathlib.Path, files: Sequence[pathlib.Path]) -> bytes:
    """Deterministic gzipped tar of `files`, named relative to `root`."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for path in sorted(files, key=lambda p: p.relative_to(root).as_posix()):
                data = path.read_bytes()
                info = tarfile.TarInfo(path.relative_to(root).as_posix())
                info.size, info.mode, info.mtime = len(data), 0o644, 0
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def okf_version(agent_dir: pathlib.Path) -> str:
    text = (agent_dir / "agent.okf.md").read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    front = yaml.safe_load(text[4:end]) if text.startswith("---\n") and end > 0 else {}
    return str((front or {}).get("okf_version", "unknown"))


@dataclasses.dataclass
class AgentBuild:
    name: str
    version: str
    okf_version: str
    revision: str
    created: str
    layer: bytes

    def annotations(self) -> Dict[str, str]:
        return {
            "org.opencontainers.image.source": SOURCE_URL,
            "org.opencontainers.image.revision": self.revision,
            "org.opencontainers.image.created": self.created,
            "org.opencontainers.image.version": self.version,
            "zuno.okf.agent": self.name,
            "zuno.okf.version": self.okf_version,
        }


def build_agent(agent_dir: pathlib.Path) -> AgentBuild:
    rel = agent_dir.relative_to(REPO_ROOT).as_posix()
    revision = git("log", "-1", "--format=%H", "--", rel)
    created = git("log", "-1", "--format=%cI", "--", rel)
    if not revision:
        raise ReleaseError(f"{rel} has no commit: commit it before building")
    return AgentBuild(
        name=agent_dir.name,
        version=read_version(agent_dir / "VERSION"),
        okf_version=okf_version(agent_dir),
        revision=revision,
        created=created,
        layer=build_layer(agent_dir, runtime_files(agent_dir)),
    )


def corp_index(release: str, channel: str, agents: Dict[str, Tuple[AgentBuild, str]]) -> bytes:
    doc = {
        "schemaVersion": 1,
        "release": release,
        "channel": channel,
        "agents": [
            {"name": name, "version": build.version, "okfVersion": build.okf_version, "reference": ref}
            for name, (build, ref) in sorted(agents.items())
        ],
    }
    return (json.dumps(doc, indent=2, sort_keys=True) + "\n").encode("utf-8")


# --- registry -----------------------------------------------------------------

class Registry:
    """Thin `oras` wrapper; a target is a registry prefix or a local OCI layout."""

    def __init__(self, registry: Optional[str], oci_layout: Optional[pathlib.Path], oras_bin: str = "oras"):
        if bool(registry) == bool(oci_layout):
            raise ReleaseError("give exactly one of --registry or --oci-layout")
        self.registry = registry.rstrip("/") if registry else None
        self.oci_layout = oci_layout
        self.oras = shutil.which(oras_bin)
        if self.oras is None:
            raise ReleaseError(f"{oras_bin} not found on PATH")

    def repository(self, name: str) -> str:
        if self.registry:
            return f"{self.registry}/okf-{name}"
        return str(self.oci_layout / f"okf-{name}")

    def _layout_flag(self) -> List[str]:
        return ["--oci-layout"] if self.oci_layout else []

    def resolve(self, repository: str, tag: str) -> Optional[str]:
        result = subprocess.run([self.oras, "resolve", *self._layout_flag(), f"{repository}:{tag}"],
                                capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None

    def push(self, repository: str, tag: str, artifact_type: str, annotations: Dict[str, str],
             layers: Sequence[Tuple[str, bytes, str]]) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            args = [self.oras, "push", *self._layout_flag(), f"{repository}:{tag}",
                    "--artifact-type", artifact_type, "--format", "json"]
            for key, value in sorted(annotations.items()):
                args += ["--annotation", f"{key}={value}"]
            for filename, data, media_type in layers:
                (pathlib.Path(tmp) / filename).write_bytes(data)
                args.append(f"{filename}:{media_type}")
            result = subprocess.run(args, cwd=tmp, capture_output=True, text=True)
        if result.returncode != 0:
            raise ReleaseError(f"oras push {repository}:{tag} failed: {(result.stderr or result.stdout).strip()}")
        try:
            return json.loads(result.stdout)["digest"]
        except (ValueError, KeyError) as exc:
            raise ReleaseError(f"unexpected oras output: {result.stdout.strip()[:300]}") from exc

    def reference(self, repository: str, digest: str) -> str:
        return f"{repository}@{digest}"


def publish(registry: Registry, channel: str, sha: str) -> Dict[str, object]:
    """Push every agent then the corp artifact; return the references."""
    if channel not in CHANNELS:
        raise ReleaseError(f"channel must be one of {CHANNELS}")
    release = read_version(REPO_ROOT / "VERSION")
    short = sha[:12]
    pushed: Dict[str, Tuple[AgentBuild, str]] = {}
    for agent_dir in agent_dirs():
        build = build_agent(agent_dir)
        repository = registry.repository(build.name)
        tag = f"{build.name}-v{build.version}" if channel == "release" else f"{channel}-{short}"
        digest = registry.push(repository, tag, AGENT_ARTIFACT_TYPE, build.annotations(),
                               [("okf-bundle.tar.gz", build.layer, AGENT_LAYER_TYPE)])
        if channel == "release":
            _refuse_moved_tag(registry, repository, tag, digest)
        pushed[build.name] = (build, registry.reference(repository, digest))

    corp_repository = registry.repository("corp")
    corp_tag = f"v{release}" if channel == "release" else f"{channel}-{short}"
    if channel == "release" and registry.resolve(corp_repository, corp_tag):
        raise ReleaseError(f"{corp_repository}:{corp_tag} already exists: releases are immutable")
    created = git("log", "-1", "--format=%cI", sha)
    corp_digest = registry.push(
        corp_repository, corp_tag, CORP_ARTIFACT_TYPE,
        {
            "org.opencontainers.image.source": SOURCE_URL,
            "org.opencontainers.image.revision": sha,
            "org.opencontainers.image.created": created,
            "org.opencontainers.image.version": release,
            "zuno.okf.release": release,
            "zuno.okf.channel": channel,
        },
        [("okf-policies.tar.gz", build_layer(POLICIES_DIR, policy_files()), POLICIES_LAYER_TYPE),
         ("okf-index.json", corp_index(release, channel, pushed), INDEX_LAYER_TYPE)],
    )
    return {
        "release": release,
        "channel": channel,
        "corp": registry.reference(corp_repository, corp_digest),
        "agents": {name: ref for name, (_, ref) in sorted(pushed.items())},
    }


def _refuse_moved_tag(registry: Registry, repository: str, tag: str, digest: str) -> None:
    # The push already happened; a different digest under an existing release
    # tag means the version gate was bypassed. Say so loudly: the operator
    # pins digests, so nothing deployed moves, but the tag is now wrong.
    current = registry.resolve(repository, tag)
    if current and current != digest:
        raise ReleaseError(f"{repository}:{tag} resolved to {current}, expected {digest}")


# --- changelog ----------------------------------------------------------------

def previous_release_base(tag: Optional[str]) -> Optional[str]:
    """The stable commit a release tag was cut from (second parent of the tag commit)."""
    if not tag:
        return None
    parents = git("rev-list", "--parents", "-n", "1", f"{tag}^{{commit}}").split()
    return parents[2] if len(parents) > 2 else parents[0]


def changelog(previous: Optional[str], date: str) -> str:
    release = read_version(REPO_ROOT / "VERSION")
    base = previous_release_base(previous)
    rev_range = f"{base}..HEAD" if base else "HEAD"
    commits = git("log", "--no-merges", "--format=- %s (%h)", rev_range).splitlines()
    lines = [f"## v{release} - {date}", "", "Agents:", ""]
    for agent_dir in agent_dirs():
        lines.append(f"- `{agent_dir.name}` {read_version(agent_dir / 'VERSION')}")
    lines += ["", "Changes:", ""] + (commits or ["- no change"]) + [""]
    return "\n".join(lines)


# --- cli ----------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check-versions", help="refuse an unreleasable VERSION state")
    build = sub.add_parser("build", help="write the layers and their metadata, no push")
    build.add_argument("--out", type=pathlib.Path, required=True)
    pub = sub.add_parser("publish", help="push agents and the corp artifact")
    pub.add_argument("--registry", help="e.g. quay.io/zuno")
    pub.add_argument("--oci-layout", type=pathlib.Path, help="local OCI layout root, for tests")
    pub.add_argument("--channel", choices=CHANNELS, required=True)
    pub.add_argument("--sha", required=True, help="the commit being published")
    pub.add_argument("--output", type=pathlib.Path, help="also write the references as JSON here")
    log = sub.add_parser("changelog", help="print the CHANGELOG section of the current VERSION")
    log.add_argument("--previous", help="the previous release tag, if any")
    log.add_argument("--date", required=True)
    args = parser.parse_args(argv)

    try:
        if args.command == "check-versions":
            problems = check_versions()
            if problems:
                print(f"{len(problems)} version issue(s):")
                for p in problems:
                    print(f"  ✗ {p}")
                print("\nRESULT: FAIL - this state cannot be released from main.")
                return 1
            print("RESULT: PASS - VERSION and every agent VERSION are releasable.")
        elif args.command == "build":
            args.out.mkdir(parents=True, exist_ok=True)
            meta = {}
            for agent_dir in agent_dirs():
                b = build_agent(agent_dir)
                (args.out / f"okf-{b.name}.tar.gz").write_bytes(b.layer)
                meta[b.name] = b.annotations()
            (args.out / "okf-policies.tar.gz").write_bytes(build_layer(POLICIES_DIR, policy_files()))
            (args.out / "metadata.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
            print(args.out)
        elif args.command == "publish":
            refs = publish(Registry(args.registry, args.oci_layout), args.channel, args.sha)
            text = json.dumps(refs, indent=2, sort_keys=True)
            if args.output:
                args.output.write_text(text + "\n")
            print(text)
        else:
            print(changelog(args.previous, args.date))
    except ReleaseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
