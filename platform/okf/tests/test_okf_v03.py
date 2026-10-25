"""OKF v0.3 (zuno-demo ADR-0579): schemas and the narrowing rule.

A complete v0.3 bundle (skills, model roles, guardrails, limits) must match
the v0.3 schemas, and each way of widening the corp policies must be
refused by check_narrowing.py.

Run from the repository root:
    python3 platform/okf/tests/test_okf_v03.py
"""
from __future__ import annotations

import pathlib
import shutil
import sys
import tempfile
import unittest

import yaml

OKF = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OKF))

import check_narrowing as narrow  # noqa: E402
import validate_okf_schema as schema  # noqa: E402

AGENT = {
    "okf_version": "v0.3", "type": "agent", "title": "Demo", "description": "A v0.3 example.",
    "zuno": {
        "name": "demo", "status": "active", "tasks": ["ask"], "graph_shape": "retrieve_reason_respond",
        "primary_task": "ask", "access": {"groups": ["agent_demo"]},
        "ui": {"displayName": "Demo", "tileDescription": "A v0.3 example.", "color": "#0066CC", "icon": "code"},
        "model": {"preferred_classification": "C2"},
        "models": {"preferred": ["reasoning"], "forbidden": ["general-external"]},
        "guardrails": {"mode": "block", "categories": ["pii"]},
        "limits": {"max_tokens": 2048, "max_concurrent_requests": 4, "quota_class": "standard",
                   "memory": {"history": {"enabled": True, "max_turns": 4, "token_budget": 4000}}},
    },
}
TASK = {
    "okf_version": "v0.3", "type": "task", "title": "Ask",
    "zuno": {"allowed_tools": ["search_docs", "web_search"], "allowed_knowledge": ["knowledge.tech"],
             "skills": ["cite-sources", "corp/house-style"],
             "models": {"preferred": ["default"]}, "limits": {"max_tokens": 1024}},
}
SKILL = {"okf_version": "v0.3", "type": "skill", "title": "Cite sources",
         "zuno": {"name": "cite-sources", "allowed_tools": ["search_docs"], "allowed_knowledge": ["knowledge.tech"]}}
CORP_SKILL = {"okf_version": "v0.3", "type": "skill", "title": "House style", "zuno": {"name": "house-style"}}


def md(front: dict, body: str = "Body.\n") -> str:
    return "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n" + body


class V03TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.bundle = self.root / "agents" / "demo"
        self.write("agents/demo/agent.okf.md", md(AGENT))
        self.write("agents/demo/tasks/ask.md", md(TASK))
        self.write("agents/demo/skills/cite-sources.md", md(SKILL, "Cite every source you use.\n"))
        self.write("policies/skills/house-style.md", md(CORP_SKILL, "Answer in short paragraphs.\n"))
        self.write("policies/models/model-catalog.yaml", yaml.safe_dump({"models": [
            {"name": "local", "kind": "local", "role": "default", "eligible_for": ["C1", "C2", "C3"]},
            {"name": "gpt-oss", "kind": "local", "role": "reasoning", "eligible_for": ["C1", "C2", "C3"]},
            {"name": "openai", "kind": "saas", "role": "general-external", "eligible_for": ["C1"]},
        ]}))
        self.write("policies/guardrails/guardrails-policy.yaml", yaml.safe_dump({
            "modes": ["off", "observe", "block"], "categories": ["pii", "injection"],
            "minimum_mode_by_classification": {"C1": "observe", "C2": "observe", "C3": "block"}}))
        self.write("policies/limits/limits-policy.yaml",
                   "max_tokens: 8192\nmax_concurrent_requests: 10\nmax_steps: 30\nmax_delegation_depth: 2\n")
        self.write("policies/quotas/quota-policy.yaml", yaml.safe_dump({"classes": {"standard": {}, "intensive": {}}}))
        self.saved = (narrow.REPO_ROOT, narrow.POLICIES, narrow.CORP_SKILLS_DIR)
        narrow.REPO_ROOT, narrow.POLICIES = self.root, self.root / "policies"
        narrow.CORP_SKILLS_DIR = self.root / "policies" / "skills"

    def tearDown(self) -> None:
        narrow.REPO_ROOT, narrow.POLICIES, narrow.CORP_SKILLS_DIR = self.saved
        shutil.rmtree(self.root)

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def set_agent(self, **zuno) -> None:
        agent = yaml.safe_load(yaml.safe_dump(AGENT))
        agent["zuno"].update(zuno)
        self.write("agents/demo/agent.okf.md", md(agent))

    def set_task(self, **zuno) -> None:
        task = yaml.safe_load(yaml.safe_dump(TASK))
        task["zuno"].update(zuno)
        self.write("agents/demo/tasks/ask.md", md(task))

    def findings(self) -> list:
        return narrow.check_bundle(self.bundle, narrow.Corp())


