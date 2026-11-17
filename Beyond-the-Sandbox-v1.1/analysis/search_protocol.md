# Search protocol and search log (task 2, revision v1.1)

AI-assisted (Claude, 12–13 November 2026). Every inclusion decision and every coded row is **pending human approval**.

**Timing disclosure.** The brief asked for this protocol to be written before searching. It was not. The three named sources were searched first, and this protocol was then fixed and applied to every later search and to all coding. The rules below are the ones actually applied. A human reviewer should judge whether searching before the protocol was written biased anything.

## 1. Scope

- **Evidence cutoff:** 25 October 2026. A source counts only if it was published on or before that date. Where a page carries dated updates, only passages dated on or before the cutoff may be coded. All updates in the coded sources are dated 26 September 2026 or earlier.
- **Units:** the nine documentary units of the frozen study. The clusters are OpenAI–Hugging Face, Anthropic and UK AISI.
- **Date range searched:** 1 May 2026 to 25 October 2026.

## 2. Inclusion rule

A source enters the ledger (`supporting_data/source_ledger/sources_v1.1_additions.csv`) if all of the following hold:

1. It is dated on or before the cutoff.
2. It makes at least one statement about one of the nine units, either naming the unit or describing it unambiguously.
3. It is publicly accessible, and its text can be cached so that every quotation is checked by script.
4. It is one of the following:
   - **(a) a first-party account:** by an operator, developer, evaluator, evaluation partner, affected party, or vendor of exploited software;
   - **(b) an investigator report** that states its own evidence base;
   - **(c) a secondary analysis**, which is included only if it is named by the authors, or if it reports something not traceable to sources already coded, such as its own records, its own interviews or its own corroboration.

**Exclusions:**

- Press coverage and aggregators (the AI Incident Database, news sites) are excluded, as in v1.0.
- Videos without a citable transcript are excluded, because their quotations cannot be checked by script.

## 3. Queries and sites

| # | Query (web search unless noted) | Purpose |
|---|---|---|
| Q1 | "Third-party cyber evaluations involving OpenAI models" (openai.com) | named source (a) |
| Q2 | JFrog blog "JFrog and OpenAI collaboration on zero-day security findings" | named source (b) |
| Q3 | preprints.org 202610.1658 | named source (c) |
| Q4 | Irregular statement Claude Opus 4.7 evaluation incident real company 2026 | evaluation partner, Anthropic units |
| Q5 | Irregular blog incident misconfiguration evaluation internet access July 2026 | evaluation partner |
| Q6 | PyPI malicious package Anthropic Claude Mythos evaluation removed statement July 2026 | affected party, INC-ANT-MY5 |
| Q7 | Cloud Security Alliance research note OpenAI Hugging Face incident 2026 | grey literature named by the authors |
| Q8 | "OpenAI and Hugging Face partner to address security incident during model evaluation" | OpenAI's initial statement, found in Alazab and Waheed's references |
| Q9 | GitHub statement UK AISI agent malicious pull request removed artefacts August 2026 | affected platform, AISI units |
| Q10 | Hugging Face blog post-mortem agent intrusion rebuilt infrastructure August 2026 | affected party, later account |
| Q11 | Reference lists of Alazab and Waheed (R73) and of the CSA notes, followed by hand | primary sources missed by the queries |
| Q12 | Ledger entries never cached: R01 and R05 (OpenAI), reopened in a real browser | primary sources previously unreadable |

**Sites searched:** openai.com, jfrog.com, preprints.org, irregular.com, labs.cloudsecurityalliance.org, huggingface.co, anthropic.com, aisi.gov.uk, and general web search (US index).

**Retrieval:**

- Pages that refuse scripted downloads (HTTP 403 from openai.com and preprints.org) were opened in a Chromium browser. Their page text was captured verbatim to `supporting_data/source_cache_v1.1/`.
- Every capture records its URL and capture time, and its SHA-256 is recorded in the ledger additions file.

## 4. Coding rules for new sources

New sources are attached **only to existing propositions**, and the total stays at 138. The relations are those of v1.0:

