---
okf_version: "0.2"
type: task
title: Answer a technical question
description: Answer a technical question from the documentation corpus and Confluence, with citations.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/tekos/tasks/answer-technical-question.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - search_confluence
    - web_search
    - git.repository.read
    - git.repository.list
    - diagram.generation.create
    - aap.platform.audit
    - aap.cluster.audit
    - k8s.resource.read
    - k8s.resource.list
    - k8s.events.read
    - k8s.logs.read
    - metrics.query
  live_read_tool: search_confluence
  allowed_knowledge:
    - knowledge.tech
    - knowledge.project
  models:
    preferred:
      - reasoning
      - reasoning-external
      - default
      - specialized
      - quality
  prompt_examples:
    - "How do I configure Keycloak as the OIDC identity provider for an OpenShift cluster?"
    - "What is the difference between a Route and an Ingress on OpenShift?"
    - "How does Argo CD decide that an Application is out of sync?"
---

# Answer a technical question

Answer a free-form technical question from the indexed documentation corpus
(`knowledge.tech`: official Red Hat product documentation and internal
Confluence content) and the consultant's project memory
(`knowledge.project`). When the retrieved documents do not ground an
answer, the live-read tool `search_confluence` reads Confluence directly;
`web_search` is the last resort, within this bundle's
`policies/web-search-scope.md`.
Every answer cites its sources.

The other tools serve specific questions:

- `git.repository.read` and `git.repository.list` read public GitHub or
  GitLab repositories. Tekos declares no private-repository or repository
  write capability.
- `diagram.generation.create` renders a Mermaid diagram to SVG.
- `aap.platform.audit` summarizes the state of Ansible Automation Platform;
  `aap.cluster.audit` launches the cluster health check through it.
- `k8s.resource.read`, `k8s.resource.list`, `k8s.events.read`,
  `k8s.logs.read` and `metrics.query` read the zuno-* namespaces and their
  metrics, for the operations persona only.

This is the agent's primary task.
