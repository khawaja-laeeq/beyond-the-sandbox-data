# Reproducibility Report — *Beyond the Sandbox*

Prepared 2026-11-12 by an AI system (Claude) at the author's request. **This report is not an independent human audit.** "Independent" below means only that the verification code was written separately from the study's scripts.

## A. Audit scope

**Tested:**

- Execution of `reproduce_all.py` in two fresh environments.
- An independent recount of every headline number from the frozen CSVs.
- Consistency between the manuscript, the stored data and the scripts.
- That every quoted passage exists in the cached sources (60 original quotes, checked by the study; 194 new proposition passages and 26 disagreement passages, checked here).
- An AI-assisted entailment check of 22 cells.
- The source ledger: cache presence, readability, encoding and dependency flags.

**Not tested:**

- Live URLs, except R03: this environment's egress is limited, and R03 on GitHub returned HTTP 200 with matching content.
- The original human coding decisions themselves.
- Any claim about what happened on affected systems.
- Prior-work claims beyond the passages read.
- Human inter-coder reliability. There is no human second coder.

## B. Computational environment

Ubuntu 24.04.5 and Python 3.12.3, with no network access needed. Run 1 used no third-party packages. Run 2 added matplotlib 3.9.2 and its dependencies (`clean_env_pip_freeze.txt`). Everything else is standard library. Details and commands are in `execution_log.md`.

## C. Execution results

| Script | Run 1 (minimal env) | Run 2 (documented env) |
|---|---|---|
| `reproduce_all.py` (21 scripts) | **Exit 1**: 20 pass; `n_refs` fails (no matplotlib) | Exit 0 |
| `analysis/src/build_analysis.py` | — | Exit 0 |
| `analysis/src/prior_work.py` | — | Exit 0 |
| `reproducibility/independent_verify.py` | Exit 0 (standard library) | Exit 0 |
| `reproducibility/evidence_audit.py` | — | Exit 0 |

The coded data were unchanged by both runs. The regenerated analysis outputs are byte-identical to the committed ones.

## D. Numerical consistency

| Quantity | Manuscript | Shipped scripts (stored data) | Independent recount |
|---|---|---|---|
| S0 documented/unknown | 40/5 | 40/5 | 40/5 |
| S1 | 36/9 | 36/9 | 36/9 |
| **S2 (two-org whole support)** | **0/45** | **1/44** | 1/44 stored; 0/45 only with the manuscript's partial assignments |
| **S3 (one whole reference)** | **39/6** | not computed | 40/5 stored; 39/6 with the manuscript's partial assignments |
| S4 / S5 | 39/6, 39/6 | 39/6, 39/6 | 39/6, 39/6 |
| S6 (human-only) | 37/8 | 37/8 | 37/8 (from `V11_Coded_Evidence.csv` plus one human change) |
| S7 / S8 / S9 | 38/7, 37/8, 3/42 | same | same |
| Single-reference documented cells | 37 | 37 | 37 |
| R08 / R02 / R10 support (all/sole) | 19/17, 10/9, 7/7 | same | same |
| **Leave-one-out R08 / R02 / R10** | **21/30/33** | **23/31/33** (`loso.csv`) | 23/31/33 by "any reference remains"; 21/30/33 by the manuscript's rule plus its partial assignments |
| Stopping mechanisms | 3/2/1/1/1/1 | same | same |
| D5 branch units C/P/N | 7/4/2 | — | 7/4/3 (2 if the qualified HF N is excluded) |

**Verdict on the numbers.** Every published number can be regenerated. Three of them (S2, S3 and leave-one-out) can be regenerated only by applying partial-support judgments that exist in the manuscript text, not in the stored data or the scripts. The manuscript's statement that the scripts "regenerate every count reported here" is therefore inaccurate.

## E. Documentary verification

**Quotations.**

- The original 60 audit quotes are present in the cache, as the study reported; this was confirmed indirectly through the passages re-read below.
- All 194 new proposition passages and all 26 disagreement passages were found by normalized string match. The check is enforced: `build_analysis.py` exits non-zero on any miss.

**Entailment: 22 cells, AI-assisted** (`manual_evidence_audit.csv`). The 22 comprise all 5 unknown cells, the 10 changed or restored cells, the 3 multi-reference cells, 5 pre-named consequential cells (two of which overlap with the groups above) and 3 cells drawn at random with seed 20261112. Results:

