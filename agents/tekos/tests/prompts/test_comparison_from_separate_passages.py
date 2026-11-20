#!/usr/bin/env python3
"""ADR-0504 prompts/ suite: the Tekos prompt keeps its rule for a comparison whose sides are described in separate passages.

Tekos used to decline a comparison ("Route versus Ingress") when no single passage compared the two sides. The paragraph added
in v1.1.4 to `answer-technical-question.md` tells it to build the comparison from the passages that describe each side, to say
which part no passage states, and never to invent a difference. This test guards that the wording is not dropped; it does not
prove a model obeys it (that is a behavioural check, on a cluster). It matches key phrases after collapsing whitespace and case,
not the whole paragraph, so rewording around them does not break it. It names no tool.

Run directly (from anywhere) or via platform/okf/run_agent_contract_tests.py:

    python3 agents/tekos/tests/prompts/test_comparison_from_separate_passages.py
"""
from __future__ import annotations

import pathlib
import re
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
PROMPT = REPO_ROOT / "agents" / "tekos" / "prompts" / "answer-technical-question.md"

# (a) a comparison whose sides are described by separate passages is built from those passages
BUILD_FROM_PASSAGES = re.compile(
    r"asks for a comparison and the passages you have describe each side separately.{0,200}build the comparison from those passages")
# (b) a comparison is not declined only because no single passage compares the two sides
NO_DECLINE = re.compile(r"do not decline a comparison only because no single passage compares the two sides")
# (c) no difference is added that no passage supports
NO_INVENTED_DIFFERENCE = re.compile(r"never add a difference that no passage supports")
# (d) a comparison is built only from passages, and a side no passage covers is reported, not described from general knowledge
# (e) a related concept is not put in the place of the one asked
NO_SUBSTITUTE_CONCEPT = re.compile(r"do not stand in a related concept for the one asked")
# (f) the comparison skeleton: one block per side with a source line that is copied or "none retrieved"
SKELETON = re.compile(r"write every comparison in this skeleton, one block per side.{0,400}source: <one url copied from the passage, or \"none retrieved\">")
# (g) a URL is copied, never built, and a placeholder is not a source
COPY_URL = re.compile(r"copy each url character for character from the passage, never build one.{0,320}a placeholder in a command .{0,40}is not a source")
ONLY_FROM_PASSAGES = re.compile(r"only from the passages in your context or returned by your searches.{0,120}no passage covers one side, say that no passage covers it")


def normalised() -> str:
    return re.sub(r"\s+", " ", PROMPT.read_text(encoding="utf-8")).lower()


class ComparisonFromSeparatePassages(unittest.TestCase):
    def test_the_prompt_exists(self):
        self.assertTrue(PROMPT.is_file(), PROMPT)

    def test_a_comparison_is_built_from_passages_that_describe_each_side_separately(self):
        self.assertRegex(normalised(), BUILD_FROM_PASSAGES,
                         "answer-technical-question.md lost the instruction to build a comparison from passages that describe each side separately")

    def test_a_comparison_is_not_declined_for_want_of_a_single_comparing_passage(self):
        self.assertRegex(normalised(), NO_DECLINE,
                         "answer-technical-question.md lost the ban on declining a comparison only because no single passage compares the two sides")

    def test_no_difference_is_invented(self):
        self.assertRegex(normalised(), NO_INVENTED_DIFFERENCE,
                         "answer-technical-question.md lost the ban on adding a difference that no passage supports")

    def test_a_side_without_a_passage_is_reported_not_described_from_general_knowledge(self):
        self.assertRegex(normalised(), ONLY_FROM_PASSAGES,
                         "answer-technical-question.md lost the rule to build a comparison only from passages and to report a side no passage covers")

    def test_a_related_concept_is_not_put_in_the_place_of_the_one_asked(self):
        self.assertRegex(normalised(), NO_SUBSTITUTE_CONCEPT,
                         "answer-technical-question.md lost the ban on standing in a related concept for the one asked")

    def test_a_comparison_is_written_in_a_skeleton_with_a_source_line_per_side(self):
        self.assertRegex(normalised(), SKELETON,
                         "answer-technical-question.md lost the comparison skeleton (one block per side with a source line)")

    def test_a_url_is_copied_never_built_and_a_placeholder_is_not_a_source(self):
        self.assertRegex(normalised(), COPY_URL,
                         "answer-technical-question.md lost the rule to copy URLs verbatim and not to count placeholders as sources")

    def test_the_patterns_do_not_match_a_bare_prompt(self):
        bare = ("answer the technical question from the passages you are given and cite their source urls. if no passage states the "
                "answer explicitly, say so and give what the closest passages do say.")
        for pattern in (BUILD_FROM_PASSAGES, NO_DECLINE, NO_INVENTED_DIFFERENCE, ONLY_FROM_PASSAGES, NO_SUBSTITUTE_CONCEPT, SKELETON, COPY_URL):
            self.assertIsNone(pattern.search(bare), pattern.pattern)


if __name__ == "__main__":
    unittest.main()
