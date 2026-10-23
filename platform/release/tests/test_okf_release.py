"""Tests for platform/release/okf_release.py, against a throwaway git repository.

Run from the repository root:
    python3 -m unittest discover -s platform/release/tests
"""
from __future__ import annotations

import gzip
import io
import json
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import okf_release  # noqa: E402

AGENT_MD = """---
okf_version: v0.2
type: agent
title: Demo
zuno:
  name: demo
---
Body.
"""


def sh(cwd: pathlib.Path, *args: str) -> str:
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class RepoTestCase(unittest.TestCase):
    """A git repository with one agent, wired into okf_release's globals."""

    def setUp(self) -> None:
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.root = self.tmp / "repo"
        agent = self.root / "agents" / "demo"
        (agent / "tasks").mkdir(parents=True)
        (agent / "tests").mkdir()
        (self.root / "policies" / "tools").mkdir(parents=True)
        (agent / "agent.okf.md").write_text(AGENT_MD)
        (agent / "tasks" / "do.md").write_text("---\ntype: task\n---\n")
        (agent / "tasks" / "README.md").write_text("notes\n")
        (agent / "tests" / "test_x.py").write_text("pass\n")
        (agent / "README.md").write_text("readme\n")
        (agent / "VERSION").write_text("1.0.0\n")
        (self.root / "policies" / "tools" / "tool-policy.yaml").write_text("tools: {}\n")
        (self.root / "VERSION").write_text("0.1.0\n")
        sh(self.root, "git", "init", "-q", "-b", "main")
        sh(self.root, "git", "config", "user.email", "t@example.com")
        sh(self.root, "git", "config", "user.name", "t")
        self.commit("initial")
        self.saved = (okf_release.REPO_ROOT, okf_release.AGENTS_DIR, okf_release.POLICIES_DIR)
        okf_release.REPO_ROOT = self.root
        okf_release.AGENTS_DIR = self.root / "agents"
        okf_release.POLICIES_DIR = self.root / "policies"

    def tearDown(self) -> None:
        okf_release.REPO_ROOT, okf_release.AGENTS_DIR, okf_release.POLICIES_DIR = self.saved
        shutil.rmtree(self.tmp)

    def commit(self, message: str) -> None:
        sh(self.root, "git", "add", "-A")
        sh(self.root, "git", "commit", "-q", "-m", message)

    def tag(self, name: str) -> None:
        sh(self.root, "git", "tag", "-a", name, "-m", name)


class LayerTest(RepoTestCase):
    def names(self, layer: bytes) -> list:
        with tarfile.open(fileobj=io.BytesIO(gzip.decompress(layer))) as tar:
            return tar.getnames()

    def test_runtime_files_only(self) -> None:
        build = okf_release.build_agent(self.root / "agents" / "demo")
        self.assertEqual(self.names(build.layer), ["agent.okf.md", "tasks/do.md"])

    def test_layer_is_deterministic(self) -> None:
        agent = self.root / "agents" / "demo"
        first = okf_release.build_agent(agent).layer
        (agent / "tasks" / "do.md").touch()
        self.assertEqual(first, okf_release.build_agent(agent).layer)

    def test_annotations_follow_the_agent_history(self) -> None:
        build = okf_release.build_agent(self.root / "agents" / "demo")
        (self.root / "policies" / "tools" / "tool-policy.yaml").write_text("tools: {x: 1}\n")
        self.commit("policy only")
        again = okf_release.build_agent(self.root / "agents" / "demo")
        self.assertEqual(build.annotations(), again.annotations())
        self.assertEqual(again.annotations()["org.opencontainers.image.version"], "1.0.0")
        self.assertEqual(again.annotations()["zuno.okf.version"], "v0.2")

    def test_corp_index_lists_agent_references(self) -> None:
        build = okf_release.build_agent(self.root / "agents" / "demo")
        index = json.loads(okf_release.corp_index("0.1.0", "release", {"demo": (build, "r/okf-demo@sha256:1")}))
        self.assertEqual(index["agents"], [{"name": "demo", "version": "1.0.0", "okfVersion": "v0.2",
                                            "reference": "r/okf-demo@sha256:1"}])


