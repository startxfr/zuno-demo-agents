---
okf_version: "0.2"
type: task
title: Check my Drive and mail
description: List the caller's own Google Drive documents and Gmail messages about an account or project.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/advantage/tasks/check-my-drive-and-mail.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - list_drive_files
    - read_gmail
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "List my Drive documents and emails about this project."
    - "Which emails mention the proposal deadline for this account?"
---

# Check my Drive and mail

List the authenticated sales administrator's own Google Drive documents and Gmail messages relevant to a given account
or project. `list_drive_files` and `read_gmail` are read-only and run with the user's delegated credentials, so they
return only content the user can already see. The `adv` business role grants both in the corp tool policy.
