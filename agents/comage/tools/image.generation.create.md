---
okf_version: "0.2"
type: tool
title: Image generation
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/comage/tools/image.generation.create.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  capability: image.generation.create
  used_by_tasks:
    - check-deal-status
  usage_notes: >-
    Photorealistic image generation from a text prompt (zuno-demo
    ADR-0415). check-deal-status uses it only for a marketing visual a user
    explicitly asks for, such as a promotional graphic or a product image.
    A chart, a mockup or any visualization of deal or pipeline data goes to
    diagram.generation.create instead. The prompt enforces this split, and
    requires an actual tool call rather than a description of one.
  known_limitations:
    - "Read access, min_classification C2 (policies/tools/tool-policy.yaml, tool generate_image)."
    - "allowed_groups: consultant, adv, sales, board, cdp."
    - "A diffusion model cannot render real figures accurately: never use it for numbers or charts."
---

# Image generation

Creates a photorealistic image from a text prompt. In Comage it serves
genuine marketing-visual requests only; every structured or numeric visual
uses diagram generation.

Documentary only: authorization stays each task's `zuno.allowed_tools`
intersected with `policies/tools/tool-policy.yaml`.
