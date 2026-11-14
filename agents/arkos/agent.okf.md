---
okf_version: "0.2"
type: agent
title: Arkos
description: >-
  Architecture assistant for architects. Drafts Design & Architecture
  Testimonials (DAT) and Odyssey architecture workshop presentations from the
  technical documentation corpus, Confluence and project memory, with Git
  repository access and Mermaid diagram generation. Also structures customer
  demos and writes code.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/agent.okf.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: arkos
  status: active
  graph_shape: plan_draft_write
  primary_task: draft-architecture-testimonial
  tasks:
    - draft-architecture-testimonial
    - workshop-presentation
    - structure-demo
    - write-code
  memory:
    # Arkos is C3, so its history-carrying calls go to local models only. The
    # narrowest local model in its fallback chains serves an 8192-token
    # window, so 6000 tokens of history plus the system prompt, project
    # context and retrieved passages can overflow it: a consumer must bound
    # the assembled prompt to the serving model's window, shedding project
    # context first, then history, and keeping the retrieved passages
    # (zuno-demo ADR-0544).
    history:
      enabled: true
      max_turns: 6
      token_budget: 6000
  model:
    preferred_classification: C3
    notes: >-
      C3 because sovereign-marked DAT workflows must run on local models
      only.
  # Arkos may ask Tekos for a technical answer while it drafts: read-only
  # delegation, one hop (zuno-demo ADR-0401). Arkos is already C3, so the C3
  # raise of a delegating task changes nothing.
  delegation:
    targets:
      - agent: tekos
        task: answer-technical-question
  limits:
    delegation:
      max_depth: 1
  access:
    # Entitlement group (zuno-demo ADR-0040). Inside Arkos, the business
    # role that gates tools and knowledge is `consultant`: architects are
    # the consultant tier (zuno-demo ADR-0349).
    groups:
      - agent_arkos
  ui:
    displayName: Arkos
    tileDescription: Architecture DAT and workshop assistant.
    color: "#8F4700"
    icon: drafting-compass
---

# Arkos

Arkos is the architecture assistant for architects. It drafts Design &
Architecture Testimonials (DAT) and Odyssey architecture workshop
presentations, structures customer demos and writes code. Status: active.

## Workflow

`zuno.graph_shape: plan_draft_write`. Each turn first plans the deliverable,
then takes one of two paths:

- **Document path** (`draft-architecture-testimonial`, the primary task, and
  `workshop-presentation`): retrieve from `knowledge.tech` and
  `knowledge.project` by topic, draft, review the draft with the task's
  `reflect` prompt, and return the document in the reply. A request about a
  workshop or Odyssey selects `workshop-presentation`.
- **Direct path** (`structure-demo`, `write-code`): answer from the user's
  message alone, with no retrieval and no tool call.

## Authorization

There is no agent-level `allowed_knowledge`: the ceiling is the union of the
tasks' declarations. The two document tasks declare Confluence read and
search, six Git repository capabilities, diagram generation and the
read-only AAP platform audit, and the domains `knowledge.tech` and
`knowledge.project`. `structure-demo` and `write-code` declare none.

Arkos may delegate one read-only hop to `tekos` / `answer-technical-question`.

The entitlement group is `agent_arkos`. Inside Arkos, the `consultant`
business role gates tools and knowledge (`policies/tools/tool-policy.yaml`,
`policies/knowledge/knowledge-policy.yaml`). The matrix below restates the
enforced intersection and the effective model chain per task.

<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_arkos`; model classification ceiling (ADR-0021): `C3`; status: `active`.

| Task (FOR WHAT) | Resource (WHAT) | Kind | Capability / server | Min class | Business roles (WHO) | Ext-model context | Quota | Policy source |
|---|---|---|---|---|---|---|---|---|
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `confluence.page.read` | tool | `confluence.page.read` @ confluence | C2 | consultant, board, cdp, lightspeed_readonly, ocp-ai-ops | blocked | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `confluence.page.read` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `confluence.page.search` | tool | `confluence.page.search` @ confluence | C2 | consultant, board, cdp, lightspeed_readonly, ocp-ai-ops | blocked | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `search_confluence` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `git.repository.read` | tool | `git.repository.read` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.read` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `git.repository.list` | tool | `git.repository.list` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.list` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `git.repository.private.read` | tool | `git.repository.private.read` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.private.read` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `git.repository.private.list` | tool | `git.repository.private.list` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.private.list` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `git.file.write` | tool | `git.file.write` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.file.write` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `git.repository.create` | tool | `git.repository.create` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.create` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `diagram.generation.create` | tool | `diagram.generation.create` @ diagram-gen | C1 | consultant, adv, sales, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `generate_diagram` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `aap.platform.audit` | tool | `aap.platform.audit` @ aap | C2 | consultant, board, cdp, ocp-ai-ops | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `aap.platform.audit` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `knowledge.tech` | knowledge | — | — | consultant, board, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.tech` |
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `confluence.page.read` | tool | `confluence.page.read` @ confluence | C2 | consultant, board, cdp, lightspeed_readonly, ocp-ai-ops | blocked | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `confluence.page.read` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `confluence.page.search` | tool | `confluence.page.search` @ confluence | C2 | consultant, board, cdp, lightspeed_readonly, ocp-ai-ops | blocked | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `search_confluence` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `git.repository.read` | tool | `git.repository.read` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.read` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `git.repository.list` | tool | `git.repository.list` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.list` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `git.repository.private.read` | tool | `git.repository.private.read` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.private.read` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `git.repository.private.list` | tool | `git.repository.private.list` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.private.list` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `git.file.write` | tool | `git.file.write` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.file.write` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `git.repository.create` | tool | `git.repository.create` @ git-forge | C2 | consultant, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `git.repository.create` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `diagram.generation.create` | tool | `diagram.generation.create` @ diagram-gen | C1 | consultant, adv, sales, board, cdp | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `generate_diagram` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `aap.platform.audit` | tool | `aap.platform.audit` @ aap | C2 | consultant, board, cdp, ocp-ai-ops | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `aap.platform.audit` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `knowledge.tech` | knowledge | — | — | consultant, board, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.tech` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `draft-architecture-testimonial` (primary; prompt: `prompts/draft-architecture-testimonial.md`) (in a classified project) | `C1/C2/C3` | `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning) | `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh`, `local-qwen35-maas`, `local-qwen35` | — | `policies/model-routing/model-routing-policy.yaml` |
| `workshop-presentation` (prompt: `prompts/workshop-presentation.md`) (in a classified project) | `C1/C2/C3` | `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning) | `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh`, `local-qwen35-maas`, `local-qwen35` | — | `policies/model-routing/model-routing-policy.yaml` |
| `structure-demo` (prompt: `prompts/structure-demo.md`) | `C3` | `local-maas` → `qwen3.6-27b-instruct` (quality) | `local`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-wesh-maas`, `local-wesh`, `local-qwen35-maas`, `local-qwen35` | — | `policies/model-routing/model-routing-policy.yaml` |
| `write-code` (prompt: `prompts/write-code.md`) | `C3` | (none eligible) | — | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default).

<!-- END GENERATED AUTHORIZATION MATRIX -->
