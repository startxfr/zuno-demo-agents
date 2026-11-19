# The agent bundle report

A single HTML page that shows what each agent declares: status and data ceiling, workflow, every task with its tools,
knowledge domains and models, and the rules its prompts set, with a comparison across agents. It is read from the bundles
under `agents/`, not from this documentation, so it answers "what does the bundle itself say".

The report is produced by a Claude Code skill kept in the repository, `.claude/skills/bundle-gen-repport/`. The skill's
own `SKILL.md` is the reference for how it runs and what it parses. This page says why it exists and what a maintainer
has to do.

## When to use it

- To review what a release gives each agent, before or after a version bump.
- To check an agent's ceiling, tools and delegation at a glance when adding or changing an agent
  ([Add an agent](add-an-agent.md)).
- To share a readable overview of the agents with someone who does not read OKF files.

## What it reads

| Shown | Source | Kept current by |
|---|---|---|
| Status, ceiling, groups, workflow shape, memory, delegation, guardrails | `agent.okf.md` | parsed on every run |
| Tasks, tools, knowledge, models, token limits, examples | `tasks/*.md`, `tools/*.md` | parsed on every run |
| Rules a prompt sets ("does", "must", "never", "limit") | `prompts/` | **written by hand**, then checked for drift |

The rules are short paraphrases of the prompts, so they can go stale. The skill stores a hash of each task's prompt files
and warns when a prompt changed after its rules were written, when a task or agent has no rules, and when a knowledge
domain has no description.

## What a maintainer does

1. After a change to a prompt, run the skill and read the drift report.
2. For each flagged task, re-read the prompt and update its rules in `.claude/skills/bundle-gen-repport/assets/rules.py`.
3. Record the new hashes with the skill's `--rehash` option. Do not rehash without re-reading the prompt.
4. Run the skill from Claude Code in this repository, and publish the page as a private artifact.

The generator is not a release check: it is not part of `ci.yml`, does not appear in a release, and the report is not
committed. A stale rule shows up in the report, never as a failing build.
