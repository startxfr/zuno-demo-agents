---
okf_version: "0.2"
type: task
title: Structure a demo
description: Structure a customer demo in the chat reply - what to show, in what order, with talking points for each section.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tasks/structure-demo.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools: []
  allowed_knowledge: []
  # Reply cap (zuno-demo ADR-0544): enough for a 5-7 section demo narrative
  # with talking points, and bounded so that its preferred model (about 18
  # tokens/s, measured) finishes in about 85 seconds.
  max_tokens: 1536
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "Structure a 30-minute platform demo for a technical audience."
    - "How should I sequence a demo showing GitOps from commit to running pod?"
---

# Structure a demo

Structure a customer demo narrative - what to show, in what order, and the
key talking points for each section - directly in the chat reply. A demo
narrative is short and conversational, never a saved document: long-form
documents belong to `draft-architecture-testimonial` and
`workshop-presentation`.

It is a direct branch of the `plan_draft_write` workflow: after the plan
step, it answers from the user's message alone, with no retrieval and no
tool call, so `allowed_tools` and `allowed_knowledge` are empty. The
narrative is therefore grounded in the conversation only, not in the
documentation corpus or Confluence.
