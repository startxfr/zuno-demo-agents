#!/usr/bin/env python3
"""Render the UnifaiAgentBundle objects of a dev run (run-dev workflow).

The dev cluster owns everything platform-specific about running an agent
(owner, LLM, MCP provider, team): it publishes it as a bundle spec template,
the `okf-dev-bundle-template` ConfigMap, key `spec.yaml`. This repository
only adds what it knows: which artifact to pull (from the corp index of the
run), how to verify it (keyless, by this repository's workflow identity), and
the ceilings, which for a dev run are exactly what the bundle declares - the
run tests that the operator accepts and emits the agent, not a policy review.

Run from the repository root:
    render_dev_bundles.py --index okf-index.json --template spec.yaml \\
        --namespace okf-dev --run-id <sha12> --identity-regexp '<regexp>'
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys
from typing import Dict, List

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / "agents"
OIDC_ISSUER = "https://token.actions.githubusercontent.com"
TRUSTED_ROOT_REF = {"name": "sigstore-trusted-root", "key": "trusted_root.json"}


def frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    return (yaml.safe_load(text[4:end]) or {}) if text.startswith("---\n") and end > 0 else {}


def ceilings(agent: str) -> Dict[str, object]:
    agent_dir = AGENTS_DIR / agent
    zuno = frontmatter(agent_dir / "agent.okf.md").get("zuno") or {}
    tools, domains = set(), set()
    for task in zuno.get("tasks") or []:
        tz = frontmatter(agent_dir / "tasks" / f"{task}.md").get("zuno") or {}
        tools.update(tz.get("allowed_tools") or [])
        domains.update(tz.get("allowed_knowledge") or [])
    return {
        "toolCapabilities": sorted(tools),
        "knowledgeDomains": sorted(domains),
        "minClassification": (zuno.get("model") or {}).get("preferred_classification", "C1"),
    }


def render(index: dict, template: dict, namespace: str, run_id: str, identity: str) -> List[dict]:
    objects = []
    for entry in index["agents"]:
        spec = copy.deepcopy(template)
        spec["source"] = {"oci": {"reference": entry["reference"]}}
        spec["verify"] = {"keyless": {"issuer": OIDC_ISSUER, "subjectRegExp": identity,
                                      "trustedRootRef": TRUSTED_ROOT_REF}}
        spec["ceilings"] = ceilings(entry["name"])
        spec.setdefault("entitlement", "GatewayOnly")
        objects.append({
            "apiVersion": "unifai.startx.fr/v1alpha1",
            "kind": "UnifaiAgentBundle",
            "metadata": {
                "name": f"okf-dev-{entry['name']}",
                "namespace": namespace,
                "labels": {"zuno.startx.fr/okf-dev-run": run_id},
            },
            "spec": spec,
        })
    return objects


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--index", type=pathlib.Path, required=True)
    parser.add_argument("--template", type=pathlib.Path, required=True)
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--identity-regexp", required=True)
    args = parser.parse_args(argv)
    index = json.loads(args.index.read_text(encoding="utf-8"))
    template = yaml.safe_load(args.template.read_text(encoding="utf-8")) or {}
    print(yaml.safe_dump_all(render(index, template, args.namespace, args.run_id, args.identity_regexp),
                             sort_keys=False), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
