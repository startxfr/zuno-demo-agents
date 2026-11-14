"""The version dispatch of zuno-demo ADR-0615 clause 5, and the frozen profile 1.0 schemas.

Run from the repository root:
    python3 platform/okf/tests/test_okf_profile.py
"""
from __future__ import annotations

import pathlib
import sys
import unittest

import yaml

REPO = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "platform" / "okf"))

import build_profile_schemas  # noqa: E402
from okf_profile import UnsupportedVersion, at_least_v03, document_version  # noqa: E402


def doc(text: str) -> dict:
    return yaml.safe_load(text)


class DispatchTests(unittest.TestCase):
    def test_profile_1_0(self):
        self.assertEqual(document_version(doc('okf_version: "0.2"\nzuno: {profile: "1.0"}')), "1.0")

    def test_legacy_versions(self):
        self.assertEqual(document_version(doc("okf_version: v0.2")), "v0.2")
        self.assertEqual(document_version(doc("okf_version: v0.3\nzuno: {name: a}")), "v0.3")

    def test_refusals_are_named(self):
        cases = {
            'okf_version: "0.2"': "unsupported zuno.profile None",
            'okf_version: "0.2"\nzuno: {profile: "2.0"}': "unsupported zuno.profile '2.0'",
            'okf_version: "0.2"\nzuno: {profile: 1.0}': "unsupported zuno.profile 1.0",
            "okf_version: 0.2\nzuno: {profile: \"1.0\"}": "unsupported okf_version 0.2",
            "okf_version: v0.9": "unsupported okf_version 'v0.9'",
            "type: agent": "unsupported okf_version None",
            'okf_version: v0.3\nzuno: {profile: "1.0"}': "zuno.profile is only valid with okf_version",
        }
        for text, needle in cases.items():
            with self.assertRaises(UnsupportedVersion, msg=text) as ctx:
                document_version(doc(text))
            self.assertIn(needle, str(ctx.exception), text)

    def test_narrowing_level_includes_the_profile(self):
        self.assertFalse(at_least_v03("v0.2"))
        self.assertTrue(at_least_v03("v0.3"))
        self.assertTrue(at_least_v03("1.0"))


class FrozenSchemaTests(unittest.TestCase):
    def test_committed_schemas_match_the_generator_and_their_hashes(self):
        self.assertEqual(build_profile_schemas.main(["--check"]), 0)

    def test_no_profile_schema_names_one_platform(self):
        for name, text in build_profile_schemas.render().items():
            self.assertIsNone(build_profile_schemas.FORBIDDEN.search(text.replace("zuno-okf-profile", "")), name)


if __name__ == "__main__":
    unittest.main()
