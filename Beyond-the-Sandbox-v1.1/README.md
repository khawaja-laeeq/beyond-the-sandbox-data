# Beyond the Sandbox: Revised Research Package, v1.1 (2026-11-13)

**Main document:** `manuscript/revised_manuscript.pdf` (24 pages, built with Word), from the source `manuscript/revised_manuscript.md` and the Word file `manuscript/revised_manuscript.docx`. The manuscript reports one version, the coded data v1.1. The files from the previous round (12 Nov) are kept in `manuscript/superseded/` and do **not** reflect v1.1.

This is an AI-assisted revision of *Beyond the Sandbox: What Public Disclosures Establish About Security Boundary Violations by Autonomous AI Agents*.

- **v1.0** is the frozen 45-cell matrix (SHA-256 `972dcdd5…`, unchanged), with the proposition layer as first released.
- **v1.1** is built by script from v1.0 plus a logged erratum, and adds sources found in this round.

**Every v1.1 change was re-checked in a second review by the same AI system (13 Nov; `analysis/ai_second_review_2026-11-13.csv`): it rejected erratum fix E09 and three new-source rows and corrected ten relations. This is not an independent check: no human has reviewed the coding.** Start with `HUMAN_REVIEW_PACKET.md`.

## Layout

| Folder or file | Contents |
|---|---|
| `HUMAN_REVIEW_PACKET.md` | Every AI decision to approve or overrule, with quote and location |
| `REMAINING_HUMAN_WORK.md` | What only the authors can do |
| `manuscript/` | `revised_manuscript.md` (source; every number tagged to the data), `.docx`, `build_docx.py`, `revision_summary.md`, `superseded/` |
| `analysis/` | Inputs edited by humans: `erratum_v1.1.csv` and `a10_independence_judgments.csv` |
| | Protocol and literature: `search_protocol.md`, `literature_candidates.md` |
| | v1.1 outputs (top level), v1.0 outputs (`v1.0/`), and the v1.1 matrix with its freeze record (`matrix_v1.1/`) |
| | `v1.0_vs_v1.1_comparison.csv`, `cell_level_results.json`, `table1_v1.0.csv`, `table1_v1.1.csv`, `candidate_propositions_v1.1.csv`, `number_check_report.csv`, the figure, and the scripts in `src/` |
| `blind_coding/` | Two blank coding sheets (one per author), `CODING_INSTRUCTIONS.md`, `draw_sample.py` (seed 20261113), `agreement.py`, and the sample key in `key/` (not for the coders) |
| `supporting_data/` | Codebook, source ledger plus `sources_v1.1_additions.csv`, the frozen v1.0 matrix with its freeze record, the selection frame plus v1.1 additions, provenance records, and `source_cache_v1.1/` (texts cached in this round) |
| `reproducibility/` | Independent recount, evidence audit, clean-run script, logs |
| `original/` | The unchanged package; checksums are in `reproducibility/original_checksums.sha256` |
| `audit/`, `reviewer_report.md`, `CHANGELOG.md` | Earlier audit, the AI self-review (not an independent review), and the change log |

## Reproduce

Run from this folder with Python 3.12. The pipeline itself uses the standard library only; the figure needs matplotlib and the DOCX needs pandoc and python-docx.

```
python3 -I analysis/src/build_matrix_v1_1.py   # v1.1 = v1.0 + erratum; checks v1.0's SHA-256 and every erratum quote
python3 -I analysis/src/build_analysis.py      # propositions for v1.0 and v1.1; fails if any quote is missing
python3 -I analysis/src/cell_recount.py        # Table I, S0-S9, leave-one-out, stopping mechanisms, D5 branches
python3 -I analysis/src/make_comparison.py     # every value that differs between v1.0 and v1.1
python3 -I analysis/src/prior_work.py
python3 -I analysis/src/make_figures.py        # needs matplotlib
python3 -I analysis/src/check_numbers.py       # fails if any manuscript number is untagged or differs from the data
python3 -I analysis/src/make_review_packet.py
python3 -I reproducibility/independent_verify.py --json reproducibility/independent_verify_results.json
python3 -I reproducibility/evidence_audit.py
python3 -I reproducibility/clean_run.py reproducibility/clean_run_results.json
python3 manuscript/build_docx.py                # needs pandoc on PATH and python-docx
```

**To reject a fix:**

1. Set its `status` to `rejected` in `analysis/erratum_v1.1.csv`, or set the row's status in `analysis/src/new_source_rows.py`.
2. Rerun the steps above.

Only that fix's cells or rows revert. `check_numbers.py` will then fail until the manuscript's numbers are updated to match.

## Headline (the coded data v1.1, as reported in the manuscript)

- **Core propositions** (they restate the coded cells; all rates are reported over these because added propositions are selection-inflated):
  - 74 of 79 have documentary support;
  - 12 have two-organization agreement, mostly on shared records.
- **Independent corroboration:** 3–6 propositions, all in the Hugging Face unit. The lower end applies the stricter rule A10.
- **All 138 propositions:** 24 have two-organization agreement, 18 of them on shared upstream records; 9 gain a second organization by relay only.
- **Cells:** S0 is 41/4.
- **Operator halts:** 2, because the primary AISI Mythos 5 sample ended at its own token limit.

The first version's values are given in manuscript Section IV-I and, in full, in `analysis/v1.0_vs_v1.1_comparison.csv`.

## Authors

Khawaja Muhammad Laeeq (L1F23BSCS0080) and Mahnoor Iftikhar (L1F23BSCS1035).
