---
okf_version: "0.2"
type: task
title: Update opportunity status
description: Change the stage, amount or close date of an existing Salesforce opportunity through the live update tool.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tasks/update-opportunity-status.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - salesforce.opportunity.update
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "Move the Startx renewal opportunity to Negotiation."
    - "Update the close date on this opportunity to the end of next month."
---

# Update opportunity status

Write a change (stage, amount, close date) to an existing Salesforce
opportunity through the live `salesforce.opportunity.update` tool. This is
the agent's only write task.

Indexed knowledge stays write-free (zuno-demo ADR-0205): a change always goes
through the live tool, never through retrieval. The task declares no
knowledge domain and no read tool.
