---
okf_version: "0.2"
type: tool
title: Git repository read (private, GitLab)
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/git.repository.private.read.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: git.repository.private.read
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Reads a file, or lists a directory, in a GitLab repository of any
    visibility: public, internal or private. Input: the provider (gitlab), the
    owner, the repository, an optional path and an optional ref. Used for
    documents about internal code.
  known_limitations:
    - "GitLab only: private GitHub access is never granted."
    - "min_classification C2. Read access. allowed_groups: consultant, board, cdp."
---

# Git repository read (private, GitLab)

The private counterpart of git.repository.read, for internal repositories a
DAT or a workshop presentation must reference.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
