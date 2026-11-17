# Remaining Work: Human Tasks Only (updated 13 Nov 2026, v1.1)

Authors: Khawaja Muhammad Laeeq (L1F23BSCS0080) and Mahnoor Iftikhar (L1F23BSCS1035)

The AI system that produced the coding cannot do the tasks below: each needs human judgment or human independence.

**Status on 13 Nov 2026:** at the authors' request, the same AI system re-checked every v1.1 decision (`analysis/ai_second_review_2026-11-13.csv`). It rejected E09 and rows N39, N41 and N49 and changed ten relations to partial. The manuscript now says the changes were checked by AI only. That does not replace item 1: if the authors later review the decisions themselves, the manuscript can say so.

## 1. Approve or overrule every v1.1 decision (highest priority)

Work through `HUMAN_REVIEW_PACKET.md`. Each item has the exact quote and location.

- **A. The 14 erratum fixes** in `analysis/erratum_v1.1.csv`. Set `status` to `approved` or `rejected`; a rejected fix reverts only its own cells. The weightiest are:
  - **E08:** Anthropic Mythos 5 D2 documented from R25's conditional quote;
  - **E07:** AISI Mythos 5 coded C, for consistency with Sol (low confidence; the alternative is neither unit C);
  - **E09:** the R26 role tag, I → O, was rejected in the AI second review; the tag stays I;
  - **E10:** the AISI Mythos 5 stopping mechanism.
- **B. The 47 new-source rows in use (50 coded; 3 rejected in the AI second review, 10 downgraded to partial) and the 13 candidate propositions.** Approve or reject each row in `analysis/src/new_source_rows.py`. Decide whether any candidate should become a proposition.
- **C. The six A10 independence judgments** in `analysis/a10_independence_judgments.csv`. They set the lower end of the independent-corroboration range.
- **D. The changed headline sentences.**
- **E. The two framing conflicts**, reworded on 13 Nov at the authors' request (AI-drafted wording; confirm or edit):
  - "authorization belief remains single-organization" is now "every supported permission belief rests on a single organization's records, none is independently corroborated" (Conclusion, Section V-B, Table VII);
  - "the affected party is the only organization with its own records" is now "the only one whose own records give whole support to claims about another organization's agent", with Irregular named (Section V-B).
- After any change, rerun the pipeline (README). `check_numbers.py` fails until the text matches the data. The manuscript now reports one version (v1.1); if you reject a fix, the numbers in the text update only after you rerun the pipeline and fix what `check_numbers.py` reports.

## 2. Blind second coding

The sheets are ready in `blind_coding/`: 36 propositions (seed 20261113), 4 per incident unit, every dimension 7–8 times.

1. Each author codes their own sheet independently, following `CODING_INSTRUCTIONS.md`, without opening `analysis/`, `blind_coding/key/` or the packet.
2. Run `python3 -I blind_coding/agreement.py`. It computes raw agreement, Cohen's kappa, Gwet's AC1 and Krippendorff's alpha: author against author, and each author against the AI.
3. Adjudicate the disagreements in `disagreements_for_adjudication.csv`.
4. Report the statistics from before adjudication. Add one sentence to the abstract (the current text says the coding is prepared but not done).

## 3. Human evidence audit

Repeat the 22-cell entailment audit in `reproducibility/manual_evidence_audit.csv`: open each source, find the passage, and judge whether it supports the coded status. Record the reviewer's name and the date.

## 4. Literature

Read the candidates in `analysis/literature_candidates.md` before using the drafted Related Work text. In particular, decide whether to replace the Bieringer sentence: the re-reading finds that their fields match ours by name but describe a different object.

## 5. Supervisor review

The professor or advisor reviews the manuscript. The independent-corroboration result is now a range, and v1.1 changes several cell codes.

## 6. Decisions before external submission (venue not yet chosen)

- **PDF:** `manuscript/revised_manuscript.pdf` (24 pages, single column, built with Word). Apply the venue's template and page limit once chosen; most workshops want 4–8 two-column pages.
- **Venue:** choose it, then apply its template and page limit.
- **Double-blind review:** if the venue uses it, remove names and student IDs, including from the coding sheets, scripts and logs, and make an anonymized package.
- **Third-party material:** remove cached web pages and full texts from any public release (`original/research/fulltext/`, `original/experiments/source_cache/`, `supporting_data/source_cache_v1.1/`). Keep the URLs, SHA-256 values and short quotations.
- **Code hosting:** choose a public home (GitHub or Zenodo) after acceptance.
