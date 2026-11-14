# Security policy

## Reporting a vulnerability

Please do **not** open a public issue, discussion or pull request for a security problem.

Use GitHub's private reporting instead: the **Security** tab of this repository, then **Report a vulnerability**. The
report reaches the maintainers only. If that button is missing, private vulnerability reporting is not enabled yet; in
that case open an issue that says only "security contact requested", without any detail, and a maintainer will reply
with a private channel.

Please include:

- what is affected: a file path, an agent or policy under this repository, and the commit or release tag you looked at;
- how to reproduce it, and what an attacker gains;
- whether you believe it is already exploited, or that a secret is exposed.

## What to expect

This is a demonstration project maintained on a best-effort basis; there is no contractual response time. We aim to
acknowledge a report within five working days, agree on a fix and a disclosure date with you, and credit you in the
fix's notes unless you prefer otherwise.

## Scope

In scope: everything in this repository, including the agent bundles, their prompts and policies, the conformance
checks, and the CI workflows that sign and publish a release.

Out of scope, please report upstream:

- the platform that serves these agents ([zuno-demo](https://github.com/startxfr/zuno-demo)): to its own repository;
- UnifAI and the other products the agents run on: to their vendors;
- third-party container images: to their publishers.

## Supported versions

Fixes land on `devel` first and reach `main` with the next release tag (see [RELEASING.md](RELEASING.md)). Only the
latest release tag and `devel` are supported; older tags are not patched.
