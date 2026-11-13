# The `UnifaiAgentBundle` custom resource

An OKF agent bundle published by this repository is turned into running UnifAI objects by one custom resource,
`UnifaiAgentBundle` (`unifai.startx.fr/v1alpha1`, short name `uab`). This page explains the resource field by field,
shows an example, and explains each status condition and what to check first when it is false.

The resource is served by the UnifAI operator. The field list below follows the operator's API types; if the two ever
disagree, the types win and this page is the one to fix.

## What the operator does, in order

A failed step emits nothing and leaves what the last good version emitted.

1. **Revocation check.** The platform's revocation list is read first (see [Revocation](#revocation)).
2. **Pull** the artifact named by `spec.source.oci.reference`, pinned by digest.
3. **Verify** the signature, before any file of the bundle is parsed (condition `Verified`).
4. **Validate** every OKF document against the schemas and the graph shape, and check the entitlement (condition `Valid`).
5. **Check the ceilings**: the bundle may narrow what the resource allows, never widen it (condition `WithinCeilings`).
6. **Emit** the UnifAI objects (condition `Emitted`). Everything emitted is owned and labelled
   `unifai.startx.fr/agent-bundle: <bundle name>`; objects of a task removed from the bundle are deleted.
   - One `router_direct` condition object.
   - Per task: an LLM, an agent and a linear workflow. The primary task's workflow is named after the bundle. For the
     graph shape `plan_draft_write` the task gets the agents of its plan, draft and write stages instead of a single agent.
   - Per task that declares `allowed_tools`, an MCP provider, when `spec.mcp` is set.
   - A team `agent-<bundle>` when `spec.groupTeam` is true.
   - With `spec.delegation`, an orchestrator `<task>-orchestrator` over each task and inline A2A nodes, one per target.

The overall `Ready` condition is true when the whole pipeline passed.

## Fields of `spec`

### Source: `source.oci`

| Field | Meaning |
|---|---|
| `reference` | The artifact, **pinned by a sha256 digest**: `registry/path@sha256:<64 hex>`. A tag is refused at admission. For a release of this repository, take the digest from the corp index (`okf-corp`), see the [README](../README.md). |
| `pullSecretRef` | Optional. Name of a `kubernetes.io/dockerconfigjson` Secret in the same namespace, for a private repository. Without it the pull is anonymous. |

### Verification: `verify`

Set **exactly one** of the two:

| Field | Meaning |
|---|---|
| `publicKeyRef` | **`v1` artifacts only.** `{name, key}` of a Secret holding the PEM public key. The operator checks the `cosign sign-blob` ECDSA signature of the bundle's **content digest**, carried in the manifest annotation `zuno.okf.signature`. With a `v2` artifact the bundle is refused (`a v2 artifact is signed keyless: set spec.verify.keyless`). |
| `keyless` | **Required for `v2` artifacts**, also accepted for a `v1` artifact whose manifest has a cosign signature. The manifest carries a cosign keyless signature (Fulcio certificate and Rekor entry), checked **offline**. Fields: `issuer` (the OIDC issuer of the certificate, for GitHub Actions `https://token.actions.githubusercontent.com`), `subjectRegExp` (a regular expression the workflow identity must match; **anchor it**), `trustedRootRef` (`{name, key}` of a Secret holding a Sigstore `trusted_root.json`). |

### Artifact types

The operator accepts two artifact types and ties the verification mode to the type:

| Artifact type | Layer | Signature | `verify` to use |
|---|---|---|---|
| `application/vnd.zuno.okf.bundle.v2` (what the releases of this repository publish) | `…v2.tar+gzip` | keyless, on the manifest | `keyless` (mandatory) |
| `application/vnd.zuno.okf.bundle.v1` | `…v1.tar+gzip` | `cosign sign-blob` of the content digest | `publicKeyRef`, or `keyless` if the manifest has a cosign signature |

