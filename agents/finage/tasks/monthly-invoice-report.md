---
okf_version: "0.2"
type: task
title: Produce the monthly invoicing report
description: Produce the monthly invoicing report (revenue, outstanding amounts, delay and forecast) for one verified engagement.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/finage/tasks/monthly-invoice-report.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - salesforce.opportunity.read
  allowed_knowledge:
    - knowledge.project
  project_required: true
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "Produce the monthly invoicing report for this engagement."
    - "Summarise revenue, outstanding amounts and forecast for this project's last month."
---

# Produce the monthly invoicing report

Produce the monthly invoicing report (revenue, outstanding amounts, delay and forecast) for one client engagement, from
its durable project memory (`knowledge.project`).

No billing history is available. Every figure is read from the engagement's project memory and attributed to it. The
report never presents a summed or derived total as an authoritative aggregate, never implies that the figures describe
the current period, and says so when the project memory holds no figures. The task declares no report-generation tool:
the report is text and tables in the answer.

`project_required: true`: the task only makes sense inside one client engagement, so it runs only after the user's
project (a name or a Salesforce opportunity id) is verified with `salesforce.opportunity.read` under the user's own
identity, failing closed. That capability is declared for this binding check only: its answer is yes or no, and no
Salesforce record content reaches the model. A verified binding scopes `knowledge.project` retrieval to that engagement.
