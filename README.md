# zuno-demo-agents

The definitions of the Zuno agents, as bundles of the
[Open Knowledge Format 0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) in the
Zuno OKF profile 1.0, and the corp policies that bound them. Released as signed OCI artifacts on quay.io; a platform
consumes a release by pinning its digest.

This repository has its own life cycle. It knows nothing about the platforms
that consume it: a platform (today [zuno-demo](https://github.com/startxfr/zuno-demo))
picks a release when it wants, verifies it, and configures itself from it.

## Use it for your own agents

This repository is a **reference you can copy**. Its structure, its checks and its release chain do not depend on Zuno:
copy it, replace the agents with yours, and you have signed, verifiable agent releases. Zuno's own agents stay here as
worked examples.

To adapt it, change four things and keep the rest:

- **Agents and corp policies:** your agents under `agents/`, your limits, tools, knowledge domains, quotas and model roles
  under `policies/`. The checks keep every agent inside the corp policies.
- **Registry:** the variable `OKF_REGISTRY` (default `quay.io/zuno`).
- **Trusted identity:** the workflow identity your consumers verify, which contains your repository path and the workflow
  file name `publish.yml`.
- **Attestation type:** the predicate type URL of the checks attestation, which should be one you own.

Adding agents is explained in [docs/add-an-agent.md](docs/add-an-agent.md); the registry, the identity and the attestation
type in [docs/publish-and-verify.md](docs/publish-and-verify.md). Start with the [documentation index](docs/README.md).

## Contents

| Path | What it is |
|---|---|
| `agents/<name>/` | One agent: `agent.okf.md`, `tasks/`, `prompts/`, `tools/`, `rag/`, `policies/`, `skills/` (Markdown + YAML frontmatter, profile 1.0), a generated `index.md`, `tests/`, and its own `VERSION` |
| `experience-clients/<name>/` | One experience client (zuno-demo ADR-0592: Open WebUI, OpenClaw): `client.okf.md` (who may use the logical agent name) and `tasks/` (the tools each task allows). Not an agent: no bundle, group, prompt or `VERSION`; it ships in the corp artifact's clients layer. See `experience-clients/README.md` |
| `policies/` | Corp policies, the ceiling for every agent: `tools/`, `knowledge/`, `quotas/`, `model-routing/`, `models/model-catalog.yaml` (the model vocabulary), `guardrails/` |
| `platform/okf/` | OKF schemas (the frozen profile 1.0 and the legacy v0.2/v0.3) and checks: version dispatch, schema validation, narrowing, authorization matrices, index generation, quota lint, contract-test runner |
| `platform/supply-chain/validate_okf_bundle.py` | Bundle structure, corp policy references and the profile 1.0 rules |
| `conformance/` | Cases every reader of the format must parse to the same result; shipped in the corp artifact |
| `platform/release/` | Release tooling: build, version gate, publish, changelog, dev-run rendering |
| `docs/` | Documentation: the [architecture](docs/architecture.md), [the lifecycle of a bundle](docs/bundle-lifecycle.md), how to [add an agent](docs/add-an-agent.md), the [OKF field reference](docs/okf-reference.md), [what travels in a release](docs/bundle-files.md), how to [publish, verify and roll back a release](docs/publish-and-verify.md), and [the `UnifaiAgentBundle` resource](docs/unifaiagentbundle.md) that turns a released bundle into running agents |
| `VERSION` | The release version |
| `CHANGELOG.md` | Written by the release chain on `stable` |

An agent may only narrow the corp policies, never widen them. The model
catalog names logical models; a consuming platform binds each name to a real
backend and refuses a release that names one it cannot serve.

## The format: Zuno OKF profile 1.0

Every document follows upstream OKF 0.2: `okf_version: "0.2"`, `type`, `title`, `description`, `resource`, and the
optional `tags`, `sources`, `generated`, `verified`, `status` and `stale_after`. Each bundle has a generated root
`index.md`. The Zuno part lives under one namespaced key, `zuno`, which carries `profile: "1.0"` and the agent's
declarations:
- tasks, model classification, access groups and display;
- model roles (`zuno.models`), guardrail modes (`zuno.guardrails`) and limits (`zuno.limits`);
- delegation, and skills.

The profile schemas (`platform/okf/schema/zuno-okf-profile-1.0-*.schema.json`) are frozen by `SHA256SUMS`: a change
needs a new profile version (zuno-demo ADR-0615). Legacy documents (`okf_version: v0.2` or `v0.3`) are still read
during a transition: zuno-demo refuses them from unifai-operator line 0.2 (zuno-demo ADR-0615, WP-268).

A bundle may only narrow the corp policies: `platform/okf/check_narrowing.py` refuses any widening, naming the corp
clause it exceeds. A corp skill a task references is embedded in that agent's artifact as `skills/corp/<name>.md`, so
an agent artifact is self-contained.

Consumers apply what they map. Today:
- **the ai-gateway** applies the model roles and the guardrail modes, and enforces `max_tokens`;
- **UnifAI** applies `max_steps`, `max_tokens_per_turn` and the history settings, and passes `max_tokens` on.

A field a consumer does not map has no runtime effect there: the corp policies remain the authority.

Read [docs/architecture.md](docs/architecture.md) for the whole picture, and [docs/okf-reference.md](docs/okf-reference.md)
for every field and the deviations from upstream.

## What a release is

Each release publishes, to `quay.io/zuno` by default:

- `okf-<agent>`: one artifact per agent, type `application/vnd.zuno.okf.bundle.v2`,
  one layer with the files a consumer reads, `index.md` included (never `tests/` nor `README.md`),
  tagged `<agent>-v<agent version>`. An agent whose files did not change
  keeps its digest.
- `okf-corp`: type `application/vnd.zuno.okf.corp.v1`, the corp policies plus
  an index of the agent digests (with each agent's `okfProfile`), the experience
  clients and the conformance cases, tagged `v<VERSION>`. **This is what a
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
python3 platform/okf/build_profile_schemas.py --check
python3 platform/okf/validate_okf_schema.py
python3 platform/okf/generate_index.py               # regenerate after any document change (--check in CI)
python3 platform/supply-chain/validate_okf_bundle.py
python3 platform/okf/check_narrowing.py
python3 platform/okf/validate_quota_policy.py
python3 platform/okf/generate_authorization_matrix.py --all    # regenerate after any task/policy change
python3 platform/okf/run_agent_contract_tests.py
python3 -m unittest discover -s platform/release/tests
python3 platform/release/okf_release.py check-versions
```

Branches, versions and releases: [RELEASING.md](RELEASING.md).

## History

Extracted on 2026-10-22 from `startxfr/zuno-demo` (branch `demo222`, since
retired and kept as the tag `archive/demo222`; commit `9b5507c6`, also in `devel`) with its history, per zuno-demo ADR-0576. Commit messages before
that date refer to zuno-demo ADRs and work packages.

## License

GPL-3.0, see [LICENSE](LICENSE).
