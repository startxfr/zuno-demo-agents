# Changelog

Written by the release chain (`.github/workflows/release.yml`) on `stable`; never edit it on `devel` or `main`.

## v0.6.1 - 2026-10-25

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.4.1

Changes:

- feat(tekos): add a Drive prompt example to find-relevant-docs; release 0.6.1 (773c3e5)
- feat(tekos): list Drive files when finding docs; add the agent_tekos_preview group (db03eb6)

## v0.5.0 - 2026-10-24

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.3.0

Changes:

- release: bump VERSION to 0.5.0 (standard token ceilings raised, evaluation quota class) (69f7f96)
- feat(policy): raise the standard token ceilings; add an evaluation quota class (a3690d7)

## v0.4.1 - 2026-10-24

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.3.0

Changes:

- release: bump VERSION to 0.4.1 (display shapes for icon and color in OKF v0.3) (96eb240)
- test(conformance): the v0.3 delegation case states its ui block (5052524)
- feat(conformance): display block shapes (icon, color) match what unifai-operator accepts (0743db7)

## v0.4.0 - 2026-10-24

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.3.0

Changes:

- release: bump VERSION to 0.4.0 (delegation fields, tool access, Tekos on OKF v0.3) (2b99ae5)
- docs: bundles may move to OKF v0.3; the consumers read it (2ab460d)
- feat(tekos): move the rag, tool and policy notes to OKF v0.3 (a5bbaea)
- feat(tekos): move the bundle to OKF v0.3 (tekos 0.3.0) (04423d7)
- test: complete the v0.3 content notes of the note-version test (f15dd27)
- fix(validate): accept v0.2 and v0.3 content notes in a bundle (1875ca7)
- feat(policy): declare read or write on every tool of the corp tool policy (3d69956)
- feat(okf): optional delegation fields in OKF v0.3 and their conformance cases (51b9e92)

## v0.3.1 - 2026-10-24

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.2.0

Changes:

- release: bump VERSION to 0.3.1 (conformance cases in the corp artifact) (a9d9472)
- feat(release): carry the OKF conformance cases in the corp artifact (33fcdcf)
- feat(conformance): OKF conformance fixtures for the platform readers (1bad85a)

## v0.3.0 - 2026-10-23

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.2.0

Changes:

- feat(tekos): sign every answer with "— Tekos" (release 0.3.0) (3405775)
- docs: the source branch of the extraction is now archived (d9df6b2)

## v0.2.0 - 2026-10-23

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.1.0

Changes:

- feat(release): embed referenced corp skills in the agent artifact (8a26fc2)
- feat(okf): OKF v0.3 schemas, corp ceilings and the narrowing rule (5d51969)

## v0.1.1 - 2026-10-22

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.1.0

Changes:

- fix(release): push the release tag alone, v0.1.1 (cf02ea6)

## v0.1.0 - 2026-10-22

Agents:

- `advantage` 0.1.0
- `arkos` 0.1.0
- `cognos` 0.1.0
- `comage` 0.1.0
- `finage` 0.1.0
- `naveo` 0.1.0
- `soursage` 0.1.0
- `tekos` 0.1.0

Changes:

