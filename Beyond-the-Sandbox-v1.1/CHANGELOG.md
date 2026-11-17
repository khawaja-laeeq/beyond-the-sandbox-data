# Changelog

## 2026-11-13: single-version manuscript and remaining text fixes (AI-assisted; at the authors' request)

No data or coding changed; all 246 numbers in the manuscript pass `check_numbers.py`.

- **One version.** The manuscript now presents one final version: the coded data after the erratum and both AI reviews (matrix v1.1). The side-by-side "v1.0; v1.1" reporting and the reading note were removed.
  - First-version values appear only where the text describes the first version: the history of the zero (IV-B) and a short "Changes from the first version's coding" section (IV-I).
  - Every value under both matrices stays in `analysis/v1.0_vs_v1.1_comparison.csv`.
  - Tables I, II, III and V show single values, with † for cells the erratum changed.
  - The framing-conflict notes moved out of the paper into `HUMAN_REVIEW_PACKET.md`.
- **Remaining text problems.**
  - The "peer review" wording and the untrue A10 and rule-design sentences had already been corrected in the second review; a search of every file found no other copy.
  - The last stale phrase, "(AI-assisted, pending approval)" on the A10 judgments in III-D, was removed.
  - **Added:** OpenAI's statement that by 26 September it had notified over 100 organizations about activity meeting its notification criteria (R05, cached; new reference [32]), in Section V-B and the corpus-coverage limitation. This is context only; R05 is not coded.
- **PDF.** Rebuilt from the DOCX with Microsoft Word: `manuscript/revised_manuscript.pdf`, 24 pages, single column.
- **Not done.** Venue template and page limit (step 7): no venue has been chosen.

## 2026-11-13: second AI review of every v1.1 decision (at the authors' request; same AI system, not a human)

The authors asked the AI to approve or reject the v1.1 decisions instead of reviewing them themselves. Every item was re-read against its cached source. Decisions and reasons: `analysis/ai_second_review_2026-11-13.csv`.

- **Erratum:** 13 of 14 fixes approved. **E09 rejected** (the I to O evidence-class change): the operator in the AISI units is UK AISI, so O misdescribes R26 as much as I; the tag stays I with a note.
- **New-source rows:** 37 approved; 10 approved with the relation corrected to partial, because the quote does not state the whole proposition (N11, N15, N20, N21, N23, N24, N27, N29, N30, N33); **3 rejected** (N39, N41, N49). Closest call: N10, which decides whether v1.1 has 6 or 5 independent propositions; approved.
- **A10 judgments:** all six confirmed.
- **Framing sentences:** both confirmed against the data.
- **Numbers that changed (v1.1 only):** support passages 244 to 241; relay-only propositions 15 to 9; W4 8 to 6; A3 two-organization 38 to 33; Irregular partial support 6 to 5 Opus 4.7 propositions; applied erratum fixes 13 to 12. Headline counts (core agreement 12 of 79, independent 3 to 6, S0 41/4) did not change.
- **Text:** "pending the authors' approval" and "provisional" replaced throughout by wording that says the v1.1 changes were checked by AI only and not by a human. Also corrected, because they were untrue: "A peer review flagged" (it was an AI-generated review), "a review brief written by the authors" (prepared with an AI assistant), "it did not approve any of its own changes", and "No rule was chosen after seeing its result" (W1 to W4 and A10 are now described as exploratory). "mostly OpenAI repeating UK AISI's findings" corrected to four of nine.
- `check_numbers.py` now counts only new-source rows that are not rejected; 384 numbers pass.

## 2026-11-13: framing conflicts reworded (at the authors' request; AI-drafted wording, pending the authors' confirmation)

Text only. No data, coding, citation or count changed; `check_numbers.py` still passes. The argument is unchanged: the sentences now say what holds in both v1.0 and v1.1.

