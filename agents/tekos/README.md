# Tekos

Technical consultant assistant. Tekos answers technical questions about
OpenShift, Kubernetes and the surrounding Red Hat ecosystem from official
product documentation and internal Confluence content, with citations. It also
finds reference material for a topic, lists the consultant's own Drive
documents, and writes code.

**Status:** active. Primary task: `answer-technical-question`.

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `answer-technical-question` | Answers a technical question, with citations | `search_confluence` (live read), `web_search`, `git.repository.read`, `git.repository.list`, `diagram.generation.create`, `aap.platform.audit`, `aap.cluster.audit`, `k8s.resource.read`, `k8s.resource.list`, `k8s.events.read`, `k8s.logs.read`, `metrics.query` | `knowledge.tech`, `knowledge.project` |
| `find-relevant-docs` | Lists the material on a topic, without composing an answer | `search_confluence`, `list_drive_files` | `knowledge.tech` |
| `check-my-drive-docs` | Lists the consultant's own Drive documents on a topic | `list_drive_files` | none |
| `write-code` | Writes code, configuration or a script in the reply | none | none |

```text
tekos/
├── README.md       this file
├── VERSION         the agent's own version, bumped when a published file changes
├── index.md        generated, do not edit
├── agent.okf.md    the agent: description, tasks, model, guardrails, history, access, UI
├── tasks/          one declaration per task: tools, knowledge, model roles, example prompts
├── prompts/        the system prompt of each task, one file per task
├── tools/          one usage note per declared tool (13 notes)
├── rag/            one note per knowledge domain (tech.md, project.md)
├── policies/       web-search-scope.md, a narrowing-only constraint on web_search
└── tests/          contract/, tasks/ and prompts/ test directories
```

The notes in `tools/` and `rag/` grant nothing, and `policies/` can only
narrow: what Tekos may call or retrieve is each task's declaration
intersected with the corp policies under `policies/` at the repository root.

See the [OKF field reference](../../docs/okf-reference.md) and the
[guide to add an agent](../../docs/add-an-agent.md).
