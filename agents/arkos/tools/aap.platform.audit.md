---
okf_version: "0.2"
type: tool
title: AAP platform audit
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/aap.platform.audit.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: aap.platform.audit
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Summarizes the Ansible Automation Platform's own state: component and
    instance health, the last Git sync of its project and the recent runs of
    the cluster health-check job template. Input: an optional number of recent
    runs. Output: the summary; every run carries a link to it, and the most
    recent one its last output lines. Used when live platform state is useful
    context for an architecture narrative.
  known_limitations:
    - "Read-only: changes nothing. Launching automation (aap.cluster.audit) is not declared."
    - "min_classification C2. allowed_groups: consultant, board, cdp, ocp-ai-ops."
---

# AAP platform audit

Gives a document current facts about the automation platform. Share the run
links it returns, and the output lines when a run failed.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
