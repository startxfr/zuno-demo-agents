# Add an agent

This guide takes you from nothing to an agent that passes every check a release runs. The steps were run on a scratch
agent against this repository; the checks all pass. Work from the repository root.

An agent here is **declarative**: Markdown files with YAML frontmatter. A platform that consumes a release supplies the
runtime. Field meanings are in the [OKF field reference](okf-reference.md); what ends up in the published artifact is in
[bundle-files.md](bundle-files.md).

## 1. Decide what the agent may touch

An agent may only **narrow** the corp policies in `policies/`, never widen them. Before writing, check what exists:

- tools: `policies/tools/tool-policy.yaml` (each tool is a capability name such as `web_search`);
- knowledge domains: `policies/knowledge/knowledge-policy.yaml` (`knowledge.<domain>`);
- model roles and limits: `policies/models/model-catalog.yaml`, `policies/limits/limits-policy.yaml`;
- quota classes: `policies/quotas/quota-policy.yaml`.

A tool or domain that does not exist there is a validation error. Adding one is a change to the corp policies, reviewed on
its own, not part of adding an agent.

## 2. Create the files

```
agents/<name>/
  agent.okf.md
  tasks/<task>.md
  prompts/<task>.md
  index.md          (generated in step 3)
  VERSION
```

Every document starts with the profile 1.0 envelope (see the [field reference](okf-reference.md#the-envelope-every-document)):
`okf_version: "0.2"` (quoted), `type`, `title`, `resource` (the file's URL on the main branch) and `zuno.profile: "1.0"`.

- `agent.okf.md`: the envelope with `description`, and the `zuno:` block (`profile`, `maintainer`, `name`, `status`, `tasks`,
  `primary_task`, `graph_shape`, `model.preferred_classification`, `access.groups`, `ui`). `access.groups` is
  `agent_<name>`; the directory name, `zuno.name` and that group must agree.
- `tasks/<task>.md`: one file per entry of `zuno.tasks`, with a one-line `description`, `allowed_tools` (required) and `allowed_knowledge`.
- `prompts/<task>.md`: the prompt text of the task, in the body. Every task has one.
- `VERSION`: `0.1.0` for a new agent.

Optional: `tools/`, `rag/`, `policies/` notes, `skills/`, and a `tests/` folder (see step 6). A minimal agent is the example
at the end of the [field reference](okf-reference.md#examples).

There is a scaffold that writes a valid profile 1.0 skeleton (`agent.okf.md` as a placeholder, the primary task, its
prompt, a README, `VERSION` 0.1.0) and generates the matrix and the index. It refuses a tool or a domain the corp
policies do not know:

```sh
python3 platform/templates/agent/scaffold_agent.py --name <name> --title <Title> --description "<one line>" \
    --primary-task <task> --primary-task-title "<Task title>" --knowledge knowledge.tech --tool web_search \
    --tile-description "<tile text>"
```

## 3. Generate the authorization matrix and the index

Each `agent.okf.md` body carries a generated section that restates who may use which tool for which task, and each
bundle has a generated `index.md` that lists its documents (upstream OKF §8). A release refuses a bundle where either
is missing or stale:

```sh
python3 platform/okf/generate_authorization_matrix.py --all      # writes the section
python3 platform/okf/generate_index.py                           # writes agents/<name>/index.md
python3 platform/okf/generate_authorization_matrix.py --check --all
python3 platform/okf/generate_index.py --check
```

Regenerate both after any change to a task, a prompt, a note or a corp policy.

## 4. Run the checks

These are the checks the release workflow re-runs on the tagged tree:

```sh
python3 platform/okf/build_profile_schemas.py --check     # the profile 1.0 schemas are unchanged (frozen)
python3 platform/okf/validate_okf_schema.py                # every document matches its schema
python3 platform/okf/generate_index.py --check             # every index.md is up to date
python3 platform/supply-chain/validate_okf_bundle.py       # structure, references and the profile 1.0 rules
python3 platform/okf/validate_quota_policy.py
python3 platform/okf/check_narrowing.py                    # nothing widens the corp policies
python3 platform/okf/generate_authorization_matrix.py --check --all
python3 platform/okf/run_agent_contract_tests.py           # per-agent contract tests, when present
python3 platform/release/okf_release.py check-versions     # needs a git checkout with its tags
```

All must print `RESULT: PASS`.

## 5. Versions

Bump `agents/<name>/VERSION` whenever a **published** file changes (see [bundle-files.md](bundle-files.md)): patch for a fix
that changes no behaviour a user relies on, minor for a new task, tool or knowledge domain, major for a removed task or a
narrowed access. A README or a test change needs no bump. The root `VERSION` is the release version and is bumped on its own.
[RELEASING.md](../RELEASING.md) has the rules and the version gate.

## 6. Tests

`tests/` has three folders, `contract/`, `tasks/` and `prompts/`, each with a README, and `test_*.py` files that run as plain
scripts: bundle self-consistency, per-task declarations and prompt lint. They use only repository files. See
`agents/arkos/tests/` for a complete example. A `tests/` folder that exists must contain the three folders and a README;
an agent with no `tests/` folder is not a finding. Tests are never published.

Some agent READMEs mention a promotion checklist, `PROMOTION.md`. It lives in the zuno-demo repository
([platform/templates/agent/PROMOTION.md](https://github.com/startxfr/zuno-demo/blob/main/platform/templates/agent/PROMOTION.md)); it
covers that platform's evaluation gates and is not needed to release an agent from this repository.

## 7. Publish

1. Open a pull request into `devel`, then `devel` into `main` as described in [RELEASING.md](../RELEASING.md).
2. **Create the registry repository `okf-<name>` first**, public, with write access for the release robot: a repository created by a
   push starts private (see "Setup" in [RELEASING.md](../RELEASING.md)).
3. The release chain publishes and signs the agent. How a consumer verifies and rolls back a release is in
   [publish-and-verify.md](publish-and-verify.md).
