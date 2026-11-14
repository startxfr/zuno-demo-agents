# Soursage

Recruiting assistant. The intended build sources new consultant candidates from LinkedIn and finds, among existing
consultants, the best profile for a mission from Workday profile data (zuno-demo ADR-0349).

**Status: placeholder.** Declared but not served: a portal shows a "coming soon" tile to members of `agent_soursage`.
The single task declares no tool and no knowledge, so the agent has no capability by construction. Intended business
roles: `recrut` and `sales`. The corp tool policy registers the read-only `workday.profile.any.read` capability (granted
to `cdp` only today); no LinkedIn capability exists yet.

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `coming-soon` | Says that Soursage is not available yet and what it will do | none | none |

```text
soursage/
├── README.md         this file (not published)
├── VERSION           the agent's version, bumped when a published file changes
├── index.md          generated, do not edit
├── agent.okf.md      the agent: identity, status, task list, model, access, tile
├── tasks/
│   └── coming-soon.md    the placeholder task
└── prompts/
    └── coming-soon.md    its system prompt
```

Building Soursage means authoring real tasks with their prompts and policy entries, then setting `status: active`. See
the [OKF field reference](../../docs/okf-reference.md) and [how to add an agent](../../docs/add-an-agent.md).
