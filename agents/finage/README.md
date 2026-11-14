# Finage

Finance assistant: invoicing and billing questions, business ready to invoice, the monthly invoicing report for one
client engagement, and the user's own Drive documents and Gmail messages. It reads the durable project memory of
engagements; no billing history is available, so every figure is retrieved and attributed, never computed. Finance
material stays on local models (`model.local_only: true`).

**Status: placeholder.** Declared but not served. Entitlement group: `agent_finage`; business role: `finance`. The two
invoice tasks are project-bound (`project_required: true`): they run only for one verified engagement.

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `answer-finance-question` (primary) | Answer an invoicing, billing or reporting question | `web_search` | `knowledge.project` |
| `identify-business-ready-to-invoice` | Business of one engagement that reached the billable state | `salesforce.opportunity.read` (project check only) | `knowledge.project` |
| `monthly-invoice-report` | Monthly invoicing report for one engagement | `salesforce.opportunity.read` (project check only) | `knowledge.project` |
| `check-my-drive-and-mail` | The user's own Drive documents and Gmail messages | `list_drive_files`, `read_gmail` | none |

```text
finage/
├── README.md         this file (not published)
├── VERSION           the agent's version, bumped when a published file changes
├── index.md          generated, do not edit
├── agent.okf.md      the agent: identity, status, task list, model, access, tile
├── tasks/
│   ├── answer-finance-question.md        primary task
│   ├── identify-business-ready-to-invoice.md
│   ├── monthly-invoice-report.md
│   └── check-my-drive-and-mail.md
├── prompts/          the system prompt of each task, one file per task, same name
└── tests/            contract/, tasks/ and prompts/ suites (not published)
```

See the [OKF field reference](../../docs/okf-reference.md) and [how to add an agent](../../docs/add-an-agent.md).