class SchemaTest(V03TestCase):
    def test_example_bundle_matches_the_v03_schemas(self) -> None:
        validators = schema.validators()
        for path in (self.bundle / "agent.okf.md", self.bundle / "tasks/ask.md",
                     self.bundle / "skills/cite-sources.md", self.root / "policies/skills/house-style.md"):
            front = schema.frontmatter(path)
            errors = list(validators["v0.3"][front["type"]].iter_errors(front))
            self.assertEqual(errors, [], f"{path.name}: {[e.message for e in errors]}")

    def test_v03_refuses_an_unknown_key_and_off(self) -> None:
        validators = schema.validators()["v0.3"]
        agent = yaml.safe_load(yaml.safe_dump(AGENT))
        agent["zuno"]["guardrails"]["mode"] = "off"
        self.assertTrue(list(validators["agent"].iter_errors(agent)))
        agent = yaml.safe_load(yaml.safe_dump(AGENT))
        agent["zuno"]["version"] = "1.0.0"
        self.assertTrue(list(validators["agent"].iter_errors(agent)))


class NarrowingTest(V03TestCase):
    def test_example_bundle_only_narrows(self) -> None:
        self.assertEqual(self.findings(), [])

    def test_v02_bundle_is_not_checked(self) -> None:
        self.write("agents/demo/agent.okf.md", md({**AGENT, "okf_version": "v0.2"}))
        self.assertEqual(self.findings(), [])

    def test_max_steps_within_the_corp_ceiling(self) -> None:
        self.set_agent(limits={**AGENT["zuno"]["limits"], "max_steps": 20})
        self.set_task(limits={"max_steps": 30})
        self.assertEqual(self.findings(), [])

    def test_max_steps_above_the_corp_ceiling(self) -> None:
        self.set_task(limits={"max_steps": 31})
        self.assertIn("max_steps 31 exceeds the corp ceiling 30", " ".join(self.findings()))

    def test_max_steps_schema_refuses_zero(self) -> None:
        validators = schema.validators()["v0.3"]
        agent = yaml.safe_load(yaml.safe_dump(AGENT))
        agent["zuno"]["limits"] = {**agent["zuno"].get("limits", {}), "max_steps": 0}
        self.assertTrue(list(validators["agent"].iter_errors(agent)))
        agent["zuno"]["limits"]["max_steps"] = 15
        self.assertEqual(list(validators["agent"].iter_errors(agent)), [])

    def test_unknown_model_role(self) -> None:
        self.set_agent(models={"preferred": ["quantum"]})
        self.assertIn("not a role", self.findings()[0])

    def test_role_not_eligible_for_the_classification(self) -> None:
        self.set_agent(models={"preferred": ["general-external"]})
        self.assertIn("no model of role 'general-external' is eligible for C2", self.findings()[0])

    def test_role_both_preferred_and_forbidden(self) -> None:
        self.set_task(models={"preferred": ["default"], "forbidden": ["default"]})
        self.assertIn("both preferred and forbidden", self.findings()[0])

    def test_guardrails_weaker_than_the_floor(self) -> None:
        self.set_agent(model={"preferred_classification": "C3"}, guardrails={"mode": "observe"})
        self.assertIn("weaker than the corp minimum 'block' for C3", self.findings()[0])

    def test_unknown_guardrail_category(self) -> None:
        self.set_agent(guardrails={"mode": "block", "categories": ["toxicity"]})
        self.assertIn("not a corp category", self.findings()[0])

    def test_limits_above_the_ceilings(self) -> None:
        self.set_agent(limits={"max_tokens": 9000, "max_concurrent_requests": 50})
        found = self.findings()
        self.assertEqual(len(found), 2)
        self.assertIn("exceeds the corp ceiling 8192", found[0])

    def test_unknown_quota_class_including_the_v02_alias(self) -> None:
        self.set_task(quota_class="unlimited")
        self.assertIn("quota_class 'unlimited'", self.findings()[0])

    def test_skill_needs_more_than_the_task(self) -> None:
        self.set_task(allowed_tools=["web_search"])
        self.assertIn("needs tool 'search_docs', which the task does not allow", self.findings()[0])

    def test_missing_skill(self) -> None:
        self.set_task(skills=["corp/nope"])
        self.assertIn("skill 'corp/nope' not found", self.findings()[0])


