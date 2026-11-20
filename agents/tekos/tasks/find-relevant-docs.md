---
okf_version: "0.2"
type: task
title: Find relevant documentation
description: List the Confluence pages, documentation sections and Drive files relevant to a topic, without composing an answer.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/tekos/tasks/find-relevant-docs.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - search_confluence
    - list_drive_files
  allowed_knowledge:
    - knowledge.tech
  models:
    preferred:
      - default
      - specialized
      - quality
      - reasoning
      - reasoning-external
  prompt_examples:
    - "Find the Confluence pages describing the satellite build architecture."
    - "Which documentation covers OpenShift AI model serving?"
    - "List the reference material we have on Keycloak realm configuration."
    - "Which of my Drive files cover the customer's OpenShift upgrade?"
---

# Find relevant documentation

Given a topic or keyword, return the most relevant internal Confluence
pages, indexed documentation sections (`knowledge.tech`) and the
consultant's own Drive files, without composing a full narrative answer: a
lookup for consultants scanning the available material before a customer
call. `search_confluence` finds the Confluence pages and `list_drive_files`
lists the Drive files.
