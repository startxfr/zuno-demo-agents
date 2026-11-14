# Cognos

Board-only financial and strategic assistant, for a Direction-level audience. The intended build answers financial and
strategic questions over a large tool set that excludes the technical tools and the technical knowledge corpora
(zuno-demo ADR-0349).

**Status: placeholder.** Declared but not served: a portal shows a "coming soon" tile to members of `agent_cognos`.
The single task declares no tool and no knowledge, so the agent has no capability by construction. Intended business
role: `board`; `preferred_classification: C3` (local models only).

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `coming-soon` | Says that Cognos is not available yet and what it will do | none | none |

```text
cognos/
├── README.md         this file (not published)
├── VERSION           the agent's version, bumped when a published file changes
├── index.md          generated, do not edit
├── agent.okf.md      the agent: identity, status, task list, model, access, tile
├── tasks/
│   └── coming-soon.md    the placeholder task
└── prompts/
    └── coming-soon.md    its system prompt
```

Building Cognos means authoring real tasks with their prompts and policy entries, then setting `status: active`. See
the [OKF field reference](../../docs/okf-reference.md) and [how to add an agent](../../docs/add-an-agent.md).
