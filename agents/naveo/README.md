# Naveo

Onboarding assistant for new team members: questions about internal processes, tooling and where to find reference
material, grounded in the technical documentation corpus, project memory and internal Confluence content, with a web
search fallback and a look at the user's own Drive. It reuses existing knowledge domains and tool capabilities only
(zuno-demo ADR-0410).

**Status: placeholder.** Declared but not served. Entitlement group: `agent_naveo`; business role: `consultant`.

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `answer-onboarding-question` (primary) | Answer an onboarding question, with citations | `search_confluence` (live read), `web_search`, `list_drive_files` | `knowledge.tech`, `knowledge.project` |

```text
naveo/
├── README.md         this file (not published)
├── VERSION           the agent's version, bumped when a published file changes
├── index.md          generated, do not edit
├── agent.okf.md      the agent: identity, status, task list, model, access, tile
├── tasks/
│   └── answer-onboarding-question.md    the primary task
└── prompts/
    └── answer-onboarding-question.md    its system prompt
```

See the [OKF field reference](../../docs/okf-reference.md) and [how to add an agent](../../docs/add-an-agent.md).
