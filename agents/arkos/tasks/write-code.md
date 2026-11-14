---
okf_version: "0.2"
type: task
title: Write code
description: Write code, a configuration file or a script in the chat reply, from the user's message alone.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tasks/write-code.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  # Reply cap (zuno-demo ADR-0544): without one, a reply once ran to about
  # 40k tokens. 8192 is the schema ceiling and leaves room for a long file.
  max_tokens: 8192
  allowed_tools: []
  allowed_knowledge: []
  # Example prompts a user interface can offer for this task. Display only: choosing one does not select the task.
  prompt_examples:
    - "Write a Helm template that renders a Route only when ingress is enabled."
    - "Generate a shell script that waits for an Argo CD Application to become Synced and Healthy."
---

# Write code

Generate code, configuration or a script (Terraform, Ansible, Kubernetes
manifests, Helm, shell, Python, Go, ...) directly in the chat reply. This is
not a document task: a coding request never goes through the DAT or
workshop drafting steps.

It is a direct branch of the `plan_draft_write` workflow: after the plan
step, it answers from the user's message alone, with no retrieval and no
tool call, so `allowed_tools` and `allowed_knowledge` are empty.

Model routing (`policies/model-routing/model-routing-policy.yaml`, zuno-demo
ADR-0417): this task is pinned to one code model, `mistral-codestral`, with
`strict: true`. If that model fails for any reason, the turn fails
explicitly instead of switching to a model the user did not ask for.