class DelegationTest(V03TestCase):
    """zuno-demo ADR-0401 / ADR-0406: the optional delegation fields."""

    def add_peer(self) -> None:
        peer = yaml.safe_load(yaml.safe_dump(AGENT))
        peer["zuno"]["name"] = "peer"
        self.write("agents/peer/agent.okf.md", md(peer))
        self.write("agents/peer/tasks/ask.md", md(TASK))

    def target(self, agent: str = "peer", task: str = "ask") -> dict:
        return {"targets": [{"agent": agent, "task": task}]}

    def test_a_declared_target_matches_the_schema_and_narrows(self) -> None:
        self.add_peer()
        self.set_agent(delegation=self.target(), limits={**AGENT["zuno"]["limits"], "delegation": {"max_depth": 2}})
        front = schema.frontmatter(self.bundle / "agent.okf.md")
        self.assertEqual(list(schema.validators()["v0.3"]["agent"].iter_errors(front)), [])
        self.assertEqual(self.findings(), [])

    def test_the_schema_refuses_empty_targets_unknown_keys_and_depth_zero(self) -> None:
        validator = schema.validators()["v0.3"]["agent"]
        for zuno in ({"delegation": {"targets": []}},
                     {"delegation": {"targets": [{"agent": "peer", "task": "ask", "extra": 1}]}},
                     {"delegation": {"targets": [{"agent": "peer"}]}},
                     {"limits": {"delegation": {"max_depth": 0}}}):
            agent = yaml.safe_load(yaml.safe_dump(AGENT))
            agent["zuno"].update(zuno)
            self.assertTrue(list(validator.iter_errors(agent)), zuno)

    def test_an_agent_cannot_target_itself(self) -> None:
        self.set_agent(delegation=self.target("demo", "ask"))
        self.assertIn("is the agent itself", self.findings()[0])

    def test_a_target_agent_must_be_in_the_release(self) -> None:
        self.set_agent(delegation=self.target("ghost", "ask"))
        self.assertIn("target agent 'ghost' is not in the release", self.findings()[0])

    def test_a_target_task_must_exist(self) -> None:
        self.add_peer()
        self.set_agent(delegation=self.target("peer", "missing"))
        self.assertIn("target task peer/missing does not exist", self.findings()[0])

    def test_depth_above_the_corp_ceiling_is_refused(self) -> None:
        self.set_agent(limits={**AGENT["zuno"]["limits"], "delegation": {"max_depth": 3}})
        self.assertIn("delegation max_depth 3 exceeds the corp ceiling 2", self.findings()[0])

    def test_delegation_is_a_v03_field(self) -> None:
        self.add_peer()
        agent = yaml.safe_load(yaml.safe_dump(AGENT))
        agent["okf_version"] = "v0.2"
        agent["zuno"]["delegation"] = self.target()
        self.write("agents/demo/agent.okf.md", md(agent))
        self.assertIn("delegation is an OKF v0.3 field", self.findings()[0])


if __name__ == "__main__":
    unittest.main()
