---
okf_version: "0.2"
type: agent
title: Advantage
description: >-
  Sales administration assistant. Surfaces new business whose client
  purchase order has just been received and produces monthly in-progress
  sales reporting, from indexed sales administration (ADV) and project
  knowledge, never from live Salesforce data. Its ADV knowledge domain
  has no ingestion source at present, so the agent stays a placeholder.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/advantage/agent.okf.md
sources:
- id: knowledge.adv
  resource: urn:zuno:knowledge:adv
  title: Knowledge domain knowledge.adv (no ingestion source at present)
- id: knowledge.project
  resource: urn:zuno:knowledge:project
  title: Knowledge domain knowledge.project (project memory)
status: draft
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: advantage
  status: placeholder
  graph_shape: retrieve_reason_respond
  primary_task: answer-project-question
  tasks:
    - answer-project-question
    - identify-new-business-with-po
    - monthly-sales-report
    - check-my-drive-and-mail
  model:
    preferred_classification: C2
    notes: >-
      C2 matches the classification of the ADV business content the agent
      reads (`knowledge.adv`).
  access:
    groups:
      - agent_advantage
  ui:
    displayName: Advantage
    tileDescription: Sales administration and PO tracking - coming soon.
    color: "#4CB140"
    icon: clipboard-check
---

# Advantage

Sales administration assistant. Its tasks answer project, delivery and bid questions, surface new business whose
client purchase order was just received, produce the monthly in-progress sales report, and list the user's own Drive
documents and Gmail messages about an account or project.

`status: placeholder`: the agent is declared but not served, and a portal shows its tile as "coming soon". Its main
knowledge domain, `knowledge.adv`, has no ingestion source at present; zuno-demo ADR-0532 accepts that the domain stays
sourceless, so the agent stays a placeholder.

The primary task, `answer-project-question`, reads `knowledge.adv` and `knowledge.project` through the
`retrieve_reason_respond` workflow and can call web search and image generation. It declares no `live_read_tool`: no
live ADV capability exists.

Cross-domain boundary (zuno-demo ADR-0326): no task declares the current-sales domain `knowledge.sales` or a live CRM
capability. Advantage holds that boundary by explicit omission from its own declaration, not by a runtime filter. Any
further commercial access must be declared here and stay policy-controlled, never inherited from the sales agent.

The knowledge ceiling is the union of the tasks' `allowed_knowledge`: `knowledge.adv` and `knowledge.project`. The
entitlement group is `agent_advantage`; inside the agent, the `adv` business role governs tool and data access through
`policies/tools/tool-policy.yaml` and `policies/knowledge/knowledge-policy.yaml`.

The bundle follows the Zuno OKF profile 1.0 (`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`).
