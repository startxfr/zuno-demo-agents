---
okf_version: v0.3
type: task
title: Chat
zuno:
  # Read-only. Writes, Git, AAP, Salesforce and web search (switched off in
  # Open WebUI, ADR-0588) are not allowed.
  allowed_tools:
    - list_drive_files
    - read_gmail
    - generate_diagram
    # zuno-demo ADR-0594 (WP-191): the same read tools as the agents, filtered
    # by the user's groups. Their results carry signed classification markers,
    # and the ai-gateway answers a turn that used them with local models only.
    - search_confluence
    - confluence.page.read
    - search_technical_docs
---

# Chat

Open WebUI's only task: a general-purpose conversation where the user may let the
model look up their own Drive files and mail, or draw a diagram.
