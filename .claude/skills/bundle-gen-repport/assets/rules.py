"""Hand-written part of the report: the rules read out of each task prompt.

Everything else in the report is parsed from the bundles. These lines are
paraphrases, so each task records the hash of its prompt files at the time it
was written (PROMPT_SHA). generate.py warns when a prompt changed since.
After re-reading the prompt and updating the rules, refresh the hash with:
    python3 .claude/skills/bundle-gen-repport/scripts/generate.py --rehash
"""
CANON = {'search_confluence': 'confluence.page.search',
         'list_drive_files': 'drive.document.search',
         'read_gmail': 'gmail.message.read'}

# ---- curated rules, each taken from the task prompt or the agent body --------
R = {}
R['tekos/answer-technical-question'] = [
 ('do', 'Answer only from the provided context. If it does not hold the answer, say so instead of inventing details.'),
 ('do', 'Cite the sources and end every answer with a final line that reads only "— Tekos".'),
 ('limit', 'Search budget: at most three search calls per question, and never repeat a search with a reworded query.'),
 ('do', 'For a comparison, when the passages describe each side separately, build it from them: each side with its source URL, then the differences those passages support, and say which part no passage states. Never add a difference no passage supports (added in 1.0.3).'),
 ('limit', 'Order of grounding: indexed documents first, then live Confluence search, web search last.'),
 ('dont', 'Never put a customer name, a project id or anything from project memory in a web search query. The bundle records that no code enforces this yet.'),
 ('limit', 'Cluster reads (events, logs, resources, metrics) are for the ocp-ai-ops group only, in zuno-* namespaces only, and never return Secrets or ConfigMaps.'),
 ('limit', 'Launching a cluster audit needs the initiating user\'s approval and only happens when the user explicitly asks for a fresh check.'),
]
R['tekos/find-relevant-docs'] = [
 ('do', 'Return a list, best first: title, source (documentation, Confluence or Drive), URL and one line on why it is relevant.'),
 ('dont', 'Do not answer the underlying question. Point to the material that covers it.'),
 ('dont', 'Never invent a title or a URL. List only what was retrieved, and say so when nothing matches.'),
]
R['tekos/check-my-drive-docs'] = [
 ('do', 'List the consultant\'s own Drive files that relate to the project or topic, with name and link.'),
 ('limit', 'Runs with the caller\'s own identity, so it only sees files that person can already see. It returns metadata, not content.'),
 ('dont', 'Never invent a file name or link, never describe content the tool did not return, never answer technical questions here.'),
]
R['tekos/write-code'] = [
 ('do', 'Fenced code block per file with its language, minimal and complete, with assumptions (versions, names, namespaces) in one line.'),
 ('dont', 'No tools and no retrieval: never claim to have checked documentation, a repository or a cluster, and never cite sources.'),
 ('dont', 'Never write a real secret, password or token. Use a clearly marked placeholder.'),
 ('limit', 'A request for an explanation rather than code gets a short answer and a pointer to the grounded Q&A task.'),
]
R['arkos/draft-architecture-testimonial'] = [
 ('do', 'Write a long structured document under Context, Architecture Overview, Key Decisions, Risks & Trade-offs and Recommendations.'),
 ('do', 'Stay grounded in the supplied context. Where it does not support a claim, say so instead of inventing architecture.'),
 ('do', 'Review its own draft before saving (the reflect pass, run at a C2 ceiling) and return only the revised body.'),
 ('do', 'A plain factual question gets a direct, short answer, not the document structure.'),
 ('must', 'A diagram request must call the diagram tool with real source. Diagram source is never pasted into the reply as if it were done.'),
 ('limit', 'Repository tools have no default owner: if the message names no GitHub org, GitLab group or user, ask before guessing.'),
 ('limit', 'Delegate each work item once, with the plan\'s exact work_item_id, never invented or omitted, plus at most one precise follow-up when the answer is incomplete (reworded in 1.0.3).'),
 ('must', 'When the delegated answer covers everything asked, mark the work item done first, then write the reply from it. When no usable answer arrives, mark it failed and say the delegated agent gave none.'),
 ('dont', 'Apart from that one follow-up, never delegate a work item that already has an answer or is marked done or failed. After the follow-up, ask the user instead of delegating again.'),
 ('limit', 'Writes are explicit: a file commit lands only in public repositories, and a new repository is private unless the call says otherwise.'),
]
R['arkos/workshop-presentation'] = [
 ('do', 'Write the presentation under Objectives, Architecture Overview, Key Decisions, Build & Run Roadmap, Discussion Points and Next Steps.'),
 ('do', 'Self-review for consistency between the architecture overview and the roadmap (reflect pass at a C2 ceiling).'),
 ('do', 'Stay grounded in documentation, Confluence and project memory, and say when the context does not support a claim.'),
 ('must', 'A diagram request must call the diagram tool with real source, never describe it as done in the reply.'),
 ('limit', 'Ask which GitHub org, GitLab group or user to check when the message does not name one.'),
 ('limit', 'Delegate each work item once, with the plan\'s exact work_item_id, plus at most one precise follow-up when the answer is incomplete (reworded in 1.0.3).'),
 ('must', 'When the delegated answer covers everything asked, mark the work item done first; when no usable answer arrives, mark it failed and say so.'),
 ('dont', 'Apart from that one follow-up, never delegate a work item that already has an answer or is marked done or failed.'),
]
R['arkos/structure-demo'] = [
 ('do', 'Reply with an opening, an ordered list of sections with a one-line purpose each, 2 to 4 talking points per section, and a closing takeaway.'),
 ('dont', 'Do not invent product capabilities. If the request is too vague to build a real sequence, ask one clarifying question.'),
 ('limit', 'No tools and no retrieval. Replies are capped at 1,536 tokens.'),
]
R['arkos/write-code'] = [
 ('do', 'Put the code in a fenced block, with a short explanation only when it adds value (an assumption, a value to fill in, how to run it).'),
 ('dont', 'Never claim to have run, tested, committed or saved the code. Say so when unsure that an option or API exists.'),
 ('limit', 'No tools, no documents: works from the message and the conversation only. Prefers local reasoning models.'),
]
R['comage/check-deal-status'] = [
 ('must', 'Say whether each answer draws on indexed knowledge, a live Salesforce read, or both.'),
 ('dont', 'Never state a stage or an amount with confidence unless the context holds a live read. Otherwise warn that indexed data may be stale.'),
 ('dont', 'Never writes to Salesforce. A change request is redirected to the update task.'),
 ('limit', 'Charts and anything built from deal figures go to the diagram tool. The image tool is for marketing visuals a person explicitly asked for.'),
 ('must', 'When a visual tool applies it must actually be called. Describing the call in the reply counts as a failure.'),
 ('limit', 'Live Salesforce data is only available to the sales and board business roles.'),
]
R['comage/update-opportunity-status'] = [
 ('must', 'The tool call is the only way a change is made. Never say a change happened unless the call succeeded.'),
 ('limit', 'Updates existing opportunities only, and only their stage, amount or close date. It cannot create an opportunity.'),
 ('do', 'Ask when the request does not identify the opportunity or the value. It has no read tool, so it cannot look one up.'),
 ('do', 'Report exactly what the tool returned, and give the tool\'s reason when a call fails or is refused.'),
]
R['comage/check-my-drive-and-mail'] = [
 ('limit', 'Acts with the user\'s delegated access, so it only sees files and mail the user can already see.'),
 ('dont', 'Read-only: never creates, edits, sends or deletes anything. Never invents a document, a message or its content.'),
 ('do', 'Say so plainly when the tools return nothing relevant.'),
]
R['advantage/answer-project-question'] = [
 ('must', 'Say whether an answer draws on indexed knowledge or on a general web search.'),
 ('dont', 'No live Salesforce or current-deal data. A question only Comage can answer is redirected, not guessed.'),
 ('limit', 'Reads knowledge.adv and project memory. By explicit omission it never declares knowledge.sales or a CRM tool.'),
]
R['advantage/identify-new-business-with-po'] = [
 ('do', 'List new business whose client purchase order arrived in the last three rolling days, with the date and the source document.'),
 ('dont', 'Retrieval is not a date filter: when a date is missing or ambiguous, say so rather than guess it.'),
 ('do', 'If the context holds nothing for the period, state plainly that there is no grounded answer.'),
 ('limit', 'No tool at all. Works from indexed ADV knowledge only.'),
]
R['advantage/monthly-sales-report'] = [
 ('do', 'Produce the monthly in-progress report as text and tables, with margin by state, by customer and by technology.'),
 ('must', 'Every figure comes from the context and cites the document it was read from.'),
 ('dont', 'Never invent a figure to fill a gap. If the month has no figures, say so instead of producing an empty or invented report.'),
]
R['advantage/check-my-drive-and-mail'] = [
 ('limit', 'Delegated, read-only access to the user\'s own Drive and Gmail.'),
 ('do', 'For each item give title or subject, date and one line on why it is relevant. Say so when nothing matches.'),
]
R['finage/answer-finance-question'] = [
 ('must', 'Say whether an answer draws on project memory or on a general web search.'),
 ('dont', 'No live Salesforce, ADV or current-deal data. A question for Comage or Advantage is redirected.'),
 ('dont', 'Never executes a financial transaction. It reports on state and does not change it.'),
]
R['finage/identify-business-ready-to-invoice'] = [
 ('must', 'Project-bound: first ask which engagement (project name or Salesforce opportunity id) and wait. Nothing proceeds until it is verified.'),
 ('limit', 'Verification is a yes or no check with the user\'s own identity and fails closed. No Salesforce record content reaches the model.'),
 ('do', 'Identify business in the "A facturer" billable state from that engagement\'s project memory, attributing each item to its record.'),
 ('dont', 'State plainly that no billing history stands behind it. Never present a retrieved state as the current state of an invoice.'),
]
R['finage/monthly-invoice-report'] = [
 ('must', 'Project-bound: ask which engagement and wait for verification before producing anything. Failed verification is reported, not worked around.'),
 ('do', 'Report revenue, outstanding amounts, delay and forecast for that engagement, attributing every figure to its record.'),
 ('dont', 'Never present a summed or derived total as authoritative, never imply the figures describe the current period.'),
 ('do', 'Say so when the project memory holds no figures.'),
]
R['finage/check-my-drive-and-mail'] = [
 ('limit', 'Delegated, read-only access to the user\'s own Drive and Gmail, about an account or invoice.'),
 ('dont', 'No live Salesforce or sales administration data, and never executes a financial transaction.'),
]
R['naveo/answer-onboarding-question'] = [
 ('do', 'Answer from the retrieved context and cite sources concisely.'),
 ('dont', 'When the context does not ground an answer, say so rather than guess.'),
 ('limit', 'Confluence search is its live-read tool. Reuses existing knowledge domains and tools only.'),
]
R['cognos/coming-soon'] = [
 ('must', 'Answer every request briefly: Cognos is coming soon and will handle Direction-level financial and strategic questions for the board.'),
 ('dont', 'Never answers the request itself and never invents figures, sources or strategic assessments.'),
]
R['soursage/coming-soon'] = [
 ('must', 'Answer every request briefly: Soursage is coming soon and will source candidates and match consultants to missions.'),
 ('dont', 'Never answers the request, never names or assesses a person, never invents a profile.'),
]

