# Arkos Contract Tests (ADR-0504)

Per-agent, repo-side, static contract suites - run by
`python3 platform/okf/run_agent_contract_tests.py` from the repository
root (a blocking lint-chain step; test files are `test_*.py` under the
three subdirectories, each executable standalone).

Three-layer boundary (ADR-0504): **schema/structural** checks are
platform-wide and live in `platform/supply-chain/` +
`platform/okf/schema/` - never duplicated here; **contract** checks
(this directory) are Arkos-specific and need only repository files - no
cluster, no credentials, no model calls; **behavioral** checks (live
evaluation scenarios) live in the zuno-demo repository.

- `contract/` - bundle-level self-consistency (declared tools/domains
  exist in policy with non-empty group intersections; the ADR-0503
  matrix is current)
- `tasks/` - per-task assertions (live_read_tool within allowed_tools,
  primary_task declared, ADR-0512 project_required marks well-formed,
  max_tokens within the schema bound)
- `prompts/` - prompt lint (required OKF frontmatter, every prompt
  referenced by a task or prompt slot, every task and slot has its file)

**Blocking rule (ADR-0504):** `contract/`, `tasks/` and `prompts/` must
contain real, green tests; step 4 of the promotion checklist
([PROMOTION.md](https://github.com/startxfr/zuno-demo/blob/main/platform/templates/agent/PROMOTION.md))
requires them. Empty stub directories do not count.
