---
okf_version: "0.2"
type: task
title: Check deal status
description: Answer a question about an opportunity or the pipeline from indexed Salesforce knowledge, with a live Salesforce read for current values.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tasks/check-deal-status.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools:
    - salesforce.opportunity.read
    - web_search
    # Photorealistic image generation (zuno-demo ADR-0415), for genuine
    # marketing-visual requests only, never for deal or pipeline charts.
    # The prompt (prompts/check-deal-status.md) enforces that scope.
    - image.generation.create
    # Mermaid-to-SVG diagram rendering (zuno-demo ADR-0516): the tool for
    # charts and structured visuals built from real deal figures.
    - diagram.generation.create
  live_read_tool: salesforce.opportunity.read
  allowed_knowledge:
    - knowledge.sales
    - knowledge.project
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "What is the current stage of the Startx renewal opportunity?"
    - "Which opportunities are expected to close this quarter?"
    - "What is the amount on the largest open deal in my pipeline?"
---

# Check deal status

Answer a free-form question about an opportunity or the pipeline. Ordinary
semantic reads come from `knowledge.sales`, the indexed Salesforce content,
and from `knowledge.project`, the durable memory of the user's project.

Indexed Salesforce content can lag behind the live records. A question that
asks for the current value of a mutable field (stage, amount), or any answer
that relies on `knowledge.sales`, therefore also triggers a live
`salesforce.opportunity.read` call (`zuno.live_read_tool`) instead of trusting
the index alone. zuno-demo ADR-0205: prefer indexed knowledge for reads, live
tools for current values and writes.

Two visual tools are declared and they are not interchangeable:
`diagram.generation.create` renders charts and structured visuals from real
figures, and `image.generation.create` is reserved for marketing visuals a
user explicitly asks for. `web_search` is also declared, for public
information outside the Salesforce data.

The task never writes to Salesforce: a change to an opportunity is the
`update-opportunity-status` task.
