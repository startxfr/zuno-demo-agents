#!/usr/bin/env python3
"""Scaffold a new agent bundle in the Zuno OKF profile 1.0 (zuno-demo ADR-0615).

Writes only the agent's own files, under agents/<name>/:
- agent.okf.md (status `placeholder`, upstream `status: draft`);
- the primary task;
- its prompt;
- a README;
- VERSION 0.1.0.

It then generates the authorization matrix and the bundle index. Nothing is written for any platform: a platform
that consumes the release configures itself from it.

Every tool and knowledge domain must already exist in the corp policies
(policies/tools/tool-policy.yaml, policies/knowledge/knowledge-policy.yaml). The scaffold refuses an unknown one:
adding a capability is a corp-policy change, reviewed on its own.

Usage, from the repository root:

    python3 platform/templates/agent/scaffold_agent.py \\
        --name naveo --title Naveo \\
        --description "Onboarding assistant for new team members." \\
        --primary-task answer-onboarding-question \\
        --primary-task-title "Answer an onboarding question" \\
        --knowledge knowledge.tech --tool web_search \\
        --classification C1 --color "#5C6BC0" --icon compass \\
        --tile-description "New-hire onboarding Q&A, for consultants."

Then review the files, write the prompt properly, run the checks of docs/add-an-agent.md, and set
`zuno.status: active` (and drop `status: draft`) when the agent is ready to be served.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from typing import List

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
RESOURCE_BASE = "https://github.com/startxfr/zuno-demo-agents/blob/main/"
NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
STALE_AFTER = '"2027-05-15T00:00:00Z"'


def corp_names() -> tuple:
    tools = yaml.safe_load((REPO_ROOT / "policies/tools/tool-policy.yaml").read_text()) or {}
    names = {e[k] for e in tools.get("tools", []) for k in ("tool", "capability") if k in e}
    knowledge = yaml.safe_load((REPO_ROOT / "policies/knowledge/knowledge-policy.yaml").read_text()) or {}
    return names, set((knowledge.get("domains") or {}).keys())


def yaml_list(items: List[str], indent: int) -> str:
    pad = " " * indent
    return "\n".join(f"{pad}- {i}" for i in items) if items else f"{pad}[]"


def render(args: argparse.Namespace) -> dict:
    n, task = args.name, args.primary_task
    rel = f"agents/{n}"
    group = args.entitlement_group or f"agent_{n.replace('-', '_')}"
    live = f"\n  live_read_tool: {args.live_read_tool}" if args.live_read_tool else ""
    files = {}
    files["agent.okf.md"] = f"""---
okf_version: "0.2"
type: agent
title: {args.title}
description: {args.description}
resource: {RESOURCE_BASE}{rel}/agent.okf.md
status: draft
stale_after: {STALE_AFTER}
zuno:
  profile: "1.0"
  maintainer: {args.maintainer}
  name: {n}
  status: placeholder
  graph_shape: {args.graph_shape}
  primary_task: {task}
  tasks:
    - {task}
  model:
    preferred_classification: {args.classification}
  access:
    groups:
      - {group}
  ui:
    displayName: {args.title}
    tileDescription: {args.tile_description}
    color: "{args.color}"
    icon: {args.icon}
---

# {args.title}

{args.description}

The agent is a `placeholder`: declared, not served. Set `zuno.status: active` and remove `status: draft` when it is
ready.
"""
    files[f"tasks/{task}.md"] = f"""---
okf_version: "0.2"
type: task
title: {args.primary_task_title}
description: {args.primary_task_title}.
resource: {RESOURCE_BASE}{rel}/tasks/{task}.md
stale_after: {STALE_AFTER}
zuno:
  profile: "1.0"
  allowed_tools:
{yaml_list(args.tool, 4)}{live}
  allowed_knowledge:
{yaml_list(args.knowledge, 4)}
---

# {args.primary_task_title}

What the task does, what it reads and which tool it calls when. Keep it factual: the frontmatter above is what the
platform enforces.
"""
    files[f"prompts/{task}.md"] = f"""---
okf_version: "0.2"
type: prompt
title: {args.title} system prompt - {task}
resource: {RESOURCE_BASE}{rel}/prompts/{task}.md
stale_after: {STALE_AFTER}
zuno:
  profile: "1.0"
---

You are {args.title}. {args.description}

Answer from the retrieved context and the results of your tools. Cite your sources concisely. If the context does not
ground an answer, say so rather than guessing.
"""
    files["README.md"] = f"""# {args.title}

{args.description}

- Status: placeholder (declared, not served).
- Primary task: `{task}`.

Files: `agent.okf.md` (the agent), `tasks/` and `prompts/` (one of each per task), `index.md` (generated, do not
edit), `VERSION`. See [the field reference](../../docs/okf-reference.md) and [add an agent](../../docs/add-an-agent.md).
"""
    files["VERSION"] = "0.1.0\n"
    return files


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Scaffold an agent bundle (Zuno OKF profile 1.0)")
    parser.add_argument("--name", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True, help="one line")
    parser.add_argument("--primary-task", required=True)
    parser.add_argument("--primary-task-title", required=True)
    parser.add_argument("--knowledge", action="append", default=[], help="knowledge.* domain of the corp policy")
    parser.add_argument("--tool", action="append", default=[], help="tool name of the corp tool policy")
    parser.add_argument("--live-read-tool", default=None)
    parser.add_argument("--entitlement-group", default=None, help="default: agent_<name>")
    parser.add_argument("--classification", default="C1", choices=["C1", "C2", "C3"])
    parser.add_argument("--graph-shape", default="retrieve_reason_respond")
    parser.add_argument("--color", default="#0066CC")
    parser.add_argument("--icon", default="code")
    parser.add_argument("--tile-description", required=True)
    parser.add_argument("--maintainer", default="Zuno Demo architecture team")
    args = parser.parse_args(argv)

    problems = []
    if not NAME_RE.match(args.name) or not NAME_RE.match(args.primary_task):
        problems.append("--name and --primary-task must match ^[a-z][a-z0-9-]*$")
    tools, domains = corp_names()
    problems += [f"unknown tool {t!r} (not in policies/tools/tool-policy.yaml)" for t in args.tool if t not in tools]
    problems += [f"unknown knowledge domain {k!r}" for k in args.knowledge if k not in domains]
    if args.live_read_tool and args.live_read_tool not in args.tool:
        problems.append("--live-read-tool must be one of --tool")
    target = REPO_ROOT / "agents" / args.name
    if target.exists():
        problems.append(f"{target.relative_to(REPO_ROOT)} already exists")
    if problems:
        print("\n".join(f"  ✗ {p}" for p in problems))
        return 2

    for rel, text in render(args).items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    for cmd in (["platform/okf/generate_authorization_matrix.py", args.name], ["platform/okf/generate_index.py"]):
        subprocess.run([sys.executable, *cmd], cwd=REPO_ROOT, check=True, capture_output=True)
    print(f"Wrote {target.relative_to(REPO_ROOT)}/. Next: review it, then run the checks of docs/add-an-agent.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
