---
okf_version: "0.2"
type: rag
title: Technical documentation retrieval
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/rag/tech.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  domain: knowledge.tech
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  freshness_expectation: semantic-read
  rationale: >-
    A DAT or a workshop presentation must be grounded in real product
    documentation: the retrieve step searches knowledge.tech with the topic
    the plan step derived from the request, before drafting. Arkos declares
    no rag.top_k, so the consumer's default number of passages applies.
---

# Technical documentation retrieval

The technical documentation corpus: official product documentation and
internal Confluence content. Arkos's two document tasks retrieve from it by
topic before drafting; `structure-demo` and `write-code` do not retrieve.

Access (`policies/knowledge/knowledge-policy.yaml`): groups consultant,
board and cdp. Documentary only: authorization is each task's
`allowed_knowledge` intersected with the knowledge policy.
