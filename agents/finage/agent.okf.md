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
    # ADR-0040: agent entitlement group, orthogonal to the `finance`
    # business role that governs tool/data permissions inside Finage.
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

<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_finage`; model classification ceiling (ADR-0021): `C2`; status: `placeholder`; local-only (ADR-0416): `true`.

| Task (FOR WHAT) | Resource (WHAT) | Kind | Capability / server | Min class | Business roles (WHO) | Ext-model context | Quota | Policy source |
|---|---|---|---|---|---|---|---|---|
| `answer-finance-question` (primary; prompt: `prompts/answer-finance-question.md`) | `web_search` | tool | `web.page.search` @ web-search | C1 | sales, consultant, adv, finance, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `web_search` |
| `answer-finance-question` (primary; prompt: `prompts/answer-finance-question.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `identify-business-ready-to-invoice` (project-required; prompt: `prompts/identify-business-ready-to-invoice.md`) | `salesforce.opportunity.read` | tool | `salesforce.opportunity.read` @ salesforce | C2 | sales, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `salesforce.opportunity.read` |
| `identify-business-ready-to-invoice` (project-required; prompt: `prompts/identify-business-ready-to-invoice.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `monthly-invoice-report` (project-required; prompt: `prompts/monthly-invoice-report.md`) | `salesforce.opportunity.read` | tool | `salesforce.opportunity.read` @ salesforce | C2 | sales, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `salesforce.opportunity.read` |
| `monthly-invoice-report` (project-required; prompt: `prompts/monthly-invoice-report.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `list_drive_files` | tool | `drive.document.search` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `list_drive_files` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `read_gmail` | tool | `gmail.message.read` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `read_gmail` |

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `answer-finance-question` (primary; prompt: `prompts/answer-finance-question.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |
| `identify-business-ready-to-invoice` (project-required; prompt: `prompts/identify-business-ready-to-invoice.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |
| `monthly-invoice-report` (project-required; prompt: `prompts/monthly-invoice-report.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default).

<!-- END GENERATED AUTHORIZATION MATRIX -->
