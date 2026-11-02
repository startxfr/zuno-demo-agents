---
okf_version: v0.3
type: task
title: Chat
zuno:
  # Read-only and C1: the conversation may be answered by a SaaS model.
  # Writes, C2+ tools (Confluence, Git, AAP, Salesforce) and web search
  # (switched off in Open WebUI, ADR-0588) are not allowed.
  allowed_tools:
    - list_drive_files
    - read_gmail
    - generate_diagram
---

# Chat

Open WebUI's only task: a general-purpose conversation where the user may let the
model look up their own Drive files and mail, or draw a diagram.
