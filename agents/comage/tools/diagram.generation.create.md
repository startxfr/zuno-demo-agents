---
okf_version: "0.2"
type: tool
title: Diagram generation
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tools/diagram.generation.create.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: diagram.generation.create
  used_by_tasks:
    - check-deal-status
  usage_notes: >-
    Renders Mermaid source into an SVG diagram (zuno-demo ADR-0516).
    check-deal-status uses it for charts and structured visuals of deal or
    pipeline data. Input: Mermaid source built from the figures retrieved
    or read live. Output: the rendered diagram.
  known_limitations:
    - "Read access, min_classification C1 (policies/tools/tool-policy.yaml, tool generate_diagram)."
    - "allowed_groups: consultant, adv, sales, board, cdp."
    - "The diagram is only as accurate as the figures written into its source."
---

# Diagram generation

Renders a Mermaid diagram to SVG. In Comage it is the tool for every chart,
mockup or structured visual of deal or pipeline data, because it draws
exact figures and legible text.

Documentary only: authorization stays each task's `zuno.allowed_tools`
intersected with `policies/tools/tool-policy.yaml`.
