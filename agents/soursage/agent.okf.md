---
okf_version: "0.2"
type: agent
title: Soursage
description: >-
  Recruiting assistant. Interacts with Workday and LinkedIn to source new
  consultant candidates and to find, among existing consultants, the best
  profile for a mission.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/soursage/agent.okf.md
status: draft
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Zuno Demo architecture team
  name: soursage
  status: placeholder
  tasks:
    - coming-soon
  model:
    preferred_classification: C2
    notes: >-
      Placeholder pending a future build (ADR-0349 defines only the
      identity footprint); C2 anticipated because candidate/consultant
      profile data requires context filtering rather than unrestricted
      SaaS use.
  access:
    groups:
      - agent_soursage
  ui:
    displayName: Soursage
    tileDescription: Consultant sourcing and staffing assistant - coming soon.
    color: "#00695C"
    icon: users
---

# Soursage

Recruiting assistant: it will source new consultant candidates and find, among existing consultants, the best profile
for a mission (zuno-demo ADR-0349).

`status: placeholder`: the agent is declared but not served, and a portal shows its tile as "coming soon" to members of
`agent_soursage`. Its single task, `coming-soon`, declares no tool and no knowledge domain, so the agent has no
capability by construction.

The intended build reads consultant profiles from Workday and candidates from LinkedIn, gated on the `recrut` and
`sales` business roles. The corp tool policy already registers the read-only `workday.profile.any.read` capability
(granted to `cdp` only today); no LinkedIn capability exists yet. Building the agent means authoring real tasks with
their prompts and policy entries, then setting `status: active`.

The bundle follows the Zuno OKF profile 1.0 (`platform/okf/schema/zuno-okf-profile-1.0-agent.schema.json`).
