# OKF field reference

Every file of an agent bundle is a Markdown document whose YAML frontmatter is checked against a JSON schema in
`platform/okf/schema/`. This page lists every field a bundle author writes, where it is valid, what bounds it and
what the platform does with it. The schemas are the source of truth: a field that no schema knows is not documented
here, and every schema refuses unknown fields (`additionalProperties: false`).

- Versions: **v0.3** is current; **v0.2** stays valid. A document names its version in `okf_version`
  (`v0.2` or `v0.3`) and is checked against the schema of that version.
- Fields marked **required** are required by the schema. The others are optional.
- Fields under a `zuno:` block are the Zuno extension. The fields outside it (`okf_version`, `type`, `title`,
  `description`, `provenance`, `verification`, `freshness`, `sources`) are the OKF core envelope.
- Check your files with `python3 platform/okf/validate_okf_schema.py`, then `python3 platform/okf/check_narrowing.py`
  (the narrowing rules below), then `python3 platform/supply-chain/validate_okf_bundle.py`.

## Layout of an agent bundle

```
agents/<name>/
  agent.okf.md          type: agent        the agent
  tasks/<task>.md       type: task         one per entry of zuno.tasks
  prompts/<task>.md     type: prompt       the prompt text of the task (the body is the prompt)
  prompts/<task>--<slot>.md                an extra prompt slot of a multi-stage task
  tools/<capability>.md type: tool         usage note for a tool a task declares
  rag/<domain>.md       type: rag          note on a knowledge domain a task reads
  policies/<name>.md    type: policy       a narrowing-only addendum
  skills/<name>.md      type: skill        reusable instructions (v0.3)
  tests/                                   contract tests, never published
```

The list of files that travel in the published artifact is in the release tooling (`platform/release/okf_release.py`),
not on this page.

## Agent: `agent.okf.md` (`type: agent`)

### OKF core

| Field | Type | Meaning |
|---|---|---|
| `okf_version` | `v0.3` (or `v0.2`), **required** | Envelope version. |
| `type` | `agent`, **required** | Document kind. |
| `title` | string, **required** | Human-readable agent name. |
| `description` | string, **required** | One or two sentences on what the agent does, independent of any UI. |
| `provenance` | `{maintainer, repository}` | Who maintains the bundle, for audit. |
| `verification` | `{status}` | `unverified`, `reviewed` or `verified`. |
| `freshness` | `{last_reviewed}` | Last-reviewed date, so a consumer can judge staleness. |
| `sources` | list of strings | External knowledge sources worth naming at bundle level. The operative authorization is the per-task declarations, not this list. |

### Zuno extension: `zuno`

