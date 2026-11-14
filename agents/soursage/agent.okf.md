---
okf_version: "0.2"
type: agent
title: Soursage
description: >-
  Recruiting assistant. Interacts with Workday and LinkedIn to source new
  consultant candidates and to find, among existing consultants, the best
  profile for a mission.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/soursage/agent.okf.md
status: draft
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: soursage
  status: placeholder
  tasks:
    - coming-soon
  model:
    preferred_classification: C2
    notes: >-
      Placeholder pending a future build (ADR-0349 defines only the
      identity footprint); C2 anticipated because candidate/consultant
      profile data requires context filtering rather than unrestricted
      SaaS use.
  access:
    # ADR-0040: agent entitlement group, orthogonal to the `recrut` and
    # `sales` business roles that will govern tool/data permissions
    # inside Soursage (ADR-0349 §6 - future tools gate on those roles
    # and on the ADR-0340 Workday capability scopes,
    # workday.profile.any.read, read-only).
    groups:
      - agent_soursage
  ui:
    displayName: Soursage
    tileDescription: Consultant sourcing and staffing assistant - coming soon.
    color: "#00695C"
    icon: users
---

# Soursage

Recruiting assistant: it will source new consultant candidates and find, among existing consultants, the best profile
for a mission (zuno-demo ADR-0349).

`status: placeholder`: the agent is declared but not served, and a portal shows its tile as "coming soon" to members of
`agent_soursage`. Its single task, `coming-soon`, declares no tool and no knowledge domain, so the agent has no
capability by construction.

The intended build reads consultant profiles from Workday and candidates from LinkedIn, gated on the `recrut` and
`sales` business roles. The corp tool policy already registers the read-only `workday.profile.any.read` capability
(granted to `cdp` only today); no LinkedIn capability exists yet. Building the agent means authoring real tasks with
their prompts and policy entries, then setting `status: active`.

The bundle follows the Zuno OKF profile 1.0 (`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`).

<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_soursage`; model classification ceiling (ADR-0021): `C2`; status: `placeholder`.

No capabilities declared: every task's `allowed_tools`/`allowed_knowledge` is empty, so this agent can invoke no tool and retrieve from no knowledge domain regardless of caller groups (the honest Stage-1 zero-capability state, ADR-0502).

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `coming-soon` (prompt: `prompts/coming-soon.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh`, `openai`, `anthropic`, `mistral-codestral`, `ovhcloud-gpt-oss-120b` | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default), `openai` → `gpt-4o-mini` (general-external), `anthropic` → `claude-3-5-sonnet-latest` (general-external), `mistral-codestral` → `codestral-latest` (code), `ovhcloud-gpt-oss-120b` → `gpt-oss-120b` (reasoning-external).

<!-- END GENERATED AUTHORIZATION MATRIX -->
