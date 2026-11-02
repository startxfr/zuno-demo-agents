---
okf_version: v0.3
type: task
title: Chat
zuno:
  # Read-only and C1, as open-webui's chat: no writes, no C2+ tools.
  allowed_tools:
    - list_drive_files
    - read_gmail
    - generate_diagram
---

# Chat

The assistant's only task: answer its persona, looking up their own Drive files and
mail, or drawing a diagram.