- **Authorization belief** (Conclusion, Section V-B bullet, Table VII row): "single-organization" becomes "every supported permission belief rests on a single organization's records, and none is independently corroborated". In v1.1, HF-D2-1 is stated by METR and OpenAI, both from OpenAI's transcripts.
- **Conclusion wording on timing:** "mostly post-hoc" becomes "mostly post-hoc or paraphrased", matching Section V-B. At proposition level only 3 of 21 supported D2 beliefs are post-hoc; most of the rest describe contemporaneous reasoning in the developer's words. The data do not record verbatim versus paraphrase, so the authors should check that "mostly paraphrased" holds.
- **Records of another organization's agent** (Section V-B): the affected party is now "the only one whose own records give whole support to claims about another organization's agent", and Irregular [31] is named with its limits.
- **Section IV-I:** the framing-conflict note now records both rewordings instead of "kept as written".
- **Review packet (E) and REMAINING_HUMAN_WORK (1E)** updated to match.
- **PDF:** built from the DOCX with LibreOffice (`manuscript/revised_manuscript.pdf`).

## 2026-11-13: v1.1 clarity and significance pass (AI-assisted; pending the authors' approval)

These changes are to text only. No data, coding, citation or count changed; all 374 numbers still pass `check_numbers.py`. The framing rule still applies: no research question, argument or contribution claim was changed.

- **Reading note:** shortened, and it now says that a single figure means the two versions agree.
- **Abstract:** restructured into Problem, Method, Findings (four points), Implication and Status. The sentences quoted in the review packet are unchanged. The upper- and lower-bound definitions moved to Section IV-B.
- **Section I:**
  - New "Why this matters": how little of the public record is independently checkable (core counts) and why that makes disclosure practice a subject in its own right.
  - New "Main findings in brief", one point per research question, and a short roadmap.
- **Section IV-B:** a summary at the top of the densest section.
- **Section V-D (new), "What different readers can do with these results":** actions for readers, publishers, affected parties and researchers. Each follows from a finding, and none is presented as tested.
- **Review packet:** the headline list was updated to match.

## 2026-11-13: v1.1 revision (AI-assisted; every change pending the authors' approval)

Following the authors' review brief (tasks 1–10). No file in `original/` was changed. The frozen v1.0 matrix (SHA-256 `972dcdd5…`) is unchanged; v1.1 is built from it by `analysis/src/build_matrix_v1_1.py` and the erratum. The rule on framing was applied as revised by the authors: numbers and the sentences that state them may change, the research questions, argument and contribution may not, and contradictions are flagged, not rewritten.

### Task 1: numbers locked to data
- The decomposition-confidence split was corrected from 107/28/3 to **119/16/3**, in III-C, in the Limitations ("28 splits" → "16") and in `reviewer_report.md`.
- `analysis/src/check_numbers.py` tags every number in the manuscript to a data key, a cached source or a stated structural reason. The build fails on any untagged or mismatching number; 369 numbers pass, and a negative test confirms that wrong numbers fail.
- No other counted number in the previous text contradicted the v1.0 data. The brief's "63 of 67" is confirmed (64 if the contested proposition is counted).

### Task 2: sources
- `analysis/search_protocol.md` records the queries, sites, date range, inclusion rule, coding rules and every include or exclude decision. It was fixed during the search, not before it, and says so.
- Newly cached and coded:
  - R71 OpenAI, 4 Aug (relays);
  - R72 JFrog, 27 Jul (relay);
  - R73 Alazab and Waheed (secondary, never counted);
  - R74 OpenAI, 21 Jul;
  - R75 Irregular, 14 Aug (partial only);
  - R01 OpenAI, 26 Aug (in the ledger, previously HTTP 403).
- R05 was re-cached; its original cache was garbled.
- Excluded: eight Cloud Security Alliance notes (derivative syntheses) and the Black Hat talk (no transcript).
- 50 support rows were attached to existing propositions only, so the total stays 138. 13 candidate propositions are listed but not coded. Every quote is checked by script.

