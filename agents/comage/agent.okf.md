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
    # Entitlement group to use the agent (zuno-demo ADR-0040), separate from
    # the `sales` business role that the tool and knowledge policies check.
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

<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_comage`; model classification ceiling (ADR-0021): `C2`; status: `active`.

| Task (FOR WHAT) | Resource (WHAT) | Kind | Capability / server | Min class | Business roles (WHO) | Ext-model context | Quota | Policy source |
|---|---|---|---|---|---|---|---|---|
| `check-deal-status` (primary; prompt: `prompts/check-deal-status.md`) | `salesforce.opportunity.read` (live-read) | tool | `salesforce.opportunity.read` @ salesforce | C2 | sales, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `salesforce.opportunity.read` |
| `check-deal-status` (primary; prompt: `prompts/check-deal-status.md`) | `web_search` | tool | `web.page.search` @ web-search | C1 | sales, consultant, adv, finance, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `web_search` |
| `check-deal-status` (primary; prompt: `prompts/check-deal-status.md`) | `image.generation.create` | tool | `image.generation.create` @ image-gen | C2 | consultant, adv, sales, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `generate_image` |
| `check-deal-status` (primary; prompt: `prompts/check-deal-status.md`) | `diagram.generation.create` | tool | `diagram.generation.create` @ diagram-gen | C1 | consultant, adv, sales, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `generate_diagram` |
| `check-deal-status` (primary; prompt: `prompts/check-deal-status.md`) | `knowledge.sales` | knowledge | — | C2 | sales, adv, board, cdp, finance | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.sales` |
| `check-deal-status` (primary; prompt: `prompts/check-deal-status.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `update-opportunity-status` (prompt: `prompts/update-opportunity-status.md`) | `salesforce.opportunity.update` | tool | `salesforce.opportunity.update` @ salesforce | C2 | sales, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `salesforce.opportunity.update` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `list_drive_files` | tool | `drive.document.search` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `list_drive_files` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `read_gmail` | tool | `gmail.message.read` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `read_gmail` |

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `check-deal-status` (primary; prompt: `prompts/check-deal-status.md`) | `C2` | `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized) | `local-wesh`, `local-qwen35-maas`, `local-qwen35`, `local-maas`, `local`, `local-gpt-oss-maas`, `local-gpt-oss`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |
| `update-opportunity-status` (prompt: `prompts/update-opportunity-status.md`) | `C2` | `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized) | `local-wesh`, `local-qwen35-maas`, `local-qwen35`, `local-maas`, `local`, `local-gpt-oss-maas`, `local-gpt-oss`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `C2` | `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized) | `local-wesh`, `local-qwen35-maas`, `local-qwen35`, `local-maas`, `local`, `local-gpt-oss-maas`, `local-gpt-oss`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default), `openai` → `gpt-4o-mini` (general-external), `anthropic` → `claude-3-5-sonnet-latest` (general-external), `mistral-codestral` → `codestral-latest` (code), `ovhcloud-gpt-oss-120b` → `gpt-oss-120b` (reasoning-external).

<!-- END GENERATED AUTHORIZATION MATRIX -->
