---
okf_version: "0.2"
type: rag
title: Sales knowledge retrieval
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/rag/sales.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  domain: knowledge.sales
  used_by_tasks:
    - check-deal-status
  freshness_expectation: current-state-read
  rationale: >-
    check-deal-status answers deal and pipeline questions from indexed
    Salesforce content first (zuno-demo ADR-0205: prefer indexed knowledge
    for reads). Its questions often ask for the current value of a mutable
    field such as a stage or an amount, so the task does not trust the
    index alone: an answer that relies on this domain also triggers the
    live salesforce.opportunity.read call.
---

# Sales knowledge retrieval

`knowledge.sales` is Salesforce sales content, indexed on a schedule, so it
can lag behind the live records. It is Comage's main knowledge domain.

The knowledge policy records a C2 classification floor for it and allows the `sales`, `adv`,
`board`, `cdp` and `finance` business roles. The domain is read-only: a
change to an opportunity goes through `update-opportunity-status` and its
live tool, never through retrieval.

Documentary only: this note grants nothing. Retrieval is authorized by the
task's `zuno.allowed_knowledge` intersected with
`policies/knowledge/knowledge-policy.yaml`.
