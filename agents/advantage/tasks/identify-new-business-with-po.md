---
okf_version: "0.2"
type: task
title: Identify new business with a client PO received
description: List new business whose client purchase order was received in the last three rolling days, from ADV knowledge.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/advantage/tasks/identify-new-business-with-po.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools: []
  allowed_knowledge:
    - knowledge.adv
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "Which new business received a client purchase order in the last three days?"
    - "List the projects whose client PO arrived this week."
---

# Identify new business with a client PO received

Surface new business whose client purchase order was received in the last three rolling days, drawing on the project
and delivery state held in `knowledge.adv`.

The task declares no tool. Retrieved knowledge cannot apply an exact purchase-order date filter: that would need a
structured-query capability against a live source, and none exists. `knowledge.adv` has no ingestion source at present.
