# zuno-demo-agents

The definitions of the Zuno agents, as OKF bundles, and the corp policies
that bound them. Released as signed OCI artifacts on quay.io; a platform
consumes a release by pinning its digest.

This repository has its own life cycle. It knows nothing about the platforms
that consume it: a platform (today [zuno-demo](https://github.com/startxfr/zuno-demo))
picks a release when it wants, verifies it, and configures itself from it.

## Contents

| Path | What it is |
|---|---|
| `agents/<name>/` | One agent: `agent.okf.md`, `tasks/`, `prompts/`, `tools/`, `rag/`, `policies/` (OKF v0.2, Markdown + YAML frontmatter), `tests/`, and its own `VERSION` |
| `policies/` | Corp policies, the ceiling for every agent: `tools/`, `knowledge/`, `quotas/`, `model-routing/`, `models/model-catalog.yaml` (the model vocabulary), `guardrails/` |
| `platform/okf/` | OKF schemas and checks: schema validation, authorization matrices, quota lint, contract-test runner |
| `platform/supply-chain/validate_okf_bundle.py` | Bundle structure and corp policy references |
| `platform/release/` | Release tooling: build, version gate, publish, changelog, dev-run rendering |
| `VERSION` | The release version |
| `CHANGELOG.md` | Written by the release chain on `stable` |

An agent may only narrow the corp policies, never widen them. The model
catalog names logical models; a consuming platform binds each name to a real
backend and refuses a release that names one it cannot serve.

## What a release is

Each release publishes, to `quay.io/zuno` by default:

- `okf-<agent>`: one artifact per agent, type `application/vnd.zuno.okf.bundle.v2`,
  one layer with the files a consumer reads (never `tests/` nor `README.md`),
  tagged `<agent>-v<agent version>`. An agent whose files did not change
  keeps its digest.
- `okf-corp`: type `application/vnd.zuno.okf.corp.v1`, the corp policies plus
  an index of the agent digests, tagged `v<VERSION>`. **This is what a
  platform pins.**

Every artifact is signed keyless by the `publish.yml` workflow of this
repository on a `v*` tag, with a contract-tests attestation; the corp
artifact also carries SLSA build provenance. Verify a release with:

```sh
cosign verify quay.io/zuno/okf-corp@sha256:<digest> \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp '^https://github\.com/startxfr/zuno-demo-agents/\.github/workflows/publish\.yml@refs/tags/v'
```

## Working on it

```sh
pip install pyyaml jsonschema
python3 platform/okf/validate_okf_schema.py
python3 platform/supply-chain/validate_okf_bundle.py
python3 platform/okf/validate_quota_policy.py
python3 platform/okf/generate_authorization_matrix.py --all    # regenerate after any task/policy change
python3 platform/okf/run_agent_contract_tests.py
python3 -m unittest discover -s platform/release/tests
python3 platform/release/okf_release.py check-versions
```

Branches, versions and releases: [RELEASING.md](RELEASING.md).

## History

Extracted on 2026-10-22 from `startxfr/zuno-demo` (branch `demo222`, commit
`9b5507c6`) with its history, per zuno-demo ADR-0576. Commit messages before
that date refer to zuno-demo ADRs and work packages.

## License

GPL-3.0, see [LICENSE](LICENSE).
