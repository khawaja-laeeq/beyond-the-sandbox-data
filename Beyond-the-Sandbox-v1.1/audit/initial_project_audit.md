# Initial Project Audit — *Beyond the Sandbox*

Audit date: 2026-11-12. Auditor: AI system (Claude Opus 5.5) working for the author. No human auditor took part. Everything below was established by reading the files in `beyond-the-sandbox-repro-2026-11-11.zip` and the uploaded manuscript PDF; nothing was reconstructed from memory.

## 1. Files discovered and their purpose

The package holds 309 files. They were copied unchanged into `original/`, and a SHA-256 snapshot of every file is in `reproducibility/original_checksums.sha256`. The uploaded manuscript is preserved as `original/manuscript_2026-11-11_as_uploaded.pdf`.

| Area | Files | Purpose |
|---|---|---|
| Manuscript (latest) | `manuscript_2026-11-11_as_uploaded.pdf` (26 pp., Chromium render, 11 Nov) | The version under revision |
| Manuscript (older) | `draft.md`, `manuscript/round14_paper.tex/.pdf/.bib`, `latex/agents_round14_build/` | Round-14 text (9 Nov). Not the uploaded version |
| Frozen case study | `experiments/protocol/coded_evidence_case_study_v1.0.csv`, `codebook_v1.0.csv`, `freeze_v1.0.json` | The 45 cells and codebook, frozen 9 Nov. The matrix SHA-256 matches the freeze record (`972dcdd5…`) |
| Working data | `experiments/data/coded_evidence.csv` (identical to the frozen file), `coded_evidence.baseline.csv` (V11 baseline, 38/7), `sources.csv` (R01–R70), `codebook.csv`, `units.csv`, `anchor_checks.csv`, `number_ledger.csv` | Inputs to the scripts |
| Human baseline | `inputs/V11_*.csv`, `inputs/Beyond_the_Sandbox_V11_Professor_Submission.pdf` | The human coder's V11 coding, used by rule S6 |
| Scripts | 58 files in `experiments/scripts/`, entry point `reproduce_all.py` (runs 21 scripts) | Recounts, checks, tables, figures |
| Results | 47 files in `experiments/results/` | Outputs cited by the manuscript |
| Source cache | 73 text files, 4 PDFs and figure assets in `experiments/source_cache/` | Cached texts used for quotation checks |
| Prior work | `research/fulltext/` (Raftari, Bouke, Amundsen: PDF and text) | Full texts of the three closest papers |
| Reviews | `reviews/round_1…14`, `manual_*` | Model-reviewer and manual review notes from earlier rounds |
| Archive | `experiments/archive/` (incl. `second_coder/`) | Earlier codings and drafts |
| Brief | `brief.md` | The study brief (scope change of 9 Nov) |

## 2. Missing or inaccessible files

1. **The editable source of the uploaded manuscript is missing.** `draft.md` and `round14_paper.tex` are the round-14 text. They say "only one cell has whole-proposition support from two organizations" (S0/S1), whereas the uploaded PDF says zero. The revised manuscript is therefore rebuilt from the PDF's text (see `manuscript/`).
2. **Two cached sources hold no usable text, and others are binary or absent.** R01 and R05 returned HTTP 403 in the original study, and the cached `R05.txt` is binary. Of the 70 ledger entries, 57 have readable text caches, 5 have binary or garbled caches and 8 have none (`reproducibility/source_verification.csv`). No frozen cell rests on an unreadable source.
3. **`R24.txt` is cp1252, not UTF-8.** A UTF-8 reader fails on it (byte `0xb7` at position 8450). The revision's scripts handle this explicitly.
4. **`lib/documentary.py` and `lib/protocol.py`, named in `requirements.txt`, are not in the package.** They are repository checkers and are not called by `reproduce_all.py`.
5. **Three relevant sources dated before the cutoff are absent from the ledger** (`analysis/sources_missing_from_ledger.csv`). They are OpenAI's 4 Aug 2026 first-party post on the AISI GPT-5.6 Sol actions, the Alazab & Waheed preprint (19 Oct 2026), and JFrog's vendor statement. They were not added to the frozen matrix.

## 3. Research questions and findings (as uploaded)

- **RQ1 (access):** D1 is documented in 8 of 9 units; Artifactory D1 is unknown.
- **RQ2 (authorization belief):** D2 is the least documented dimension (5 documented / 4 unknown under S0; 1 / 8 under S1). Only Hugging Face D2 is verbatim and contemporaneous.
- **RQ3 (detection and stopping):** All 9 D4 cells are documented, and activity stopped through six mechanisms.
- **RQ4 (effects):** C appears in 7 units, P in 4 and N in 2 (unqualified).
- **Headline:** "No claim has whole support from two organizations" (S2 = 0/45).

## 4. Current research limitations (as stated)

