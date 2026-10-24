"""Presentation shapes of `zuno.ui` (zuno-demo WP-167).

unifai-operator copies `zuno.ui` into the agent's display block and the UnifAI
API refuses a value outside these shapes, so an agent that passes the OKF schema
but not this check would fail at emission. The patterns below mirror
`_DISPLAY_ICON` and `_DISPLAY_COLOR` in the UnifAI fork
(`multi-agent/lib/mas/blueprints/service.py`) and the OKF v0.3 schema.

Run from the repository root:
    python3 conformance/test_ui_display.py
"""
from __future__ import annotations

import copy
import pathlib
import re
import sys
import unittest

import yaml

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "platform" / "okf"))

import validate_okf_schema as schema  # noqa: E402

ICON = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")
COLOR = re.compile(r"^(#[0-9a-fA-F]{6}|[a-zA-Z]{3,30})$")
UI_FIELDS = ("displayName", "tileDescription", "color", "icon")

GOOD_ICONS = ["code", "drafting-compass", "clipboard-check", "a", "0", "x" * 40]
BAD_ICONS = ["", "Code", "code icon", "-code", "icon_1", "x" * 41, "../x", "https://x/y.svg"]
GOOD_COLORS = ["#0066CC", "#f0ab00", "teal", "rebeccapurple"]
BAD_COLORS = ["", "ab", "#fff", "#12345g", "0066CC", "dark-blue", "x" * 31, "rgb(0,0,0)"]


def frontmatter(path: pathlib.Path) -> dict:
    return yaml.safe_load(path.read_text().split("---")[1])


def agent_files():
    return sorted((REPO / "agents").glob("*/agent.okf.md"))


class ShapeTests(unittest.TestCase):
    def test_icon_shape(self):
        for value in GOOD_ICONS:
            self.assertTrue(ICON.match(value), value)
        for value in BAD_ICONS:
            self.assertFalse(ICON.match(value), value)

    def test_color_shape(self):
        for value in GOOD_COLORS:
            self.assertTrue(COLOR.match(value), value)
        for value in BAD_COLORS:
            self.assertFalse(COLOR.match(value), value)


class SchemaTests(unittest.TestCase):
    """The v0.3 schema refuses what the operator refuses."""

    def setUp(self):
        self.validator = schema.validators()["v0.3"]["agent"]

    def agent_doc(self):
        doc = frontmatter(REPO / "conformance" / "cases" / "valid-v03-full" / "agents" / "gamma" / "agent.okf.md")
        return copy.deepcopy(doc)

    def errors(self, doc):
        return [e.message for e in self.validator.iter_errors(doc)]

    def test_fixture_is_valid(self):
        self.assertEqual(self.errors(self.agent_doc()), [])

    def test_bad_icon_is_refused(self):
        for value in BAD_ICONS:
            doc = self.agent_doc()
            doc["zuno"]["ui"]["icon"] = value
            self.assertTrue(self.errors(doc), f"icon {value!r} should be refused")

    def test_bad_color_is_refused(self):
        for value in BAD_COLORS:
            doc = self.agent_doc()
            doc["zuno"]["ui"]["color"] = value
            self.assertTrue(self.errors(doc), f"color {value!r} should be refused")

    def test_good_values_are_accepted(self):
        for icon, color in zip(GOOD_ICONS, GOOD_COLORS * 2):
            doc = self.agent_doc()
            doc["zuno"]["ui"]["icon"] = icon
            doc["zuno"]["ui"]["color"] = color
            self.assertEqual(self.errors(doc), [], (icon, color))


class RealAgentTests(unittest.TestCase):
    """Every agent of the corp artifact carries a display block the operator accepts,
    whatever its okf_version (the v0.2 schema stays free-form, the operator does not)."""

    def test_there_are_agents(self):
        self.assertTrue(agent_files())

    def test_every_agent_has_a_valid_ui_block(self):
        for path in agent_files():
            ui = (frontmatter(path).get("zuno") or {}).get("ui") or {}
            for field in UI_FIELDS:
                self.assertTrue(ui.get(field), f"{path.parent.name}: zuno.ui.{field} is missing")
            self.assertRegex(ui["icon"], ICON, f"{path.parent.name}: icon {ui['icon']!r}")
            self.assertRegex(ui["color"], COLOR, f"{path.parent.name}: color {ui['color']!r}")


if __name__ == "__main__":
    unittest.main()
