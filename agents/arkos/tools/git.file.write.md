---
okf_version: "0.2"
type: tool
title: Git file write
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/git.file.write.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: git.file.write
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Creates or updates one file in a repository as a single commit, when the
    user asks Arkos to publish supporting material such as a document or a
    sample manifest. Input: the provider, the owner, the repository, the file
    path, its content, a commit message and an optional branch.
  known_limitations:
    - "Write access. Commits land only in public repositories, on GitHub or GitLab, whatever the request."
    - "min_classification C2. allowed_groups: consultant, board, cdp."
---

# Git file write

Used only on an explicit request to publish material. A drafted document is
returned in the reply, not committed.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
