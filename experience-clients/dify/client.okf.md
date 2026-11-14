---
okf_version: "0.2"
type: experience-client
title: Dify
description: >-
  No-code LLM workflow canvas (zuno-demo ADR-0599). Every model and tool call goes through
  the zuno-token-proxy (ADR-0601), which signs it with the dify Keycloak client's persona
  token, to the ai-gateway and the mcp-gateway.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/experience-clients/dify/client.okf.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: dify
  tasks:
    - chat
    # zuno-demo ADR-0596: the model routing of "Zuno Code"; no tools.
    - code
  # Same as open-webui and openclaw (zuno-demo ADR-0594): MCP at C2, model calls at C1,
  # C2 tool turns kept on local models by the ai-gateway.
  classification: C2
  access:
    # The dify Keycloak client's service account carries the groups of its persona
    # (consultant-02). The people allowed through the front door are narrower (oauth2-proxy).
    groups:
      - consultant
---

# Dify

Experience client of zuno-demo ADR-0599. The token proxy in front of Dify sends
`X-Zuno-Agent: dify`, `X-Zuno-Task: chat` and, on the MCP side, `X-Zuno-Data-Classification: C2`,
with a client-credentials token of persona consultant-02. The mcp-gateway lists the tools of
the task `chat` that the persona's groups may use (tool policy); every other tool is refused.
Calls are counted per persona, not per Dify user (ADR-0601 decision 5).
