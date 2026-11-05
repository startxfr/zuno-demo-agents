---
okf_version: v0.3
type: experience-client
title: kagent
description: >-
  Kubernetes-native operations assistant (zuno-demo ADR-0600). A thin client: its model calls and tool
  calls go through the zuno-token-proxy (ADR-0601) to the ai-gateway and the mcp-gateway, signed with the
  kagent Keycloak client's persona token. It brings no tool server of its own.
provenance:
  maintainer: Zuno Demo architecture team
  repository: zuno-demo
freshness:
  last_reviewed: "2026-11-05"
zuno:
  name: kagent
  tasks:
    - diagnose
  classification: C2
  access:
    # The kagent Keycloak client's service account carries the groups of its operations persona.
    # Only the platform operations groups may use the cluster-reading tools (tool-policy.yaml).
    groups:
      - ocp-ai-ops
      - aap_ops
---

# kagent

Experience client of zuno-demo ADR-0600. The token proxy in front of kagent sends `X-Zuno-Agent: kagent` and
`X-Zuno-Task: diagnose`. Calls are counted per persona, not per kagent user (ADR-0601 decision 5).
