---
okf_version: "0.2"
type: task
title: Coming soon
description: Placeholder task. Soursage is not built yet and declares no capability.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/soursage/tasks/coming-soon.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools: []
---

# Coming soon

Soursage is not built yet. Planned tasks (zuno-demo ADR-0349): source new consultant candidates from LinkedIn, and find,
among existing consultants, the best profile for a mission from Workday profile data, gated on the `recrut` and `sales`
business roles.

`allowed_tools` stays empty while the agent is a placeholder: it has no tool-call capability by construction. The corp
tool policy already registers the read-only `workday.profile.any.read` capability (minimum classification C3, granted
to `cdp` only today); no LinkedIn capability exists yet.
