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
    # ADR-0040: agent entitlement group, orthogonal to the
    # `consultant` business role that governs tool/data
    # permissions inside Naveo (policies/tools/tool-policy.yaml).
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

<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_naveo`; model classification ceiling (ADR-0021): `C1`; status: `placeholder`.

| Task (FOR WHAT) | Resource (WHAT) | Kind | Capability / server | Min class | Business roles (WHO) | Ext-model context | Quota | Policy source |
|---|---|---|---|---|---|---|---|---|
| `answer-onboarding-question` (primary; prompt: `prompts/answer-onboarding-question.md`) | `search_confluence` (live-read) | tool | `confluence.page.search` @ confluence | C2 | consultant, board, cdp, lightspeed_readonly, ocp-ai-ops | blocked | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `search_confluence` |
| `answer-onboarding-question` (primary; prompt: `prompts/answer-onboarding-question.md`) | `web_search` | tool | `web.page.search` @ web-search | C1 | sales, consultant, adv, finance, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `web_search` |
| `answer-onboarding-question` (primary; prompt: `prompts/answer-onboarding-question.md`) | `list_drive_files` | tool | `drive.document.search` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `list_drive_files` |
| `answer-onboarding-question` (primary; prompt: `prompts/answer-onboarding-question.md`) | `knowledge.tech` | knowledge | — | — | consultant, board, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.tech` |
| `answer-onboarding-question` (primary; prompt: `prompts/answer-onboarding-question.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `answer-onboarding-question` (primary; prompt: `prompts/answer-onboarding-question.md`) (in a classified project) | `C1/C2/C3` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default).

<!-- END GENERATED AUTHORIZATION MATRIX -->
