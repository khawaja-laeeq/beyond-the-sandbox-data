# beyond-the-sandbox: reproducibility package

Data, coding and scripts behind the paper *Beyond the Sandbox*. The folder layout matches the authoring
repository, so the scripts run unchanged.

## Run

Python 3.10+, standard library only (matplotlib for one figure, `n_refs.py`). No network access.

    python -X utf8 beyond-the-sandbox/experiments/scripts/reproduce_all.py

It re-runs every recount and check script, prints sha256 for each `data/` and `results/` file, and reports
whether `data/` changed (it should not). Compare its output with `beyond-the-sandbox/experiments/results/` as shipped:
every file except `run_log.md` (timestamps) should be byte-identical. PNG figures can differ in bytes across
matplotlib versions; the counts they draw are in `results/n_refs_counts.json`.

## What is where

| What | File(s) under `beyond-the-sandbox/` |
|---|---|
| 45-cell coded matrix | `experiments/data/coded_evidence.csv`; frozen copy and hash in `experiments/protocol/` |
| Codebook | `experiments/data/codebook.csv`; frozen `experiments/protocol/codebook_v1.0.csv` |
| Original human coding (V11) | `inputs/V11_*.csv`, `experiments/data/coded_evidence.baseline.csv` |
| Source ledger | `experiments/data/sources.csv`; fetch metadata `experiments/source_manifest.csv` |
| Selection frame | `experiments/results/selection_frame.csv` (`scripts/selection_frame.py`) |
| Change log and provenance | `experiments/results/coding_change_log.csv`, `change_provenance.csv`, `provenance_net.json`, `audit_trail.csv` |
| Quoted-passage audit | `experiments/results/evidence_audit.csv`, `quote_check_summary.json`, `anchor_check.json` |
| Rule variants and sensitivity | `experiments/results/rule_variants.csv`, `sensitivity*.csv`, `appendix_e_flips.csv`, `loso.csv` |
| Manuscript the table checks compare against | `draft.md` |
| Scripts | `experiments/scripts/` (entry point `reproduce_all.py`) |

## Not included

- **Third-party source texts.** See `beyond-the-sandbox/experiments/SOURCES.md` for URLs, hashes and how to rebuild them.
- **Full texts of related papers.** Cite and fetch them from their publishers.
- Internal review rounds, pipeline logs and superseded drafts.

`experiments/results/blind_recheck*.csv` is an AI re-check of the coding, not human second coding.

127 files.
