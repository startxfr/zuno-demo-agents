---
okf_version: "0.2"
type: task
title: Answer a project or bid question
description: Answer a project, delivery or bid question from ADV and project knowledge, with a web-search fallback.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/advantage/tasks/answer-project-question.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - web_search
    # zuno-demo ADR-0415: image generation, offered as a callable tool for
    # project or bid questions that call for a visual (mockup, diagram).
    - image.generation.create
  allowed_knowledge:
    - knowledge.adv
    - knowledge.project
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "What is the current delivery status of this project?"
    - "Who owns this bid, and which business unit is it attached to?"
---

# Answer a project or bid question

Answer a free-form question about project or delivery status, ownership, business unit, or bid and proposal support,
grounded in `knowledge.adv` and in the engagement's durable `knowledge.project` memory. Fall back to a constrained web
search when the internal corpus has no grounded answer. `image.generation.create` is available when a question calls
for a visual, such as a mockup or a diagram.

The task declares no `live_read_tool`: no live ADV capability exists, and `knowledge.adv` has no ingestion source at
present, so the task reads indexed knowledge only.

`allowed_knowledge` never includes the current-sales domain `knowledge.sales`, and `allowed_tools` never includes a live
CRM capability: Advantage holds this cross-domain boundary by explicit omission, not by a runtime filter (zuno-demo
ADR-0326). Any further commercial access must be added here explicitly and stay policy-controlled.
