---
okf_version: v0.3
type: task
title: Chat
zuno:
  # Read-only, as open-webui's chat: no writes, no Git, AAP or Salesforce.
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

The assistant's only task: answer its persona, looking up their own Drive files and
mail, or drawing a diagram.
