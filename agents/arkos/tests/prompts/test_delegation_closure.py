#!/usr/bin/env python3
"""ADR-0504 prompts/ suite: the two Arkos prompts that delegate keep their delegation-closure wording.

Arkos delegated a work item to Tekos and, once Tekos answered, never marked the item done, so it delegated the same item
again. The closing paragraph of `draft-architecture-testimonial.md` and `workshop-presentation.md` says what to do instead.
This test guards that the wording is not dropped; it does not prove a model obeys it (that is a behavioural check, on a
cluster). It matches key phrases, after collapsing whitespace and case, not the whole paragraph, so rewording the
sentences around them does not break it. It does not name the tool that marks an item: the runtime exposes it under two
spellings and the prompt deliberately describes it by what it does.

Run directly (from anywhere) or via platform/okf/run_agent_contract_tests.py:

    python3 agents/arkos/tests/prompts/test_delegation_closure.py
"""
from __future__ import annotations

import pathlib
import re
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
PROMPTS = ("draft-architecture-testimonial.md", "workshop-presentation.md")

# (a) when the answer covers everything asked, the work item is marked done
MARK_DONE = re.compile(r"covers everything you asked, mark that work item done")
# (b) when no usable answer arrives, the work item is marked failed
MARK_FAILED = re.compile(r"no usable answer arrives, mark the work item failed")
# (c) apart from the one follow-up, a work item that already has an answer is never delegated again
NO_REDELEGATION = re.compile(r"apart from that one follow-up, never delegate a work item that already has an answer")


def normalised(name: str) -> str:
    text = (REPO_ROOT / "agents" / "arkos" / "prompts" / name).read_text(encoding="utf-8")
    return re.sub(r"\s+", " ", text).lower()


class DelegationClosure(unittest.TestCase):
    def test_both_prompts_exist(self):
        for name in PROMPTS:
            self.assertTrue((REPO_ROOT / "agents" / "arkos" / "prompts" / name).is_file(), name)

    def test_an_answer_that_covers_the_request_closes_the_work_item_as_done(self):
        for name in PROMPTS:
            self.assertRegex(normalised(name), MARK_DONE,
                             f"{name} lost the instruction to mark the work item done once the answer covers everything asked")

    def test_no_usable_answer_closes_the_work_item_as_failed(self):
        for name in PROMPTS:
            self.assertRegex(normalised(name), MARK_FAILED,
                             f"{name} lost the instruction to mark the work item failed when no usable answer arrives")

    def test_an_item_with_an_answer_is_never_delegated_again_apart_from_one_follow_up(self):
        for name in PROMPTS:
            self.assertRegex(normalised(name), NO_REDELEGATION,
                             f"{name} lost the ban on delegating a work item that already has an answer (apart from one follow-up)")

    def test_the_patterns_do_not_match_a_prompt_without_the_paragraph(self):
        bare = "when you delegate a work item to another agent, delegate it once. use the work_item_id exactly as it appears."
        self.assertIsNone(MARK_DONE.search(bare))
        self.assertIsNone(MARK_FAILED.search(bare))
        self.assertIsNone(NO_REDELEGATION.search(bare))


if __name__ == "__main__":
    unittest.main()
