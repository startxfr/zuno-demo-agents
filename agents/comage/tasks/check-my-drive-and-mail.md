---
okf_version: "0.2"
type: task
title: Check my Drive and mail
description: List the user's own Google Drive documents and Gmail messages about an account or opportunity, with the user's delegated access.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tasks/check-my-drive-and-mail.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - list_drive_files
    - read_gmail
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "List my Drive documents and emails about the Startx account."
    - "Which recent emails mention the renewal negotiation?"
---

# Check my Drive and mail

List the authenticated sales rep's own Google Drive documents and Gmail
messages relevant to a given account or opportunity. Both tools use
delegated end-user OAuth2 (zuno-demo ADR-0014), so only content the user can
already see is returned.

The task only reads: it declares no write tool and no knowledge domain.
