# Comage contract tests (zuno-demo ADR-0504)

Per-agent, static contract suites, run from the repository root by
`python3 platform/okf/run_agent_contract_tests.py`. Test files are
`test_*.py` under the three subdirectories; each runs standalone and needs
only repository files: no cluster, no credentials, no model calls.

- `contract/`: bundle self-consistency (declared tools and domains exist in
  the policies with a non-empty group intersection; the generated
  authorization matrix is current).
- `tasks/`: per-task assertions (`live_read_tool` is one of the task's
  `allowed_tools`, `primary_task` is declared).
- `prompts/`: prompt lint (OKF `type: prompt` frontmatter, every prompt
  referenced by a task).

Schema and structural checks are platform-wide (`platform/okf/`,
`platform/supply-chain/`) and are not duplicated here. Behavioural
evaluation lives outside this repository.

The three subdirectories hold no suite yet. Filling them is a step of
[PROMOTION.md](https://github.com/startxfr/zuno-demo/blob/main/platform/templates/agent/PROMOTION.md)
(step 4).
