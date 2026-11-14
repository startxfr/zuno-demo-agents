---
okf_version: "0.2"
type: task
title: Identify business ready to invoice
description: Identify the business of one verified engagement that has reached the billable state, from its project memory.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/finage/tasks/identify-business-ready-to-invoice.md
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
    - "Which business on this project has reached the billable state?"
    - "List the quotes for this engagement that are ready to invoice."
---

# Identify business ready to invoice

Identify business that has reached the `A facturer` (billable) state or later, for one client engagement, from that
engagement's durable project memory (`knowledge.project`).

No billing history is available. The task reports only what the project memory of the verified engagement holds,
attributes it to the records it came from, and says plainly that no billing history stands behind it. It never presents
a retrieved state as the current state of an outstanding invoice.

`project_required: true`: the task only makes sense inside one client engagement, so it runs only after the user's
project (a name or a Salesforce opportunity id) is verified with `salesforce.opportunity.read` under the user's own
identity, failing closed. That capability is declared for this binding check only: its answer is yes or no, and no
Salesforce record content reaches the model. A verified binding scopes `knowledge.project` retrieval to that engagement.
