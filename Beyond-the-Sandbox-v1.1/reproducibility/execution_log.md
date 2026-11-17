# Execution Log

All runs were made by an AI system (Claude) in an isolated Linux container. No human ran these commands. The container's clock reads about one day behind the session date; timestamps below are the container's UTC clock.

## Environment

| Item | Value |
|---|---|
| OS | Ubuntu 24.04.5 LTS (Linux 6.18.44, x86_64, glibc 2.39) |
| Python | 3.12.3 (the version the package documents as tested) |
| Run 1 venv | `python3 -m venv /tmp/venv1`. Only `pip 24.0` is installed: no third-party packages and no cache reuse |
| Run 2 venv | `python3 -m venv /tmp/venv_clean`, then `pip install matplotlib==3.9.2`. The full list is in `clean_env_pip_freeze.txt` (matplotlib 3.9.2, numpy 2.5.4, pillow 13.0.0, contourpy 1.4.0, …) |
| Network | Not needed by any script. The container's egress is limited to package hosts and GitHub |
| Environment variables | None set beyond the defaults; `-I` (isolated mode) was used for every Python call |
| Input checksums | `original_checksums.sha256` (309 files). The frozen matrix's SHA-256 `972dcdd5…9b024` matches `freeze_v1.0.json` |

## Run 1: original package, unmodified, minimal environment

```
cp -r <package> /tmp/run1/
/tmp/venv1/bin/python -I experiments/scripts/reproduce_all.py
```

- Exit code: **1**. Wall time: **52.8 s**.
- 20 of 21 scripts exited 0. `n_refs` exited 1 with `ModuleNotFoundError: No module named 'matplotlib'`.
- `reproduce_all.py` reported that the `data/` hashes were unchanged (`True`).
- Standard output and error are saved in `runs/run1_original_stdout.txt` and `runs/run1_original_stderr.txt`. Standard error was empty.
- Regenerated `results/` files were compared byte by byte with the shipped files. Eleven differ, and on inspection every difference is a line ending (CRLF in the shipped files, LF regenerated) or the timestamped `run_log.md`. No numerical discrepancy was found.
- There were no encoding errors in the original scripts. Our own first attempt to read `source_cache/R24.txt` as UTF-8 failed; the file is cp1252. The original scripts use another route and are not affected.
- There were no missing files or warnings.

**Cause of the failure.** matplotlib is an optional dependency for one figure. `reproduce_all.py` looks for a repository `.venv` that is not shipped and otherwise falls back to the current interpreter.

**Correction.** The scripts were not changed. The second environment installs the documented optional dependency (`matplotlib>=3.5`, pinned here to 3.9.2).

## Additional findings while comparing results to the manuscript

- `results/rule_variants.csv` gives V2 (the manuscript's S2) as 1 documented, against 0 in the manuscript. `results/analyst_r14_s2.json` records `stored_partial_support_HF_D4 = ""` and `S2_documented_with_R14_1b_applied = []`.
- `results/loso.csv` gives 23, 31 and 33 documented cells after dropping R08, R02 and R10; the manuscript reports 21, 30 and 33.
- `reproducibility/independent_verify.py` reproduces the manuscript's 0, 39/6 and 21/30/33 **only** after applying the partial-support assignments stated in the manuscript text. With the stored (empty) assignments it gives 1/44 for S2 and 40/5 for S3.

## Run 2: clean rerun of everything, documented environment

```
python3 -m venv /tmp/venv_clean && /tmp/venv_clean/bin/pip install matplotlib==3.9.2
/tmp/venv_clean/bin/python -I reproducibility/clean_run.py reproducibility/clean_run_results.json
```

`clean_run.py` copies `original/`, `analysis/` and `reproducibility/` into a new temporary directory and deletes every generated analysis output there. It then runs the steps below and writes `clean_run_results.json`.

| Step | Exit | Seconds |
|---|---|---|
| `reproduce_all.py` (original package) | 0 | 51.9 |
| `analysis/src/build_analysis.py` | 0 | 0.8 |
| `analysis/src/prior_work.py` | 0 | 0.0 |
| `reproducibility/independent_verify.py` | 0 | 0.0 |
| `reproducibility/evidence_audit.py` | 0 | 0.2 |

- The original tree matched the 309-file snapshot before the run, and no coded data or protocol file changed during it.
- `reproduce_all.py` rewrote files in its own `results/` and `figures/` folders, as designed (line endings, timestamps, PNG).
- The regenerated analysis tables are **byte-identical** to the committed ones.
- Every published value checked matches except one: the N-branch count is 3 recomputed against 2 published. The recount counts Hugging Face's qualified N and the manuscript does not, so this is a definitional difference, not an error.

## Repairs made

No original file was edited. All new code lives in `analysis/src/` and `reproducibility/`. The only fix to new code was to the publication-date parser used for display: it mis-read the R24 incident ID as a date and missed the "July 27, 2026" form. The fix was made before run 2. Counts were unaffected.

## Run 3: second-pass rerun (container clock 2026-11-12T06:14Z)

The rerun used the same `/tmp/venv_clean` environment and the same `clean_run.py` command. It came after the second-pass edits: the wording of two rows in `prior_work.py`, and the manuscript text.

- Every step exited 0.
- The original tree matched the snapshot, and no coded data or protocol file changed.
- The regenerated analysis tables are byte-identical to the committed ones.
- The published-value check differs in one item, as before: the N-branch count is 3 recomputed against 2 published, a definitional difference.

## 2026-11-13: v1.1 run (Windows 11, Python 3.12.10, matplotlib 3.11.2, pandoc 3.14)

Every script was rerun in order (log: `reproducibility/runs/run_v1.1_2026-11-13.txt`). All exited 0:
build_matrix_v1_1, build_analysis, cell_recount, make_comparison, prior_work, make_figures, check_numbers (369 numbers, all ok),
make_review_packet, independent_verify, evidence_audit, build_docx (DOCX only; no LibreOffice, so no PDF).

The clean run (`clean_run_results.json`) copied the package to a temporary directory, deleted every generated output, and reran
every step. Results:
- all steps exited 0;
- the regenerated analysis tables are byte-identical to the committed ones;
- no coded data or protocol file in `original/` changed;
- all 309 files in `original/` still match `original_checksums.sha256`.

**Encoding note.** On Windows, two original scripts (selection_frame, analyst_round13j) fail under the default cp1252 encoding,
because they read UTF-8 files without naming the encoding. They pass in UTF-8 mode, and they passed on Linux in the supplied
package. `original/` was not edited. Instead, `reproducibility/run_original_utf8.py` runs `reproduce_all.py` with UTF-8 mode
passed to its child scripts, and the clean run uses it on Windows.

**Independent recount.** It matches 25 of the 26 published v1.0 values. The exception is D5 N, published as 2 and recounted as 3.
That difference is already in the supplied package: the published figure counts only unqualified N codes.
