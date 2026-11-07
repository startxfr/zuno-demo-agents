---
okf_version: v0.3
type: task
title: Blender Python script
zuno:
  # zuno-demo ADR-0610 clause 2: gpt-oss-20b (reasoning) first, qwen3.5-9b (default)
  # after it, then the rest of the corp order. Every external role is excluded; the
  # ai-gateway's C3 floor on the client `blender` already keeps the call local.
  allowed_tools: []
  models:
    preferred:
      - reasoning
      - default
    forbidden:
      - general-external
      - reasoning-external
      - code
---

# Blender Python script

A prompt describing a 3D object or scene. The answer is a Blender Python (`bpy`) script
that the add-on shows to the user, checks statically and runs only on the user's click.