- **supports:** an OpenAI statement about OpenAI's own systems, or about its agents' own actions (base: OpenAI records).
- **relays:** a statement made on another organization's authority, for example "UK AISI told us", "UK AISI found", or OpenAI reporting that Hugging Face "detected and stopped" the activity.
- **partial:** the passage is not specific to the unit (it names no model, run or customer), or it states only part of the proposition.
- **Secondary analyses (R73)** are recorded as relays and are excluded from every organization count.
- **Same-organization partial restatements** of a proposition that the organization already wholly supports are not added, because they change no count.
- **Candidate propositions:** anything a new source states that matches no existing proposition goes to `analysis/candidate_propositions_v1.1.csv` (13 candidates). They are not coded.
- **Quote check:** every coded quotation (50 rows) and every candidate quotation (13) is checked against the cache by `analysis/src/build_analysis.py`, and the build fails if one is missing.

## 5. Decisions

### Included

| Source | Decision | Why |
|---|---|---|
| R71 OpenAI, 4 Aug 2026 | included; 11 rows, all relays or relayed counterevidence | First-party, unit-specific for AISI Sol; OpenAI learned the facts from UK AISI. |
| R72 JFrog, 27 Jul 2026 | included; 1 relay | Vendor confirmation of the Artifactory vulnerabilities; the incident facts come from OpenAI. |
| R73 Alazab and Waheed, 19 Oct 2026 | included as secondary; 11 secondary rows, never counted | Named by the authors; synthesis of public disclosures. |
| R74 OpenAI, 21 Jul 2026 | included; 6 rows | OpenAI's initial first-party statement; found through R73's references. |
| R75 Irregular, 14 Aug 2026 | included; 6 partial rows | Evaluation partner's own account. It names no model, so it is partial only, and its independence is uncertain because its findings came from joint work with the developer. |
| R01 OpenAI, 26 Aug 2026 | newly cached and coded; 15 rows | In the ledger, but HTTP 403 in the original study. |
| R05 OpenAI, 4 Sep 2026 | newly cached; not coded | Its incident passages repeat R74. |

### Excluded

| Source | Decision | Why |
|---|---|---|
| Cloud Security Alliance research notes on the OpenAI–Hugging Face incident (8 PDFs: 22 Jul, 23 Jul ×2, 30 Jul, 16 Aug, 24 Aug, 1 Sep, 2 Sep 2026) | excluded | They meet the date rule but fail 4(c). Each note is a synthesis of press and primary disclosures already coded (their reference lists cite The Hacker News, Fortune, Axios, BleepingComputer, OpenAI and Hugging Face). Each states that it "was generated with AI assistance and has not undergone official CSA review". A scripted search found no claim to own records or telemetry. Text cached in `supporting_data/source_cache_v1.1/csa_screened/`. R38 and R48, already in the ledger, are notes of the same series and stay context only. |
| OpenAI Black Hat USA talk, 5 Aug 2026 (video) | excluded | No citable transcript, so quotations cannot be checked. |
| Socket, BleepingComputer, Implicator, Elastic and other blog or press coverage found by Q6, Q9 and Q10 | excluded | Press or vendor commentary. Screened at search-result level only; not opened. |
| A standalone PyPI or GitHub statement | not found | Q6 and Q9 found none. GitHub's role is reported only through UK AISI's report (R10). |
| Hugging Face "rebuilt one-third" post-mortem | not found as a Hugging Face document | Q10 found only press reports of it. Recorded as candidate C13 through R73. |
| The OpenAI-model event in an Irregular evaluation (R71) | outside the frame | A separate event outside the clusters, like the Gemini and Meta Irregular events. Logged in `supporting_data/selection_frame/selection_frame_v1.1_additions.csv`. |

## 6. Effect on the counts

All effects are reported in `analysis/v1.0_vs_v1.1_comparison.csv` and in the manuscript (Section IV-B and Table II). In short:

- **R01** adds OpenAI as a second organization for HF-D2-1. That agreement is on shared records, because METR used OpenAI's transcripts.
- **R01** also adds a new independent pair for HF-D3-3: OpenAI's own account of its agents' exploit, against Hugging Face's records.
- **R71** turns four AISI Mythos 5 propositions and five Sol propositions into repeated reporting, and **R74** does the same for one Hugging Face proposition (HF-D4-3). These relays add no independence.
- **R75** gives Opus 4.7 its first second-organization passages. They are partial only, so no Anthropic proposition gains cross-organization agreement.
