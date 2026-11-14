# Finage contract tests

Static, repository-only suites for this agent: no cluster, no credentials, no model calls. Each `test_*.py` runs as a
plain script; `python3 platform/okf/run_agent_contract_tests.py` runs them all from the repository root. Tests are
never published.

- `contract/`: bundle self-consistency (every declared tool and knowledge domain resolves in the corp policies with a
  non-empty group intersection; the generated authorization matrix is current).
- `tasks/`: per-task declarations (`live_read_tool` within `allowed_tools`, `primary_task` declared,
  `project_required` marks well-formed).
- `prompts/`: prompt lint (OKF frontmatter, one prompt per task).

Only `tasks/` holds a suite today (`test_task_declarations.py`); `contract/` and `prompts/` hold none yet. Schema and
structure checks are platform-wide (`platform/okf/`, `platform/supply-chain/`) and are not repeated here; behavioural
evaluation belongs to the platform that serves the agent. The zuno-demo [promotion
checklist](https://github.com/startxfr/zuno-demo/blob/main/platform/templates/agent/PROMOTION.md) asks for real, green
suites in all three folders before the agent is promoted.
