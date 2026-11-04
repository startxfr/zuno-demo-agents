# Experience clients

User interfaces over the governed chain (zuno-demo ADR-0587, ADR-0592): Open WebUI
and OpenClaw. They are not agents. Each one calls the mcp-gateway on behalf of the
signed-in user under a logical agent name (`X-Zuno-Agent`) and a task
(`X-Zuno-Task`). This directory says who may use that name and which tools each
task allows.

```
experience-clients/<name>/
  client.okf.md        # type: experience-client (zuno-okf-experience-client-v0.3.schema.json)
  tasks/<task>.md      # type: task: allowed_tools (mcp-gateway), zuno.models (ai-gateway routing, ADR-0596)
```

What an experience client is not:

- not a UnifAI bundle, not a Keycloak `agent_*` group, not a MaaS subscription;
- not an A2A endpoint, not a delegation target;
- no prompts, graph, RAG or UI tile.

A task may declare `zuno.models` (zuno-demo ADR-0596). zuno-demo's generator turns it
into the ai-gateway routing entry of (client, task), with the agents' rules: roles
reorder, `forbidden` excludes, nothing is added. The task `code` puts the `code`
role (Codestral) first; the ai-gateway routes the "Zuno Code" model (`zuno-code`)
under it. Its MCP calls stay on `chat`.

`access.groups` are business groups: a client serves every employee. Each tool is
still narrowed by `policies/tools/tool-policy.yaml` (the caller's groups and the
request classification). A client that declares `classification: C1` may only
allow tools whose `min_classification` is C1 (checked by
`platform/supply-chain/validate_okf_bundle.py`).

The release ships them in their own layer of the corp artifact (signed with it);
they have no per-client `VERSION`, quay repository or tag.
