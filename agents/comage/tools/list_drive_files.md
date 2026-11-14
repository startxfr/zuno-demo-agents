---
okf_version: "0.2"
type: tool
title: List Drive files
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tools/list_drive_files.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: list_drive_files
  used_by_tasks:
    - check-my-drive-and-mail
  usage_notes: >-
    check-my-drive-and-mail calls it to list the user's own Google Drive
    documents relevant to an account or opportunity. It acts with the
    user's delegated OAuth2 access (zuno-demo ADR-0014), so it lists only
    files the user can already see.
  known_limitations:
    - "Read access, min_classification C1 (policies/tools/tool-policy.yaml, capability drive.document.search)."
    - "allowed_groups: consultant, board, cdp, sales, adv, finance."
    - "Lists documents; it never creates or edits one (no Drive write tool is declared by Comage)."
---

# List Drive files

Lists Google Drive documents with the user's own delegated access. In
Comage it finds account material in the sales rep's Drive for
`check-my-drive-and-mail`.

Documentary only: authorization stays each task's `zuno.allowed_tools`
intersected with `policies/tools/tool-policy.yaml`.
