# OKF conformance fixtures

Release-shaped trees that every OKF reader of the platform must parse to the
same result (zuno-demo ADR-0508, WP-51). A reader is any component that reads
agent bundles: mcp-gateway, the admission and stack-configuration tooling in
`zuno-demo`, and later mlops. Each reader keeps its own parser (ADR-0508
clause 4); these fixtures are what keep the parsers from drifting apart.

Each case is a directory:

    cases/<name>/agents/<agent>/agent.okf.md   the bundle under test
    cases/<name>/agents/<agent>/tasks/*.md
    cases/<name>/expected.json                 the expected result per reader

`expected.json` carries `mcp_gateway` and `admission` sections. Both describe a
successful load (`agents`, and a `null` error) or a refusal (an error substring
that must appear in the reader's message, and no agents).

Case prefixes: `valid-` (loads, schema-valid), `security-` (loads, and the
result must stay deny-by-default; schema-invalid on purpose), `invalid-`
(refused with a named error).

Supported `okf_version`: `v0.2` and `v0.3` (zuno-demo ADR-0579 clause 6).

`python3 conformance/test_fixtures.py` checks the fixtures themselves: every
`valid-` case matches the OKF schemas, every `expected.json` is well formed, and
no case is orphaned. The per-reader tests live with the readers.
