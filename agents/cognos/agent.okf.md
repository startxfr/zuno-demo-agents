---
okf_version: v0.2
type: agent
title: Cognos
description: >-
  Board-only financial and strategic assistant. Answers Direction-level
  financial and strategic questions with access to a large tool set
  explicitly excluding technical tools and the technical RAG corpora.
provenance:
  maintainer: Zuno Demo architecture team
  repository: zuno-demo
verification:
  status: unverified
freshness:
  last_reviewed: "2026-08-15"
sources: []
zuno:
  name: cognos
  status: placeholder
  tasks:
    - coming-soon
  model:
    preferred_classification: C3
    notes: >-
      Placeholder pending a future build (ADR-0349 defines only the
      identity footprint); C3 anticipated because Direction-level
      financial and strategic material is local-model-only by nature.
  access:
    # ADR-0040: agent entitlement group, orthogonal to the `board`
    # business role that will govern tool/data permissions inside Cognos
    # (ADR-0349 §6 - audience is Direction only).
    groups:
      - agent_cognos
  ui:
    displayName: Cognos
    tileDescription: Board financial and strategic assistant - coming soon.
    color: "#4A148C"
    icon: chart-line
---

# Cognos

ADR-0349 §6: `status` is `placeholder` - this bundle, the
`cognos-frontend` Keycloak client, the `agent_cognos` entitlement group
and this portal tile are the only things that exist for Cognos today
(the original placeholder pattern comage/advantage/finage/arkos each
started from). No dedicated namespace is reserved (ADR-0329): a future
active Cognos deployment would run in the shared `zuno-ai-run`
namespace, CR-managed via the AIAgent operator (ADR-0327/ADR-0308) like
every agent onboarded since WP-38.

`tasks/coming-soon.md` describes the intended build - Direction-level
financial and strategic Q&A over RAG/MCP capabilities that explicitly
exclude the technical tools and technical RAG corpora - kept here so
onboarding Cognos later is primarily a `status: active` flip plus real
task implementation through the ADR-0307 template workflow
(`platform/templates/agent/`), not a redesign.

Its first real task, `review-historical-commercial-data`, was removed on 2026-11-02 (WP-185): its only
knowledge source, the pre-2021 SXA record, is no longer served since the RAG moved to UnifAI (WP-168).
Cognos is back to the `coming-soon` placeholder until a real task is authored (`NEXT_STEPS.md`).

<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_cognos`; model classification ceiling (ADR-0021): `C3`; status: `placeholder`.

No capabilities declared: every task's `allowed_tools`/`allowed_knowledge` is empty, so this agent can invoke no tool and retrieve from no knowledge domain regardless of caller groups (the honest Stage-1 zero-capability state, ADR-0502).

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `coming-soon` | `C3` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default).

<!-- END GENERATED AUTHORIZATION MATRIX -->
