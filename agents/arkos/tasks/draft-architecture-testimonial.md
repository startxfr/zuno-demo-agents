---
okf_version: "0.2"
type: task
title: Draft an architecture testimonial
description: Draft a Design & Architecture Testimonial (DAT) from the technical documentation, Confluence and project memory, with diagrams on request.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tasks/draft-architecture-testimonial.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  # Reply cap (zuno-demo ADR-0544): without one, a reply once ran to about
  # 40k tokens. A DAT is about 4k tokens; 8192 is the schema ceiling and
  # leaves room for a long one.
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
    # Mermaid-to-SVG rendering for architecture, sequence and relationship
    # diagrams (zuno-demo ADR-0516). Photorealistic image generation is not
    # declared: the visuals a DAT needs are diagrams.
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
  # (prompts/draft-architecture-testimonial--reflect.md). zuno-demo
  # ADR-0550 decision 4: for this task the review follows the turn's
  # classification, like the draft, rather than the C2 ceiling below; the
  # slot stays declared because it carries the review prompt.
  prompts:
    reflect:
      classification_ceiling: C2
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
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

Tools:

- `confluence.page.search`, `confluence.page.read`: internal Confluence
  pages. Their content is processed by local models only.
- `git.repository.read`, `git.repository.list`: public repositories, on
  GitHub and GitLab.
- `git.repository.private.read`, `git.repository.private.list`: private and
  internal repositories, GitLab only.
- `git.file.write`: commits land only in public repositories, whatever the
  request. `git.repository.create`: creates a repository, public or
  private. Both are write tools.
- `diagram.generation.create`: renders Mermaid source into a diagram. Any
  request for a diagram or schema goes through it.
- `aap.platform.audit`: a read-only summary of the Ansible Automation
  Platform's state.

Not declared: writing to Google Drive or Docs, so the document comes back
in the reply and is not saved; Jira; repository fork and delete; image
generation.
