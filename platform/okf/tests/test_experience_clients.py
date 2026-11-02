"""Experience clients (zuno-demo ADR-0592): experience-clients/<name> declares
who may use a logical agent name at the mcp-gateway and which tools its tasks
allow. The validator refuses what would make a client more than that: a name
that is also an agent's, RAG, and a tool above the client's classification.

Run from the repository root:
    python3 platform/okf/tests/test_experience_clients.py
"""
from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "platform" / "supply-chain"))

import validate_okf_bundle as validator  # noqa: E402

CLIENT = """---
okf_version: v0.3
type: experience-client
title: Chat UI
description: test client
zuno:
  name: {name}
  tasks: [chat]
  classification: C1
  access:
    groups: [sales]
---
"""
TASK = """---
okf_version: v0.3
type: task
title: Chat
zuno:
  allowed_tools: [{tools}]
{extra}---
"""


class ExperienceClients(unittest.TestCase):
    def setUp(self):
        self.saved_root = validator.REPO_ROOT
        self.root = pathlib.Path(tempfile.mkdtemp())
        validator.REPO_ROOT = self.root

    def tearDown(self):
        validator.REPO_ROOT = self.saved_root

    def client(self, name="chat-ui", tools="list_drive_files", extra=""):
        d = self.root / "experience-clients" / name
        (d / "tasks").mkdir(parents=True)
        (d / "client.okf.md").write_text(CLIENT.format(name=name))
        (d / "tasks" / "chat.md").write_text(TASK.format(tools=tools, extra=extra))
        return d

    def findings(self, d, agents=()):
        return [f.message for f in validator.validate_client(d, validator._known_tool_names(), set(agents))]

    def test_committed_clients_are_valid(self):
        validator.REPO_ROOT = self.saved_root
        clients = sorted(p for p in validator.CLIENTS_DIR.iterdir() if p.is_dir())
        self.assertIn("open-webui", [c.name for c in clients])
        agents = {p.name for p in validator.AGENTS_DIR.iterdir() if p.is_dir()}
        for c in clients:
            self.assertEqual([f.message for f in validator.validate_client(c, validator._known_tool_names(), agents)], [])

    def test_a_c1_tool_is_accepted(self):
        self.assertEqual(self.findings(self.client()), [])

    def test_a_tool_above_the_classification_is_refused(self):
        found = self.findings(self.client(tools="search_confluence"))
        self.assertTrue(any("needs C2, above the client's classification C1" in f for f in found), found)

    def test_an_unknown_tool_is_refused(self):
        found = self.findings(self.client(tools="no_such_tool"))
        self.assertTrue(any("unknown tool" in f for f in found), found)

    def test_a_name_shared_with_an_agent_is_refused(self):
        found = self.findings(self.client(name="tekos"), agents=["tekos"])
        self.assertTrue(any("is also an agent" in f for f in found), found)

    def test_rag_is_refused(self):
        found = self.findings(self.client(extra="  allowed_knowledge: [knowledge.tech]\n"))
        self.assertTrue(any("allowed_knowledge must be empty" in f for f in found), found)


if __name__ == "__main__":
    unittest.main()