Each OKF document is validated against the schema of its own `okf_version` (v0.2 and v0.3 are embedded in the operator).
The releases of this repository are signed keyless by their `publish.yml` workflow (see the README, "What a release is").
Its identity regular expression is the one in the `cosign verify` command shown there.

### Ceilings: `ceilings`

The ceilings are reviewed in Git with the resource, independently of the bundle content. A bundle may declare less,
never more.

| Field | Meaning |
|---|---|
| `toolCapabilities` | Tool names the tasks may list in `allowed_tools`. |
| `knowledgeDomains` | Knowledge domains the tasks may list in `allowed_knowledge`. |
| `minClassification` | Required, `C1`, `C2` or `C3`. The least restrictive classification the bundle may run at: a bundle declaring a lower level is refused. |
| `maxSteps` | Most reasoning or tool rounds a task may declare in `zuno.limits.max_steps`, 1 to 1000. Unset means 50. |
| `maxTokensPerTurn` | Most tokens one user turn of a task may use over all its model calls. A task declaring more is refused; a task declaring none gets this value. Unset means no ceiling. |
| `delegationTargets` | Targets the bundle may delegate to, as `<agent>/<task>` (up to 64). Empty means none. |

### Entitlement and visibility

| Field | Meaning |
|---|---|
| `entitlement` | `Enforced` (default) refuses a bundle that declares `zuno.access.groups`, because UnifAI cannot hide an agent by group. `GatewayOnly` emits it and relies on the gateways checking the caller's token groups. |
| `groupTeam` | `true` emits a team named `agent-<bundle>` whose members are the bundle's access groups, and puts everything emitted in its workspace, so UnifAI's own visibility restricts the agent to those groups. This satisfies `Enforced`. Exclusive with `teamId` and `teamRef`; the bundle must declare access groups. |
| `owner` | The UnifAI user that owns the emitted objects (default `admin`; set it to a user that exists in your identity provider). |
| `unifaiName` | Name in UnifAI, defaults to `metadata.name`. |
| `teamId`, `teamRef` | Team workspace to use instead of the owner's personal one. `teamRef` names a team resource of the same namespace; the bundle waits until that team is ready. Exclusive with each other. |

### Model, tools and retrieval