### Task 3: matrix v1.1
- `analysis/erratum_v1.1.csv` holds 14 fixes in 21 field rows, each with source, exact quote, location, reason, confidence and status "pending human approval":
  - E01–E05, E07: D5 branches;
  - E06: no change, the flag is recorded;
  - E08: Anthropic Mythos 5 D2;
  - E09: AISI Mythos 5 D2 role tag;
  - E10: AISI Mythos 5 stopping mechanism;
  - E11: Sol interruption not stated;
  - E12–E14: the stored partial-support judgments that S2, S3 and leave-one-out depend on.
- Rejecting one fix reverts only its cells (tested).

### Task 4: recomputation
- Table I, Table III, the stopping-mechanism counts, S0–S9, leave-one-out, W1–W4, A1–A10 and the figure are computed for both versions.
- `analysis/v1.0_vs_v1.1_comparison.csv` lists every value that differs (185).
- Manuscript Section IV-I states which headline results changed and which did not.

### Task 5: rule A10
- Six judgments are recorded, covering same act, uncertainty and derivation from Hugging Face.
- Independent corroboration is now reported as a range: 2–5 (v1.0) and 3–6 (v1.1), in the abstract, findings and conclusion. The dropped propositions are given with their passages.

### Task 6: selection effect
- Evidence-strength statements now use core propositions, or are labelled "all propositions".
- Sentences on the selection effect and on per-unit publication volume were added to Methods and Limitations.

### Task 7: text
- III-C states the actual rule for creating propositions.
- X07/X08 are stated precisely.
- References [9], [10], [24], [25] and [26] are cited where used.
- Citations are numeric throughout, with ledger codes only in Table VIII.
- There is one reading guide for the rule labels.
- The AI-use statement was rewritten for this round.
- This file, README and the revision summary now agree with the manuscript:
  - case studies are in IV-G;
  - references run [1]–[31] (three were added by task 2);
  - no PDF or page count, because LibreOffice is unavailable.

### Task 8: literature
- `analysis/literature_candidates.md`: intelligence source evaluation (the Butler Review read in full; Irwin and Mandel abstract only, full text closed), inter-coder reliability, Uuk et al. (read), and a Bieringer re-reading with exact overlaps.
- Draft Related Work text, marked pending author reading.

### Task 9: blind coding
- `blind_coding/`: 36 propositions (seed 20261113), two identical blank sheets, instructions, and `agreement.py` (raw agreement, kappa, AC1, alpha).
- Not filled in.

### Task 10: review packet
- `HUMAN_REVIEW_PACKET.md` is generated from the decision files.
- `REMAINING_HUMAN_WORK.md` is updated.

### Outputs moved
- The 12 Nov PDFs and DOCX were moved to `manuscript/superseded/`; they do not reflect v1.1.

## 2026-11-12: Research revision (AI-assisted; pending human review)

No file in `original/` was changed. The frozen 45-cell matrix (SHA-256 `972dcdd5…`) is untouched.

### Changed conclusions

| Was (uploaded manuscript, 11 Nov) | Now | Basis |
|---|---|---|
| "No claim has whole support from two organizations" (S2 = 0/45), headline in abstract and conclusion | Withdrawn as stated. Stored data give 1/44; all cached sources give 3 cells; propositions give 22/138 with two-org agreement and 5/138 with independent corroboration (all in the HF unit) | `analysis/atomic_sensitivity_results.csv` (W1–W4, A1–A9); `reproducibility/independent_verify_results.json` |
| "First detection is not independently established" (HF D4) | The operator's own account documents affected-party precedence; it is not independently corroborated | R02 VI.A; HF-D4-7 |
| Six stopping mechanisms, with AISI Mythos 5 as operator halt | The primary AISI Mythos 5 sample ended at its own token limit before the halt; the halt covered other samples. For Sol, interruption is not stated | R24 3.1, 4.1; R26 (X06) |
| D5: C 7, P 4, N 2 | Unchanged in frozen data. AI-assisted flags: P also stated for Artifactory, HF and Opus 4.6; HF N need not be qualified; C inconsistent (AISI Mythos 5 vs Sol) | `analysis/d5_branch_support.csv` |
| Anthropic's later assessment withdraws belief attribution (asserted) | Confirmed with the exact passage; classified as a later correction | X10 |
| Data Availability: "scripts regenerate every count" | Corrected: S2, S3 and leave-one-out need in-text partial judgments that are not in stored data | REPRODUCIBILITY_REPORT §D |
| AI-use statement: "independent model reviewers" | Corrected: same-pipeline reviewers, not independent | manuscript |

