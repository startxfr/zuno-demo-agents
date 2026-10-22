# Branches, versions and releases

## Branches

| Branch | Who writes | What runs |
|---|---|---|
| `devel` | maintainers, direct push | CI (lint, test, secrets); publish `devel-<sha12>` artifacts; run them on the dev cluster (never blocking) |
| `main` | pull requests from `devel` only, 1 review, green checks | CI; publish `main-<sha12>` artifacts; **every push is a release** |
| `stable` | the release bot only | nothing: it records what was released |
| tags `v*`, `<agent>-v*` | the release bot only, never moved or deleted | `v*` starts the release publication |

Work happens on `devel`. When it is ready, open a pull request `devel` →
`main`. Its required checks are `lint`, `test`, `secrets`, `version-gate`
and, once the dev cluster is wired, `run-dev`.

## Versions

Both are bumped by hand on `devel`, before the pull request to `main`:

- `VERSION`: the release version. Every release needs a new one.
- `agents/<name>/VERSION`: the agent's own version. Bump it when the agent's
  published files change (`agent.okf.md`, `tasks/`, `prompts/`, `skills/`,
  `tools/`, `rag/`, `policies/`). README and test changes need no bump.

Use semantic versioning: patch for a fix that changes no behaviour a user
relies on, minor for a new task, tool or knowledge domain, major for a removed
task or a narrowed access. `version-gate` refuses a pull request that reuses a
released version or changes an agent without bumping it:

```sh
python3 platform/release/okf_release.py check-versions
```

## The release chain

Merging into `main` starts `release.yml`, which:

1. merges `main` into `stable` (`--no-ff`);
2. writes the `CHANGELOG.md` section of the new version on `stable` and
   pushes `stable`;
3. cuts the immutable tag: a commit whose tree is exactly `stable`'s and
   whose parents are the previous release tag and `stable`, so that
   `git log --first-parent v<VERSION>` lists releases only; tags it
   `v<VERSION>`, plus `<agent>-v<version>` for every agent version not yet
   released; pushes the tags.

The `v<VERSION>` tag starts `publish.yml`, which re-runs every check on the
tagged tree, publishes the agent and corp artifacts, signs them keyless,
attests the checks and the build provenance, and creates the GitHub release
whose notes give the corp digest to pin.

Nothing is ever re-tagged. A broken release is fixed by a new one.

## Dev artifacts

Every push to `devel` or `main` publishes `devel-<sha12>` / `main-<sha12>`
tags in the same repositories, signed keyless by `publish-dev.yml` on that
branch. The release verification policy only accepts `publish.yml` on a `v*`
tag, so a dev artifact can be run on the dev cluster but never admitted as a
release by a platform.

`run-dev.yml` applies the `devel` artifacts of a commit on the dev cluster as
`UnifaiAgentBundle` objects (namespace `okf-dev`), waits for the operator to
report them `Ready`, then deletes them. The platform-specific part of the
bundle spec (owner, LLM, MCP provider, team) comes from the cluster's
`okf-dev-bundle-template` ConfigMap, key `spec.yaml`: this repository does
not know it.

## Setup

The workflows are inert until these exist. Repository **variables**
(Settings → Secrets and variables → Actions → Variables):

| Variable | Value | Effect |
|---|---|---|
| `OKF_PUBLISH_ENABLED` | `true` | turns on `publish-dev.yml` and `publish.yml` |
| `OKF_RELEASE_ENABLED` | `true` | turns on `release.yml` |
| `OKF_RUN_DEV_ENABLED` | `true` | turns on `run-dev.yml` (needs an operator with keyless verification) |
| `OKF_RUN_DEV_REQUIRED` | `true` | makes `run-dev` blocking on pull requests to `main` |
| `OKF_REGISTRY` | `quay.io/zuno` (default) | where artifacts go |
| `OKF_DEV_NAMESPACE` | `okf-dev` (default) | dev cluster namespace |

**Secrets:**

| Secret | Where | For |
|---|---|---|
| `QUAY_ROBOT_USERNAME`, `QUAY_ROBOT_TOKEN` | repository | pushing to quay.io (robot with write on `okf-*`) |
| `RELEASE_BOT_APP_ID`, `RELEASE_BOT_PRIVATE_KEY` | environment `release` | the GitHub App that pushes `stable` and tags |
| `DEMO333_API_URL`, `DEMO333_TOKEN`, `DEMO333_CA` | environment `dev-demo333` | the dev cluster run |

**Rulesets** (Settings → Rules → Rulesets):

- `devel`: block force pushes and deletion.
- `main`: require a pull request (1 approval), require status checks `lint`,
  `test`, `secrets`, `version-gate` (and `run-dev` once enabled), block force
  pushes and deletion.
- `stable`: restrict creations, updates and deletions, block force pushes;
  bypass: the release GitHub App only.
- Tag ruleset on `v*` and `*-v*`: restrict creations, updates and deletions;
  bypass: the release GitHub App only.

**quay.io** (organization `zuno`): public repositories `okf-corp` and
`okf-<agent>` for each agent, created before the first push (a repository
created by a push starts private), and a robot account with write permission
on them. A new agent needs its repository created first.