- **Status:** 21 of 22 agree with the frozen status. The exception is INC-ANT-MY5/D2. It is still unknown under the frozen rule, but R25 holds a contemporaneous conditional permission quote that the cell never considered, so it needs a human decision.
- **Qualifications** needed in 5 cells:
  - INC-OAI-HF/D2: the out-of-scope quotes are curated from OpenAI's records and their run coverage is unstated.
  - INC-OAI-HF/D4: the cell rests only on combined partial support, which the stored data do not record. The operator's own account does document that the affected party detected first.
  - INC-ANT-OP47/D4: the run that stopped is unspecified.
  - INC-AISI-MY5/D4: the "operator halt" stopping mechanism is not entailed for the primary run, which ended at its own token limit.
  - INC-AISI-SOL/D4: that the evaluation-wide halt covered this run is an inference.
- **D5 branch readings** differ in 2 audited cells:
  - INC-OAI-HF/D5: P is present, and N does not need to be qualified.
  - INC-AISI-MY5/D5: C is coded inconsistently with INC-AISI-SOL/D5.

**Source ledger** (`source_verification.csv`, 70 entries):

- 57 readable text caches, 5 binary or garbled (none supports a coded cell), 8 with no cache.
- R24 is cp1252.
- Shared-record dependencies are flagged for R04, R06, R07, R25, R26 and the AI Incident Database entries.
- Three relevant pre-cutoff sources are absent from the ledger (`analysis/sources_missing_from_ledger.csv`).

## F. Discrepancies, questionable judgments and fixes

1. **S2 = 0 is not in the stored data.** Fix in the revision: report both values and make the partial judgment explicit. The frozen file is not edited.
2. **S3 and leave-one-out depend on unstored partial assignments.** Fix: as above.
3. **The Data Availability sentence is inaccurate.** It is rewritten in the revised manuscript.
4. **The "independent model reviewers" wording.** It is changed to "model reviewers from the same pipeline (not independent)".
5. **The AISI Mythos 5 stopping mechanism.** It is reported as a sensitivity row and in the text.
6. **D5 branch under-coding.** P appears in the sources for Artifactory, Hugging Face and Opus 4.6. N appears for Anthropic Mythos 5 and the internal model, at medium confidence. C is coded inconsistently between AISI Mythos 5 and Sol. These are reported as AI-assisted flags that need a human; the frozen branches are not changed.
7. **The zero-corroboration headline rests partly on which references were attached to cells.** Over the full cached corpus, three documented cells have whole support from two organizations: INC-OAI-ART/D5, INC-AISI-MY5/D1 and INC-AISI-MY5/D5. None of the three rests on independent records.
8. **The "I" role tag for INC-AISI-MY5/D2 is questionable**, because R26 is the developer analysing the evaluator's records.
9. **Amundsen DOI suffix:** `…990` cited, `…991` in the PDF.

## G. Residual limitations

- **No human verification.** All new coding and all entailment judgments are by an AI system. The proposition split itself involves judgment, and 3 of the 138 propositions are low-confidence.
- **Independence is judged from what each source says about its own records.** Raw logs could not be compared.
- **Live web verification was not possible** for 69 of the 70 ledger URLs.
- **The cached sources are the study's snapshot.** Later edits to those pages are not detected.
- **Possible further gaps in the corpus.** The ledger misses at least three relevant pre-cutoff sources, so the corpus-level counts may change if they are added.

## H. Verdict

**Computational reproducibility: partially computationally reproducible.**

- Every script runs in the documented environment.
- Every number in the manuscript can be regenerated.
- But the headline S2 = 0, S3 and the leave-one-out counts are not produced by the shipped scripts from the stored data. The upgrade path is to store the partial-support assignments and add them to a script.

The revision's own computations (proposition layer, independent recount, audit tables) **are** fully computationally reproducible from `original/` plus `analysis/src/`.

**Documentary verifiability: partially verifiable, AI-assisted only.**

- Every quoted passage can be traced to a cached source, and the cached texts are shipped.
- Entailment judgments have been checked only by an AI system.
- The documentary analysis should not be called independently verified until a human auditor repeats the 22-cell audit and a blind second coder recodes a sample of the propositions.

A computational recount is not a scientific replication.
