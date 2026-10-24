---
okf_version: v0.3
type: agent
title: Alpha
description: Conformance fixture.
zuno:
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
  delegation:
    targets:
    - agent: beta
      task: ask
  limits:
    delegation:
      max_depth: 2
---
Body.
