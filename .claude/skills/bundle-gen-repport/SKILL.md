---
name: bundle-gen-repport
description: Generate the interactive HTML report of the Zuno agent bundles (zuno-demo-agents), read from the OKF bundles only and not from the documentation. For each agent it shows status, data ceiling, workflow, every task with its flow, tools (read/write), knowledge domains, model preference and the rules set by its prompt, plus a cross-agent comparison matrix. Use when the user asks what each agent does, for a bundle report or synthesis, or to refresh it after a release.
---

# bundle-gen-repport

Builds one self-contained HTML page (English, light and dark themes, no external data) from `agents/*/` and publishes it as a **private Artifact**. Run it from the root of the zuno-demo-agents checkout.

## Run

1. Build: `python3 -I .claude/skills/bundle-gen-repport/scripts/generate.py . <scratchpad>/zuno-agent-bundles.html`
   It prints one row per agent (status, ceiling, tasks, tool notes) and then a drift report.
2. Read the drift report before publishing (see below), and fix what it flags.
3. Publish with the Artifact tool, file path `<scratchpad>/zuno-agent-bundles.html`, icon `diagram`, title `Zuno Agent Bundles`. Re-use the same path in the same conversation to keep the URL. From a new conversation, find the existing artifact with `action: "list"` and pass its URL.
4. Tell the user: release shown, which agents are active, and anything the drift report raised.

Do not read the documentation (`docs/`, READMEs, `index.md`). The point of the report is to say what the bundles themselves declare. Do not commit the output.

## What is parsed and what is hand-written

| Part of the page | Source | Parsed or written |
|---|---|---|
| Agent header: status, ceiling (C1 to C3), `local_only`, groups, workflow shape, memory, delegation, guardrails, colour | `agent.okf.md` frontmatter | parsed |
| Tasks: description, tools, knowledge, live-read tool, models, max tokens, `project_required`, reflect ceiling, example prompts | `tasks/*.md` frontmatter | parsed |
| Tools: read or write, minimum class, allowed groups, local-only, usage and limits | `tools/*.md` (`known_limitations`) | parsed with regexes in `parse_tool` |
| Knowledge domain descriptions | `assets/rules.py` (`DOMAIN`) | written |
| Rules ("does", "must", "never", "limit") per task and per agent | task prompts and agent body | **written** in `assets/rules.py` (`R`, `AGENT_RULES`) |
| Flow diagram of a turn | `graph_shape` + the task's tools and knowledge | derived in the template |

The rules are paraphrases, not extracted text, so they can go stale. `rules.py` stores a hash of each task's prompt files (`PROMPT_SHA`).

## Drift report

The generator warns when:

- a task has no rules, or an agent has no agent-level rules (new task or new agent);
- a task's prompt changed since its rules were written (hash mismatch);
- a knowledge domain has no description;
- rules exist for an agent that no longer has a bundle;
- a task declares a tool the bundle holds no note for. This is informational: the page shows a hollow marker and says so.

To clear a prompt-hash warning: re-read the changed prompt, edit the matching entries in `assets/rules.py`, then run `generate.py . --rehash` to record the new hashes. Never rehash without re-reading the prompt.

For a new agent also check `CANON` in `rules.py`: it groups capabilities that the bundles declare under two names (`search_confluence` and `confluence.page.search`, `list_drive_files` and `drive.document.search`, `read_gmail` and `gmail.message.read`). Add a pair only when a prompt or tool note itself ties the two names together.

## Rule wording

Write each rule from what the prompt says, in one sentence. Tags:

- `do` expected behaviour; `must` required; `dont` forbidden; `limit` a boundary (access, budget, scope).
- Say plainly when the bundle records a gap, for example a constraint stated in a prompt that no code enforces.
- Never write a rule the prompt does not support.

## Files

- `scripts/generate.py` parses the bundles, builds the data, injects it into the template, prints the drift report. `--rehash` records prompt hashes.
- `assets/template.html` the page. The data goes in at the single `/*DATA*/null` placeholder.
- `assets/rules.py` the hand-written rules, domain descriptions, capability aliases and prompt hashes.

## Checks after changing the template

Extract the `<script>` from the output and run `node --check` on it. The page renders entirely from the injected data, so a missing field shows as `undefined` in the markup.
