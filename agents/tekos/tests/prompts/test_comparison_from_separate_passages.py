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
# (h) v1.2.2: a page about HTTPRoute or the Gateway API describes HTTPRoute, never Ingress (the replay of 2026-11-20 labelled it Ingress)
HTTPROUTE_NOT_INGRESS = re.compile(
    r"a page about httproute or the gateway api describes httproute, never ingress.{0,200}write \"none retrieved\" for it.{0,200}"
    r"never put httproute facts under the ingress block")
# (i) v1.2.3: a missing side gives "none stated" differences and only topic names under "Not stated by any passage" (replay of 2026-11-21: run 3
# wrote differences from general knowledge, runs 2 and 4 described Ingress under "Not stated")
MISSING_SIDE_NO_CLAIMS = re.compile(
    r"when a side is \"none retrieved\", write \"none stated\" for the differences.{0,40}under \"not stated by any passage\" write only the names of the missing topics"
    r".{0,160}never a sentence that says what the missing side is or does")
# (j) v1.2.6: the skeleton is for comparisons only; any other question gets a short answer with the passage URL, never "none retrieved" (live check
# #11 of 2026-11-22/23: 4 of 8 replies to "What is a namespace in OpenShift?" were "None retrieved."), and no figure without a passage URL (c2: RHEL 12 date)
NON_COMPARISON_SHORT_ANSWER = re.compile(
    r"for a question that does not ask to compare two things, never use the comparison skeleton below and never write \"none retrieved\" or \"none stated\" for it"
    r".{0,400}end with that passage's source url copied")
# (k) v1.2.7: v1.2.6 made the live check #11 worse (8 of 8 replies "no passage defines a namespace", 4 of 8 before): a passage that describes the
# thing is enough, no formal definition needed, and the figure rule covers dates, versions and numeric limits only
DESCRIBED_IS_ENOUGH = re.compile(
    r"a passage does not need to contain a formal definition to answer, and you never say that no passage defines something when a passage describes it")
NO_FIGURE_WITHOUT_URL = re.compile(
    r"a date, a version number or a numeric limit is written only when a passage in your context states it, with the url of that passage"
    r".{0,120}give no value\. this applies to those values only, not to explanations or descriptions")
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

    def test_an_httproute_page_is_never_the_ingress_side(self):
        self.assertRegex(normalised(), HTTPROUTE_NOT_INGRESS,
                         "answer-technical-question.md lost the rule that a page about HTTPRoute or the Gateway API never describes Ingress")

    def test_a_missing_side_gets_no_differences_and_no_description(self):
        self.assertRegex(normalised(), MISSING_SIDE_NO_CLAIMS,
                         "answer-technical-question.md lost the rule that a side with no passage gets 'none stated' differences and only topic names under 'Not stated by any passage'")

    def test_a_question_that_is_not_a_comparison_gets_a_short_answer_with_the_passage_url(self):
        self.assertRegex(normalised(), NON_COMPARISON_SHORT_ANSWER,
                         "answer-technical-question.md lost the rule that only a comparison uses the skeleton and any other question gets a short answer ending with the passage URL")

    def test_a_passage_that_describes_the_thing_is_enough_to_answer(self):
        self.assertRegex(normalised(), DESCRIBED_IS_ENOUGH,
                         "answer-technical-question.md lost the rule that a passage describing the thing answers, with no formal definition needed")

    def test_no_date_or_figure_without_a_passage_url(self):
        self.assertRegex(normalised(), NO_FIGURE_WITHOUT_URL,
                         "answer-technical-question.md lost the rule that a date or figure is written only with the URL of a passage that states it")

    def test_the_patterns_do_not_match_a_bare_prompt(self):
        bare = ("answer the technical question from the passages you are given and cite their source urls. if no passage states the "
                "answer explicitly, say so and give what the closest passages do say.")
        for pattern in (BUILD_FROM_PASSAGES, NO_DECLINE, NO_INVENTED_DIFFERENCE, ONLY_FROM_PASSAGES, NO_SUBSTITUTE_CONCEPT, SKELETON, COPY_URL,
                        HTTPROUTE_NOT_INGRESS, MISSING_SIDE_NO_CLAIMS, NON_COMPARISON_SHORT_ANSWER, DESCRIBED_IS_ENOUGH, NO_FIGURE_WITHOUT_URL):
            self.assertIsNone(pattern.search(bare), pattern.pattern)


if __name__ == "__main__":
    unittest.main()