class CorpSkillTest(RepoTestCase):
    """OKF v0.3 corp skills travel inside the agent artifact (skills/corp/<name>.md)."""

    def use_corp_skill(self) -> None:
        (self.root / "policies" / "skills").mkdir(parents=True)
        (self.root / "policies" / "skills" / "house-style.md").write_text("---\ntype: skill\n---\nBe brief.\n")
        (self.root / "agents" / "demo" / "tasks" / "do.md").write_text(
            "---\ntype: task\nzuno:\n  skills: [corp/house-style]\n---\n")
        self.commit("use a corp skill")

    def names(self, layer: bytes) -> list:
        with tarfile.open(fileobj=io.BytesIO(gzip.decompress(layer))) as tar:
            return tar.getnames()

    def test_corp_skill_is_embedded(self) -> None:
        self.use_corp_skill()
        layer = okf_release.build_agent(self.root / "agents" / "demo").layer
        self.assertEqual(self.names(layer), ["agent.okf.md", "skills/corp/house-style.md", "tasks/do.md"])

    def test_changed_corp_skill_needs_an_agent_bump(self) -> None:
        self.use_corp_skill()
        self.tag("v0.1.0")
        self.tag("demo-v1.0.0")
        (self.root / "VERSION").write_text("0.2.0\n")
        (self.root / "policies" / "skills" / "house-style.md").write_text("---\ntype: skill\n---\nBe briefer.\n")
        self.commit("change the corp skill")
        problems = okf_release.check_versions()
        self.assertEqual(len(problems), 1)
        self.assertIn("agents/demo changed since demo-v1.0.0", problems[0])

    def test_missing_corp_skill_stops_the_build(self) -> None:
        (self.root / "agents" / "demo" / "tasks" / "do.md").write_text(
            "---\ntype: task\nzuno:\n  skills: [corp/nope]\n---\n")
        with self.assertRaises(okf_release.ReleaseError):
            okf_release.build_agent(self.root / "agents" / "demo")


class VersionGateTest(RepoTestCase):
    def test_first_release_passes(self) -> None:
        self.assertEqual(okf_release.check_versions(), [])

    def test_release_version_must_grow(self) -> None:
        self.tag("v0.1.0")
        self.assertIn("VERSION 0.1.0 is not greater", okf_release.check_versions()[0])
        (self.root / "VERSION").write_text("0.2.0\n")
        self.assertEqual(okf_release.check_versions(), [])

    def test_changed_agent_must_bump(self) -> None:
        self.tag("v0.1.0")
        self.tag("demo-v1.0.0")
        (self.root / "VERSION").write_text("0.2.0\n")
        (self.root / "agents" / "demo" / "tasks" / "do.md").write_text("---\ntype: task\n---\nchanged\n")
        self.commit("change task")
        problems = okf_release.check_versions()
        self.assertEqual(len(problems), 1)
        self.assertIn("agents/demo changed since demo-v1.0.0", problems[0])
        (self.root / "agents" / "demo" / "VERSION").write_text("1.1.0\n")
        self.assertEqual(okf_release.check_versions(), [])

    def test_non_runtime_change_needs_no_agent_bump(self) -> None:
        self.tag("v0.1.0")
        self.tag("demo-v1.0.0")
        (self.root / "VERSION").write_text("0.2.0\n")
        (self.root / "agents" / "demo" / "README.md").write_text("better readme\n")
        (self.root / "agents" / "demo" / "tests" / "test_x.py").write_text("assert True\n")
        self.commit("docs and tests")
        self.assertEqual(okf_release.check_versions(), [])

    def test_new_runtime_file_counts_as_a_change(self) -> None:
        self.tag("v0.1.0")
        self.tag("demo-v1.0.0")
        (self.root / "VERSION").write_text("0.2.0\n")
        (self.root / "agents" / "demo" / "tasks" / "new.md").write_text("---\ntype: task\n---\n")
        self.commit("new task")
        self.assertIn("agents/demo changed", okf_release.check_versions()[0])

    def test_malformed_version(self) -> None:
        (self.root / "agents" / "demo" / "VERSION").write_text("v1\n")
        self.assertIn("not a MAJOR.MINOR.PATCH", okf_release.check_versions()[0])


class ChangelogTest(RepoTestCase):
    def test_changes_since_the_previous_release_base(self) -> None:
        base = sh(self.root, "git", "rev-parse", "HEAD")
        # A release tag commit: parents are (previous tag commit, stable).
        tree = sh(self.root, "git", "rev-parse", "HEAD^{tree}")
        tag_commit = sh(self.root, "git", "commit-tree", tree, "-p", base, "-p", base, "-m", "Release v0.1.0")
        sh(self.root, "git", "tag", "-a", "v0.1.0", tag_commit, "-m", "v0.1.0")
        (self.root / "VERSION").write_text("0.2.0\n")
        self.commit("feat: something new")
        text = okf_release.changelog("v0.1.0", "2026-10-22")
        self.assertIn("## v0.2.0 - 2026-10-22", text)
        self.assertIn("feat: something new", text)
        self.assertNotIn("initial", text)


if __name__ == "__main__":
    unittest.main()
