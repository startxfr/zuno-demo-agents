---
okf_version: "0.2"
type: tool
title: Git repository read (public)
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/git.repository.read.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: git.repository.read
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Reads a file, or lists a directory, in a public GitHub or GitLab
    repository. Input: the provider (github or gitlab), the owner, the
    repository, an optional path (empty reads the root) and an optional ref.
    Used to describe or cite real source code, or to answer a factual question
    about a repository's content.
  known_limitations:
    - "Public repositories only, on GitHub and GitLab: a private repository is refused."
    - "min_classification C2. Read access. allowed_groups: consultant, board, cdp."
    - "No default organization or user: the user must name the owner."
---

# Git repository read (public)

Lets Arkos ground a statement about a repository in its actual content instead
of guessing.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
