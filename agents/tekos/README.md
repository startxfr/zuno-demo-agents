# Tekos Agent

- **Purpose:** Technical consultant assistant
- **Primary integrations:** Official technical RAG, Confluence, web search
- **Initial tasks:** Technical Q&A with concise citations; first MVP vertical slice

## Stage (ADR-0502)

**Stage 2 — promoted** (grandfathered on criterion b: Tekos deliberately
stays on plain manifests as the ADR-0350/ADR-0308 coexistence proof — it
is the one agent whose deployment interface is not an `AIAgent` CR).

- `zuno.status: active`; the only agent with a live Agent Runtime route
  (`POST /v1/agents/tekos/chat`, `retrieve_reason_respond` graph shape).
- Deployed by `gitops/charts/tekos/` (raw Deployment/Service/Route set)
  via `gitops/apps/api/application-d1.yaml`.
- Evaluations: `evaluations/tekos/` is the canonical shared
  implementation every other agent's wrappers delegate to (ADR-0342);
  Tekos cleared the ADR-0027/0028 gates as the v0 vertical slice
  (ADR-0031).
- Stage-2 criterion c is structural debt shared by every agent:
  `deployment/` and `tests/` gain their real ADR-0503/ADR-0504 content
  with WP-45/WP-46; `policies/`, `rag/` and `tools/` gain theirs with
  WP-56/ADR-0513.

**Next step:** none for promotion (already Stage 2); migrating off plain
manifests remains a deliberate non-goal while the coexistence proof
stands.

## Declarative structure (ADR-0038: OKF Markdown bundles)

The whole bundle is OKF v0.3 (ADR-0579): the agent declares its guardrail
mode and each task its model roles; the `rag/`, `tools/` and `policies/`
notes only change their version.

```text
tekos/
├── README.md
├── VERSION               the agent's own version (bumped when published files change)
├── agent.okf.md          Agent index bundle (YAML frontmatter + Markdown body)
├── tasks/
│   ├── answer-technical-question.md   (primary task, the live chat route)
│   ├── find-relevant-docs.md
│   ├── check-my-drive-docs.md
│   └── write-code.md
├── prompts/
│   └── answer-technical-question.md   System prompt of the primary task
├── policies/             1 narrowing-only addendum (web-search-scope.md)
├── rag/                  2 per-domain retrieval notes (tech.md, project.md)
├── tools/                3 per-tool usage notes
└── tests/                contract/, tasks/, prompts/ (structure; suites are added at promotion)
```

The agent is declarative: `agent.okf.md` plus linked per-task and per-prompt Markdown
documents. A platform that consumes a release supplies the runtime. This directory
contains only the agent's behavior, policy and knowledge references. See the
[OKF field reference](../../docs/okf-reference.md) and the
[guide to add an agent](../../docs/add-an-agent.md).
