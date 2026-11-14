---
okf_version: "0.2"
type: task
title: Produce the monthly in-progress sales report
description: Produce the monthly in-progress sales administration report (margin by state, customer and technology) from ADV knowledge.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/advantage/tasks/monthly-sales-report.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools: []
  allowed_knowledge:
    - knowledge.adv
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "Produce the monthly in-progress sales report."
    - "Break down margin by customer and technology for this month."
---

# Produce the monthly in-progress sales report

Produce the monthly in-progress sales administration report, with margin by state, by customer and by technology,
drawing on the project and delivery state held in `knowledge.adv`.

The task declares no tool: the report is text and tables in the answer. `knowledge.adv` has no ingestion source at
present.
