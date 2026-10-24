"""Self-check of the conformance fixtures (see conformance/README.md).

Run from the repository root:
    python3 conformance/test_fixtures.py
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
CASES = pathlib.Path(__file__).resolve().parent / "cases"
sys.path.insert(0, str(REPO / "platform" / "okf"))

import validate_okf_schema as schema  # noqa: E402

PREFIXES = ("valid-", "security-", "invalid-")


class FixtureTests(unittest.TestCase):
    def cases(self):
        return sorted(p for p in CASES.iterdir() if p.is_dir())

    def test_every_case_has_a_known_prefix_and_expected_sections(self):
        self.assertTrue(self.cases())
        for case in self.cases():
            self.assertTrue(case.name.startswith(PREFIXES), case.name)
            expected = json.loads((case / "expected.json").read_text())
            self.assertTrue(expected["description"], case.name)
            self.assertIn("mcp_gateway", expected, case.name)
            self.assertIn("admission", expected, case.name)
            refused = case.name.startswith("invalid-")
            self.assertEqual(expected["mcp_gateway"]["load_error"] is not None, refused, case.name)
            self.assertEqual(expected["admission"]["error"] is not None, refused, case.name)

    def test_valid_cases_match_the_schemas(self):
        validators = schema.validators()
        for case in self.cases():
            if not case.name.startswith("valid-"):
                continue
            for bundle in sorted((case / "agents").iterdir()):
                self.assertEqual(schema.check_bundle(bundle, validators), [], f"{case.name}/{bundle.name}")

    def test_security_cases_are_schema_invalid_on_purpose(self):
        validators = schema.validators()
        for case in self.cases():
            if not case.name.startswith("security-"):
                continue
            findings = [f for b in sorted((case / "agents").iterdir()) for f in schema.check_bundle(b, validators)]
            self.assertTrue(findings, f"{case.name} should be refused by the schema yet still be read deny-by-default")


if __name__ == "__main__":
    unittest.main()
