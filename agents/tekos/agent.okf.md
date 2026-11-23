---
okf_version: "0.2"
type: agent
title: Tekos
description: >-
  Technical consultant assistant. Answers technical questions grounded in
  official product documentation and internal Confluence content, with
  concise citations, and helps consultants locate relevant reference
  material across the RAG corpus and their own Drive.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/tekos/agent.okf.md
sources:
- id: technical-docs
  resource: urn:zuno:knowledge:tech
  title: Official product documentation (OpenShift, Kubernetes, Keycloak, Ansible, Argo CD, Helm, Go), indexed as knowledge.tech
- id: confluence
  resource: urn:zuno:source:confluence
  title: Internal Confluence spaces, through the search_confluence tool
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: tekos
  status: active
  graph_shape: retrieve_reason_respond
  primary_task: answer-technical-question
  tasks:
    - answer-technical-question
    - find-relevant-docs
    - check-my-drive-docs
    - write-code
  rag:
    top_k: 5
  model:
    preferred_classification: C2
    notes: >-
      Public product documentation and general technical Q&A are C1. The
      agent's ceiling is C2 because it reads Confluence content (C2) and,
      for the platform personas, cluster logs and AAP state (C2), so every
      call is routed at C2 at least. Confluence content stays on local
      models through the tool policy and the tasks' local_only_for, and C2
      leaves out the C1-only SaaS models (gemini, mistral). The model
      catalog and each task's preference live in
      policies/models/model-catalog.yaml and
      policies/model-routing/model-routing-policy.yaml; the resolved chain is
      in docs/authorization-matrix/tekos.md.
  guardrails:
    mode: observe
  limits:
    memory:
      history:
        enabled: true
        max_turns: 6
        token_budget: 6000
  access:
    groups:
      - agent_tekos
      - agent_tekos_preview
  ui:
    displayName: Tekos
    tileDescription: Technical Q&A with citations, for consultants.
    color: "#0066CC"
    icon: code
---

# Tekos

Technical consultant assistant. Tekos answers technical questions about
OpenShift, Kubernetes and the surrounding Red Hat ecosystem from official
product documentation and internal Confluence content, with citations. It
also finds reference material for a topic, lists the consultant's own Drive
documents, and writes code.

The bundle follows the Zuno OKF profile 1.0
(`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`). Each task of
`zuno.tasks` is declared in `tasks/<task>.md` and has its system prompt in
`prompts/<task>.md`; `answer-technical-question` is the primary task.

`zuno.graph_shape: retrieve_reason_respond` names the workflow of a turn:
retrieve from the task's knowledge domains, an optional live-read tool call,
reason, respond.

Tekos declares no agent-level `allowed_tools` or `allowed_knowledge`: its
ceiling is the union of its tasks' declarations (zuno-demo ADR-0203). That
union is 13 tools and two knowledge domains, `knowledge.tech` (from
`answer-technical-question` and `find-relevant-docs`) and
`knowledge.project` (from `answer-technical-question`).
