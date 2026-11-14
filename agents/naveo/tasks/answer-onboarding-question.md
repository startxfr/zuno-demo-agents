---
okf_version: "0.2"
type: task
title: Answer an onboarding question
description: Answer a new team member's question about internal processes, tooling and reference material, with citations.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/naveo/tasks/answer-onboarding-question.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - search_confluence
    - web_search
    - list_drive_files

  live_read_tool: search_confluence
  allowed_knowledge:
    - knowledge.tech
    - knowledge.project
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "What do I need to set up on my first day?"
    - "Who should I contact to get access to the internal Confluence?"
    - "Where do I find the onboarding checklist for a new consultant?"
---

# Answer an onboarding question

Answer a new team member's question about internal processes, tooling and where to find reference material, grounded
in the technical documentation corpus (`knowledge.tech`), project memory (`knowledge.project`) and internal Confluence
content.

`search_confluence` is the live-read tool: the workflow's live-read branch calls it for current Confluence content.
`web_search` is the fallback when the internal sources have no grounded answer, and `list_drive_files` finds onboarding
documents in the user's own Drive. The task reuses existing knowledge domains and tool capabilities only, with no new
external system (zuno-demo ADR-0410).
