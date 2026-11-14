---
okf_version: "0.2"
type: rag
title: Project memory retrieval
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/rag/project.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  domain: knowledge.project
  used_by_tasks:
    - check-deal-status
  freshness_expectation: semantic-read
  rationale: >-
    check-deal-status also retrieves durable, cross-session project memory
    (zuno-demo ADR-0209), so an answer about a deal can use what earlier
    conversations on the same engagement established, not only Salesforce
    content. Memory is retrievable as soon as it is written, so no
    staleness override applies.
---

# Project memory retrieval

`knowledge.project` is durable memory scoped to one project, written from
earlier conversations rather than ingested from a source system.

The knowledge policy lists every business role for this domain on purpose:
the real gate is the user's membership of the project, checked at query
time and failing closed.

Documentary only: this note grants nothing. Retrieval is authorized by the
task's `zuno.allowed_knowledge` intersected with
`policies/knowledge/knowledge-policy.yaml`.
