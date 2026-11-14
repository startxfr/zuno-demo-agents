---
okf_version: "0.2"
type: agent
title: Alpha
description: Conformance fixture.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/conformance/cases/invalid-profile-unsupported/agents/alpha/agent.okf.md
zuno:
  profile: "2.0"
  maintainer: Conformance fixtures
  name: alpha
  status: active
  graph_shape: retrieve_reason_respond
  primary_task: ask
  tasks:
  - ask
  model:
    preferred_classification: C1
  ui:
    displayName: Alpha
    tileDescription: Fixture agent.
    color: '#0066CC'
    icon: code
  access:
    groups:
    - agent_demo
---
Body.
