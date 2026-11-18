---
okf_version: "0.2"
type: experience-client
title: Claude Code on sovereign models
description: >-
  Claude Code on a presenter's workstation (zuno-demo ADR-0619 clause 8, WP-298). It reaches
  the Praxis AI alternative gateway through its workstation entry with the signed-in user's
  own token (device sign-in, Keycloak client `claude-code`, apiKeyHelper). Praxis translates
  its Anthropic Messages calls for the local models and refuses every SaaS model for this
  client. No MCP tools; local models only.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/experience-clients/claude-code/client.okf.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: claude-code
  tasks:
    # zuno-demo ADR-0619 clause 8: coding on the local models; no tools.
    - code
  # Source code shown to a coding assistant stays on the platform, as for Blender (ADR-0610 clause 3).
  classification: C3
  access:
    groups:
      - consultant
      - cdp
      - ocp-ai-dev
      - ocp-ai-ops
      - ocp-paas-dev
      - ocp-paas-ops
---

# Claude Code on sovereign models

Experience client of zuno-demo ADR-0619 (clause 8). Claude Code sends its Anthropic Messages
calls, with the user's own token, to the Praxis workstation entry, whose Kuadrant AuthPolicy
admits only tokens of the Keycloak clients `claude-code` and `blender`. Praxis, not the
Zuno ai-gateway, serves it: Praxis applies its own policy (the `zuno` JWT, the model list,
SaaS models refused for `claude-code`), not the Zuno quota ledger, floors or per-agent
routing. This declaration keeps the client name, its groups and its task on record, and
holds the routing the ai-gateway would apply if the client were pointed at it.
It never calls the mcp-gateway, so its task allows no tool.
