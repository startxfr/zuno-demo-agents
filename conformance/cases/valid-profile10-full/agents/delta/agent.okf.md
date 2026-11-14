---
okf_version: "0.2"
type: agent
title: Delta
description: Conformance fixture.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/conformance/cases/valid-profile10-full/agents/delta/agent.okf.md
tags:
- fixture
sources:
- id: docs
  resource: https://example.com/docs
  title: Example documentation
generated:
  by: human:fixture-author
  at: "2026-11-14T10:00:00Z"
verified:
- by: process:zuno-demo-agents/ci
  at: "2026-11-14T10:05:00Z"
status: stable
stale_after: "2027-05-14T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Conformance fixtures
  name: delta
  status: active
  graph_shape: retrieve_reason_respond
  primary_task: ask
  tasks:
  - ask
  model:
    preferred_classification: C2
  ui:
    displayName: Delta
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
