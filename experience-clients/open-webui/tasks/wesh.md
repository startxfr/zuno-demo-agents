---
okf_version: "0.2"
type: task
title: Wesh
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/experience-clients/open-webui/tasks/wesh.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  # zuno-demo ADR-0619 amendment 2026-11-17 (owner request): the ai-gateway routes the
  # "Zuno wesh" model (zuno-wesh) under this task, so the owner can compare it side by
  # side with praxis.qwen3.5-9b-wesh in Open WebUI. The `specialized` role is the wesh
  # fine-tune (model-roles registry), then the local models in the corp order. No tools
  # of its own: the MCP connection stays on `chat`. The classification and ADR-0594
  # still keep a turn with a tool result local.
  allowed_tools: []
  models:
    preferred:
      - specialized
---

# Wesh

A chat the user sends with the "Zuno wesh" model: the answer comes from the
street-French fine-tune of Qwen3.5-9B, served locally, through the default Zuno
ai-gateway. It exists to compare that path with the same model through the
alternative Praxis gateway.
