# Tekos contract tests (ADR-0504)

Per-agent, static contract suites, run by
`python3 platform/okf/run_agent_contract_tests.py` from the repository root.
Test files are `test_*.py` under the three subdirectories, each executable
standalone. They need only repository files: no cluster, no credentials, no
model calls. Schema and structure checks are repository-wide and live in
`platform/okf/` and `platform/supply-chain/`, never here; behavioural
evaluations are not part of the bundle.

- `contract/` - bundle-level self-consistency (declared tools and domains
  exist in the corp policies with non-empty group intersections)
- `tasks/` - per-task assertions (live_read_tool within allowed_tools,
  primary_task declared)
- `prompts/` - prompt lint (OKF frontmatter, referenced by a task)

Today the three directories hold only their README: Tekos has no suite yet.
`https://github.com/startxfr/zuno-demo/blob/main/platform/templates/agent/PROMOTION.md`
step 4 requires real, green suites here: empty directories do not count.
