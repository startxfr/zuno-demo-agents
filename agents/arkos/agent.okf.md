---
okf_version: "0.2"
type: agent
title: Arkos
description: >-
  Architecture assistant for architects. Drafts Design & Architecture
  Testimonials (DAT) and Odyssey architecture workshop presentations from the
  technical documentation corpus, Confluence and project memory, with Git
  repository access and Mermaid diagram generation. Also structures customer
  demos and writes code.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/agent.okf.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: arkos
  status: active
  graph_shape: plan_draft_write
  primary_task: draft-architecture-testimonial
  tasks:
    - draft-architecture-testimonial
    - workshop-presentation
    - structure-demo
    - write-code
  memory:
    history:
      enabled: true
      max_turns: 6
      token_budget: 6000
  model:
    preferred_classification: C2
    notes: >-
      C2 (was C3 until v1.2.4): the architecture material is C2. Sovereign
      DAT workflows, structure-demo and write-code keep running on local
      models through local_only_for in
      policies/model-routing/model-routing-policy.yaml, not through the
      ceiling.
  delegation:
    targets:
      - agent: tekos
        task: answer-technical-question
  limits:
    delegation:
      max_depth: 1
  access:
    groups:
      - agent_arkos
  ui:
    displayName: Arkos
    tileDescription: Architecture DAT and workshop assistant.
    color: "#8F4700"
    icon: drafting-compass
---

# Arkos

Arkos is the architecture assistant for architects. It drafts Design &
Architecture Testimonials (DAT) and Odyssey architecture workshop
presentations, structures customer demos and writes code. Status: active.

## Workflow

`zuno.graph_shape: plan_draft_write`. Each turn first plans the deliverable,
then takes one of two paths:

- **Document path** (`draft-architecture-testimonial`, the primary task, and
  `workshop-presentation`): retrieve from `knowledge.tech` and
  `knowledge.project` by topic, draft, review the draft with the task's
  `reflect` prompt, and return the document in the reply. A request about a
  workshop or Odyssey selects `workshop-presentation`.
- **Direct path** (`structure-demo`, `write-code`): answer from the user's
  message alone, with no retrieval and no tool call.

## Authorization

There is no agent-level `allowed_knowledge`: the ceiling is the union of the
tasks' declarations. The two document tasks declare Confluence read and
search, six Git repository capabilities, diagram generation and the
read-only AAP platform audit, and the domains `knowledge.tech` and
`knowledge.project`. `structure-demo` and `write-code` declare none.

Arkos may delegate one hop to `tekos` / `answer-technical-question`. The delegation is not read-only by
construction: a write the target asks for happens only after the initiating user approves it, and only for a target
that `delegation.write_allowed` in `policies/limits/limits-policy.yaml` lists (Tekos's cluster audit).

The entitlement group is `agent_arkos`. Inside Arkos, the `consultant`
business role gates tools and knowledge (`policies/tools/tool-policy.yaml`,
`policies/knowledge/knowledge-policy.yaml`). The matrix in
`docs/authorization-matrix/arkos.md` restates the enforced intersection and
the effective model chain per task.
