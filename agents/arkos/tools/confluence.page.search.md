---
okf_version: "0.2"
type: tool
title: Confluence page search
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/confluence.page.search.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: confluence.page.search
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Searches internal Confluence pages by text, optionally within one space,
    for the document's topic. Input: a text query, an optional space key and a
    result limit. Output: matching pages with their ids, which
    confluence.page.read opens. Used while drafting a DAT or a workshop
    presentation, next to the retrieved documentation.
  known_limitations:
    - "min_classification C2; external_model_policy.allow_context false: results are processed by local models only."
    - "Read access. allowed_groups: consultant, board, cdp, lightspeed_readonly, ocp-ai-ops."
---

# Confluence page search

Finds the internal Confluence pages that describe the architecture being
written up, so a document can cite real internal content alongside the
documentation corpus.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
