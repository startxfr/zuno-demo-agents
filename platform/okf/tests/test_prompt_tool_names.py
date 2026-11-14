"""A profile 1.0 prompt or skill names a tool by its capability (zuno-demo ADR-0615 clause 10).

The runtime offers a tool to the model under its `capability` (for example `drive.document.search`), not under the
legacy `tool` name of the tool policy (`list_drive_files`). A prompt that names the legacy name points the model at
a tool it is never offered, so validate_okf_bundle refuses it.

Run from the repository root:
    python3 platform/okf/tests/test_prompt_tool_names.py
"""
from __future__ import annotations

import pathlib
import shutil
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "platform" / "supply-chain"))

import validate_okf_bundle as validator  # noqa: E402

PROMPT = "agents/tekos/prompts/find-relevant-docs.md"


class PromptToolNames(unittest.TestCase):
    def findings(self, rewrite) -> list:
        root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        shutil.copytree(REPO / "agents" / "tekos", root / "agents" / "tekos")
        prompt = root / PROMPT
        prompt.write_text(rewrite(prompt.read_text(encoding="utf-8")), encoding="utf-8")
        saved = validator.REPO_ROOT
        validator.REPO_ROOT = root
        try:
            found = validator.validate_bundle(root / "agents" / "tekos", validator._known_tool_names(),
                                              validator._known_knowledge_domains())
        finally:
            validator.REPO_ROOT = saved
        return [f.message for f in found if "names the tool" in f.message]

    def test_capability_names_pass(self):
        self.assertEqual(self.findings(lambda text: text), [])

    def test_legacy_tool_name_is_refused(self):
        found = self.findings(lambda text: text.replace("`drive.document.search`", "`list_drive_files`"))
        self.assertEqual(len(found), 1, found)
        self.assertIn("'list_drive_files'", found[0])
        self.assertIn("'drive.document.search'", found[0])

    def test_untagged_prose_is_not_checked(self):
        # Only a backticked name is a tool reference; the word in prose is not.
        self.assertEqual(self.findings(lambda text: text + "\nThe list_drive_files name is legacy.\n"), [])


if __name__ == "__main__":
    unittest.main()
