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
    # ADR-0040: agent entitlement group, orthogonal to the `adv` business
    # role that governs tool/data permissions inside Advantage.
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

<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_advantage`; model classification ceiling (ADR-0021): `C2`; status: `placeholder`.

| Task (FOR WHAT) | Resource (WHAT) | Kind | Capability / server | Min class | Business roles (WHO) | Ext-model context | Quota | Policy source |
|---|---|---|---|---|---|---|---|---|
| `answer-project-question` (primary; prompt: `prompts/answer-project-question.md`) | `web_search` | tool | `web.page.search` @ web-search | C1 | sales, consultant, adv, finance, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `web_search` |
| `answer-project-question` (primary; prompt: `prompts/answer-project-question.md`) | `image.generation.create` | tool | `image.generation.create` @ image-gen | C2 | consultant, adv, sales, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `generate_image` |
| `answer-project-question` (primary; prompt: `prompts/answer-project-question.md`) | `knowledge.adv` | knowledge | — | C2 | adv, board, cdp, finance | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.adv` |
| `answer-project-question` (primary; prompt: `prompts/answer-project-question.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `identify-new-business-with-po` (prompt: `prompts/identify-new-business-with-po.md`) | `knowledge.adv` | knowledge | — | C2 | adv, board, cdp, finance | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.adv` |
| `monthly-sales-report` (prompt: `prompts/monthly-sales-report.md`) | `knowledge.adv` | knowledge | — | C2 | adv, board, cdp, finance | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.adv` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `list_drive_files` | tool | `drive.document.search` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `list_drive_files` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `read_gmail` | tool | `gmail.message.read` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `read_gmail` |

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `answer-project-question` (primary; prompt: `prompts/answer-project-question.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |
| `identify-new-business-with-po` (prompt: `prompts/identify-new-business-with-po.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |
| `monthly-sales-report` (prompt: `prompts/monthly-sales-report.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default), `openai` → `gpt-4o-mini` (general-external), `anthropic` → `claude-3-5-sonnet-latest` (general-external), `mistral-codestral` → `codestral-latest` (code), `ovhcloud-gpt-oss-120b` → `gpt-oss-120b` (reasoning-external).

<!-- END GENERATED AUTHORIZATION MATRIX -->
