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
  VERSION
```

- `agent.okf.md`: `okf_version`, `type: agent`, `title`, `description`, and the `zuno:` block (`name`, `status`, `tasks`,
  `primary_task`, `graph_shape`, `model.preferred_classification`, `access.groups`, `ui`). `access.groups` is
  `agent_<name>`; the directory name, `zuno.name` and that group must agree.
- `tasks/<task>.md`: one file per entry of `zuno.tasks`, with `allowed_tools` (required) and `allowed_knowledge`.
- `prompts/<task>.md`: the prompt text of the task, in the body.
- `VERSION`: `0.1.0` for a new agent.

Optional: `tools/`, `rag/`, `policies/` notes, `skills/`, and a `tests/` folder (see step 6). A minimal agent is the example
at the end of the [field reference](okf-reference.md#examples).

There is a scaffold, `platform/templates/agent/scaffold_agent.py`, written for the platform that owns this repository. It writes
a valid `agents/<name>/` skeleton, **and also** `gitops/` charts and `evaluations/` folders that belong to that platform and do not
exist in this repository, plus a `keycloak-fragment.json` and a `NEXT_STEPS.md` for it. Those extra files are not part of the
agent and are never published. Use the scaffold only to get the skeleton, and delete what you do not need; it does not
create `VERSION`. Writing the three files by hand is just as quick.

## 3. Generate the authorization matrix

Each `agent.okf.md` body carries a generated section that restates who may use which tool for which task. A release refuses
a file where it is missing or stale:

```sh
python3 platform/okf/generate_authorization_matrix.py --all      # writes the section
python3 platform/okf/generate_authorization_matrix.py --check --all
```

Regenerate it after any change to a task or to a corp policy.

## 4. Run the checks

These are the checks the release workflow re-runs on the tagged tree:

```sh
python3 platform/okf/validate_okf_schema.py                # every document matches its schema
python3 platform/supply-chain/validate_okf_bundle.py       # structure, and every policy reference resolves
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
