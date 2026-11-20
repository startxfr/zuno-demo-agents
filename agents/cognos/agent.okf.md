---
okf_version: "0.2"
type: agent
title: Cognos
description: >-
  Board-only financial and strategic assistant. Answers Direction-level
  financial and strategic questions with access to a large tool set
  explicitly excluding technical tools and the technical RAG corpora.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/cognos/agent.okf.md
status: draft
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: cognos
  status: placeholder
  tasks:
    - coming-soon
  model:
    preferred_classification: C3
    notes: >-
      Placeholder pending a future build (ADR-0349 defines only the
      identity footprint); C3 anticipated because Direction-level
      financial and strategic material is local-model-only by nature.
  access:
    groups:
      - agent_cognos
  ui:
    displayName: Cognos
    tileDescription: Board financial and strategic assistant - coming soon.
    color: "#4A148C"
    icon: chart-line
---

# Cognos

Board-only financial and strategic assistant, for a Direction-level audience (zuno-demo ADR-0349).

`status: placeholder`: the agent is declared but not served, and a portal shows its tile as "coming soon" to members of
`agent_cognos`. Its single task, `coming-soon`, declares no tool and no knowledge domain, so the agent has no capability
by construction.

The intended build answers financial and strategic questions over a large tool set that explicitly excludes the
technical tools and the technical knowledge corpora, gated on the `board` business role.
`preferred_classification: C3` because Direction-level material stays on local models. Building it means authoring
real tasks with their prompts and policy entries, then setting `status: active`.

The bundle follows the Zuno OKF profile 1.0 (`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`).
