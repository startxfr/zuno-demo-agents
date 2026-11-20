---
okf_version: "0.2"
type: agent
title: Naveo
description: >-
  Onboarding assistant for new team members. Answers questions about internal processes, tooling and where to find reference material, grounded in the technical RAG corpus and internal Confluence content, and can check the caller's own Drive for onboarding documents.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/naveo/agent.okf.md
sources:
- id: knowledge.tech
  resource: urn:zuno:knowledge:tech
  title: Knowledge domain knowledge.tech (technical documentation)
- id: knowledge.project
  resource: urn:zuno:knowledge:project
  title: Knowledge domain knowledge.project (project memory)
status: draft
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: naveo
  status: placeholder
  graph_shape: retrieve_reason_respond
  primary_task: answer-onboarding-question
  tasks:
    - answer-onboarding-question
  rag:
    top_k: 5
  model:
    preferred_classification: C1
    notes: >-
      Reuses the retrieve_reason_respond shape and existing knowledge and
      tool capabilities only; no new external system.
  access:
    groups:
      - agent_naveo
  ui:
    displayName: Naveo
    tileDescription: New-hire onboarding Q&A, for consultants - coming soon.
    color: "#5C6BC0"
    icon: compass
---

# Naveo

Onboarding assistant for new team members. It answers questions about internal processes, tooling and where to find
reference material, grounded in the technical documentation corpus and internal Confluence content, and can check the
user's own Drive for onboarding documents.

`status: placeholder`: the agent is declared but not served, and a portal shows its tile as "coming soon".

Its single task, `answer-onboarding-question`, reuses existing knowledge domains (`knowledge.tech`, `knowledge.project`)
and existing tool capabilities (`search_confluence`, `web_search`, `list_drive_files`) only, with no new knowledge
domain or external system (zuno-demo ADR-0410). `search_confluence` is its live-read tool. The entitlement group is
`agent_naveo`; inside the agent, the `consultant` business role governs tool and data access through
`policies/tools/tool-policy.yaml` and `policies/knowledge/knowledge-policy.yaml`.

The bundle follows the Zuno OKF profile 1.0 (`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`).
