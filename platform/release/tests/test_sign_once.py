"""Tests for platform/release/sign_once.py, with a fake cosign/oras runner.

Run from the repository root:
    python3 -m unittest discover -s platform/release/tests
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import sign_once  # noqa: E402

REF = "quay.io/zuno/okf-arkos@sha256:" + "a" * 64
RELEASE = r"^https://github\.com/startxfr/zuno-demo-agents/\.github/workflows/publish\.yml@refs/tags/v"


class FakeRunner:
    """Answers oras/cosign like a registry holding `layers` layers, signed by us when `signed`."""

    def __init__(self, layers: int = 0, signed: bool = False):
        self.layers = layers
        self.signed = signed
        self.calls = []

    def __call__(self, args):
        args = list(args)
        self.calls.append(args)
        ok, out = 0, ""
        if args[:3] == ["oras", "manifest", "fetch"]:
            if self.layers:
                out = json.dumps({"layers": [{}] * self.layers})
            else:
                ok = 1
        elif args[:2] in (["cosign", "verify"], ["cosign", "verify-attestation"]):
            ok = 0 if self.signed else 1
        elif args[:2] == ["cosign", "clean"]:
            self.layers, self.signed = 0, False
        elif args[:2] in (["cosign", "sign"], ["cosign", "attest"]):
            self.layers += 1
            self.signed = True
        return subprocess.CompletedProcess(args, ok, out, "")

    def verbs(self):
        return [" ".join(c[:2]) for c in self.calls]


class SignOnceTest(unittest.TestCase):
    def test_suffix_ref(self):
        self.assertEqual(sign_once.suffix_ref(REF, "sig"), "quay.io/zuno/okf-arkos:sha256-" + "a" * 64 + ".sig")
        with self.assertRaises(ValueError):
            sign_once.suffix_ref("quay.io/zuno/okf-arkos:v1", "sig")

    def test_unsigned_artifact_is_signed(self):
        runner = FakeRunner()
        log = sign_once.process([REF], "sign", RELEASE, None, None, None, runner)
        self.assertEqual(runner.verbs(), ["cosign verify", "cosign sign"])
        self.assertTrue(log[0].endswith("signed"))

    def test_artifact_already_signed_by_the_identity_is_skipped(self):
        runner = FakeRunner(layers=3, signed=True)
        log = sign_once.process([REF], "sign", RELEASE, 16, None, None, runner)
        self.assertNotIn("cosign sign", runner.verbs())
        self.assertNotIn("cosign clean", runner.verbs())
        self.assertIn("skipped", log[0])
        # the identity is passed to cosign verify with the GitHub issuer
        verify = next(c for c in runner.calls if c[:2] == ["cosign", "verify"])
        self.assertIn(RELEASE, verify)
        self.assertIn(sign_once.ISSUER, verify)

    def test_too_many_layers_are_removed_then_signed_once(self):
        runner = FakeRunner(layers=35, signed=True)
        sign_once.process([REF], "sign", RELEASE, 16, None, None, runner)
        self.assertEqual(runner.verbs(), ["oras manifest", "cosign clean", "cosign sign"])
        self.assertEqual(runner.layers, 1)
        clean = next(c for c in runner.calls if c[:2] == ["cosign", "clean"])
        self.assertEqual(clean[2:4], ["--type", "signature"])

    def test_without_clean_above_nothing_is_ever_removed(self):
        """The dev workflow must never strip the release signature."""
        runner = FakeRunner(layers=35, signed=False)
        sign_once.process([REF], "sign", "publish-dev", None, None, None, runner)
        self.assertNotIn("cosign clean", runner.verbs())
        self.assertNotIn("oras manifest", runner.verbs())

    def test_attest_reads_the_att_manifest_and_skips_when_present(self):
        runner = FakeRunner(layers=2, signed=True)
        log = sign_once.process([REF], "attest", RELEASE, 16, "https://x/y", "p.json", runner)
        fetch = next(c for c in runner.calls if c[:2] == ["oras", "manifest"])
        self.assertTrue(fetch[3].endswith(".att"))
        verify = next(c for c in runner.calls if c[:2] == ["cosign", "verify-attestation"])
        self.assertEqual(verify[2:4], ["--type", "https://x/y"])
        self.assertIn("skipped", log[0])

    def test_failed_signature_stops_the_run(self):
        def failing(args):
            args = list(args)
            code = 1 if args[:2] in (["cosign", "verify"], ["cosign", "sign"]) else 0
            return subprocess.CompletedProcess(args, code, "", "boom")
        with self.assertRaises(RuntimeError):
            sign_once.process([REF], "sign", RELEASE, None, None, None, failing)


if __name__ == "__main__":
    unittest.main()