AGENT_RULES = {
 'tekos': [
  ('limit','Entitled groups: agent_tekos and agent_tekos_preview. Guardrails run in observe mode.'),
  ('limit','Conversation memory keeps the last 6 turns within a 6,000 token budget.'),
  ('limit','Confluence results stay on local models even though the agent ceiling is C1.'),
  ('dont','Web search is narrowed to public technical topics (policies/web-search-scope.md). Recorded as a known gap: nothing checks the query in code yet.'),
 ],
 'arkos': [
  ('limit','Local models only: the agent is C3 because sovereign-marked architecture documents must never leave the cluster.'),
  ('limit','May delegate one hop to tekos / answer-technical-question, depth 1. A write the target asks for (its cluster audit) waits for the approval of the initiating user.'),
  ('limit','Conversation memory keeps the last 6 turns within a 6,000 token budget.'),
  ('limit','The only agent here with write tools: commit one file to a public repository, create a repository (private by default).'),
 ],
 'comage': [
  ('limit','Entitled group: agent_comage. Both Salesforce tools are restricted to the sales and board roles.'),
  ('limit','Update tool is the only write tool, and indexed knowledge is read-only: every change goes through the live call.'),
 ],
 'advantage': [
  ('dont','Holds the line with Comage by omission: no knowledge.sales, no CRM capability, nothing inherited from the sales agent.'),
  ('limit','Placeholder: its main domain knowledge.adv has no ingestion source, so the agent is declared but not served.'),
 ],
 'finage': [
  ('limit','local_only: finance material stays on local models at every classification, including C1.'),
  ('dont','No finance knowledge domain, no billing history, no arithmetic: every number is retrieved and attributed, never computed.'),
  ('dont','Holds its scope by omission: no knowledge.sales, no knowledge.adv, no capability that reads Salesforce data into an answer.'),
 ],
 'naveo': [
  ('limit','Placeholder: declared but not served, shown as "coming soon" in a portal.'),
  ('limit','Reuses retrieve_reason_respond and existing capabilities only: no new knowledge domain, no new external system.'),
 ],
 'cognos': [('limit','Placeholder with no capability. Its task list is a single "coming soon" reply.')],
 'soursage': [('limit','Placeholder with no capability. Intended to work with Workday and LinkedIn once built.')],
}

