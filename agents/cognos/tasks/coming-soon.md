---
okf_version: "0.2"
type: task
title: Coming soon
description: Placeholder task. Cognos is not built yet and declares no capability.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/cognos/tasks/coming-soon.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  allowed_tools: []
---

# Coming soon

Cognos is not built yet. Planned scope (zuno-demo ADR-0349): board-only financial and strategic question answering over
a large tool and knowledge set that explicitly excludes the technical tools and the technical knowledge corpora
(`knowledge.tech` never appears in a Cognos task), gated on the `board` business role.

`allowed_tools` stays empty while the agent is a placeholder: it has no tool-call capability by construction.

Two corp policy entries already anticipate the build and stay inert until then:

- the tool policy's `generate_image` entry (`image.generation.create`) lists `board`, so a future Cognos task can
  declare it without a policy change;
- the model-routing policy prefers `ovhcloud-gpt-oss-120b` for this task on C1 and C2 turns; a turn that reaches C3
  excludes it and falls back to local models.
