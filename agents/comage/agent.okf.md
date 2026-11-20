---
okf_version: "0.2"
type: agent
title: Comage
description: >-
  Sales assistant. Answers deal-status questions grounded in indexed and
  live Salesforce data, updates opportunities, and checks the user's own
  Drive/Gmail for account-relevant material.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/agent.okf.md
sources:
- id: knowledge.sales
  resource: urn:zuno:knowledge:sales
  title: Knowledge domain knowledge.sales, ingested from Salesforce
- id: salesforce
  resource: urn:zuno:source:salesforce
  title: Salesforce, through the opportunity tools
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: comage
  status: active
  graph_shape: retrieve_reason_respond
  primary_task: check-deal-status
  tasks:
    - check-deal-status
    - update-opportunity-status
    - check-my-drive-and-mail
  model:
    preferred_classification: C2
    notes: >-
      C2 matches the classification of the sales data the agent reads
      (`knowledge.sales` and the `salesforce.*` tools).
  access:
    groups:
      - agent_comage
  ui:
    displayName: Comage
    tileDescription: Sales follow-up and pipeline assistant.
    color: "#F0AB00"
    icon: handshake
---

# Comage

Comage is Zuno's sales assistant. It answers deal and pipeline questions,
updates Salesforce opportunities, and finds account material in the user's
own Google Drive and Gmail. Status: `active`.

## Tasks

- `check-deal-status` (primary task): answers from indexed Salesforce
  knowledge (`knowledge.sales`) and project memory (`knowledge.project`), and
  calls `salesforce.opportunity.read` live (`zuno.live_read_tool`) when the
  answer needs a current value such as a stage or an amount. It can render a
  chart from real figures (`diagram.generation.create`), create a marketing
  visual on explicit request (`image.generation.create`) and search the web
  (`web_search`). It never writes.
- `update-opportunity-status`: writes a stage, amount or close-date change to
  an existing opportunity through `salesforce.opportunity.update`, the
  agent's only write tool. Indexed knowledge stays read-only: every change
  goes through the live tool (zuno-demo ADR-0205).
- `check-my-drive-and-mail`: lists the user's own Drive documents and Gmail
  messages about an account or opportunity (`list_drive_files`,
  `read_gmail`), with the user's delegated access.

## Workflow, knowledge and access

`zuno.graph_shape: retrieve_reason_respond` (zuno-demo ADR-0342) is the same
workflow shape Tekos uses: retrieve from the allowed knowledge, call the
live-read tool when the answer needs current data, then reason and respond.

Comage declares no agent-level knowledge list: its knowledge ceiling is the
union of its tasks' `zuno.allowed_knowledge`, today
`[knowledge.sales, knowledge.project]`.

`zuno.access.groups` (`agent_comage`) is the entitlement to use the agent.
Inside it, `policies/tools/tool-policy.yaml` and
`policies/knowledge/knowledge-policy.yaml` limit each tool and domain to
business roles: both Salesforce tools to `sales` and `board`.

Conforms to the Zuno OKF profile 1.0
(`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`).
