---
okf_version: "0.2"
type: agent
title: Finage
description: >-
  Finance assistant. Identifies business ready to invoice and produces
  monthly invoice reporting from the durable project memory of one client
  engagement, never from live Salesforce or sales administration data.
  No billing history is available, so every figure is retrieved and
  attributed, never computed.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/finage/agent.okf.md
sources:
- id: knowledge.project
  resource: urn:zuno:knowledge:project
  title: Knowledge domain knowledge.project (project memory)
status: draft
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: finage
  status: placeholder
  graph_shape: retrieve_reason_respond
  primary_task: answer-finance-question
  tasks:
    - answer-finance-question
    - identify-business-ready-to-invoice
    - monthly-invoice-report
    - check-my-drive-and-mail
  model:
    preferred_classification: C2
    local_only: true
    notes: >-
      Placeholder pending the live acceptance gate; C2 default.
      ADR-0416:
      `local_only: true` makes Finage local-model-only
      unconditionally, at every classification including C1 - finance
      material never leaves the cluster, full stop, rather than riding
      the standard C2 restricted-SaaS-allowlist default every other C2
      agent gets.
  access:
    groups:
      - agent_finage
  ui:
    displayName: Finage
    tileDescription: Billing and invoice reporting assistant - coming soon.
    color: "#5752D1"
    icon: calculator
---

# Finage

Finance assistant. Its tasks answer invoicing and billing questions, identify business ready to invoice, produce the
monthly invoicing report for one engagement, and list the user's own Drive documents and Gmail messages about an
account or invoice.

`status: placeholder`: the agent is declared but not served, and a portal shows its tile as "coming soon".

No finance-specific knowledge domain exists, so the tasks that retrieve read `knowledge.project`, the durable memory of
client engagements. No billing history and no exact-figure capability are available either: every number Finage
reports is retrieved and attributed, never computed, and never presented as the current state of an invoice.

The two invoice tasks set `project_required: true`. They run only after the user's project is verified with
`salesforce.opportunity.read` under the user's own identity, failing closed. That capability is declared for the
binding check only: no Salesforce record content reaches the model. A verified binding scopes `knowledge.project`
retrieval to that engagement.

Least privilege (zuno-demo ADR-0326): no task declares `knowledge.sales`, `knowledge.adv` or a capability that reads
Salesforce data into an answer, so Finage stays finance-scoped by explicit omission from its own declaration, not by a
runtime filter. `model.local_only: true` keeps finance material on local models at every classification (zuno-demo
ADR-0416).

The knowledge ceiling is the union of the tasks' `allowed_knowledge`: `knowledge.project`. The entitlement group is
`agent_finage`; inside the agent, the `finance` business role governs tool and data access through
`policies/tools/tool-policy.yaml` and `policies/knowledge/knowledge-policy.yaml`.

The bundle follows the Zuno OKF profile 1.0 (`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`).
