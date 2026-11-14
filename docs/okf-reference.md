# OKF field reference: the Zuno OKF profile 1.0

Every file of an agent bundle is a Markdown document whose YAML frontmatter is checked against a JSON schema in
`platform/okf/schema/`. This page lists every field a bundle author writes, where it is valid, what bounds it and
what the platform does with it. The schemas are the source of truth: a field that no schema knows is not documented
here, and every schema refuses unknown fields (`additionalProperties: false`).

- **The base format** is the upstream [Open Knowledge Format 0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
  (Google Cloud, Apache-2.0). Upstream defines the envelope: `type`, `title`, `description`, `resource`, `tags`,
  `sources`, `generated`, `verified`, `status`, `stale_after`. It also defines the bundle-root `index.md`.
- **The Zuno profile 1.0** adds the namespaced `zuno` block and the constraints of this page (zuno-demo
  [ADR-0615](https://github.com/startxfr/zuno-demo/blob/devel/docs/adr/0615-align-the-zuno-okf-profile-with-upstream-okf-0-2-and-freeze-it-as-profile-1-0.md)).
  The profile schemas are frozen (`platform/okf/schema/SHA256SUMS`): a change needs a new profile version.
- **Legacy documents** (`okf_version: v0.2` or `v0.3`) are read until 2026-12-01, then refused. See
  [Legacy versions](#legacy-versions).
- Fields marked **required** are required by the schema. The others are optional.
- Check your files with these, in order:
  1. `python3 platform/okf/validate_okf_schema.py`;
  2. `python3 platform/okf/check_narrowing.py` (the narrowing rules below);
  3. `python3 platform/supply-chain/validate_okf_bundle.py` (structure, references and the profile rules);
  4. `python3 platform/okf/generate_index.py --check`.

## Versions and dispatch

Every document carries two version keys:
- **`okf_version: "0.2"`** (always quoted: an unquoted `0.2` is a YAML number) is the upstream version;
- **`zuno.profile: "1.0"`** is the Zuno profile.

Every reader of this format applies the same table, one document at a time:

| `okf_version` | `zuno.profile` | Result |
|---|---|---|
| `"v0.2"` or `"v0.3"` | absent | Legacy document, legacy schema (until 2026-12-01) |
| `"0.2"` | `"1.0"` | Profile 1.0 schema of the document's `type` |
| `"0.2"` | absent or another value | Refused: `unsupported zuno.profile` |
| anything else | - | Refused: `unsupported okf_version` |

A reader skips a document without frontmatter, or with a `type` it does not know. The narrowing rules apply from
legacy v0.3 up, profile 1.0 included: readers compare levels, never version strings.

## Layout of an agent bundle

```
agents/<name>/
  index.md              (no type)          generated listing of the bundle (upstream §8); never edit it
  agent.okf.md          type: agent        the agent
  tasks/<task>.md       type: task         one per entry of zuno.tasks
  prompts/<task>.md     type: prompt       the system prompt of the task (the body is the prompt); one per task
  prompts/<task>--<slot>.md                an extra prompt slot of a multi-stage task
  tools/<capability>.md type: tool         usage note for a tool a task declares
  rag/<domain>.md       type: rag          note on a knowledge domain a task reads
  policies/<name>.md    type: policy       a narrowing-only addendum
  skills/<name>.md      type: skill        reusable instructions
  VERSION                                  the agent's version (not published)
  tests/                                   contract tests (not published)
```

The list of files that travel in the published artifact is in [bundle-files.md](bundle-files.md).

## The envelope (every document)

| Field | Type | Meaning |
|---|---|---|
| `okf_version` | `"0.2"`, **required** | The upstream version (see [Versions and dispatch](#versions-and-dispatch)). |
| `type` | **required** | Document kind: `agent`, `task`, `prompt`, `tool`, `rag`, `policy`, `skill`, `experience-client`. |
| `title` | string, **required** | Human-readable name. |
| `description` | string, **required** for an agent and an experience client | One line on what the document is; `index.md` shows it. Give one to every task too. |
| `resource` | `https://...`, **required** | The canonical URI of the document: its file on the main branch, `https://github.com/startxfr/zuno-demo-agents/blob/main/<path>`. `validate_okf_bundle.py` checks it matches the path. |
| `tags` | list of `^[a-z0-9][a-z0-9._-]*$` | Free classification tags. |
| `sources` | list of `{id, resource, title, author, usage_count, last_modified}`, `resource` **required** | What the document draws on. Descriptive provenance, never a grant: the tasks' declarations are the authorization. A logical source has a `urn:zuno:` resource, for example `urn:zuno:knowledge:tech`. |
| `generated` | `{by, at}`, `by` **required** | How the content was produced: `by` is an actor (`human:<id>`, `process:<id>` or `<producer>/<version>`). |
| `verified` | list of `{by, at}`, both **required** | Independent confirmations. Absent or empty: unverified; machine actors only: machine-confirmed; a `human:` actor: human-reviewed. Advisory. Always a list. |
| `status` | `draft`, `stable`, `deprecated` | Upstream lifecycle; absent means stable. On an agent it must agree with `zuno.status`: `draft` for placeholder, `stable` (or absent) for active, `deprecated` for deprecated or retired. |
| `stale_after` | ISO 8601 instant with an offset, quoted | When the content should be reviewed again. The checks warn once it is past; they never fail on it. |
| `zuno` | object, **required** | The Zuno block. Every document's `zuno` has `profile: "1.0"` (**required**); a prompt's `zuno` holds only that. |

All timestamps are ISO 8601 with an offset, quoted so YAML keeps them as strings: `"2026-11-14T10:00:00Z"`.

### From the legacy envelope

| Legacy field | Profile 1.0 |
|---|---|
| `okf_version: v0.2` / `v0.3` | `okf_version: "0.2"` and `zuno.profile: "1.0"` |
| `provenance.repository` | `resource` |
| `provenance.maintainer` | `zuno.maintainer` |
| `verification.status` | `verified: [{by, at}]` (absent: unverified) |
| `freshness.last_reviewed` | `verified[].at`, and `stale_after` for the next review |
| `sources: [strings]` | `sources: [{id, resource, title}]` |

## Agent: `agent.okf.md` (`type: agent`)

The envelope above, with `description` required. The body is free Markdown for readers, plus the authorization
matrix that `generate_authorization_matrix.py` writes between its markers. The matrix restates the enforced
intersection for review; nothing reads it at runtime.

### Zuno extension: `zuno`

| Field | Type | Meaning |
|---|---|---|
| `profile` | `"1.0"`, **required** | The Zuno profile. |
| `maintainer` | string | Who maintains the bundle; consumers display it. |
| `name` | `^[a-z][a-z0-9-]*$`, **required** | Stable agent identifier. Matches the `agents/<name>` directory and the entitlement group `agent_<name>`. |
| `status` | `active`, `placeholder`, `deprecated`, `retired`, **required** | Lifecycle state. `active`: really served. `placeholder`: declared but not served. `deprecated`: still served, flagged. `retired`: no longer served. |
| `tasks` | list of task names, **required**, at least 1 | Ordered tasks, each resolved to `tasks/<task>.md`. |
| `graph_shape` | `^[a-z][a-z0-9_]*$` | The workflow shape the agent executes, for example `retrieve_reason_respond` or `plan_draft_write`. The consumer must have a template for it. |
| `primary_task` | `^[a-z][a-z0-9-]*$` | The entry of `tasks` that the chat route, and a delegation call that names no task, reach. |
| `rag.top_k` | integer 1 to 50 | Number of retrieval results per turn. |
| `memory.history` | `{enabled, max_turns, token_budget}` | Conversation history carried into the prompt: `max_turns` 1 to 50 recent turn pairs kept verbatim, `token_budget` 100 to 32000 (about 4 characters per token) for summary plus history. Older turns are folded into a running summary. |
| `memory.project_context` | `{enabled, token_budget}` | The standing context of the project a conversation belongs to, injected as a delimited background block, never as instructions. |
| `model` | **required** | `preferred_classification` (**required**: `C1`, `C2` or `C3`, the highest data classification the agent is routed for; `C3` means local models only), `notes` (free text), `local_only` (boolean, default false: a hard restriction to local models whatever the classification). |
| `access.groups` | list of strings matching `^agent_[a-z0-9_]+$`, **required**, at least 1 | Identity groups allowed to use the agent (the entitlement group, for example `agent_tekos`, as it appears in the JWT `groups` claim without a leading slash). |
| `ui` | **required** | `displayName`, `tileDescription`, `color` (a `#rrggbb` hex or a CSS color keyword) and `icon` (a short keyword `^[a-z0-9][a-z0-9-]{0,39}$`), all required: how a portal renders the agent's tile. |
| `models` | `{preferred, forbidden}` | Model preferences by **role** (the roles of `policies/models/model-catalog.yaml`), never by model name. |
| `guardrails` | `{mode, categories}` | `mode` is `observe` or `block`; `categories` is a subset of the corp categories. |
| `limits` | see [Limits](#limits) | Per-agent bounds. |
| `delegation` | `{targets: [{agent, task}]}` | See [Delegation](#delegation). |

### Limits

`zuno.limits` is valid on an agent and on a task. A task takes `max_tokens`, `max_concurrent_requests`, `max_steps`, `max_tokens_per_turn` and `quota_class`; `memory` and `delegation` are agent level only. Each value is at most the corp ceiling
in `policies/limits/limits-policy.yaml`.

| Field | Type | Meaning |
|---|---|---|
| `max_tokens` | integer 1 to 8192 | Generation ceiling per model call. |
| `max_concurrent_requests` | integer at least 1 | Concurrent requests one user may have open on the agent. |
| `max_steps` | integer at least 1 | Most reasoning or tool rounds of one turn; the agent then answers from what it gathered. |
| `max_tokens_per_turn` | integer at least 1 | Most model tokens one user turn may use over all its calls; the turn ends cleanly when it is reached. |
| `quota_class` | `^[a-z][a-z0-9-]*$` | A class of `policies/quotas/quota-policy.yaml`. |
| `memory` | same shape as `zuno.memory` | Alias placement for the history settings. Agent level only. |
| `delegation.max_depth` | integer at least 1 | Most delegation hops starting from this agent; at most the corp `max_delegation_depth`. Agent level only. |

The older spellings `zuno.max_tokens` (task) and `zuno.memory` (agent) remain valid as aliases.

### Delegation

`zuno.delegation.targets` lists the agents this agent may call over A2A, each as `{agent, task}`. Absent means none; a
target is never inferred. A target must name **another agent of the same release** and one of its tasks, never the
agent itself. A legacy v0.2 bundle declaring delegation is a finding. Delegation is read-only unless the corp
`delegation.write_allowed` list names the target in `policies/limits/limits-policy.yaml`. How a platform consumes
the declaration is up to the consumer; see the [UnifaiAgentBundle page](unifaiagentbundle.md) for one.

## Task: `tasks/<task>.md` (`type: task`)

The envelope, with a one-line `description` (shown by `index.md`). All Zuno fields are under `zuno` (**required**),
with `profile: "1.0"`.

| Field | Type | Meaning |
|---|---|---|
| `allowed_tools` | list of strings, **required** | The tool names (capabilities) the task may invoke, from the corp tool vocabulary `policies/tools/tool-policy.yaml`. The effective authorization is the intersection with the corp policy and the caller's groups. |
| `allowed_knowledge` | list of strings | Knowledge domain ids (`knowledge.<domain>`) the task may retrieve from. Independent of `allowed_tools`. |
| `live_read_tool` | string | The single entry of `allowed_tools` that the live-read branch of the workflow invokes. |
| `prompts` | map of slot name to `{classification_ceiling}` | Extra prompt slots for multi-stage graph shapes; the slot text lives in `prompts/<task>--<slot>.md`. `classification_ceiling` is `C1`, `C2` or `C3`. |
| `prompt_examples` | list of strings | Editable example prompts a frontend can offer for the task. |
| `project_required` | boolean, default false | The task demands a verified project id as session context before any tool call or model action. |
| `quota_class` | `^[a-z][a-z0-9-]*$` | Named quota class; absent means `standard`. |
| `max_tokens` | integer 1 to 8192 | Generation ceiling of the task's model call, sent per request as the `X-<Ns>-Max-Tokens` header (`X-Zuno-Max-Tokens` for the `zuno` namespace). |
| `skills` | list of strings | Skills whose instructions are appended to the task's system prompt, in order: `<name>` is `agents/<agent>/skills/<name>.md`, `corp/<name>` is a corp skill. |
| `models` | `{preferred, forbidden}` | Model role preferences for this task. |
| `limits` | `{max_tokens, max_concurrent_requests, max_steps, max_tokens_per_turn, quota_class}` | Per-task bounds, see [Limits](#limits). |

## Prompt: `prompts/<task>.md` (`type: prompt`)

The envelope; `zuno` holds only `profile: "1.0"`. The Markdown body, everything after the frontmatter, is the literal
prompt text: the system prompt of the task of the same name. **Every task has one** in profile 1.0. A consumer that
finds no prompt for a task falls back to its own default (the agent description and the task body, for UnifAI), so
the prompt is what keeps the behaviour explicit and reviewable.

## Tool note: `tools/<capability>.md` (`type: tool`)

Documentation of how the agent uses one tool. `okf_version`, `type: tool`, `title` and `zuno` are required.

| Field | Type | Meaning |
|---|---|---|
| `capability` | tool name, **required** | Any tool or capability name of `policies/tools/tool-policy.yaml` that a task of the bundle declares. `validate_okf_bundle.py` checks the vocabulary. |
| `used_by_tasks` | list of task names, **required**, at least 1 | **Every** task that declares the capability in `allowed_tools`, checked in both directions. Documents a fact; it grants nothing. |
| `live_read` | boolean | Mirrors a task's `live_read_tool`. Documentary. |
| `usage_notes` | string | How the tasks use the tool: inputs, outputs, when it is chosen. |
| `known_limitations` | list of strings | Rate limits, partial coverage, demo-only behaviour. |

## RAG note: `rag/<domain>.md` (`type: rag`)

Documentation of a knowledge domain the agent reads. `okf_version`, `type: rag`, `title` and `zuno` are required.

| Field | Type | Meaning |
|---|---|---|
| `domain` | `^knowledge\.[a-z][a-z0-9_-]*$`, **required** | The domain documented; the agent must be able to reach it. |
| `used_by_tasks` | list of task names, **required**, at least 1 | **Every** task that declares the domain in `allowed_knowledge`, checked in both directions. |
| `top_k_hint` | integer 1 to 50 | Suggested per-domain override of `zuno.rag.top_k`. Documentary. |
| `filters` | `{technology, source_classes}` | Narrowing hints in the domain's own taxonomy, both lists of strings. Documentary. |
| `freshness_expectation` | `semantic-read` or `current-state-read` | Which operation class of the domain the agent's use matches. |
| `rationale` | string | Why the agent needs the domain. |

## Policy addendum: `policies/<name>.md` (`type: policy`)

A constraint an agent adds to the corp policies. It can only narrow. `okf_version`, `type: policy`, `title` and `zuno`
are required.

| Field | Type | Meaning |
|---|---|---|
| `narrows_platform_policy` | `true`, **required** | An explicit acknowledgment that the addendum only restricts. |
| `constraint_type` | enum, **required** | `human_review_required`, `quota_override`, `data_handling_addendum`, `escalation_requirement` or `other`. |
| `applies_to` | **required** | `tasks` (**required**, at least 1), and optionally `tools` and `knowledge` to scope it to some of the tasks' tools or domains. |
| `rationale` | string, **required** | Why the constraint exists, for whoever would relax it. |
| `enforcement` | **required** | `mechanism` (**required**: `manual-process`, `external-system` or `none-yet`) and `notes`. Says honestly whether anything enforces it. |

## Skill: `skills/<name>.md` (`type: skill`)

Reusable instructions shared by tasks. `okf_version`, `type: skill`, `title` and `zuno` are required; `description` is
optional. In `zuno`: `name` (**required**), `allowed_tools` and `allowed_knowledge`. The body is the instruction text,
appended to the system prompt of every task that lists the skill. A skill may need a subset of its task's tools and
knowledge, never more. A corp skill is `policies/skills/<name>.md`, referenced as `corp/<name>`, and is embedded in
each artifact that uses it.

## Experience client: `experience-clients/<name>/client.okf.md`

A user interface over the governed chain (for example a chat UI) that calls the gateway for a signed-in user under a
logical agent name. `okf_version`, `type: experience-client`, `title`, `description` and `zuno` are required;
the envelope is as for an agent. In `zuno`: `profile`, `maintainer`, `name` (**required**, must not be the name of an agent),
`tasks` (**required**, task files under `experience-clients/<name>/tasks/`, of which only `allowed_tools` is read),
`classification` (`C1`, `C2` or `C3`, descriptive) and `access.groups` (**required**, business groups such as `sales` or `consultant`, without a leading slash, not an `agent_*` group; the tool policy still narrows each tool to its own allowed groups).

## Narrowing: a bundle may only narrow the corp policies

`python3 platform/okf/check_narrowing.py` refuses any declaration that would widen what the corp policies allow, and
names the clause it exceeds. The rules apply to profile 1.0 and legacy v0.3 bundles:

- **skills:** every skill a task lists exists, is a `type: skill` document and needs no tool or domain the task does not allow.
- **models:** the roles exist in the model catalog; a preferred role has a model eligible for the agent's classification;
  no role is both preferred and forbidden.
- **guardrails:** the mode is at least the corp minimum for the agent's classification; the categories are corp categories.
- **limits:** each value is at most the corp ceiling; `quota_class` is a class of the quota policy; `delegation.max_depth`
  is at most `max_delegation_depth`.
- **delegation:** targets name another agent of the release and one of its tasks.

The corp policies themselves are under `policies/` (`tools`, `knowledge`, `quotas`, `limits`, `guardrails`, `models`,
`model-routing`). Tool and knowledge references are checked by `platform/supply-chain/validate_okf_bundle.py`.

## Deviations from upstream OKF

The profile meets every MUST of upstream §11 for published files. Where it differs from upstream, it does so on purpose:

| Upstream | Profile 1.0 | Why |
|---|---|---|
| `okf_version` is declared once, in the bundle-root `index.md` (§12) | Also repeated in every document | Readers such as the gateways and the operator read one file at a time and must know its version |
| A consumer must not reject unknown keys or types (§11) | Unknown keys are refused, in the envelope and in `zuno` | A bundle is an authorization contract: a misspelled key must fail, not be ignored |
| A consumer tries an unknown version on a best-effort basis (§12) | An unknown version is refused, with a named error | Same reason; the conformance cases pin the messages |
| `verified` may be a bare mapping (§11) | Always a list | One shape for every reader |
| `README.md` is not reserved (§3) | Each directory may keep a `README.md` without frontmatter | READMEs are never published, so the published artifact still conforms |

## Legacy versions

Documents written with `okf_version: v0.2` or `v0.3` (the profile before 1.0) are read until 2026-12-01 and refused
after it. Their envelope used `provenance`, `verification` and `freshness`; their `zuno` fields are those of this page.
v0.3 added `models`, `guardrails`, `limits`, `delegation` and skills to v0.2, and profile 1.0 keeps them all. To move a
bundle, see [the lifecycle page](bundle-lifecycle.md#moving-a-legacy-bundle-to-profile-10).

## Examples

A minimal agent and task that satisfy the schemas (the prompt, the index and `VERSION` are omitted):

```yaml
---
okf_version: "0.2"
type: agent
title: Example
description: Answers questions about the example product.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/example/agent.okf.md
stale_after: "2027-05-15T00:00:00Z"
zuno:
  profile: "1.0"
  maintainer: Example team
  name: example
  status: active
  graph_shape: retrieve_reason_respond
  primary_task: answer
  tasks: [answer]
  model:
    preferred_classification: C1
  access:
    groups: [agent_example]
  ui:
    displayName: Example
    tileDescription: Questions about the example product
    color: "#0066cc"
    icon: code
  limits:
    max_steps: 10
---
```

```yaml
---
okf_version: "0.2"
type: task
title: Answer a question
description: Answer a question about the example product from its documentation.
resource: https://github.com/startxfr/zuno-demo-agents/blob/main/agents/example/tasks/answer.md
zuno:
  profile: "1.0"
  allowed_tools: [web_search]
  allowed_knowledge: [knowledge.tech]
  max_tokens: 1024
---
```
