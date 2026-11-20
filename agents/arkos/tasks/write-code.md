---
okf_version: "0.2"
type: task
title: Write code
description: Write code, a configuration file or a script in the chat reply, from the user's message alone.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/arkos/tasks/write-code.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  max_tokens: 8192
  allowed_tools: []
  allowed_knowledge: []
  models:
    preferred:
      - reasoning
      - quality
  prompt_examples:
    - "Write a Helm template that renders a Route only when ingress is enabled."
    - "Generate a shell script that waits for an Argo CD Application to become Synced and Healthy."
    - "Write the Kustomize overlay for our customer's sovereign cluster, using their internal registry and namespace names."
---

# Write code

Generate code, configuration or a script (Terraform, Ansible, Kubernetes
manifests, Helm, shell, Python, Go, ...) directly in the chat reply. This is
not a document task: a coding request never goes through the DAT or
workshop drafting steps.

It is a direct branch of the `plan_draft_write` workflow: after the plan
step, it answers from the user's message alone, with no retrieval and no
tool call, so `allowed_tools` and `allowed_knowledge` are empty.

Model routing (`policies/model-routing/model-routing-policy.yaml`): Arkos is
a C3 agent, so this task runs on local models only, at every level:
gpt-oss-20b first, the local quality model as fallback. The code model
`mistral-codestral` is eligible for C1 and C2 only and never serves it; coding
with Codestral on C1/C2 data is Tekos's `write-code` task. If every local
model fails, the turn fails instead of leaving the cluster.
