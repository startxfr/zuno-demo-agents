---
okf_version: "0.2"
type: task
title: Check my Drive and mail
description: List the caller's own Google Drive documents and Gmail messages about an account or invoice.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/finage/tasks/check-my-drive-and-mail.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - list_drive_files
    - read_gmail
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "List my Drive documents and emails about this customer's invoices."
    - "Which emails mention an unpaid invoice for this account?"
---

# Check my Drive and mail

List the authenticated finance user's own Google Drive documents and Gmail messages relevant to a given account or
invoice. `list_drive_files` and `read_gmail` are read-only and run with the user's delegated credentials, so they
return only content the user can already see. The `finance` business role grants both in the corp tool policy.
