"""tool-policy.yaml `access` (zuno-demo ADR-0406, ADR-0409): every committed entry
declares it, and the validator refuses a value other than read or write.

Run from the repository root:
    python3 platform/okf/tests/test_tool_policy_access.py
"""
from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

import yaml

REPO = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "platform" / "supply-chain"))

import validate_okf_bundle as validator  # noqa: E402


class ToolPolicyAccess(unittest.TestCase):
    def _policy(self, entries):
        path = pathlib.Path(tempfile.mkdtemp()) / "tool-policy.yaml"
        path.write_text(yaml.safe_dump({"tools": entries}))
        return path

    def test_every_committed_entry_declares_read_or_write(self):
        doc = yaml.safe_load(validator.TOOL_POLICY_PATH.read_text())
        for entry in doc["tools"]:
            self.assertIn(entry.get("access"), ("read", "write"), entry["tool"])
        self.assertEqual(validator.tool_policy_findings(), [])

    def test_the_mutating_tools_are_write(self):
        by_cap = {e.get("capability") or e["tool"]: e["access"]
                  for e in yaml.safe_load(validator.TOOL_POLICY_PATH.read_text())["tools"]}
        for cap in ("confluence.page.create", "salesforce.opportunity.update", "git.repository.delete", "aap.cluster.audit"):
            self.assertEqual(by_cap[cap], "write", cap)
        for cap in ("confluence.page.search", "diagram.generation.create", "aap.platform.audit"):
            self.assertEqual(by_cap[cap], "read", cap)

    def test_an_unknown_value_is_a_finding_and_absence_is_not(self):
        bad = self._policy([{"tool": "a", "access": "rw"}, {"tool": "b"}])
        findings = validator.tool_policy_findings(bad)
        self.assertEqual(len(findings), 1)
        self.assertIn("access must be 'read' or 'write'", findings[0].message)


if __name__ == "__main__":
    unittest.main()
