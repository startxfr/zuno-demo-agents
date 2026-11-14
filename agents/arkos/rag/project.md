---
okf_version: "0.2"
type: rag
title: Project memory retrieval
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/rag/project.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  domain: knowledge.project
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  freshness_expectation: semantic-read
  rationale: >-
    A DAT or a workshop presentation is written for one engagement: the
    retrieve step also searches the durable memory of the user's selected
    project, so the draft can reuse the decisions and facts recorded in
    earlier sessions, by any agent working on that project.
---

# Project memory retrieval

Cross-session, cross-agent memory scoped to one project (zuno-demo
ADR-0209). It becomes retrievable as soon as it is written; it has no
ingestion schedule. Arkos's two document tasks retrieve from it alongside
`knowledge.tech`.

Access (`policies/knowledge/knowledge-policy.yaml`): every business group is
listed, because project membership, not the business role, is the real gate:
a user retrieves only the memory of projects they are a member of.
Documentary only: authorization is each task's `allowed_knowledge`
intersected with the knowledge policy.
