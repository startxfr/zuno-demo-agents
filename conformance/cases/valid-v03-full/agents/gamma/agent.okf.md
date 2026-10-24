---
okf_version: v0.3
type: agent
title: Gamma
description: Conformance fixture.
zuno:
  name: gamma
  status: active
  graph_shape: retrieve_reason_respond
  primary_task: ask
  tasks:
  - ask
  model:
    preferred_classification: C2
  ui:
    displayName: Gamma
    tileDescription: Fixture agent.
    color: '#0066CC'
    icon: code
  access:
    groups:
    - agent_demo
  models:
    preferred:
    - reasoning
  guardrails:
    mode: observe
    categories:
    - pii
  limits:
    max_tokens: 2048
    quota_class: standard
---
Body.
