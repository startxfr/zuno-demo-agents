---
okf_version: v0.3
type: task
title: Chat
zuno:
  # Read-only, as open-webui's chat: no writes, no Git, AAP or Salesforce. Dify's MCP tool
  # provider is the mcp-gateway behind the zuno-token-proxy (zuno-demo ADR-0599, ADR-0601).
  allowed_tools:
    - list_drive_files
    - read_gmail
    - generate_diagram
    # zuno-demo ADR-0594: the same read tools as the agents, filtered by the caller's groups.
    # Their results carry signed classification markers, and the ai-gateway answers a turn
    # that used them with local models only. search_technical_docs is also what the
    # External Knowledge adapter (WP-205) calls.
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

Every Dify model call and tool call: a workflow drawn on the canvas that may let the model look
up Drive files and mail, draw a diagram, or search Confluence and the technical documentation.
The token proxy sends this task on every request, so the Dify identity is the persona of its
Keycloak client (consultant-02), not the person who signed in.
