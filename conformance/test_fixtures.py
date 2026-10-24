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

import check_narrowing as narrow  # noqa: E402
import validate_okf_schema as schema  # noqa: E402

PREFIXES = ("valid-", "security-", "invalid-", "narrowing-")


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

    def _findings(self, case):
        corp = narrow.Corp()
        return [f for b in sorted((case / "agents").iterdir()) for f in narrow.check_bundle(b, corp)]

    def test_valid_cases_only_narrow_the_corp_policies(self):
        for case in self.cases():
            if case.name.startswith("valid-"):
                self.assertEqual(self._findings(case), [], case.name)

    def test_narrowing_cases_load_but_are_refused_by_the_narrowing_check(self):
        validators = schema.validators()
        for case in self.cases():
            if not case.name.startswith("narrowing-"):
                continue
            for bundle in sorted((case / "agents").iterdir()):
                self.assertEqual(schema.check_bundle(bundle, validators), [], f"{case.name}/{bundle.name}")
            needle = json.loads((case / "expected.json").read_text())["delegation"]["narrowing_error"]
            self.assertTrue(any(needle in f for f in self._findings(case)), f"{case.name}: {needle!r}")

    def test_the_delegation_section_matches_what_the_bundles_declare(self):
        import yaml

        for case in self.cases():
            section = json.loads((case / "expected.json").read_text()).get("delegation")
            if section is None:
                continue
            self.assertEqual(sorted(section["agents"]), sorted(p.name for p in (case / "agents").iterdir()), case.name)
            for agent, want in section["agents"].items():
                text = (case / "agents" / agent / "agent.okf.md").read_text()
                zuno = yaml.safe_load(text.split("---", 2)[1]).get("zuno") or {}
                self.assertEqual((zuno.get("delegation") or {}).get("targets") or [], want["targets"], case.name)
                self.assertEqual(((zuno.get("limits") or {}).get("delegation") or {}).get("max_depth"),
                                 want["max_depth"], case.name)

    def test_security_cases_are_schema_invalid_on_purpose(self):
        validators = schema.validators()
        for case in self.cases():
            if not case.name.startswith("security-"):
                continue
            findings = [f for b in sorted((case / "agents").iterdir()) for f in schema.check_bundle(b, validators)]
            self.assertTrue(findings, f"{case.name} should be refused by the schema yet still be read deny-by-default")


if __name__ == "__main__":
    unittest.main()
