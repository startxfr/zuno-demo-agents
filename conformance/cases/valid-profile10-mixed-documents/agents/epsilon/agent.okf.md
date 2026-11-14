---
okf_version: "0.2"
type: agent
title: Epsilon
description: Conformance fixture.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/conformance/cases/valid-profile10-mixed-documents/agents/epsilon/agent.okf.md
zuno:
  profile: "1.0"
  maintainer: Conformance fixtures
  name: epsilon
  status: active
  graph_shape: retrieve_reason_respond
  primary_task: ask
  tasks:
  - ask
  model:
    preferred_classification: C1
  ui:
    displayName: Epsilon
    tileDescription: Fixture agent.
    color: '#0066CC'
    icon: code
  access:
    groups:
    - agent_demo
---
Body.
