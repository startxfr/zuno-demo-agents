---
okf_version: "0.2"
type: tool
title: Salesforce opportunity read
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tools/salesforce.opportunity.read.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: salesforce.opportunity.read
  used_by_tasks:
    - check-deal-status
  live_read: true
  usage_notes: >-
    The live-read tool of check-deal-status (zuno.live_read_tool). The task
    calls it when a question needs the current value of a mutable field
    (stage, amount) or when the answer relies on knowledge.sales, because
    indexed Salesforce content can lag behind the live records. Input: a
    query that names the opportunity. Output: the matching opportunities
    with their current stage, amount and close date.
  known_limitations:
    - "Read access, min_classification C2 (policies/tools/tool-policy.yaml)."
    - "allowed_groups: sales, board. Other business roles get no live Salesforce data through this tool."
    - "No external_model_policy restriction: results can reach any model the C2 classification allows."
    - "Read-only: it never changes an opportunity; update-opportunity-status does that."
---

# Salesforce opportunity read

Reads the current state of Salesforce opportunities, live. In Comage it
checks the index: when `check-deal-status` answers about a stage or an
amount, this call supplies the current value, and the prompt forbids
stating such a value with confidence without it.

Documentary only: authorization stays each task's `zuno.allowed_tools`
intersected with `policies/tools/tool-policy.yaml`.
