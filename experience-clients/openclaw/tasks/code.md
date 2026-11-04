---
okf_version: v0.3
type: task
title: Code
zuno:
  # zuno-demo ADR-0596 (WP-194): the ai-gateway routes the "Zuno Code" model
  # (zuno-code) under this task. Codestral first, then the local models in the
  # corp order. No tools of its own: the MCP connection stays on `chat`. The
  # classification and ADR-0594 still keep a turn with a tool result local.
  allowed_tools: []
  models:
    preferred:
      - code
---

# Code

A code question the user sends with the "Zuno Code" model. It is answered by the
code-specialized SaaS model when the conversation is C1 and holds no tool result,
otherwise by a local model.
