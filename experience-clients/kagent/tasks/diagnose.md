---
okf_version: v0.3
type: task
title: Diagnose
zuno:
  # Read-only cluster reads, nothing else (zuno-demo ADR-0600 clauses 1 and 6): no write capability exists.
  allowed_tools:
    - k8s.resource.read
    - k8s.resource.list
    - k8s.events.read
    - k8s.logs.read
    - metrics.query
---

# Diagnose

An operator asks why a pod is failing or a service is slow. The assistant lists the resources of the
zuno-* namespaces, reads their events and logs and queries the monitoring, then explains what it found.
It cannot change anything.
