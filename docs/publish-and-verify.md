# Publish, verify and roll back a release

[RELEASING.md](../RELEASING.md) says how the maintainers cut a release. This page is for the people who **consume** one
and for anyone who **copies this repository** to publish their own agents. Every command below was run against the real
release `v0.14.3` (cosign 2.4.1, oras 1.2.2); the outputs are described, not pasted.

## What is published

A release `vX.Y.Z` publishes, to `quay.io/zuno` by default (see the README, "What a release is"):

- `okf-<agent>`: one artifact per agent, type `application/vnd.zuno.okf.bundle.v2`.
- `okf-corp`: type `application/vnd.zuno.okf.corp.v1`, the corp policies, an index of the agent digests and the
  conformance cases. **A platform pins the digest of `okf-corp`** and reaches the agents through its index.

Each artifact carries three kinds of evidence, all created by the `publish.yml` workflow on the `v*` tag:

| Evidence | What it proves | How it is stored |
|---|---|---|
| Keyless signature | The artifact was published by that workflow, on a release tag | cosign signature, tag `sha256-<digest>.sig` |
| `contract-tests` attestation | The checks passed on that exact tree: schema, bundle, quota, narrowing, authorization matrix, contract tests, release tooling tests | cosign attestation, tag `sha256-<digest>.att`, predicate type `https://zuno.startx.fr/okf/contract-tests/v1` |
| Build provenance (corp artifact only) | The corp artifact was built from this repository by that workflow (SLSA provenance v1) | a Sigstore bundle stored as an OCI referrer of the artifact |

## Verify what you pull

The identity a consumer trusts is the certificate of `publish.yml` on a release tag, issued by GitHub Actions. Do not
accept anything else: the dev workflow signs `devel-<sha>` and `main-<sha>` artifacts with another identity on purpose,
so a dev artifact can never be admitted as a release.

```sh
ID='^https://github\.com/startxfr/zuno-demo-agents/\.github/workflows/publish\.yml@refs/tags/v'
ISS=https://token.actions.githubusercontent.com
DIGEST=$(oras resolve quay.io/zuno/okf-corp:v0.14.3)

# 1. the corp artifact: signature
cosign verify quay.io/zuno/okf-corp@$DIGEST \
  --certificate-identity-regexp "$ID" --certificate-oidc-issuer "$ISS"

# 2. its contract-tests attestation
cosign verify-attestation quay.io/zuno/okf-corp@$DIGEST \
  --type https://zuno.startx.fr/okf/contract-tests/v1 \
  --certificate-identity-regexp "$ID" --certificate-oidc-issuer "$ISS"
```

Both succeed on `v0.14.3`. The output names the workflow ref (`refs/tags/v0.14.3`) and the repository. The attestation
payload lists the checks that passed, the commit and the run URL.

**Verify each agent artifact too.** The corp index names every agent by digest. Read the index layer
(`application/vnd.zuno.okf.index.v1+json`: `release`, `channel`, and `agents[]` with `name`, `version`, `okfVersion`,
`reference`), then verify each `reference` with the same two commands. Verified on the first agent of `v0.14.3`.
A consumer that only verifies the corp artifact trusts the index, which is signed, so the index digests are covered;
verifying each agent is the check that also catches a registry serving different bytes under an agent digest.

**A tampered or foreign artifact fails.** Verifying `v0.14.3` with an identity of another repository stops with
`no matching signatures: none of the expected identities matched what was in the certificate`, and the message prints the
subject that was found. Anchor the regular expression: an unanchored expression accepts a longer, attacker-chosen path.

**Offline.** `cosign verify ... --offline` verifies without reaching the transparency log; the signature and certificate
are checked against the Sigstore trusted root. This is what `UnifaiAgentBundle` `verify.keyless` does with its
`trustedRootRef`.

**Build provenance.** The corp artifact has a Sigstore bundle referrer (`oras discover quay.io/zuno/okf-corp@$DIGEST`
lists type `application/vnd.dev.sigstore.bundle.v0.3+json`). Its statement is SLSA provenance v1 with subject
`quay.io/zuno/okf-corp` and the workflow `.github/workflows/publish.yml` at `refs/tags/<tag>` of this repository.
The statement can be decoded from the referrer (`oras manifest fetch` the referrer, then `oras blob fetch` its layer).
The GitHub CLI is the documented route to verify it:
`gh attestation verify oci://quay.io/zuno/okf-corp@$DIGEST --repo startxfr/zuno-demo-agents`. That last command was not
run when this page was written (the GitHub CLI was not available); the signature and the `contract-tests` attestation
above were.

