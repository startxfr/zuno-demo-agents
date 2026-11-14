---
okf_version: "0.2"
type: tool
title: Salesforce opportunity update
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tools/salesforce.opportunity.update.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: salesforce.opportunity.update
  used_by_tasks:
    - update-opportunity-status
  usage_notes: >-
    The only write tool of the agent. update-opportunity-status calls it to
    change an existing opportunity. Input: the opportunity's record id and
    at least one new value among stage, amount and close date. Output: the
    opportunity's fields after the write, or an error when the opportunity
    is not found or the call is refused.
  known_limitations:
    - "Write access, min_classification C2 (policies/tools/tool-policy.yaml)."
    - "allowed_groups: sales, board."
    - "No external_model_policy restriction: arguments and results can reach any model the C2 classification allows."
    - "Updates existing opportunities only. Creating one is a separate capability (salesforce.opportunity.create) that no Comage task declares."
    - "update-opportunity-status declares no read tool, so it cannot look an opportunity up: the user or the conversation must identify it."
---

# Salesforce opportunity update

Writes a stage, amount or close-date change to an existing Salesforce
opportunity. Indexed knowledge never records a change (zuno-demo
ADR-0205): this live call is the only write path of Comage.

Documentary only: authorization stays each task's `zuno.allowed_tools`
intersected with `policies/tools/tool-policy.yaml`.
