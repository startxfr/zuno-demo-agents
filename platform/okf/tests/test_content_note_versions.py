"""validate_okf_bundle accepts v0.2 and v0.3 content notes (rag/, tools/, policies/) in a bundle
(zuno-demo ADR-0579 clause 6) and still refuses any other version or a wrong type.

Not a conformance case: the readers of zuno-demo parse the agent index and the tasks, never the
notes; the notes are checked here and by the schema validator.

Run from the repository root:
    python3 platform/okf/tests/test_content_note_versions.py
"""
from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

import yaml

REPO = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "platform" / "supply-chain"))
sys.path.insert(0, str(REPO / "platform" / "okf"))

import validate_okf_bundle as validator  # noqa: E402
import validate_okf_schema as schema  # noqa: E402


def md(front: dict) -> str:
    return "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\nBody.\n"


def bundle(versions: dict) -> pathlib.Path:
    root = pathlib.Path(tempfile.mkdtemp())
    b = root / "agents" / "demo"
    for d in ("tasks", "rag", "tools", "policies"):
        (b / d).mkdir(parents=True)
    (b / "agent.okf.md").write_text(md({"okf_version": "v0.3", "type": "agent", "title": "Demo", "description": "d",
        "zuno": {"name": "demo", "status": "active", "tasks": ["ask"], "graph_shape": "retrieve_reason_respond",
                 "primary_task": "ask", "model": {"preferred_classification": "C1"},
                 "access": {"groups": ["agent_demo"]},
                 "ui": {"displayName": "Demo", "tileDescription": "d", "color": "#0066CC", "icon": "code"}}}))
    (b / "tasks" / "ask.md").write_text(md({"okf_version": "v0.3", "type": "task", "title": "Ask",
        "zuno": {"allowed_tools": ["search_docs"], "allowed_knowledge": ["knowledge.tech"]}}))
    (b / "rag" / "tech.md").write_text(md({"okf_version": versions["rag"], "type": "rag", "title": "Tech",
        "zuno": {"domain": "knowledge.tech", "used_by_tasks": ["ask"]}}))
    (b / "tools" / "search.md").write_text(md({"okf_version": versions["tool"], "type": "tool", "title": "Search",
        "zuno": {"capability": "search_docs", "used_by_tasks": ["ask"]}}))
    (b / "policies" / "scope.md").write_text(md({"okf_version": versions["policy"], "type": "policy", "title": "Scope",
        "zuno": {"applies_to": {"tasks": ["ask"], "tools": ["search_docs"]}}}))
    return b


class NoteVersions(unittest.TestCase):
    def validate(self, versions):
        b = bundle(versions)
        saved = validator.REPO_ROOT
        validator.REPO_ROOT = b.parents[1]
        try:
            return validator.validate_bundle(b, {"search_docs"}, {"knowledge.tech"})
        finally:
            validator.REPO_ROOT = saved

    def test_every_mix_of_v02_and_v03_notes_is_accepted(self):
        for rag in ("v0.2", "v0.3"):
            for tool in ("v0.2", "v0.3"):
                for policy in ("v0.2", "v0.3"):
                    findings = self.validate({"rag": rag, "tool": tool, "policy": policy})
                    self.assertEqual(findings, [], (rag, tool, policy, [f.message for f in findings]))

    def test_another_version_is_refused_by_note_kind(self):
        findings = [f.message for f in self.validate({"rag": "v0.9", "tool": "v0.3", "policy": "v0.1"})]
        self.assertEqual(len(findings), 2, findings)
        self.assertTrue(any("rag/tech.md: expected okf_version v0.2 or v0.3 and type rag" in m for m in findings))
        self.assertTrue(any("policies/scope.md: expected okf_version v0.2 or v0.3 and type policy" in m for m in findings))

    def test_v03_notes_match_their_v03_schemas(self):
        validators = schema.validators()
        b = bundle({"rag": "v0.3", "tool": "v0.3", "policy": "v0.3"})
        saved = schema.REPO_ROOT
        schema.REPO_ROOT = b.parents[1]
        try:
            self.assertEqual(schema.check_bundle(b, validators), [])
        finally:
            schema.REPO_ROOT = saved


if __name__ == "__main__":
    unittest.main()
