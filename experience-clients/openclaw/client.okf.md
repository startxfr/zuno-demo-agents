---
okf_version: "0.2"
type: experience-client
title: OpenClaw
description: >-
  Per-persona personal assistants (zuno-demo ADR-0589). Each assistant calls the
  mcp-gateway with its persona's service-account token, under the logical name
  openclaw, for the read-only tools its persona's groups allow.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/experience-clients/openclaw/client.okf.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: openclaw
  tasks:
    - chat
    # zuno-demo ADR-0596: the model routing of "Zuno Code"; no tools.
    - code
  # Same as open-webui (zuno-demo ADR-0594): MCP at C2, model calls at C1,
  # C2 tool turns kept on local models by the ai-gateway.
  classification: C2
  access:
    # The persona service accounts (service-account-openclaw-<persona>) carry
    # their persona's business groups.
    groups:
      - consultant
      - sales
---

# OpenClaw

Experience client of zuno-demo ADR-0589. Each persona's assistant sends
`X-Zuno-Agent: openclaw`, `X-Zuno-Task: chat` and `X-Zuno-Data-Classification: C2`
on its MCP credential. The mcp-gateway lists the tools of the task `chat` that the
persona's groups may use (tool policy); every other tool is refused.
