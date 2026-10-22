#!/usr/bin/env python3
"""Validate every OKF document's frontmatter against its JSON schema.

Mirrors what unifai-operator does before it emits anything
(fork/unifai-operator/internal/okf/schema.go `ValidateSchemas`): every `.md`
file of a bundle whose frontmatter declares a known OKF `type` is checked
against the schema of that type, and must declare the schema's
`okf_version`. Files without frontmatter (README notes) are not OKF
documents and are skipped, as are `tests/` trees, which never enter a
published layer (ADR-0577 clause 1).

A bundle that fails here would be refused by the operator with
`Valid=False`; catching it in CI keeps that from being discovered on a
cluster.

Run from the repository root:
    python3 platform/okf/validate_okf_schema.py            # every agent
    python3 platform/okf/validate_okf_schema.py agents/tekos
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Dict, List, Optional

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / "agents"
SCHEMA_DIR = REPO_ROOT / "platform" / "okf" / "schema"

# OKF document `type` -> schema file, per supported okf_version.
SCHEMAS: Dict[str, Dict[str, str]] = {
    "v0.2": {
        "agent": "zuno-okf-v0.2.schema.json",
        "task": "zuno-okf-task-v0.2.schema.json",
        "prompt": "zuno-okf-prompt-v0.2.schema.json",
        "tool": "zuno-okf-tool-v0.2.schema.json",
        "rag": "zuno-okf-rag-v0.2.schema.json",
        "policy": "zuno-okf-policy-v0.2.schema.json",
    },
}
SKIPPED_DIRS = {"tests", "__pycache__"}


def frontmatter(path: pathlib.Path) -> Optional[dict]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    return yaml.safe_load(text[4:end]) or {}


def validators() -> Dict[str, Dict[str, Draft202012Validator]]:
    out: Dict[str, Dict[str, Draft202012Validator]] = {}
    for version, files in SCHEMAS.items():
        out[version] = {
            typ: Draft202012Validator(json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8")))
            for typ, name in files.items()
        }
    return out


def check_bundle(bundle_dir: pathlib.Path, schemas: Dict[str, Dict[str, Draft202012Validator]]) -> List[str]:
    problems: List[str] = []
    for path in sorted(bundle_dir.rglob("*.md")):
        rel = path.relative_to(bundle_dir)
        if SKIPPED_DIRS.intersection(rel.parts):
            continue
        label = path.relative_to(REPO_ROOT).as_posix()
        try:
            doc = frontmatter(path)
        except yaml.YAMLError as exc:
            problems.append(f"{label}: frontmatter is not valid YAML: {exc}")
            continue
        if not isinstance(doc, dict) or "type" not in doc:
            continue
        version = doc.get("okf_version")
        if version not in schemas:
            problems.append(f"{label}: okf_version {version!r} is not one of {sorted(schemas)}")
            continue
        validator = schemas[version].get(doc["type"])
        if validator is None:
            continue
        for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
            where = "/".join(str(p) for p in error.path) or "(root)"
            problems.append(f"{label}: {where}: {error.message}")
    return problems


def main(argv: List[str]) -> int:
    bundles = [REPO_ROOT / a for a in argv] if argv else sorted(
        p.parent for p in AGENTS_DIR.glob("*/agent.okf.md"))
    schemas = validators()
    problems: List[str] = []
    for bundle in bundles:
        problems += check_bundle(bundle, schemas)
    if problems:
        print(f"{len(problems)} schema issue(s):")
        for p in problems:
            print(f"  ✗ {p}")
        print("\nRESULT: FAIL - unifai-operator would refuse these bundles (Valid=False).")
        return 1
    print(f"Validated the OKF documents of {len(bundles)} bundle(s) against {SCHEMA_DIR.relative_to(REPO_ROOT)}.")
    print("\nRESULT: PASS - every OKF document matches its schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
