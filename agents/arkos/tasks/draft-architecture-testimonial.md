---
okf_version: "0.2"
type: task
title: Draft an architecture testimonial
description: Draft a Design & Architecture Testimonial (DAT) from the technical documentation, Confluence and project memory, with diagrams on request.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tasks/draft-architecture-testimonial.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  max_tokens: 8192
  allowed_tools:
    - confluence.page.read
    - confluence.page.search
    - git.repository.read
    - git.repository.list
    - git.repository.private.read
    - git.repository.private.list
    - git.file.write
    - git.repository.create
    - diagram.generation.create
    - aap.platform.audit
  allowed_knowledge:
    - knowledge.tech
    - knowledge.project
  prompts:
    reflect:
      classification_ceiling: C2
  prompt_examples:
    - "Draft an architecture testimonial for a customer running OpenShift with Keycloak-backed SSO."
    - "Write a Design and Architecture Testimonial covering a GitOps delivery chain based on Argo CD."
---

# Draft an architecture testimonial

Draft a Design & Architecture Testimonial (DAT): a long-form document that
describes an architecture, grounded in the technical documentation corpus,
internal Confluence content and the user's project memory, and return it in
the reply. A plain factual question gets a direct, short answer instead of a
document.

The `plan_draft_write` steps:

1. Plan: derive the document's topic and title from the request.
2. Retrieve: search `knowledge.tech` and `knowledge.project` by topic.
3. Draft: write the long-form document.
4. Reflect: review and improve the draft with the `reflect` prompt.
5. Write: return the document in the reply.

Tools: see `allowed_tools` and the notes in `tools/`.

Not declared: writing to Google Drive or Docs, so the document comes back
in the reply and is not saved; Jira; repository fork and delete; image
generation.
