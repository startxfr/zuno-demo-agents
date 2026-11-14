---
okf_version: "0.2"
type: tool
title: Diagram generation
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tools/diagram.generation.create.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: diagram.generation.create
  used_by_tasks:
    - draft-architecture-testimonial
    - workshop-presentation
  usage_notes: >-
    Renders Mermaid source into an SVG diagram: architecture, sequence and
    relationship diagrams that need precise boxes, arrows and legible text.
    Input: the Mermaid source. Output: the rendered diagram, or the rendering
    error so the source can be fixed and sent again. Every request for a
    diagram or a schema goes through this tool; diagram source is never left
    in the reply text in its place.
  known_limitations:
    - "min_classification C1: rendering stays on the platform, no external service sees the diagram."
    - "Read access (generates content, changes nothing). allowed_groups: consultant, adv, sales, board, cdp."
---

# Diagram generation

Draws the architecture overview of a DAT or a workshop presentation, or a
standalone diagram the user asks for. Photorealistic image generation is not
declared.

Documentary only: authorization is each task's allowed_tools intersected with
policies/tools/tool-policy.yaml.
