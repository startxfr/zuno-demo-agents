---
okf_version: "0.2"
type: task
title: Diagnose
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/experience-clients/kagent/tasks/diagnose.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  # Read-only cluster reads, nothing else (zuno-demo ADR-0600 clauses 1 and 6): no write capability exists.
  allowed_tools:
    - k8s.resource.read
    - k8s.resource.list
    - k8s.events.read
    - k8s.logs.read
    - metrics.query
  # zuno-demo ADR-0596, user decision 2026-11-07: answer with the fast local reasoning model first (gpt-oss-20b,
  # about 85 tok/s, 131k context). Without a preference the ai-gateway walked its providers in file order and served
  # qwen3.6-27b (about 22 tok/s): 24 to 56 s for a short answer on demo333. Only reorders: the other local models
  # follow as fallbacks, and the classification and local-only rules are unchanged.
  models:
    preferred:
      - reasoning
---

# Diagnose

An operator asks why a pod is failing or a service is slow. The assistant lists the resources of the
zuno-* namespaces, reads their events and logs and queries the monitoring, then explains what it found.
It cannot change anything.
