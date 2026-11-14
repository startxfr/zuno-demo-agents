# Advantage

Sales administration assistant: project, delivery and bid questions, new business whose client purchase order was just
received, the monthly in-progress sales report, and the user's own Drive documents and Gmail messages. It reads indexed
sales administration (ADV) and project knowledge, never live Salesforce data.

**Status: placeholder.** Declared but not served. Its main knowledge domain, `knowledge.adv`, has no ingestion source
(zuno-demo ADR-0532), so the agent stays a placeholder. Entitlement group: `agent_advantage`; business role: `adv`.

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `answer-project-question` (primary) | Answer a project, delivery or bid question | `web_search`, `image.generation.create` | `knowledge.adv`, `knowledge.project` |
| `identify-new-business-with-po` | New business with a client PO received in the last three days | none | `knowledge.adv` |
| `monthly-sales-report` | Monthly in-progress sales report (margin by state, customer, technology) | none | `knowledge.adv` |
| `check-my-drive-and-mail` | The user's own Drive documents and Gmail messages | `list_drive_files`, `read_gmail` | none |

```text
advantage/
├── README.md         this file (not published)
├── VERSION           the agent's version, bumped when a published file changes
├── index.md          generated, do not edit
├── agent.okf.md      the agent: identity, status, task list, model, access, tile
├── tasks/
│   ├── answer-project-question.md        primary task
│   ├── identify-new-business-with-po.md
│   ├── monthly-sales-report.md
│   └── check-my-drive-and-mail.md
├── prompts/          the system prompt of each task, one file per task, same name
└── tests/            contract/, tasks/ and prompts/ suites (not published)
```

See the [OKF field reference](../../docs/okf-reference.md) and [how to add an agent](../../docs/add-an-agent.md).
