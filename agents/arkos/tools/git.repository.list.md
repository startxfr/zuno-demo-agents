---
okf_version: "0.2"
type: tool
title: Git repository list (public)
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/git.repository.list.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: git.repository.list
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Lists public repositories of a GitHub user or organization, or of a GitLab
    user or group. Input: the provider, the owner and the owner type (user or
    organization). Output: up to 10 of the most-starred and up to 10 of the
    most recently active repositories, with a count.
  known_limitations:
    - "A sample, not the full list: its count is not the owner's total number of repositories."
    - "Public repositories only, on GitHub and GitLab."
    - "min_classification C2. Read access. allowed_groups: consultant, board, cdp."
    - "No default organization or user: Arkos asks which owner to list when the message does not say."
---

# Git repository list (public)

Finds the repository to read next and gives an overview of an owner's most
visible projects.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
