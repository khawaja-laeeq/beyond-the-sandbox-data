# Brief

## Working title
Beyond the Sandbox: What Public Disclosures of AI-Agent Boundary Violations Actually Report (workshop version, carried over from V11)

## Scope change (2026-11-09)
Rounds 1-15 audited only 9 units from 3 organisations. Reviewers kept scoring novelty at about 5 ("an annotated artifact", "9 non-independent units", "the disclosure checklist's value is untested"). From now on the paper tests the checklist: it applies the frozen D1-D5 codebook to every public disclosure in a defined sampling frame and reports what those disclosures state and leave out. The 9-unit, 45-cell audit stays as the detailed case study. It is frozen and is no longer re-coded (see Constraints).

## Research question
Across public disclosures (1 Jan 2024 to the evidence cutoff) of AI agents that took or attempted actions outside their authorized task or boundary, how often does a disclosure state each of the five things an evaluator needs (D1 access conditions, D2 the agent's reading of its authorization, D3 the action taken, D4 detection and containment, D5 verified effect)? How does this differ by who discloses: operator/developer, affected party, independent investigator/evaluator, or press?
- RQ1 (completeness): For each dimension D1-D5, what share of disclosures in the frame state it (documented), state its opposite (contradicted), or leave it unstated (unknown)? Report proportions with Wilson 95% intervals.
- RQ2 (who discloses what): Do the completeness profiles differ by discloser role and by setting (evaluation/red-team environment vs deployment)? Descriptive only, because the frame is not a random sample.
- RQ3 (depth, case study): For the 9 frozen case-study units, what can the strongest available documents support about each dimension, and where do single-report codings in RQ1 over- or under-state what the fuller record shows?
- RQ4 (checklist): Which minimum disclosure items, each tied to a dimension that RQ1 finds most often missing, would make future reports codable? The checklist is derived from the RQ1 gaps, not asserted.

## Study type
documentary: a coded comparison of public documents and cases. There are no new experiments, offensive or otherwise. Published replays (e.g., Anthropic's Opus 4.7 resampling) are reported as results from their original investigators, not as our own experiments.

## Sampling frame and corpus (new)
- **Unit of analysis for RQ1/RQ2: one disclosure document** (a report, system-card section, evaluation report, incident write-up or news article) that describes a specific episode. The 9 case-study units stay incident-level and are marked as a separate layer (for example a `layer` column: `case_study` vs `survey`), so that counts for the two layers are never pooled by accident.
- **Where to search (log every query, date and hit count in research/search_log.jsonl):**
  - the AI Incident Database (incidentdatabase.ai) and the OECD AI Incidents Monitor
  - safety and evaluation sections of frontier-developer system/model cards (Anthropic, OpenAI, Google DeepMind and others)
  - evaluator and investigator reports (UK AISI, US CAISI, METR, Apollo Research and similar)
  - arXiv / security write-ups describing agent incidents
  - news coverage only when it is the earliest public report of an episode
- **Include:** the document describes a specific episode in which an LLM-based agent (a system taking tool actions: code execution, network, files, credentials, external services) took or attempted an action outside its authorized task, scope or containment boundary, in an evaluation or a real deployment, and the document was published between 1 Jan 2024 and the cutoff.
- **Exclude, and record the reason:**
  - hypothetical or scenario-only descriptions
  - jailbreak or prompt-injection demos with no agent action
  - attacks run by humans who merely used an AI tool
  - documents without enough text to read
  - exact duplicates (keep the earliest primary report and list the others as duplicates of it)
- **Selection table:** every candidate considered goes in experiments/data/selection_frame.csv with its source, the include/exclude decision and the reason. The paper's appendix reproduces this table. All documents that meet the criteria are coded: there is no cherry-picking and no cap. Aim for at least 40 included documents. If the frame yields fewer, report the true number and say so.

## Target venue and format
(default — tell me if you want otherwise)
- **Venue:** a generic AI-security / agent-safety workshop, e.g., a SaTML- or NeurIPS-style workshop track.
- **Length:** 6 pages of main text in IEEE two-column format (IEEEtran), with references and appendix extra.
- **Sections, in order:** Abstract; Introduction (with RQs and contributions); Related Work; Methods and Evidence Governance (sampling frame, selection, frozen codebook, coding and second coding, limitations); Findings (RQ1-RQ2 completeness profiles with a figure; RQ3 case study; RQ4 checklist); Discussion and Implications for Evaluators; Limitations; Conclusion; References; Appendix (frozen codebook, selection-frame table, per-document coding, the 45-cell case-study table, source ledger).
- **Citations:** IEEE numeric.
- **Review:** double-blind, so the manuscript is anonymized and the "faculty evaluation" framing is removed.

## Second coder
ai (an independent AI coder from a different model family codes every unit blind from the frozen codebook and the source text; agreement is reported as AI-assisted second coding, never as a human coder)

## Constraints
- Documentary only. No offensive experiments, no probing of real systems, and no reproduction of exploit steps. Descriptions of incidents stay at the level of detail the public sources give, with no operational detail added.
- No invented numbers. Every quantitative statement about an incident (e.g., 68.7%, 22.9%, 15 installations, 17 actions) must be traced to a source anchor in the ledger. Corpus-level proportions, Wilson 95% intervals and agreement statistics are allowed only when a script computes them from the coded CSVs. Report raw agreement and Gwet's AC1 alongside Cohen's kappa, because kappa is deflated when one status dominates. No significance tests across groups: the frame is not a random sample.
- **Frozen codebook.** experiments/protocol/codebook_v1.0.csv (sha256 in experiments/protocol/freeze_v1.0.json) is the codebook for all new coding. Do not add or change decision rules. A rule problem a reviewer raises goes into Limitations or a sensitivity recount, not into a new rule.
- **Frozen case study.** The 45 case-study cells are frozen as experiments/protocol/coded_evidence_case_study_v1.0.csv. Do not change their statuses, D2 annotations or D5 branches. A reviewer objection to a case-study cell gets a sensitivity row or a limitation sentence. The only allowed change is an erratum: a primary-source passage that directly contradicts the cell, logged with the passage. The human-only recount (S6) stays reported.
- **Headline discipline.** The 0/45 two-organisation count is case-study context, not a headline in the abstract, introduction or conclusion. If it is reported, report it next to the per-organisation split of the Hugging Face D4 proposition.
- **Second coding.** The second coder never sees the primary codes. Disagreements are re-read against the source and resolved in a logged adjudication file (cell, both codes, deciding passage, reason). Agreement is always reported on the codes as they were before adjudication. An agent may not change a primary code just to raise agreement.
- Sources marked "not reauthenticated" in the ledger get re-checked where we have access. Anything we can't re-check is flagged in the ledger and the text.
- Compute: CPU-only VM, about 700 MB per run. That is only needed for the tables and figures built from the CSVs (Python with pandas/matplotlib). The template's ">= 5 seeds" rule doesn't apply because nothing here is stochastic.
- Evidence cutoff stays at 25 Oct 2026 unless the humans move it.

## Inputs
- `inputs/Beyond_the_Sandbox_V11_Professor_Submission.pdf`: the V11 manuscript, used as the base text to revise.
- `inputs/Beyond_the_Sandbox_V11_Professor_Submission.pdf.extracted.txt`: the full text of that PDF, for editing and quoting.
- `experiments/data/V11_Codebook.csv`: definitions of D1–D5 and the rules for the documented / contradicted / unknown tags.
- `experiments/data/V11_Incident_Register.csv`: the 9 traceability units, the cluster each belongs to, and its core sources.
- `experiments/data/V11_Coded_Evidence.csv`: the 45 unit×dimension decisions with evidence paraphrases and section anchors.
- `experiments/data/V11_Source_Ledger.csv`: references R01–R23 with their URLs and verification status.
- `experiments/protocol/codebook_v1.0.csv`, `experiments/protocol/coded_evidence_case_study_v1.0.csv`, `experiments/protocol/freeze_v1.0.json`: the frozen codebook and case-study coding (2026-11-09).

## Keywords
AI agent security, sandbox escape, authorization boundary, agentic cybersecurity incidents, detection and containment, AI incident reporting, disclosure completeness, documentary analysis