| Field | Meaning |
|---|---|
| `llm` | Template of the LLM emitted for every task: `type` (`openai_compatible`), `config` (`model_name`, `base_url`, `forward_user_token`, `timeout_seconds`…), `maxTokens` (1 to 8192, the generation ceiling of every task that declares none; sent as `X-<Ns>-Max-Tokens`, see [Header namespace](#header-namespace-contractnamespace)). The operator adds the agent, task, effective classification and run-id headers to `config.default_headers`. |
| `mcp` | Template of the MCP provider emitted per task that declares `allowed_tools`, with the same agent headers added to `config.additional_headers`. |
| `providers` | Names of shared MCP provider objects attached to tasks that declare `allowed_tools`, sent without the agent headers. |
| `retriever` | Name of the retriever object attached to tasks that declare `allowed_knowledge`. |
| `retrieveFirst` | `true` makes every retriever-backed agent search with the user's message before the model reasons. Only for multiagent images that know that option. |
| `agentConfig` | Extra agent settings merged under every emitted agent (for example `hitl_mode`, `max_rounds`). A bundle's `zuno.limits.max_steps` replaces `max_rounds`, within `ceilings.maxSteps`. |
| `classificationOverrides` | Per-task map to `C1`, `C2` or `C3`. It may only **raise** a task's level. |
| `servePlaceholder` | `true` serves a bundle whose OKF says `zuno.status: placeholder`. By default such a bundle stays pending and emits nothing. |

### Header namespace: `contractNamespace`

Available from the UnifAI release that carries R-555 (after v0.1.70). Pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`. The LLMs,
MCP providers and A2A nodes the bundle emits send `X-<Ns>-Agent`, `X-<Ns>-Task`, `X-<Ns>-Data-Classification`,
`X-<Ns>-Run-Id`, `X-<Ns>-Max-Tokens`, `X-<Ns>-Delegated-By` and `X-<Ns>-Delegation-Depth`. With `contractNamespace: zuno` the
names are exactly `X-Zuno-Agent` and so on. Set the **same** value on the `UnifaiStack` (`spec.contractNamespace`, passed to
multiagent and its worker as `UNIFAI_CONTRACT_NAMESPACE`), which reads `X-<Ns>-Data-Classification` (the floor) and
`X-<Ns>-Max-Tokens`, and exchanges the A2A metadata `<ns>.approval` and `<ns>.classification`.

When it is not set, UnifAI sends and accepts both `unifai` and `zuno` until its 0.2 line, then `unifai` alone. To depend on no
default, set it explicitly on the stack and on every bundle.

### Delegation: `delegation`

Without this block, a bundle that declares `zuno.delegation.targets` is refused (`DelegationUnsupported`). Delegation is
read-only, through the A2A gateway.

| Field | Meaning |
|---|---|
| `gatewayURL` | Required. Base URL of the gateway; a target agent is called at `<gatewayURL>/agents/<agent>`. |
| `maxRounds` | Rounds of the orchestrator per turn, 1 to 50, default 5. |
| `timeoutSeconds` | Seconds a call waits for a target before the remote task is cancelled, 1 to 900. Unset: the server holds the request until the task is done. |
| `approval` | What happens when a target asks for approval before a write: `skip` rejects it (the write does not run), `ask` relays it to the human of the session, `dynamic` relays it only when the session has human approval enabled. |
| `maxApprovals` | How many approval requests the whole session may relay. Past it, requests are refused and the remote task is cancelled. |

Rules that follow:
- A target missing from `ceilings.delegationTargets` makes `WithinCeilings` false (`Widening`).
- Each target must itself be a `Verified` and `Ready` `UnifaiAgentBundle` in the same namespace, otherwise `Valid` is false
  (`DelegationTargetUnresolved`).
- Every task of a delegating agent runs at the **highest classification** of the task and its targets, from its first call.
  A target is never raised by what delegates to it.

## Example

The digest and the repository are placeholders. The example verifies a release of this repository (a `v2` artifact, keyless).
The Secret `sigstore-trusted-root` holds the Sigstore `trusted_root.json` and must exist in the namespace.

```yaml
apiVersion: unifai.startx.fr/v1alpha1
kind: UnifaiAgentBundle
metadata: {name: my-agent}
spec:
  source:
    oci:
      reference: quay.io/zuno/okf-my-agent@sha256:0000000000000000000000000000000000000000000000000000000000000000
  verify:
    keyless:
      issuer: https://token.actions.githubusercontent.com
      subjectRegExp: '^https://github\.com/<owner>/<repo>/\.github/workflows/publish\.yml@refs/tags/v'
      trustedRootRef: {name: sigstore-trusted-root, key: trusted_root.json}
  ceilings:                       # reviewed in Git: the bundle may narrow these, never widen them
    toolCapabilities: [search_confluence, web_search]
    knowledgeDomains: [knowledge.tech]
    minClassification: C1
  entitlement: GatewayOnly
  llm:
    type: openai_compatible
    config:
      model_name: auto
      base_url: http://ai-gateway.example.svc:8080/v1
      forward_user_token: true
  providers: [mcp-gateway]        # attached to tasks that declare allowed_tools
  retriever: knowledge            # attached to tasks that declare allowed_knowledge
  agentConfig: {hitl_mode: skip, max_rounds: 10}
  classificationOverrides:
    write-code: C2                # may only raise the bundle's level
```

For a `v1` artifact signed with a key you hold, replace the `verify` block and add the key Secret:

```yaml
apiVersion: v1
kind: Secret
metadata: {name: okf-signer}
stringData:
  cosign.pub: |
    -----BEGIN PUBLIC KEY-----
    REPLACE-WITH-YOUR-PUBLIC-KEY
    -----END PUBLIC KEY-----
---
# in the UnifaiAgentBundle spec:
  verify:
    publicKeyRef: {name: okf-signer, key: cosign.pub}
```

## Conditions

`kubectl get uab` shows the phase (`Ready`, `Error` or `Pending`), the agent and whether it is verified. The conditions
in `status.conditions` say which step stopped. The reasons below are the ones the operator sets.

| Condition | True reasons | False reasons and the first thing to check |
|---|---|---|
| `Verified` | `SignatureValid` | `SignatureInvalid`: the key or the identity does not match. Check `verify.publicKeyRef` (the right public key), or for keyless the `issuer`, the anchored `subjectRegExp` and the trusted root. |
| `Valid` | `Valid`, `Deprecated` (still served), `PlaceholderNotServed`, `Retired` | `SchemaInvalid` or `Invalid`: the OKF documents break a schema; run the repository's validators on the bundle. `ShapeMissing` or `ShapeNotImplemented`: the graph shape is not declared or has no template in this operator. `EntitlementUnsupported`: access groups with `entitlement: Enforced`; set `groupTeam` or `entitlement: GatewayOnly`. `DelegationUnsupported`: set `spec.delegation`. `DelegationTargetUnresolved`: the target bundle is not Verified and Ready in the namespace. `MissingReason`: a retired agent needs the reason annotation. `Revoked`: see below. `RevocationListUnreadable`: the revocation ConfigMap exists but cannot be parsed; nothing new is admitted until it is fixed. |
| `WithinCeilings` | `WithinCeilings` | `Widening`: the bundle declares a tool, domain, classification, step count, token count or delegation target outside `spec.ceilings`. Review the ceilings in Git, do not widen them to make it pass without review. |
| `Emitted` | `Emitted` | `EmitFailed`: the objects could not be created; read the message. `PlaceholderNotServed`, `Retired`, `Revoked`: nothing is emitted by design. |
| `Ready` | reason is the phase | `Pending`: waiting or retrying (pull, key, a missing target). `Error`: a permanent error, the message says which; nothing changes until the cause is fixed. |

`status` also reports `resolvedDigest` (manifest digest pulled), `bundleDigest` (content digest the signature covers),
`signer` (the certificate subject for keyless), `okfVersion`, `agent`, `primaryTask`, `tasks`, `children` (the emitted
objects) and `unmapped` (OKF content with no UnifAI equivalent: per-task tool allow-lists, which the tool gateway enforces,
`rag.top_k`, UI fields and prompt examples).

## Revocation

An agent can be switched off without a new release. The platform owns a ConfigMap named `unifai-agent-revocations` in
the namespace of the bundles, managed through GitOps. The operator reads it and never writes it. Its key `revoked` holds a
YAML list of entries:

```yaml
revoked:
- {bundle: my-agent, reason: "withdrawn after review 1234", actor: someone}
```

A listed bundle gets `Valid=False` and `Emitted=False` with reason `Revoked`, and its emitted objects are removed. To lift
it, remove the entry. Label the ConfigMap `app.kubernetes.io/part-of=unifai`: the operator watches only labelled
ConfigMaps, so without the label a change waits for the next resync (10 minutes).

Two related states come from the bundle itself (`zuno.status`): `deprecated` keeps serving and says so, `retired` removes
the objects and requires the annotation `unifai.startx.fr/reason`. The annotations `unifai.startx.fr/actor` and
`unifai.startx.fr/reason` are written by the promotion pull request and copied into events and conditions.

## Checking a resource before applying it

The resource is validated at admission, with the message of the rule that failed. To check rendered manifests without a
cluster change, use a server-side dry run: `kubectl apply --dry-run=server -f bundle.yaml`.