DOMAIN = {
 'knowledge.tech': 'Official Red Hat product documentation (C1) and internal Confluence content (C2), retrieved by topic.',
 'knowledge.project': 'Durable memory of one engagement, written from earlier conversations. Access follows project membership, checked at query time.',
 'knowledge.sales': 'Salesforce content indexed on a schedule, so it can lag behind live records. C2 floor.',
 'knowledge.adv': 'Sales administration content. It has no ingestion source at present.',
}


PROMPT_SHA = {
 "advantage/answer-project-question": "7cb1614dc508",
 "advantage/check-my-drive-and-mail": "a31df7c0e52a",
 "advantage/identify-new-business-with-po": "517265cf809d",
 "advantage/monthly-sales-report": "8f9bd97640b8",
 "arkos/draft-architecture-testimonial": "5c685a3cfbb9",
 "arkos/structure-demo": "215eaa1a60dd",
 "arkos/workshop-presentation": "86d7f16ccded",
 "arkos/write-code": "38b1c3e49735",
 "cognos/coming-soon": "ccbe5b38a4fb",
 "comage/check-deal-status": "421fe3cdf744",
 "comage/check-my-drive-and-mail": "8cc72bc35157",
 "comage/update-opportunity-status": "17a2e917739a",
 "finage/answer-finance-question": "fec225a64dd9",
 "finage/check-my-drive-and-mail": "daaaca7c3505",
 "finage/identify-business-ready-to-invoice": "0c6a6e17f0a9",
 "finage/monthly-invoice-report": "d84a2e564256",
 "naveo/answer-onboarding-question": "fc5efa8dc4c8",
 "soursage/coming-soon": "0114bc203303",
 "tekos/answer-technical-question": "c3514e61b2d6",
 "tekos/check-my-drive-docs": "6daac0c384c3",
 "tekos/find-relevant-docs": "6913cf88b4e1",
 "tekos/write-code": "affa4b40e04b"
}
