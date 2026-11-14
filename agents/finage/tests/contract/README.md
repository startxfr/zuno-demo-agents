# contract/

Bundle-level self-consistency suites (`test_*.py`): every `allowed_tools` entry resolves in
`policies/tools/tool-policy.yaml` and every `allowed_knowledge` entry in `policies/knowledge/knowledge-policy.yaml`, each
with a non-empty `allowed_groups` intersection for the agent's intended roles; the generated authorization matrix is
current. Static repository checks only.
