---
okf_version: v0.3
type: experience-client
title: OpenClaw
description: >-
  Per-persona personal assistants (zuno-demo ADR-0589). Each assistant calls the
  mcp-gateway with its persona's service-account token, under the logical name
  openclaw, for a few read-only C1 tools.
provenance:
  maintainer: Zuno Demo architecture team
  repository: zuno-demo
freshness:
  last_reviewed: "2026-11-02"
zuno:
  name: openclaw
  tasks:
    - chat
  # Same rule as open-webui: the assistant's model calls are C1 (SaaS allowed),
  # so its tools must be C1.
  classification: C1
  access:
    # The persona service accounts (service-account-openclaw-<persona>) carry
    # their persona's business groups.
    groups:
      - consultant
      - sales
---

# OpenClaw

Experience client of zuno-demo ADR-0589. Each persona's assistant sends
`X-Zuno-Agent: openclaw`, `X-Zuno-Task: chat` and `X-Zuno-Data-Classification: C1`
on its MCP credential. The mcp-gateway lists the tools of the task `chat` that the
persona's groups may use (tool policy); every other tool is refused.
