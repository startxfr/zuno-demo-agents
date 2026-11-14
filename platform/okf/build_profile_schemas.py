#!/usr/bin/env python3
"""Generate and freeze the JSON schemas of the Zuno OKF profile 1.0 (zuno-demo ADR-0615 clauses 4 and 7).

Each profile schema is the v0.3 schema of the same document type with three changes:

1. **The upstream envelope.** The Open Knowledge Format 0.2 fields replace the old Zuno envelope:
   - `okf_version: "0.2"`;
   - `resource`, `tags`, `sources[]`, `generated`, `verified[]`, `status`, `stale_after`.

   `provenance`, `verification` and `freshness` are gone. Upstream SPEC:
   https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
2. **`zuno.profile: "1.0"`** is required in every document. Prompts gain a minimal `zuno` block for it.
   Agents and experience clients gain `zuno.maintainer`.
3. **The tool-note `capability`** is a name pattern; `validate_okf_bundle.py` checks it against
   policies/tools/tool-policy.yaml.

Descriptions are written for any consumer: no path or component of a particular platform. The output is
frozen by `SHA256SUMS`. `--check` fails when a profile file differs from what this script generates, or from
its recorded hash. Changing a frozen profile needs a new profile version, never an edit.

Run from the repository root:
    python3 platform/okf/build_profile_schemas.py           # write the files and SHA256SUMS
    python3 platform/okf/build_profile_schemas.py --check   # CI
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
from typing import Dict, List

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "platform" / "okf" / "schema"
SUMS = SCHEMA_DIR / "SHA256SUMS"
PROFILE = "1.0"
UPSTREAM = "0.2"
SPEC = "https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md"
ID_BASE = "https://github.com/startxfr/zuno-demo-agents/blob/main/platform/okf/schema/"

BASES = {
    "agent": "zuno-okf-v0.3.schema.json",
    "task": "zuno-okf-task-v0.3.schema.json",
    "prompt": "zuno-okf-prompt-v0.3.schema.json",
    "tool": "zuno-okf-tool-v0.3.schema.json",
    "rag": "zuno-okf-rag-v0.3.schema.json",
    "policy": "zuno-okf-policy-v0.3.schema.json",
    "skill": "zuno-okf-skill-v0.3.schema.json",
    "experience-client": "zuno-okf-experience-client-v0.3.schema.json",
}
WHERE = {
    "agent": "agents/<name>/agent.okf.md",
    "task": "tasks/<task>.md of an agent or an experience client",
    "prompt": "agents/<name>/prompts/<task>.md (the Markdown body is the prompt text)",
    "tool": "agents/<name>/tools/<capability>.md, a usage note that grants nothing",
    "rag": "agents/<name>/rag/<domain>.md, a note on a knowledge domain that grants nothing",
    "policy": "agents/<name>/policies/<name>.md, a constraint that may only narrow the corp policies",
    "skill": "agents/<name>/skills/<name>.md or policies/skills/<name>.md (corp skill)",
    "experience-client": "experience-clients/<name>/client.okf.md",
}

ISO_INSTANT = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$"
ACTOR = r"^((human|process):[A-Za-z0-9._@/-]+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+)$"
NAME_PATTERN = "^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)*$"

# Text that names a component, path or version of one particular platform. None may appear in a profile schema.
FORBIDDEN = re.compile(r"Agent Runtime|agent-runtime|components/|evaluations/|gitops/|MEMORY\.md|agent-frontend|"
                       r"agent-bff|platform/ai-gateway|docs/agents|\bv0\b|app/graph|knowledge/<domain>|"
                       r"zuno-okf-[a-z-]*v0\.[23]", re.I)

ENVELOPE = {
    "okf_version": {
        "description": f"[OKF] Version of the upstream Open Knowledge Format this document follows (SPEC §12): "
                       f"always the quoted string \"{UPSTREAM}\". Repeated in every document so a reader can "
                       f"dispatch one file at a time (a declared deviation: upstream declares it once, in the "
                       f"bundle-root index.md).",
        "type": "string", "const": UPSTREAM},
    "resource": {
        "description": "[OKF] Canonical URI of this document (SPEC §4): its file on the main branch of the "
                       "repository that publishes it.",
        "type": "string", "pattern": "^https://"},
    "tags": {
        "description": "[OKF] Free classification tags (SPEC §4).",
        "type": "array", "uniqueItems": True,
        "items": {"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]*$"}},
    "sources": {
        "description": "[OKF] What the document was derived from (SPEC §5 provenance). Descriptive, never a grant: "
                       "the tasks' declarations are the authorization surface.",
        "type": "array",
        "items": {
            "type": "object", "additionalProperties": False, "required": ["resource"],
            "properties": {
                "id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]*$"},
                "resource": {"type": "string", "minLength": 1},
                "title": {"type": "string", "minLength": 1},
                "author": {"type": "string", "minLength": 1},
                "usage_count": {"type": "integer", "minimum": 0},
                "last_modified": {"type": "string", "pattern": ISO_INSTANT},
            }}},
    "generated": {
        "description": "[OKF] How the content was produced (SPEC §5 trust): an actor (`human:<id>`, "
                       "`process:<id>` or `<producer>/<version>`) and an instant.",
        "type": "object", "additionalProperties": False, "required": ["by"],
        "properties": {"by": {"type": "string", "pattern": ACTOR},
                       "at": {"type": "string", "pattern": ISO_INSTANT}}},
    "verified": {
        "description": "[OKF] Independent confirmations (SPEC §5 trust). Absent or empty: unverified; machine "
                       "actors only: machine-confirmed; a `human:` actor: human-reviewed. Advisory, never a grant. "
                       "Always a list (a declared deviation: upstream also tolerates a bare mapping).",
        "type": "array",
        "items": {"type": "object", "additionalProperties": False, "required": ["by", "at"],
                  "properties": {"by": {"type": "string", "pattern": ACTOR},
                                 "at": {"type": "string", "pattern": ISO_INSTANT}}}},
    "status": {
        "description": "[OKF] Lifecycle of the document (SPEC §5): absent means stable. For an agent it agrees "
                       "with zuno.status: draft for placeholder, stable for active, deprecated for deprecated or "
                       "retired.",
        "type": "string", "enum": ["draft", "stable", "deprecated"]},
    "stale_after": {
        "description": "[OKF] Instant after which the content should be reviewed again (SPEC §5), with an offset.",
        "type": "string", "pattern": ISO_INSTANT},
}
ZUNO_PROFILE = {
    "description": f"[ZUNO] Version of the Zuno OKF profile this document follows: always the quoted string "
                   f"\"{PROFILE}\" (zuno-demo ADR-0615).",
    "type": "string", "const": PROFILE}
ZUNO_MAINTAINER = {
    "description": "[ZUNO] Who maintains the bundle, shown by consumers.",
    "type": "string", "minLength": 1}

OVERRIDES: Dict[str, Dict[str, str]] = {
    "agent": {
        "/properties/zuno": "[ZUNO] The Zuno extension: what an agent declares beyond the OKF envelope (tasks, "
                            "model, access, display, limits). Unknown keys are refused.",
        "/properties/zuno/properties/status": "Lifecycle state of the agent in this release: `active` is served, "
                                              "`placeholder` is declared but not served, `deprecated` is served "
                                              "and flagged, `retired` is withdrawn.",
        "/properties/zuno/properties/tasks": "Ordered task names, each resolved to tasks/<task>.md in the same bundle.",
        "/properties/zuno/properties/graph_shape": "Name of the workflow shape a consumer runs for this agent (for "
                                                   "example `retrieve_reason_respond` or `plan_draft_write`); the "
                                                   "consumer must know the shape.",
        "/properties/zuno/properties/rag": "Retrieval parameters of the agent.",
        "/properties/zuno/properties/memory": "Conversation history carried into the prompt; "
                                              "`zuno.limits.memory` is the preferred placement.",
        "/properties/zuno/properties/memory/properties/history/properties/token_budget":
            "Approximate token budget (about 4 characters per token) for the running summary plus the "
            "verbatim history.",
        "/properties/zuno/properties/access/properties/groups":
            "Identity groups allowed to use the agent, as they appear in the token's `groups` claim without a "
            "leading slash (for example `agent_tekos`).",
        "/properties/zuno/properties/limits/properties/memory":
            "Conversation history carried into the prompt (the preferred placement of `zuno.memory`).",
        "/properties/zuno/properties/limits/properties/memory/properties/history/properties/token_budget":
            "Approximate token budget (about 4 characters per token) for the running summary plus the "
            "verbatim history.",
        "/properties/zuno/properties/memory/properties/project_context/properties/token_budget":
            "Approximate token budget (about 4 characters per token) for the injected project context, separate "
            "from the history budget so a long briefing never crowds out the conversation.",
        "/properties/zuno/properties/limits/properties/memory/properties/project_context/properties/token_budget":
            "Approximate token budget (about 4 characters per token) for the injected project context, separate "
            "from the history budget so a long briefing never crowds out the conversation.",
    },
    "task": {
        "/properties/zuno/properties/quota_class": "Named quota class of policies/quotas/quota-policy.yaml; "
                                                   "absent means `standard`.",
        "/properties/zuno/properties/project_required": "The task needs a verified project id as session context "
                                                        "before any tool call, retrieval or model call.",
        "/properties/zuno/properties/max_tokens": "Generation ceiling of the task's model call; "
                                                  "`zuno.limits.max_tokens` is the preferred placement.",
        "/properties/zuno/properties/allowed_knowledge": "Knowledge domain ids (`knowledge.<domain>`) of "
                                                         "policies/knowledge/knowledge-policy.yaml the task may "
                                                         "retrieve from; independent of allowed_tools.",
        "/properties/zuno/properties/prompts": "Extra prompt slots of a multi-stage task: slot name to settings. "
                                               "Each slot's text is prompts/<task>--<slot>.md.",
        "/properties/zuno/properties/live_read_tool": "The single entry of allowed_tools that the workflow's live-read "
                                                      "branch invokes. Explicit configuration, never derived from "
                                                      "caller data; omit it when the task never reads live.",
    },
    "rag": {
        "/properties/zuno/properties/domain": "Knowledge domain id (`knowledge.<domain>`) this note documents; at "
                                              "least one task of `used_by_tasks` must allow it.",
        "/properties/zuno/properties/freshness_expectation": "Which operation class of the domain the agent's use "
                                                             "matches. Documentary.",
        "/properties/zuno/properties/top_k_hint": "Suggested per-domain override of the agent's `zuno.rag.top_k`. "
                                                  "Documentary.",
        "/properties/zuno/properties/filters": "Narrowing hints in the domain's own taxonomy. Documentary.",
    },
    "tool": {
        "/properties/zuno/properties/live_read": "Mirrors a task's `zuno.live_read_tool`. Documentary.",
    },
    "experience-client": {
        "/properties/zuno/properties/tasks": "Task names the client sends; each is tasks/<task>.md of the client, "
                                             "of which only allowed_tools is read.",
    },
}


def _at(node: dict, pointer: str) -> dict:
    for part in pointer.strip("/").split("/"):
        node = node[part]
    return node


def _forbidden(node, path: str, out: List[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("description", "title") and isinstance(v, str) and FORBIDDEN.search(v):
                out.append(f"{path}/{k}: {FORBIDDEN.search(v).group(0)!r}")
            _forbidden(v, f"{path}/{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _forbidden(v, f"{path}[{i}]", out)


def profile_schema(typ: str) -> dict:
    base = json.loads((SCHEMA_DIR / BASES[typ]).read_text(encoding="utf-8"))
    out: dict = {
        "$schema": base["$schema"],
        "$id": f"{ID_BASE}zuno-okf-profile-{PROFILE}-{typ}.schema.json",
        "title": f"Zuno OKF profile {PROFILE}: {typ} document",
        "description": f"Frontmatter of {WHERE[typ]} in a Zuno OKF profile {PROFILE} bundle: the upstream Open "
                       f"Knowledge Format {UPSTREAM} envelope ({SPEC}) plus the namespaced `zuno` block. Frozen "
                       f"(zuno-demo ADR-0615): a change needs a new profile version.",
        "type": "object",
        "additionalProperties": False,
    }
    props = copy.deepcopy(base["properties"])
    for gone in ("okf_version", "provenance", "verification", "freshness", "sources"):
        props.pop(gone, None)
    typ_prop = props.pop("type")
    typ_prop["description"] = f"[OKF] Document kind (SPEC §4): always \"{typ}\" in this schema."
    title = props.pop("title", {"type": "string", "minLength": 1})
    title["description"] = "[OKF] Human-readable name (SPEC §4)."
    description = props.pop("description", {"type": "string", "minLength": 1})
    description["description"] = "[OKF] One-line summary of the document (SPEC §4)."
    zuno = props.pop("zuno", None)
    if zuno is None:  # prompt: the profile key needs a zuno block
        zuno = {"type": "object", "additionalProperties": False, "required": [], "properties": {}}
    zuno.setdefault("description", "[ZUNO] The Zuno extension of this document. Unknown keys are refused.")
    zuno["properties"] = {"profile": ZUNO_PROFILE, **zuno["properties"]}
    if typ in ("agent", "experience-client"):
        zuno["properties"]["maintainer"] = ZUNO_MAINTAINER
    zuno["required"] = ["profile"] + [r for r in zuno.get("required", []) if r != "profile"]
    if typ == "tool":
        zuno["properties"]["capability"] = {
            "description": "Tool or capability name of policies/tools/tool-policy.yaml this note documents; the "
                           "vocabulary is checked by validate_okf_bundle.py, not by this schema.",
            "type": "string", "pattern": NAME_PATTERN}
    out["properties"] = {"okf_version": ENVELOPE["okf_version"], "type": typ_prop, "title": title,
                         "description": description,
                         **{k: copy.deepcopy(v) for k, v in ENVELOPE.items() if k != "okf_version"},
                         "zuno": zuno}
    required = ["okf_version", "type", "title"]
    if "description" in base.get("required", []):
        required.append("description")
    out["required"] = required + ["resource", "zuno"]
    for pointer, text in OVERRIDES.get(typ, {}).items():
        _at(out, pointer)["description"] = text
    problems: List[str] = []
    _forbidden(out, typ, problems)
    if problems:
        raise SystemExit("platform-specific text left in the profile schema:\n  " + "\n  ".join(problems))
    return out


def index_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"{ID_BASE}zuno-okf-profile-{PROFILE}-index.schema.json",
        "title": f"Zuno OKF profile {PROFILE}: bundle index frontmatter",
        "description": f"The only frontmatter a bundle-root index.md may carry (upstream SPEC §8, §12: {SPEC}): the "
                       f"OKF version of the bundle. The body lists every published document with a link and a "
                       f"one-line description; platform/okf/generate_index.py writes it.",
        "type": "object",
        "additionalProperties": False,
        "required": ["okf_version"],
        "properties": {"okf_version": {"description": "[OKF] Always the quoted string \"0.2\".",
                                       "type": "string", "const": UPSTREAM}},
    }


def render() -> Dict[str, str]:
    files = {f"zuno-okf-profile-{PROFILE}-{t}.schema.json": profile_schema(t) for t in BASES}
    files[f"zuno-okf-profile-{PROFILE}-index.schema.json"] = index_schema()
    return {name: json.dumps(doc, indent=2, ensure_ascii=False) + "\n" for name, doc in files.items()}


def sums(rendered: Dict[str, str]) -> str:
    return "".join(f"{hashlib.sha256(text.encode('utf-8')).hexdigest()}  {name}\n"
                   for name, text in sorted(rendered.items()))


def main(argv: List[str]) -> int:
    rendered = render()
    if "--check" in argv:
        problems = []
        for name, text in rendered.items():
            path = SCHEMA_DIR / name
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                problems.append(f"{name} differs from what build_profile_schemas.py generates")
        recorded = SUMS.read_text(encoding="utf-8") if SUMS.is_file() else ""
        for line in recorded.splitlines():
            digest, name = line.split(maxsplit=1)
            path = SCHEMA_DIR / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                problems.append(f"{name} does not match its frozen hash in SHA256SUMS")
        if recorded != sums(rendered):
            problems.append("SHA256SUMS does not list exactly the generated profile files")
        if problems:
            print("\n".join(f"  ✗ {p}" for p in problems))
            print(f"\nRESULT: FAIL - profile {PROFILE} is frozen: a change needs a new profile version (ADR-0615).")
            return 1
        print(f"\nRESULT: PASS - the {len(rendered)} profile {PROFILE} schemas match their generator and SHA256SUMS.")
        return 0
    for name, text in rendered.items():
        (SCHEMA_DIR / name).write_text(text, encoding="utf-8")
    SUMS.write_text(sums(rendered), encoding="utf-8")
    print(f"Wrote {len(rendered)} profile {PROFILE} schemas and {SUMS.relative_to(REPO_ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
