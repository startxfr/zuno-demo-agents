---
okf_version: "0.2"
type: tool
title: Git repository create
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/git.repository.create.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: git.repository.create
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Creates a repository on GitHub or GitLab when the user asks to publish
    supporting material in a repository of its own. Input: the provider, the
    name, an optional owner (organization or group), whether it is private
    (the default) and a description.
  known_limitations:
    - "Write access. Any visibility; private unless the call asks otherwise."
    - "min_classification C2. allowed_groups: consultant, board, cdp."
---

# Git repository create

Used only on an explicit request. Arkos declares no repository fork or delete
capability.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
