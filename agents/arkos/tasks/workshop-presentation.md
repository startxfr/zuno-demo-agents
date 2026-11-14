---
okf_version: "0.2"
type: task
title: Prepare an Odyssey workshop presentation
description: Draft an Odyssey architecture workshop presentation from the technical documentation, Confluence and project memory.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tasks/workshop-presentation.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  # Reply cap (zuno-demo ADR-0544): without one, a reply once ran to about
  # 40k tokens. 8192 is the schema ceiling and leaves room for a long
  # presentation.
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
    # Mermaid-to-SVG rendering for architecture diagrams (zuno-demo
    # ADR-0516). Photorealistic image generation is not declared.
    - diagram.generation.create
    # The read-only AAP audit only (zuno-demo ADR-0355): live platform state
    # is useful context for an architecture narrative, but a drafting task
    # has no reason to launch automation, so aap.cluster.audit is not
    # declared.
    - aap.platform.audit
  allowed_knowledge:
    - knowledge.tech
    - knowledge.project
  # `reflect`: a self-review pass over the draft, with its own prompt
  # (prompts/workshop-presentation--reflect.md) and a C2 classification
  # ceiling.
  prompts:
    reflect:
      classification_ceiling: C2
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "Prepare an Odyssey workshop presentation on OpenShift AI model serving."
    - "Draft the workshop agenda for an architecture review of a Keycloak-based SSO."
---

# Prepare an Odyssey workshop presentation

Draft an Odyssey architecture workshop presentation: a structured document
covering what the workshop will present, grounded in the technical
documentation corpus, internal Confluence content and the user's project
memory, and return it in the reply. A plain factual question gets a direct,
short answer instead of a document.

It runs the same `plan_draft_write` steps as `draft-architecture-testimonial`
(plan, retrieve, draft, reflect, write): the plan step selects this task
instead of the DAT when the request is about a workshop or Odyssey
(zuno-demo ADR-0514, a second document kind through the same workflow).

Scope: one presentation document per turn. The other artifacts of an
Odyssey engagement (Google Sheets and Slides, the build and run roadmap,
workshop reports) are not produced by this task.

Tools and knowledge are the same as `draft-architecture-testimonial`'s, with
the same rules: Confluence content is processed by local models only,
private repositories are read on GitLab only, `git.file.write` commits only
to public repositories, and every diagram goes through
`diagram.generation.create`. Not declared: writing to Google Drive or Docs,
Jira, repository fork and delete, image generation.
