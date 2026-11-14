---
okf_version: "0.2"
type: experience-client
title: Open WebUI
description: >-
  General-purpose chat for every employee (zuno-demo ADR-0588). It chats through
  the ai-gateway and calls the read-only tools the user's groups allow through the mcp-gateway, always
  with the signed-in user's own token.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/experience-clients/open-webui/client.okf.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: open-webui
  tasks:
    - chat
    # zuno-demo ADR-0596: the model routing of "Zuno Code"; no tools.
    - code
  # zuno-demo ADR-0594: the MCP connection calls at C2 so Confluence and the
  # technical knowledge base are listed; the model connection stays C1, and the
  # ai-gateway keeps a turn that used a C2 tool on local models (signed markers).
  classification: C2
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
`X-Zuno-Task: chat` and `X-Zuno-Data-Classification: C2` on its MCP connection, with
the user's access token. The mcp-gateway lists the tools of the task `chat` that
the user's groups may use (tool policy); every other tool is refused.
