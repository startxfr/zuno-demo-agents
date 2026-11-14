---
okf_version: "0.2"
type: tool
title: Web search
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tools/web_search.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: web_search
  used_by_tasks:
    - check-deal-status
  usage_notes: >-
    Declared by check-deal-status for public web information that the
    Salesforce data and project memory do not hold. Input: a search query.
    Output: matching web pages. Neither the task nor its prompt sets a
    dedicated rule for when to call it.
  known_limitations:
    - "Read access, min_classification C1 (policies/tools/tool-policy.yaml, capability web.page.search)."
    - "allowed_groups: sales, consultant, adv, finance, board."
    - "Web results carry no classification or access metadata, unlike indexed knowledge."
---

# Web search

Searches the public web. In Comage it is a complement to the Salesforce
data, never a source for an opportunity's own fields: those come from
`knowledge.sales` and the live Salesforce read.

Documentary only: authorization stays each task's `zuno.allowed_tools`
intersected with `policies/tools/tool-policy.yaml`.
