# Documentation

How to author, release, verify and consume agent bundles with this repository.

| Page | Read it to |
|---|---|
| [Add an agent](add-an-agent.md) | create an agent and pass every check a release runs |
| [OKF field reference](okf-reference.md) | know every field of an agent, task, prompt, tool, rag, policy and skill document, and the narrowing rules |
| [What travels in a release](bundle-files.md) | know which files an agent artifact and the corp artifact contain |
| [Publish, verify and roll back](publish-and-verify.md) | verify a release with cosign, check its attestations, go back to the previous release, and adapt the trust settings |
| [The `UnifaiAgentBundle` resource](unifaiagentbundle.md) | turn a released bundle into running agents on UnifAI: every field, condition and the revocation list |

Related, at the repository root: [README.md](../README.md) (what the repository is) and [RELEASING.md](../RELEASING.md)
(branches, versions and the release chain).