The study has a single human coder plus AI revisions and no independent second coder. Its nine units are dependent and purposively selected. Support is concentrated: 37 of 40 documented cells cite one reference, and R08 alone supports 19. D2 depends on which kinds of evidence are accepted.

## 5. Reproducibility risks found

| # | Risk | Evidence |
|---|---|---|
| R-1 | **The headline S2 = 0 is not computed from stored data.** `partial_support` is empty for every cell in the frozen file. The shipped scripts therefore give S2 = 1 (INC-OAI-HF/D4); zero requires judgment R14-1b "applied in memory". | `results/analyst_r14_s2.json`; `results/rule_variants.csv` (V2 documented = 1) |
| R-2 | **`round14.py`'s idempotence guard prevents the partial assignment from being written.** It checks whether "R14-1b" is already in `change_log` before setting `partial_support`, so after the text was added once, the field is never written again. | `scripts/round14.py` lines 43–49 |
| R-3 | **The manuscript's S3 (39/6) and leave-one-source-out (21/30/33) come from no shipped script.** They need partial-support assignments (HF D4: R02, R03; Opus 4.7 D4/D5: R25) that exist only in the manuscript text. `results/loso.csv` gives 23/31/33. | `results/loso.csv`; manuscript §IV.F, Appendix E |
| R-4 | **The figure script needs matplotlib.** `reproduce_all.py` exits 1 in an environment without it (`n_refs`). It is documented as optional. | run 1 |
| R-5 | **The scripts write into `results/` in place.** Regenerated files differ from the shipped ones only in line endings (CRLF to LF) and timestamps. | run 1 diff |
| R-6 | **The Data Availability sentence overstates what the scripts cover.** It says the scripts "regenerate every count reported here", which is untrue for R-1 and R-3. | manuscript §VIII |
| R-7 | **The manuscript misdescribes the AI review.** The AI-use statement calls the model reviewers "independent". | manuscript, Disclosure of AI Use |

## 6. Manuscript-versus-data inconsistencies

1. **S2.** The manuscript says 0/45 and the stored data give 1/44 (R-1).
2. **S3 and leave-one-source-out.** The manuscript's values depend on partial assignments that are not stored (R-3).
3. **The headline changed between rounds through an AI-agent judgment.** The round-14 draft said one cell (HF D4) had two-organization support; the uploaded paper says zero. The change came from judgment R14-1b.
4. **The scope differs from the package's own brief.** `brief.md` (9 Nov) moves the paper to a survey layer and says the 0/45 count must not appear in the abstract, introduction or conclusion. The uploaded PDF leads with it. This revision keeps the uploaded paper's scope (the 9-unit study), as instructed, and records the conflict.
5. **One N-branch count depends on an unstated choice.** "N in two units" counts unqualified N only; the data list N for three units, one of them qualified (HF). This is consistent once stated.
6. **One unit's role tag is doubtful.** AISI Mythos 5 D2 is tagged I (investigator), but it rests on R26, which the model developer wrote using the evaluator's records.
7. **A DOI may be wrong.** Amundsen's DOI is cited as `…22981990`; the paper's PDF states `…22981991`. This may be a concept-versus-version DOI and needs checking.
8. **A suspected error was cleared.** The METR author list (Greenblatt, Cotra, Wijk), flagged earlier as uncertain, is confirmed by R07.

## 7. Baseline numerical results (reproduced)

Clean run 1 used Python 3.12.3 on Ubuntu 24.04.5 with no extra packages. `reproduce_all.py` exited 1 after 52.8 s: 20 of 21 scripts passed and `n_refs` failed for lack of matplotlib. The data hashes were unchanged, and every regenerated result matched the shipped file apart from line endings.

The headline statuses reproduce:

- S0: 40/5
- S1: 36/9
- S6: 37/8
- S7: 38/7
- S8: 37/8
- S9: 3/42

The counts that depend on partial support (S2, S3 and leave-one-source-out) reproduce only after applying the partial assignments stated in the manuscript text. `reproducibility/independent_verify.py` confirms this.

## 8. Plan for strengthening the research without changing evidence

1. Keep the frozen 45 cells untouched. Build the proposition layer as a separate dataset with its own coder label.
2. Decompose each cell into propositions, and code every source passage that bears on each one with an explicit relation and evidence base. Check every quote against the cache by script.
3. Define organization and independence rules before counting, and report agreement and independence separately.
4. Recount under declared sensitivity rules, including the original whole-cell rules with stored and with manuscript partial support.
5. Read the prior-work full texts, and search for other work dated before the cutoff.
6. Recompute the published numbers with independent code, audit at least 15 cells by a fixed selection procedure, and verify the source ledger.
7. Revise the manuscript only where the new analysis requires it. Record every changed conclusion in `CHANGELOG.md`.
8. Label all new coding as AI-assisted and list what needs a human.
