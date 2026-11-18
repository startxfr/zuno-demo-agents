---
okf_version: "0.2"
type: task
title: Coding assistant on local models
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/experience-clients/claude-code/tasks/code.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  # zuno-demo ADR-0619 clause 8: the local quality model (qwen3.6-27b-instruct) first,
  # gpt-oss-20b (reasoning) after it. Every external role is excluded, Codestral (code)
  # included: nothing of the user's code leaves the cluster.
  allowed_tools: []
  models:
    preferred:
      - quality
      - reasoning
    forbidden:
      - general-external
      - reasoning-external
      - code
---

# Coding assistant on local models

Claude Code's turns: reading, explaining and changing the code of the user's working copy.
The answer is text and file edits proposed by Claude Code; it runs no tool of the platform.