## The signature manifest limit (32 layers)

`cosign sign` appends one layer to the manifest `sha256-<digest>.sig` every time it runs. An agent whose files did not
change keeps its digest across releases, so a digest published often accumulated signatures (35 on one agent by
release 0.6.1). A consumer reads a bounded number: `unifai-operator` reads at most **32 layers** and then refuses the
bundle. The release workflow therefore signs through `platform/release/sign_once.py`, which skips an artifact already signed by the
identity and empties a manifest with more than 16 layers before signing again (`--clean-above 16`). Only the release
workflow may empty it: the dev workflow must never strip the release signature.

Check it for a digest:

```sh
oras manifest fetch quay.io/zuno/okf-corp:sha256-<digest-hex>.sig | jq '.layers | length'
```

It was 1 for `okf-corp` at `v0.14.3` (and 1 for its attestation manifest). If you see more than 16, run the release
signing step again through `sign_once.py` instead of signing by hand.

## Roll back

A release is never repaired in place. Tags are immutable, nothing is re-tagged and nothing is deleted from the registry
(`okf_release.py` refuses to move a tag). To go back:

1. Take the corp digest of the previous release. It is in the notes of its GitHub release ("Corp artifact (pin this)"),
   or from `oras resolve quay.io/zuno/okf-corp:v<previous>`.
2. **Verify it** with the commands above. The previous release `v0.14.2` verifies today.
3. Re-pin the consumer to that digest, through the consumer's normal review (a pull request, for a platform that pins in Git).
4. Fix forward: the fix is a new release with a new version, never an edit of the broken one.

The agents come back with the old corp digest, because the index names their digests.

## Adapt it to your own identity, registry and attestation

Copy the repository, then change these, and nothing else:

| What | Where |
|---|---|
| Registry (default `quay.io/zuno`) | the repository variable `OKF_REGISTRY`. Create the repositories `okf-corp` and `okf-<agent>` as **public** before the first push (a repository created by a push starts private), with a robot account that can write to them. |
| Trusted workflow identity | the `--identity` regular expression in `publish.yml` (the `sign_once.py` calls), and the expression your consumers verify with. It contains the repository path and the workflow file name. **Do not rename `publish.yml`** without changing every consumer's policy. |
| Attestation predicate type | the `--type` of the "Attest the checks that passed" step of `publish.yml` (`https://zuno.startx.fr/okf/contract-tests/v1`), and the `--type` your consumers verify. Pick a URL you own. |
| Other settings | the variables, secrets and rulesets listed in [RELEASING.md](../RELEASING.md), "Setup". |

A consumer that is not UnifAI does the same checks with the cosign commands above.

## No GitHub identity: signing without GitHub OIDC

The release tooling signs **keyless only**, and artifacts of type `…bundle.v2` are signed keyless on the manifest. The
`UnifaiAgentBundle` resource refuses a `v2` artifact verified by `publicKeyRef`: key-based verification belongs to the
older `v1` artifact type, which this repository's tooling no longer builds. So there is no supported key-only path for a
release of this repository today.

What a team without GitHub OIDC can do within the current design:

- Use another OIDC issuer that Fulcio accepts (set the issuer in the verification policy: `verify.keyless.issuer` in a
  `UnifaiAgentBundle`, `--certificate-oidc-issuer` in cosign).
- Run a private Sigstore stack and give consumers its `trusted_root.json` (`verify.keyless.trustedRootRef`).

Supporting a long-lived signing key for `v2` artifacts would need changes in the release tooling **and** in the consumer.
That is a decision for the maintainers, not something this page promises.

## SBOM

No software bill of materials is produced today. A bundle is text (Markdown and YAML) plus deterministic layers; it
holds no code, no packages and no model, so an SBOM would list nothing a consumer can act on. The evidence that matters
here is the signature, the attestation of the checks and the build provenance. **Recommendation: do not add an SBOM
now**, and revisit it if a bundle ever embeds code, a dependency list or a model file. This is a maintainer decision;
the page states the current situation either way.