### Added

- Atomic-proposition layer: 138 propositions, 194 support passages, all quote-checked.
- Disagreement table: 13 disagreements, 26 quote-checked passages.
- Prior-work comparison: the Alazab and Waheed preprint was found and cited; Raftari, Bouke and Amundsen were read in full; Bieringer was not re-read.
- A list of pre-cutoff sources missing from the ledger (3).
- Independent recount, a 22-cell AI-assisted audit, source verification, and two clean runs.
- Revised manuscript (MD, DOCX, PDF) and reviewer report.

### Not done (requires a human)

- Blind second coding of propositions and adjudication.
- Human repetition of the 22-cell audit.
- Decisions on the D5 branch flags and on Anthropic Mythos 5 D2.
- Adding the missing sources to the ledger and recoding.
- Restoring the full reference list.
- Checking the Amundsen DOI.

## 2026-11-12, second pass (AI-assisted)

- **Manuscript, Findings IV-H:** added three comparative case studies.
- **References:** restored [1]–[25] in full, and corrected the Amundsen DOI to …991.
- **Manuscript IV-C:** corrected an overstatement. HF-D2-4 has hedged two-organization support (a target-relevance belief). No permission-belief proposition has support from more than one organization.
- **Manuscript Table IV:** now lists the five cross-organization disagreements (X01, X02, X05, X09, X13). X03 is within-organization and was listed by mistake.
- **Prior-work table:** Raftari lists UK AISI disclosures as sources but does not analyse the AISI incident.
- **Sources outside the ledger:** confirmed by web search that the OpenAI 4 Aug and JFrog 27 Jul posts exist, with those dates; neither was cached or coded. The Alazab and Waheed preprint (doi:10.20944/preprints202610.1658.v1) was re-confirmed.
- **Clean run 3:** every step exited 0.
- No count changed.

## 2026-11-12, clarity pass (at the author's request: clarity only, no content change)

These edits change wording and layout only. No finding, count, citation or claim changed; a script check confirmed that no number was removed from the text.

- **Abstract:** long sentences split, and the second paragraph divided into two.
- **Methods III-F:** added a short reading guide to the rule labels (S, W, A), restating definitions given elsewhere.
- **Findings:** the case studies are now IV-G and the sensitivity section IV-H, so the sections run in order.
- **Wording:** clarified two sentences, the detection/cessation sentence (IV-D) and the zero sentence (IV-B).
- **Layout:** tables use fixed column widths, a smaller font, repeating header rows and rows that do not split across pages; captions stay with their tables; A4 page with 0.8-inch margins. The PDF is now 15 pages.

## 2026-11-12, author names and packaging

- Added the authors to the manuscript: Khawaja Muhammad Laeeq (L1F23BSCS0080) and Mahnoor Iftikhar (L1F23BSCS1035). They replace "Anonymous Authors". The AI-use statement now reads "at the authors' request".
- Added `REMAINING_HUMAN_WORK.md`, covering human tasks only and written without assuming a venue.
- Added `manuscript/build_docx.py`, which rebuilds the DOCX and PDF with the table layout.
- The manuscript PDF is placed at the top level of the zip.
