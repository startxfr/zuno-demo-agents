---
okf_version: v0.3
type: experience-client
title: Open WebUI
description: >-
  General-purpose chat for every employee (zuno-demo ADR-0588). It chats through
  the ai-gateway and calls a few read-only C1 tools through the mcp-gateway, always
  with the signed-in user's own token.
provenance:
  maintainer: Zuno Demo architecture team
  repository: zuno-demo
freshness:
  last_reviewed: "2026-11-02"
zuno:
  name: open-webui
  tasks:
    - chat
  # The chat may go to SaaS models (C1), so its tools must be C1: Confluence and
  # the technical knowledge base stay with the agents, on local models.
  classification: C1
  access:
    groups:
      - sales
      - consultant
      - adv
      - finance
      - board
      - cdp
      - recrut
      - ocp-ai-dev
      - ocp-ai-ops
      - ocp-paas-dev
      - ocp-paas-ops
---

# Open WebUI

Experience client of zuno-demo ADR-0588. Open WebUI sends `X-Zuno-Agent: open-webui`,
`X-Zuno-Task: chat` and `X-Zuno-Data-Classification: C1` on its MCP connection, with
the user's access token. The mcp-gateway lists the tools of the task `chat` that
the user's groups may use (tool policy); every other tool is refused.
