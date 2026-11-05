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
---

# Chat

Every Dify model call and tool call: a workflow drawn on the canvas that may let the model look
up Drive files and mail, draw a diagram, or search Confluence and the technical documentation.
The token proxy sends this task on every request, so the Dify identity is the persona of its
Keycloak client (consultant-02), not the person who signed in.
