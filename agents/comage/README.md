# Comage

Sales assistant: answers deal and pipeline questions from indexed and live
Salesforce data, updates opportunities, and finds account material in the
user's own Google Drive and Gmail.

**Status:** active (`zuno.status: active`). Entitlement group `agent_comage`;
the Salesforce tools are limited to the `sales` and `board` business roles.

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `check-deal-status` (primary) | Answers a deal or pipeline question, with a live read for current values | `salesforce.opportunity.read` (live read), `web_search`, `image.generation.create`, `diagram.generation.create` | `knowledge.sales`, `knowledge.project` |
| `update-opportunity-status` | Changes the stage, amount or close date of an existing opportunity (write) | `salesforce.opportunity.update` | none |
| `check-my-drive-and-mail` | Lists the user's own Drive documents and Gmail messages about an account | `list_drive_files`, `read_gmail` | none |

```text
comage/
├── README.md            this file
├── VERSION              the agent's own version
├── agent.okf.md         agent document: identity, access, model, tasks
├── index.md             bundle index (generated, do not edit)
├── tasks/               one document per task: tools, knowledge, scope
├── prompts/             the system prompt of each task
├── tools/               one usage note per declared tool (grants nothing)
├── rag/                 one note per knowledge domain: sales.md, project.md (grants nothing)
└── tests/               contract/, tasks/, prompts/ suites (structure only today)
```

See the [OKF field reference](../../docs/okf-reference.md) and the
[guide to add an agent](../../docs/add-an-agent.md).
