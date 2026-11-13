# What travels in a release artifact

A release publishes two kinds of artifact, built by `platform/release/okf_release.py` (`build`, `publish`). This page
lists the files each one holds. It is derived from that script, not from memory: if the script changes, this page is wrong.

## An agent artifact (`okf-<agent>`)

Type `application/vnd.zuno.okf.bundle.v2`, one layer `application/vnd.zuno.okf.bundle.v2.tar+gzip`.

**Included**, from `agents/<name>/`:

| Path | Notes |
|---|---|
| `agent.okf.md` | The agent. |
| `tasks/` | Every file under it. |
| `prompts/` | Every file under it, including `--<slot>` prompts. |
| `skills/` | Every file under it. |
| `tools/`, `rag/`, `policies/` | Every file under them. |
| `skills/corp/<name>.md` | Added automatically for each corp skill (`corp/<name>`) a task lists. It is copied from `policies/skills/<name>.md`, so the agent artifact is self-contained. |

**Never included:**

- every file named `README.md`, at any level;
- `tests/`, `VERSION`, `NEXT_STEPS.md`, `keycloak-fragment.json` and any other file or folder not listed above.

**Reproducible.** Entries are sorted, with a zero modification time, owner `0` and mode `0644`. An agent whose published
files did not change keeps the same digest from one release to the next, whatever else changed in the repository.

**Consequence.** Changing a corp skill changes the digest of every agent that uses it, so their `VERSION` must be bumped
(`okf_release.py check-versions` refuses a merge otherwise).

Manifest annotations: `org.opencontainers.image.source`, `.revision`, `.created`, `.version` (the agent `VERSION`), and
`zuno.okf.agent` and `zuno.okf.version` (the agent name and its `okf_version`). The revision and date come from the last
commit that touched the agent's own files, which is also why an unchanged agent keeps its digest.

## The corp artifact (`okf-corp`)

Type `application/vnd.zuno.okf.corp.v1`. This is what a platform pins. Layers, in order:

| Layer media type | Content |
|---|---|
| `application/vnd.zuno.okf.policies.v1.tar+gzip` | The whole `policies/` folder, minus `README.md` files. |
| `application/vnd.zuno.okf.index.v1+json` | The index of the release: `release`, `channel` and, for each agent, `name`, `version`, `okfVersion` and the digest `reference` of its artifact. |
| `application/vnd.zuno.okf.clients.v1.tar+gzip` | Present when the repository has experience clients: each `experience-clients/<name>/client.okf.md` and its `tasks/`, never READMEs. |
| `application/vnd.zuno.okf.conformance.v1.tar+gzip` | Present when `conformance/cases/` exists: the OKF reader conformance cases, never the README or the self-check test. Always last. |

The optional layers come after the first two, so a consumer that reads only the policies and the index by media type is
not affected when they appear.

## Tags and immutability

An agent artifact is tagged `<agent>-v<agent version>`; the corp artifact is `v<VERSION>`. Dev pushes publish
`devel-<sha12>` and `main-<sha12>`. A tag that already exists with a different digest is refused: nothing is moved.
