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
  # zuno-demo ADR-0596, user decision 2026-11-07: answer with the fast local reasoning model first (gpt-oss-20b,
  # about 85 tok/s, 131k context). Without a preference the ai-gateway walked its providers in file order and served
  # qwen3.6-27b (about 22 tok/s): 24 to 56 s for a short answer on demo333. Only reorders: the other local models
  # follow as fallbacks, and the classification and local-only rules are unchanged.
  models:
    preferred:
      - reasoning
---

# Chat

The assistant's only task: answer its persona, looking up their own Drive files and
mail, or drawing a diagram.
