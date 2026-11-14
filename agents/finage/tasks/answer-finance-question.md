---
okf_version: "0.2"
type: task
title: Answer a finance or billing question
description: Answer an invoicing, billing or financial reporting question from project memory, with a web-search fallback.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/finage/tasks/answer-finance-question.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - web_search
  allowed_knowledge:
    - knowledge.project
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "What is the invoicing status for this engagement?"
    - "How much is still outstanding on this account?"
---

# Answer a finance or billing question

Answer a free-form question about invoicing, billing status or financial reporting, grounded in the engagement's durable
`knowledge.project` memory. Fall back to a constrained web search when the internal corpus has no grounded answer.

The task declares no `live_read_tool`: its only tool is `web_search`, and no live billing capability exists. There is no
finance-specific knowledge domain and no billing history, so an answer reports what the project memory holds,
attributed to its source.

`allowed_knowledge` never includes `knowledge.sales` or `knowledge.adv`, and `allowed_tools` never includes a Salesforce
capability: Finage stays finance-scoped without inheriting broader sales or sales administration access (zuno-demo
ADR-0326).
