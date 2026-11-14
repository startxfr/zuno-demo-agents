---
okf_version: "0.2"
type: tool
title: Git repository list (private, GitLab)
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/git.repository.private.list.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: git.repository.private.list
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Lists repositories of a GitLab user or group, of any visibility. Input:
    the provider (gitlab), the owner and the owner type. Output: up to 10 of
    the most-starred and up to 10 of the most recently active repositories,
    with a count.
  known_limitations:
    - "A sample, not the full list, and not a private-only filter."
    - "GitLab only: private GitHub access is never granted."
    - "min_classification C2. Read access. allowed_groups: consultant, board, cdp."
---

# Git repository list (private, GitLab)

The private counterpart of git.repository.list.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
