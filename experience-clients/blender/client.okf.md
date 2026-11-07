---
okf_version: v0.3
type: experience-client
title: Blender 3D generator
description: >-
  Blender add-on on a workstation (zuno-demo ADR-0610). It asks a local model, through
  the ai-gateway's workstation entry and with the signed-in user's own token (device
  sign-in, Keycloak client `blender`), for a Blender Python script, shows it and runs it
  on the user's click. No MCP tools; local models only.
provenance:
  maintainer: Zuno Demo architecture team
  repository: zuno-demo
freshness:
  last_reviewed: "2026-11-07"
zuno:
  name: blender
  tasks:
    # zuno-demo ADR-0610: the model routing of a bpy script; no tools.
    - bpy
  # zuno-demo ADR-0610 clause 3: design prompts and generated code stay on the platform.
  # The ai-gateway also holds a C3 floor on the Keycloak client `blender`.
  classification: C3
  access:
    groups:
      - sales
      - consultant
      - adv
      - finance
      - board
      - cdp
      - recrut
      - ocp-ai-dev
      - ocp-ai-ops
      - ocp-paas-dev
      - ocp-paas-ops
---

# Blender 3D generator

Experience client of zuno-demo ADR-0610. The add-on sends `X-Zuno-Agent: blender` and
`X-Zuno-Task: bpy` with the user's own token to the ai-gateway's workstation entry, whose
Kuadrant AuthPolicy admits only tokens of the Keycloak client `blender`. It never calls the
mcp-gateway, so its tasks allow no tool. Calls are counted per user (ADR-0593).
