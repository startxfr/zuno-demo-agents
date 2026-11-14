---
okf_version: "0.2"
type: task
title: Produce the monthly invoicing report
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/finage/tasks/monthly-invoice-report.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
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
    - "Produce the monthly invoicing report for this engagement."
    - "Summarise revenue, outstanding amounts and forecast for this project's last month."
---

# Produce the monthly invoicing report

Produce the monthly invoicing report (MEMORY.md section 9: revenue,
outstanding amounts, delay and forecast) for one client engagement, from its durable project memory (`knowledge.project`).

**No billing history is available (WP-185, 2026-11-02).** This task was built on `sxa.aggregate.revenue-by-year` and
`sxa.record.lookup` (ADR-0017), then on retrieval over the closed pre-2021 SXA record (ADR-0219).
That domain is no longer served since the RAG moved to UnifAI (WP-168). Every figure this task reports is read out of
the engagement's project memory and must be attributed to it. It must not present a summed or derived total as an
authoritative aggregate, it must not imply the numbers describe the current period, and it states when the project
memory holds no figures.

`zuno.project_required: true` (ADR-0512/WP-55): this report only makes
sense for one client engagement, so Agent Runtime refuses to execute it
until the prompt-collected project (name or Salesforce id) is verified
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
endpoint only executes `answer-finance-question`. Report generation
(text/table + PDF) is v1 scope, not built here; the project_required
mark and binding enforcement above are real and schema/contract-tested
today, and take effect automatically the moment this task is ever made
`primary_task`-routed.
