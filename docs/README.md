# Documentation

How to author, release, verify and consume agent bundles with this repository.

| Page | Read it to |
|---|---|
| [Architecture](architecture.md) | see the pieces, how a release travels to a running agent, the trust chain and the versions |
| [The lifecycle of a bundle](bundle-lifecycle.md) | follow one bundle from the first file to a running agent, then change, roll back, revoke or retire it |
| [Add an agent](add-an-agent.md) | create an agent and pass every check a release runs |
| [OKF field reference](okf-reference.md) | know the Zuno OKF profile 1.0: its link to upstream OKF 0.2, every field of every document, the narrowing rules and the deviations from upstream |
| [What travels in a release](bundle-files.md) | know which files an agent artifact and the corp artifact contain |
| [Publish, verify and roll back](publish-and-verify.md) | verify a release with cosign, check its attestations, go back to the previous release, and adapt the trust settings |
| [The `UnifaiAgentBundle` resource](unifaiagentbundle.md) | turn a released bundle into running agents on UnifAI: every field, condition and the revocation list |

Related, at the repository root: [README.md](../README.md) (what the repository is) and [RELEASING.md](../RELEASING.md)
(branches, versions and the release chain).

Documentation that lives with the code of the other repositories:

- [zuno-demo: platform integration](https://github.com/startxfr/zuno-demo/blob/devel/docs/platform/agents-release-integration.md),
  how one platform pins, promotes, admits, mirrors and consumes a release.
- [UnifAI (startx fork): the operator and OKF bundles](https://github.com/startxfr/UnifAI/blob/devel/fork/unifai-operator/docs/okf-agent-bundles.md),
  how the operator reads, verifies, validates and maps a bundle, and what each operator version accepts.
- [Upstream Open Knowledge Format 0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
