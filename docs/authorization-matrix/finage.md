<!-- BEGIN GENERATED AUTHORIZATION MATRIX (ADR-0503) - do not edit; regenerate with: python3 platform/okf/generate_authorization_matrix.py -->

## Authorization matrix

Generated per ADR-0503 from this bundle's frontmatter, `policies/tools/tool-policy.yaml`, `policies/knowledge/knowledge-policy.yaml`, `policies/models/model-catalog.yaml` and `policies/model-routing/model-routing-policy.yaml` — the enforced intersection (ADR-0011/ADR-0203) restated for review, never read at runtime. Entitlement (ADR-0040): `agent_finage`; model classification ceiling (ADR-0021): `C2`; status: `placeholder`; local-only (ADR-0416): `true`.

| Task (FOR WHAT) | Resource (WHAT) | Kind | Capability / server | Min class | Business roles (WHO) | Ext-model context | Quota | Policy source |
|---|---|---|---|---|---|---|---|---|
| `answer-finance-question` (primary; prompt: `prompts/answer-finance-question.md`) | `web_search` | tool | `web.page.search` @ web-search | C1 | sales, consultant, adv, finance, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `web_search` |
| `answer-finance-question` (primary; prompt: `prompts/answer-finance-question.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `identify-business-ready-to-invoice` (project-required; prompt: `prompts/identify-business-ready-to-invoice.md`) | `salesforce.opportunity.read` | tool | `salesforce.opportunity.read` @ salesforce | C2 | sales, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `salesforce.opportunity.read` |
| `identify-business-ready-to-invoice` (project-required; prompt: `prompts/identify-business-ready-to-invoice.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `monthly-invoice-report` (project-required; prompt: `prompts/monthly-invoice-report.md`) | `salesforce.opportunity.read` | tool | `salesforce.opportunity.read` @ salesforce | C2 | sales, board | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `salesforce.opportunity.read` |
| `monthly-invoice-report` (project-required; prompt: `prompts/monthly-invoice-report.md`) | `knowledge.project` | knowledge | — | — | consultant, board, sales, adv, finance, cdp | — | `standard` (user 60 req/5m) | `knowledge/knowledge-policy.yaml` `knowledge.project` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `list_drive_files` | tool | `drive.document.search` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `list_drive_files` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `read_gmail` | tool | `gmail.message.read` @ google-workspace | C1 | consultant, board, cdp, sales, adv, finance | allowed | `standard` (user 60 req/5m) | `tools/tool-policy.yaml` `read_gmail` |

### Model routing

Effective per-task model chain (ADR-0021/ADR-0303/ADR-0412), resolved from `policies/models/model-catalog.yaml`'s classification eligibility reordered by this `(agent, task)`'s `policies/model-routing/model-routing-policy.yaml` preference — the first entry is the reference model, the rest are fallback alternatives, in try order. The reference model is annotated with the model id it actually serves and that model's architectural role (`default`, `quality`, `reasoning`, `specialized`, `reasoning-external`, `code`, `general-external`); `model-catalog.yaml`'s `role` key is the authority for both, and every model reachable through the fallback chain is named in the **Available models** rollup below the table.

| Task | Classification ceiling | Reference model | Fallback chain | Adapter | Policy source |
|---|---|---|---|---|---|
| `answer-finance-question` (primary; prompt: `prompts/answer-finance-question.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |
| `identify-business-ready-to-invoice` (project-required; prompt: `prompts/identify-business-ready-to-invoice.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |
| `monthly-invoice-report` (project-required; prompt: `prompts/monthly-invoice-report.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |
| `check-my-drive-and-mail` (prompt: `prompts/check-my-drive-and-mail.md`) | `C2` | `local-qwen35-maas` → `qwen3.5-9b` (default) | `local-qwen35`, `local-gpt-oss-maas`, `local-gpt-oss`, `local-maas`, `local`, `local-wesh-maas`, `local-wesh` | — | `policies/model-routing/model-routing-policy.yaml` |

**Available models** (ADR-0419, generated): the union of every model reachable by any task or prompt slot above, at any classification, each with the model id it serves and that model's role - `local-maas` → `qwen3.6-27b-instruct` (quality), `local` → `qwen3.6-27b-instruct` (quality), `local-gpt-oss-maas` → `gpt-oss-20b` (reasoning), `local-gpt-oss` → `gpt-oss-20b` (reasoning), `local-wesh-maas` → `qwen3.5-9b-wesh` (specialized), `local-wesh` → `qwen3.5-9b-wesh` (specialized), `local-qwen35-maas` → `qwen3.5-9b` (default), `local-qwen35` → `qwen3.5-9b` (default).

<!-- END GENERATED AUTHORIZATION MATRIX -->
