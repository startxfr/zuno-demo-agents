"""Every task that reads Confluence or the technical documentation is local only at every level
(zuno-demo WP-187).

UnifAI sets a turn's data level from what the task declares, not from what the retriever returned, and the
external providers accept C1 and C2. So a task whose context can hold Confluence content must carry
`local_only_for: [C1, C2, C3]` in the corp routing policy, or an external fallback could receive that content.

Run from the repository root:
    python3 platform/okf/tests/test_confluence_tasks_local_only.py
"""
from __future__ import annotations

import pathlib
import re
import unittest

import yaml

REPO = pathlib.Path(__file__).resolve().parents[3]
POLICY = REPO / "policies" / "model-routing" / "model-routing-policy.yaml"
LEVELS = {"C1", "C2", "C3"}


def _reading_tasks():
    for path in sorted((REPO / "agents").glob("*/tasks/*.md")):
        match = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
        if not match:
            continue
        zuno = (yaml.safe_load(match.group(1)) or {}).get("zuno") or {}
        if "search_confluence" in (zuno.get("allowed_tools") or []) or "knowledge.tech" in (zuno.get("allowed_knowledge") or []):
            yield path.parts[-3], path.stem


class ConfluenceTasksLocalOnly(unittest.TestCase):
    def test_every_task_reading_confluence_is_local_only_at_every_level(self):
        prefs = {(p["agent"], p["task"]): p for p in yaml.safe_load(POLICY.read_text())["preferences"]}
        tasks = list(_reading_tasks())
        self.assertTrue(tasks, "no task reads Confluence or knowledge.tech: the discovery is broken")
        for key in tasks:
            self.assertIn(key, prefs, f"{key} has no routing entry")
            self.assertTrue(LEVELS <= set(prefs[key].get("local_only_for") or []), f"{key} can reach an external model")


if __name__ == "__main__":
    unittest.main()