| Field | Type | Meaning |
|---|---|---|
| `name` | `^[a-z][a-z0-9-]*$`, **required** | Stable agent identifier. Matches the `agents/<name>` directory and the entitlement group `agent_<name>`. |
| `status` | `active`, `placeholder`, `deprecated`, `retired`, **required** | Lifecycle state. `active`: really served. `placeholder`: declared but not served (a placeholder declares exactly one task). `deprecated`: still served, flagged. `retired`: no longer served. |
| `tasks` | list of task names, **required**, at least 1 | Ordered tasks, each resolved to `tasks/<task>.md`. |
| `graph_shape` | `^[a-z][a-z0-9_]*$` | The workflow shape the agent executes, for example `retrieve_reason_respond` or `plan_draft_write`. The consumer must have a template for it. |
| `primary_task` | `^[a-z][a-z0-9-]*$` | The entry of `tasks` that the chat route, and a delegation call that names no task, reach. |
| `rag.top_k` | integer 1 to 50 | Number of retrieval results per turn. |
| `memory.history` | `{enabled, max_turns, token_budget}` | Conversation history carried into the prompt: `max_turns` 1 to 50 recent turn pairs kept verbatim, `token_budget` 100 to 32000 (about 4 characters per token) for summary plus history. Older turns are folded into a running summary. |
| `memory.project_context` | `{enabled, token_budget}` | The standing context of the project a conversation belongs to, injected as a delimited background block, never as instructions. |
| `model` | **required** | `preferred_classification` (**required**: `C1`, `C2` or `C3`, the highest data classification the agent is routed for; `C3` means local models only), `notes` (free text), `local_only` (boolean, default false: a hard restriction to local models whatever the classification). |
| `access.groups` | list of strings matching `^agent_[a-z0-9_]+$`, **required**, at least 1 | Identity groups allowed to use the agent (the entitlement group, for example `agent_tekos`, as it appears in the JWT `groups` claim without a leading slash). |
| `ui` | **required** | `displayName`, `tileDescription`, `color` (a `#rrggbb` hex or a CSS color keyword) and `icon` (a short keyword `^[a-z0-9][a-z0-9-]{0,39}$`), all required: how a portal renders the agent's tile. |
| `models` (v0.3) | `{preferred, forbidden}` | Model preferences by **role** (the roles of `policies/models/model-catalog.yaml`), never by model name. |
| `guardrails` (v0.3) | `{mode, categories}` | `mode` is `observe` or `block`; `categories` is a subset of the corp categories. |
| `limits` (v0.3) | see [Limits](#limits-v03) | Per-agent bounds. |
| `delegation` (v0.3) | `{targets: [{agent, task}]}` | See [Delegation](#delegation-v03). |

### Limits (v0.3)

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

### Delegation (v0.3)

`zuno.delegation.targets` lists the agents this agent may call over A2A, each as `{agent, task}`. Absent means none; a
target is never inferred. A target must name **another agent of the same release** and one of its tasks, never the
agent itself. A v0.2 bundle declaring delegation is a finding. Delegation is read-only unless the corp
`delegation.write_allowed` list names the target in `policies/limits/limits-policy.yaml`. How a platform consumes
the declaration is up to the consumer; see the [UnifaiAgentBundle page](unifaiagentbundle.md) for one.

## Task: `tasks/<task>.md` (`type: task`)

Core fields: `okf_version` (**required**), `type: task` (**required**), `title` (**required**). All Zuno fields are under
`zuno` (**required**).

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
| `skills` (v0.3) | list of strings | Skills whose instructions are appended to the task's system prompt, in order: `<name>` is `agents/<agent>/skills/<name>.md`, `corp/<name>` is a corp skill. |
| `models` (v0.3) | `{preferred, forbidden}` | Model role preferences for this task. |
| `limits` (v0.3) | `{max_tokens, max_concurrent_requests, max_steps, max_tokens_per_turn, quota_class}` | Per-task bounds, see [Limits](#limits-v03). |

## Prompt: `prompts/<task>.md` (`type: prompt`)

`okf_version`, `type: prompt` and `title` are required. There are no Zuno fields. The Markdown body, everything after the
frontmatter, is the literal prompt text, normally the system prompt of the task of the same name.

## Tool note: `tools/<capability>.md` (`type: tool`)

Documentation of how the agent uses one tool. `okf_version`, `type: tool`, `title` and `zuno` are required.

| Field | Type | Meaning |
|---|---|---|
| `capability` | enum, **required** | The capability documented: `search_confluence`, `list_drive_files`, `read_gmail`, `web_search`, `send_technical_report_email`, `confluence.page.read`, `confluence.page.search`, `drive.document.create`, `drive.document.update`, `salesforce.opportunity.read`, `salesforce.opportunity.create`, `salesforce.opportunity.update`, `git.repository.read`, `git.repository.list`, `git.repository.private.read`, `git.repository.private.list`, `git.file.write`, `git.repository.create`. |
| `used_by_tasks` | list of task names, **required**, at least 1 | Tasks that declare the capability in `allowed_tools`. Documents a fact; it grants nothing. |
| `live_read` | boolean | Mirrors a task's `live_read_tool`. Documentary. |
| `usage_notes` | string | How the tasks use the tool: inputs, outputs, when it is chosen. |
| `known_limitations` | list of strings | Rate limits, partial coverage, demo-only behaviour. |

## RAG note: `rag/<domain>.md` (`type: rag`)

Documentation of a knowledge domain the agent reads. `okf_version`, `type: rag`, `title` and `zuno` are required.

| Field | Type | Meaning |
|---|---|---|
| `domain` | `^knowledge\.[a-z][a-z0-9_-]*$`, **required** | The domain documented; the agent must be able to reach it. |
| `used_by_tasks` | list of task names, **required**, at least 1 | Tasks that declare the domain in `allowed_knowledge`. |
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

## Skill: `skills/<name>.md` (v0.3, `type: skill`)

Reusable instructions shared by tasks. `okf_version`, `type: skill`, `title` and `zuno` are required; `description` is
optional. In `zuno`: `name` (**required**), `allowed_tools` and `allowed_knowledge`. The body is the instruction text,
appended to the system prompt of every task that lists the skill. A skill may need a subset of its task's tools and
knowledge, never more. A corp skill is `policies/skills/<name>.md`, referenced as `corp/<name>`, and is embedded in
each artifact that uses it.

## Experience client: `experience-clients/<name>/client.okf.md` (v0.3)

A user interface over the governed chain (for example a chat UI) that calls the gateway for a signed-in user under a
logical agent name. `okf_version`, `type: experience-client`, `title`, `description` and `zuno` are required;
`provenance` and `freshness` are as for an agent. In `zuno`: `name` (**required**, must not be the name of an agent),
`tasks` (**required**, task files under `experience-clients/<name>/tasks/`, of which only `allowed_tools` is read),
`classification` (`C1`, `C2` or `C3`, descriptive) and `access.groups` (**required**, business groups such as `sales` or `consultant`, without a leading slash, not an `agent_*` group; the tool policy still narrows each tool to its own allowed groups).

## Narrowing: a bundle may only narrow the corp policies

`python3 platform/okf/check_narrowing.py` refuses any v0.3 declaration that would widen what the corp policies allow, and
names the clause it exceeds:

- **skills:** every skill a task lists exists, is a `type: skill` document and needs no tool or domain the task does not allow.
- **models:** the roles exist in the model catalog; a preferred role has a model eligible for the agent's classification;
  no role is both preferred and forbidden.
- **guardrails:** the mode is at least the corp minimum for the agent's classification; the categories are corp categories.
- **limits:** each value is at most the corp ceiling; `quota_class` is a class of the quota policy; `delegation.max_depth`
  is at most `max_delegation_depth`.
- **delegation:** targets name another agent of the release and one of its tasks.

The corp policies themselves are under `policies/` (`tools`, `knowledge`, `quotas`, `limits`, `guardrails`, `models`,
`model-routing`). Tool and knowledge references are checked by `platform/supply-chain/validate_okf_bundle.py`.

## From v0.2 to v0.3

A v0.2 bundle stays valid and passes the narrowing check trivially. v0.3 adds:

- on the agent: `models`, `guardrails`, `limits` (with `memory` and `delegation.max_depth`) and `delegation`;
- on the task: `skills`, `models` and `limits`;
- the `skill` and `experience-client` document types.

A consumer reads the version of each document. Check the consumer's documentation for which fields it applies: a field
that a consumer does not map has no runtime effect there, and the corp policies stay the authority.

## Examples

A minimal agent and task that satisfy the schemas (the surrounding files, such as the prompt, are omitted):

```yaml
---
okf_version: v0.3
type: agent
title: Example
description: Answers questions about the example product.
zuno:
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
okf_version: v0.3
type: task
title: Answer a question
zuno:
  allowed_tools: [web_search]
  allowed_knowledge: [knowledge.tech]
  max_tokens: 1024
---
```