- ci(release): read the App ID from a secret or a variable (b4f0e6c)
- ci: first dev publication (e93bd99)
- ci: trigger CI now that Actions are enabled (ff77dbf)
- ci: trigger the first CI run (6de7ba2)
- ci: allow running CI by hand (7d149d6)
- chore: add CODEOWNERS (1391aab)
- docs: README, RELEASING and license (5ef9911)
- ci: devel/main/stable branch model and release chain (c7d3eb6)
- feat(release): versioned OKF releases on an OCI registry (9d7d427)
- chore: make the repository self-contained (bc059c0)
- feat(wp-150/adr-0564): publish signed OKF bundles as OCI artifacts for unifai-operator (4208175)
- vault: sync zuno-platform-signer.pub with live Transit key (version 1, created 2026-08-24T13:11:44.806340175Z) (8c8a59d)
- policy(lightspeed): grant ocp-ai-ops read access to Confluence + RAG tools (1791caf)
- feat(aap-mcp): add AAP Controller job link + last log lines to audit tools (fd9fc52)
- fix(aap-mcp): make cluster_audit launch-and-return, not block for minutes (0def225)
- fix(mcp-gateway): give front-door tools real descriptions (ADR-0524 ext.) (97c5b32)
- feat(day3): parallel-by-default stresstest, generalized quota/limit exhaustion proofs (ADR-0555/WP-142) (6ce5d08)
- fix(lightspeed): switch to gpt-oss-20b, add technical-docs RAG + AAP audit tools (ADR-0524 ext.) (7f4922f)
- vault: sync zuno-platform-signer.pub with live Transit key (version 1, created 2026-09-06T17:50:44.980301959Z) (b3d41b0)
- vault: sync zuno-platform-signer.pub with live Transit key (version 1, created 2026-09-06T15:07:16.632266382Z) (9dd3965)
- WP-137 step 4: regenerate Arkos's authorization matrix for DAT's classification-tiered routing (d853074)
- WP-137 step 2: add per-task classification-scoped local-only override, apply it to Arkos DAT (b47ce77)
- WP-137 step 1: make Arkos DAT's baseline classification project-derived, scope reflect_node to follow it (c380614)
- ADR-0544: bound every model call at both ends (2749add)
- arkos: replace two estimated findings with live measurements (0b89cdc)
- docs: repair 60 relative ADR links and guard them, correct two model-fleet descriptions (d794737)
- model-roles: declare the fleet's architectural roles and enforce them (f462358)
- WP-112: widen the narration trigger; close two of the three tekos findings (8d03ae3)
- guardrails: WP-120 the NeMo server demands config.yaml, not config.yml (b40833a)
- WP-112: apply the Arkos-precedent prompt fix, and repair a silently-failing drift check (531cf2d)
- guardrails: WP-120 move the policy out of the image into NeMo rails config (800cbc4)
- agents/arkos: tell the model to actually call the diagram tool (17f55d2)
- okf: regenerate stale deployment snapshots (ADR-0503) (edbae86)
- quota: raise standard class 24h token budgets (6x undersized) (2deb29e)
- docs(finage): drop stale reference to deterministic SXA queries (c800731)
- fix(adr-0206): reclassify knowledge.sxa-legacy from C3 to C2 (2b45a51)
- ADR-0326/WP-31/33/35/36: retroactive gate catch-up, close the four-agent generalization (b15d5ff)
- ADR-0531/WP-096: qwen3.5-9b fleet default, extend OVH reasoning to Tekos/Comage (7f175aa)
- ADR-0304/ADR-0305/WP-40: run the live benchmark+report loop, close both ADRs (8bc226c)
- WP-090/ADR-0528: telemetry confirmed live, tool-policy decided, legend fixed (3e75d5f)
- agent-frontend: reframe the composer, and give the slash menu real OKF content (6435dc0)
- WP-090: quota and telemetry key on the Zuno project id, not Salesforce (508c2ec)
- WP-088 Part A: the project entity, its RBAC, and the context it carries (7fdf940)
- WP-087 Part D: route Comage/Tekos to the -wesh variant, meter it, regen OKF (1765422)
- WP-074: mcp-aap server exposing AAP audits to Tekos and Arkos (a720498)
- ADR-0524/WP-085: drop the OKF bundle, authorize /mcp per end user (c360e58)
- ADR-0524/WP-085: implement the OpenShift Lightspeed integration (repo side) (9f036f1)
- ADR-0516: close out the status, add evidence, retire the Lucidchart claims (69f9b22)
- ADR-0219: retarget the evaluation probes that relied on sxa.* and sales-db (c272ad3)
- ADR-0219: remove the sxa.* capabilities and retire knowledge.sxa (c032495)
- Regenerate authorization matrices and reconcile operator samples (ADR-0521 fallout) (ec8b8c2)
- ADR-0218: remove the Aramis adapter for real, defer Salesforce to v0.7 (7813a24)
- WP-076/ADR-0521: qwen MaaS provider entry (local-maas) + adapter guard + cost rows (016c1ec)
- ADR-0521/WP-076 step 4: enable MaaS transport for gpt-oss-20b (qwen deferred) (ce91dad)
- supply-chain: relocate zuno-platform-signer.pub to agents/ (2012079)
- ADR-0518: modernize local models - Qwen3.6-27B chat, Qwen3-Embedding-0.6B, Qwen3.5-9B training (53af81a)
- Restrict photorealistic image generation to Comage marketing visuals; make diagram generation a default baseline (0a0a18a)
- Wire real git-forge tool-calling into Arkos and Tekos (34e9be5)
- Add ADR-0516: generate_diagram, self-hosted Mermaid rendering alongside SDXL (35f1bb4)
- WP-069/WP-070 (part 2): the actual mechanism changes (cedefd2)
- WP-33 follow-up: flip comage zuno.status to active (0b2ce12)
- WP-067: ingest a weekly, already-anonymized SXA corpus as a new RAG domain (a0e8065)
- WP-55: implement project-bound tasks with Salesforce-verified context (ADR-0512) (b1cca6a)
- Disable Drive on arkos's tasks - no google-workspace MCP server exists (0ba01e6)
- WP-061: implement per-conversation tabs, one browser tab per agent (ADR-0515) (98ada9e)
- WP-11: flip arkos zuno.status to active (628d7c1)
- WP-6 (comment/memory compaction): compact dated comments in ansible/, components/*, evaluations/, policies/, Makefile (6383403)
- WP-10: update arkos README + scenarios.yaml for the two new tasks (d6c6b9f)
- WP-9: fill arkos's tests/{contract,tasks,prompts} with real ADR-0504 suites (aacf2e3)
- WP-8: regenerate arkos's authorization matrix for the two new tasks (0b051cf)
- WP-7: ADR-0514 + arkos workshop-presentation task, generalizing plan_draft_write (5a80a6d)
- WP-6: arkos structure-demo task + early-exit demo_node (dd295eb)
- WP-5: generated Available models rollup, fleet-wide (9ca713a)
- WP-4: formalize reflect_node's C2 ceiling as a declarative prompt slot (9df4f85)
- WP-3: fix generator's strict: blindness (ADR-0417 + ADR-0419) (243c553)
- WP-2: tekos general tasks prefer OVH ahead of openai/gemini/anthropic (44028cd)
- WP-1: preferred:/fallback: schema, backward-compatible with prefer: (efa05d8)
- WP-8b: regenerate remaining OKF matrices for mistral-codestral's fleet-wide fallback visibility (8f1f542)
- WP-8: regenerate OKF authorization matrices for arkos/tekos (045763f)
- WP-6: tekos shared coding node (data-driven, no-op for other agents) (7d1d4de)
- WP-5: arkos write-code task + early-exit coding node (e305d19)
- WP-4: policy entries for arkos/tekos write-code preferences (96bef78)
- agents: WP-46 corrective - tests/README.md states a blocking rule, not a description (d496480)
- WP-6: ADR-0416 + regenerate all OKF authorization matrices (5e9589e)
- WP-5: finage - enforce genuine local-only, unconditionally (05c4865)
- WP-4: arkos - reflect_node prefers gpt-oss-120b via a scoped C2 ceiling (d1d3ab0)
- WP-3: comage - register gpt-oss-120b as an eligible provider (OKF only) (91e0c00)
- WP-2: cognos prefers gpt-oss-120b for C1/C2 reflection, local-only at C3 (6360780)
- Add stable-diffusion-xl image generation via OVHcloud AI Endpoints (ADR-0415) (493af87)
- WP-060: implement conversation history in agent prompts (ADR-0215) (777cd9c)
- WP-059: wire Tekos and Arkos to git-forge with a public/private split (ADR-0121) (9a71192)
- WP-058: git-forge multi-provider GitHub/GitLab MCP server (ADR-0120) (1c26adb)
- okf: give rag/, tools/ and policies/ bundle directories a real schema (185a06b)
- okf: surface per-task model routing in the generated authorization matrix (a72dfcb)
- ajout d'une reponse type pour l'agent tekos (13d660f)
- okf: WP-54 Part A - quota policy file, schema, lint, matrix column (6d4b248)
- okf: WP-46 - agent tests/ target structure (content deferred) (8ea25c8)
- okf: WP-45 - real deployment/ content for the five skeleton agents (c34e87a)
- okf: WP-44 Part B - authorization matrices for remaining six agents (6c2ee91)
- okf: WP-44 Part A - authorization matrix generator + Tekos/Naveo (934b542)
- agents: WP-43 maturity alignment - stages, PROMOTION.md, READMEs (064651f)
- ADR-0412: gpt-oss-20b second local model + per-(agent,task) preferences (edfe44f)
- ADR-0349 part 2: persona restructure, ocp-* cluster access, ArgoCD policy (78e6136)
- ADR-0349 part 1: soursage and cognos placeholder agents (70f3e11)
- Propagate the 2026-08-15 ADR renumbering across every cross-reference (0b27dce)
- WP-41b: Naveo, the sixth agent, generated via the template (ADR-0306) (c41cb0f)
- WP-41a: self-service agent onboarding template (ADR-0307) (321520b)
- WP-40: automated benchmarking and routing optimization (ADR-0305, ADR-0304) (5b38844)
- WP-39: dynamic LoRA adapter selection (ADR-0303) (8112cea)
- WP-36 part (a): Finage OKF bundle, closing ADR-0326's four-agent set (16d202b)
- WP-35 part (a): Advantage OKF bundle, reusing retrieve_reason_respond (06479d1)
- WP-33 part (a): Comage OKF bundle, Salesforce MCP server, generalized retrieve_reason_respond (8aed8f7)
- WP-32: cdp role and scoped capabilities (ADR-0340) (4ad1f83)
- WP-31 part (a): Arkos OKF bundle, policies and plan_draft_write shape (674d4ce)
- WP-30: multi-shape Agent Runtime (ADR-0342) (066941c)
- WP-28: project-scoped agent memory (ADR-0209) (c151e84)
- WP-23: separate current Salesforce knowledge from legacy SXA (ADR-0206) (42ac3e4)
- WP-20 Part B: enforce knowledge authorization as policy intersection (ADR-0203) (25e9f92)
- Implement ADR-0106: OKF bundle signing and validation (efffa50)
- Implement ADR-0117: real Confluence Cloud MCP server (d2a2423)
- Implement ADR-0116: decouple logical tool capabilities from physical bindings (4566aec)
- update dsc and openshift-ai version (406902d)
- Add zuno-ai-platform namespace and retire per-agent namespaces (8eb62aa)
- feat: implement ADR-0038 (OKF Markdown bundles), ADR-0039 (Agent Runtime executes OKF contract), ADR-0036 (full MCP authorization intersection) (02c9f4f)
- feat: implement ADR-0040 (agent entitlement vs business role) and ADR-0041 (remove nominative demo identities/passwords) (2b794f0)
- feat: implement ADR-0034 and ADR-0035 — dynamic classification and external-model restrictions (cdacbe9)
- refactor: reorganize namespaces by functional domain (3729ca0)
- repalce symbols (7d327b1)
- feat: implement the v0 Tekos vertical slice end to end (b369b64)
- chore: scaffold agents platform data and policy domains (820bc98)

