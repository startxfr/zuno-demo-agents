---
okf_version: "0.2"
type: tool
title: Confluence page read
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/confluence.page.read.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: confluence.page.read
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Reads one Confluence page's current content and metadata by page id,
    usually a page found by confluence.page.search. Output: the page body, its
    space and version, used to ground a section of the document.
  known_limitations:
    - "min_classification C2; external_model_policy.allow_context false: content is processed by local models only."
    - "Read access. allowed_groups: consultant, board, cdp, lightspeed_readonly, ocp-ai-ops."
---

# Confluence page read

Opens a Confluence page in full when a search hit is relevant enough to ground
part of the document. Arkos declares no Confluence write capability.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
