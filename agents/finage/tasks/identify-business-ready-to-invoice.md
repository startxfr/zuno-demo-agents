---
okf_version: v0.2
type: task
title: Identify business ready to invoice
zuno:
  allowed_tools:
    - salesforce.opportunity.read
  allowed_knowledge:
    - knowledge.project
  project_required: true
  # ADR-0515: editable starters. Shown in the chat empty state, and in the
  # composer's slash menu (agent-frontend web/src/chat/TaskPromptMenu.tsx).
  # UX only - never parsed or enforced server-side, and picking one does NOT
  # select this task: the chat route always runs primary_task (ADR-0342).
  prompt_examples:
    - "Which business on this project has reached the billable state?"
    - "List the quotes for this engagement that are ready to invoice."
---

# Identify business ready to invoice

Identify business that has reached the `A facturer`/billable state and
later (MEMORY.md section 9), from the engagement's own durable project memory (`knowledge.project`).

**No billing history is available (WP-185, 2026-11-02).** This task was built on the deterministic
`sxa.customer.read`/`sxa.quote.read` lookups (ADR-0017), then on retrieval over `knowledge.sxa-legacy`, the company's
closed pre-2021 record (ADR-0219). That domain is no longer served: the platform's RAG moved to UnifAI (WP-168)
without a source for it. The task therefore reports only what the project memory of the verified engagement holds,
attributes it to the records it came from, and says plainly that no billing history stands behind it. It never
presents a retrieved state as the current state of an outstanding invoice.

`zuno.project_required: true` (ADR-0512/WP-55): this task only makes
sense inside one client engagement, so Agent Runtime refuses to execute
it until the prompt-collected project (name or Salesforce id) is verified
via `salesforce.opportunity.read` under the caller's own identity,
fail-closed. That capability is declared here only for this binding
check - it is a standalone pre-graph call that never populates the
model's tool results or context, so `answer-finance-question`'s "Finage
has no live Salesforce access" boundary (ADR-0326) is unaffected: no
Salesforce record content ever reaches this task's answer path either. A
verified binding scopes `knowledge.project` retrieval to that engagement
and draws its ADR-0511 project quota first.

Declared for the OKF catalog (ADR-0038); no distinct Agent Runtime route
exists for it yet in v0 - the single `POST /v1/agents/finage/chat`
endpoint only executes `answer-finance-question`. Wiring a dedicated
route for this deterministic-query task is v1 scope, matching every
other agent's own catalog-only tasks; the project_required mark and
binding enforcement above are real and schema/contract-tested today, and
take effect automatically the moment this task is ever made
`primary_task`-routed.
