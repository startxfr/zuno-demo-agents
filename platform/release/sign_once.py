#!/usr/bin/env python3
"""Sign (or attest) each published OKF artifact once per signer identity.

Builds are reproducible, so an agent that did not change keeps its digest
from one run to the next. `cosign sign` appends a new layer to the same
`sha256-<digest>.sig` manifest on every run, so a digest published by every
devel and main push accumulated one signature per push (35 on okf-arkos by
release 0.6.1). Consumers read a bounded number of them: unifai-operator
reads at most 32 layers and then refuses the bundle.

This script reads artifact references (`repo@sha256:...`, one per line) on
stdin and, for each one:

1. with --clean-above N, when its signature (or attestation) manifest has
   more than N layers, removes them all (`cosign clean`) before signing.
   Only the release workflow passes it, and it re-signs at once: removing
   signatures from the dev workflow would strip the release signature that
   deployed platforms verify;
2. skips the artifact when it already carries a signature (or an
   attestation of --type) whose certificate identity matches --identity;
3. otherwise signs (or attests) it.

Run from the repository root, in a workflow already logged in to the
registry with cosign and oras:

    jq -r '.corp, .agents[]' refs.json | python3 platform/release/sign_once.py sign \\
        --identity '^https://github\\.com/startxfr/zuno-demo-agents/\\.github/workflows/publish\\.yml@refs/tags/v' \\
        --clean-above 16
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Callable, List, Optional, Sequence

ISSUER = "https://token.actions.githubusercontent.com"

Runner = Callable[[Sequence[str]], subprocess.CompletedProcess]


def run(args: Sequence[str]) -> subprocess.CompletedProcess:
    return subprocess.run(list(args), capture_output=True, text=True)


def suffix_ref(ref: str, suffix: str) -> str:
    """repo@sha256:abc -> repo:sha256-abc.<suffix>, cosign's tag for that digest."""
    repo, _, digest = ref.partition("@")
    if not digest.startswith("sha256:"):
        raise ValueError(f"{ref}: not a digest reference")
    return f"{repo}:{digest.replace(':', '-')}.{suffix}"


def layer_count(ref: str, suffix: str, runner: Runner) -> int:
    result = runner(["oras", "manifest", "fetch", suffix_ref(ref, suffix)])
    if result.returncode != 0:
        return 0  # no signature manifest yet
    return len(json.loads(result.stdout).get("layers", []))


def already_signed(ref: str, mode: str, identity: str, attest_type: Optional[str], runner: Runner) -> bool:
    if mode == "sign":
        args = ["cosign", "verify"]
    else:
        args = ["cosign", "verify-attestation", "--type", attest_type or ""]
    args += ["--certificate-identity-regexp", identity, "--certificate-oidc-issuer", ISSUER, ref]
    return runner(args).returncode == 0


def process(refs: List[str], mode: str, identity: str, clean_above: Optional[int],
            attest_type: Optional[str], predicate: Optional[str], runner: Runner = run) -> List[str]:
    """Sign or attest each ref at most once for `identity`; return a log line per ref."""
    suffix = "sig" if mode == "sign" else "att"
    log = []
    for ref in refs:
        cleaned = False
        if clean_above is not None:
            layers = layer_count(ref, suffix, runner)
            if layers > clean_above:
                kind = "signature" if mode == "sign" else "attestation"
                check(runner(["cosign", "clean", "--type", kind, "--force", ref]), ref)
                log.append(f"{ref}: {layers} {kind} layers (> {clean_above}) removed")
                cleaned = True
        if not cleaned and already_signed(ref, mode, identity, attest_type, runner):
            log.append(f"{ref}: already {'signed' if mode == 'sign' else 'attested'} by this identity, skipped")
            continue
        if mode == "sign":
            check(runner(["cosign", "sign", "--yes", ref]), ref)
            log.append(f"{ref}: signed")
        else:
            check(runner(["cosign", "attest", "--yes", "--type", attest_type or "",
                          "--predicate", predicate or "", ref]), ref)
            log.append(f"{ref}: attested")
    return log


def check(result: subprocess.CompletedProcess, ref: str) -> None:
    if result.returncode != 0:
        raise RuntimeError(f"{ref}: {' '.join(result.args)} failed: {result.stderr.strip()}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=["sign", "attest"])
    parser.add_argument("--identity", required=True, help="certificate identity regexp that counts as signed")
    parser.add_argument("--clean-above", type=int, help="remove all layers first when there are more than this")
    parser.add_argument("--type", dest="attest_type", help="attestation predicate type (attest)")
    parser.add_argument("--predicate", help="attestation predicate file (attest)")
    args = parser.parse_args(argv)
    if args.mode == "attest" and not (args.attest_type and args.predicate):
        parser.error("attest needs --type and --predicate")
    refs = [line.strip() for line in sys.stdin if line.strip()]
    try:
        for line in process(refs, args.mode, args.identity, args.clean_above, args.attest_type, args.predicate):
            print(line)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
