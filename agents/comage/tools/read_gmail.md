---
okf_version: "0.2"
type: tool
title: Read Gmail
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tools/read_gmail.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: read_gmail
  used_by_tasks:
    - check-my-drive-and-mail
  usage_notes: >-
    check-my-drive-and-mail calls it to find the user's own Gmail messages
    relevant to an account or opportunity. Input: a mail search query.
    It acts with the user's delegated OAuth2 access (zuno-demo ADR-0014),
    so it returns only messages the user can already see.
  known_limitations:
    - "Read access, min_classification C1 (policies/tools/tool-policy.yaml, capability gmail.message.read)."
    - "allowed_groups: consultant, board, cdp, sales, adv, finance."
    - "Reads only: Comage declares no tool that sends, changes or deletes mail."
---

# Read Gmail

Reads Gmail messages with the user's own delegated access. In Comage it
finds account correspondence in the sales rep's mailbox for
`check-my-drive-and-mail`.

Documentary only: authorization stays each task's `zuno.allowed_tools`
intersected with `policies/tools/tool-policy.yaml`.
