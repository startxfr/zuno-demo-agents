# Arkos

Architecture assistant for architects. Arkos drafts Design & Architecture
Testimonials (DAT) and Odyssey architecture workshop presentations, grounded
in the technical documentation, Confluence and project memory, with Git
repository access and Mermaid diagrams. It also structures customer demos and
writes code.

**Status:** active. Graph shape `plan_draft_write`, primary task
`draft-architecture-testimonial`. It may delegate one read-only hop to
`tekos` / `answer-technical-question`.

| Task | What it does | Tools | Knowledge |
|---|---|---|---|
| `draft-architecture-testimonial` | Draft a DAT, with diagrams on request | Confluence search and read, 6 Git capabilities, diagram generation, AAP platform audit | `knowledge.tech`, `knowledge.project` |
| `workshop-presentation` | Draft an Odyssey workshop presentation | same as above | same as above |
| `structure-demo` | Structure a customer demo with talking points | none | none |
| `write-code` | Write code, configuration or a script | none | none |

```text
arkos/
├── README.md       this file (not published)
├── VERSION         the agent's version, bumped when a published file changes
├── index.md        generated, do not edit
├── agent.okf.md    agent declaration, with the generated authorization matrix
├── tasks/          one file per task: scope, tools, knowledge, reply cap
├── prompts/        one system prompt per task, plus the reflect-slot prompts
├── tools/          one usage note per declared tool, named after the capability
├── rag/            one note per knowledge domain: tech.md, project.md
└── tests/          contract, task and prompt checks (not published)
```

See the [OKF field reference](../../docs/okf-reference.md) and the
[guide to add an agent](../../docs/add-an-agent.md).
