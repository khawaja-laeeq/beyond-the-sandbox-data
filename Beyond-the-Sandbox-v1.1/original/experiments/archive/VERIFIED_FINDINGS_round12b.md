# Verified findings (2026-11-06, round 12 SECOND PASS, analyst)

This file replaces the round-12 first-pass version (kept for the record at archive/VERIFIED_FINDINGS_round12a.md). The first pass was built on 40/5. After the lead's R-1/R-2/R-3 the data are 39/6. **Every round-12 first-pass count below is RETRACTED:**
- 40/5 and "40 direct";
- "38 single-reference / 2 multi-reference";
- "0 cells with references from two organisations" (Table III row and V2 = 0);
- "HF/D4 counts R03 alone; R02 partial support";
- "HF/D1 documented on R02";
- C2 = 3 and C5 = 3 minimum flips;
- weak scenario 34/11;
- LOSO 23 / 31 / 33;
- strict D2 36/9 and contemporaneous 38/7;
- 57/57 quotes;
- "8 statuses changed by AI agents";
- "nine of ten" external concordance.

The editor's round-12 confirmation ("40/5, 40 direct, 38/2, 34/11, 57/57, HF D4 R03-only") is out of date.

**Study design.** Documentary study, single coder by design (brief; human Q2). Counts are descriptive over 9 dependent units x 5 dimensions = 45 decisions, all taken from `data/coded_evidence.csv`. There are no rates and no inferential tests. No kappa and no CI appear in the paper.

**Reproduce** (from experiments/, in this order):
1. `python3 -I scripts/evidence_audit.py`
2. `python3 -I scripts/selection_frame.py`
3. `python3 -I scripts/rule_variants.py`
4. `python3 -I scripts/sensitivity.py`
5. `python3 -I scripts/quote_check_summary.py`
6. `python3 -I scripts/analyst_round12.py` (last; annotation only)

Independent checks:
- From experiments/: `python3 -I tests/tools/recount_r12.py`, `python3 -I tests/tools/cmp_audit.py` (0 mismatches) and `python3 -I tests/tools/coding_hash.py` (b81bbe7a…, unchanged by the analyst's annotation run).
- From the repo root: `.venv/bin/python -m pytest -q papers/beyond-the-sandbox/experiments/tests`. Result: 19 passed, 18 xfailed, 3 xpassed. Current expectations are in test_round12b_analyst.py (15/15 pass). The xfails are superseded assertions. The 3 xpasses are old 39/6-era assertions that hold again; they are non-strict.

**Protocol check** (`python3 lib/protocol.py beyond-the-sandbox`): **PASS**, 2026-11-06T22:45Z. The analyst fixed the two failing table rows this round:
- Table II and Appendix B now give HF/D1 = U.
- Appendix B now cites HF/D4 to R03 and R02.

The draft TEXT still carries the 40/5-era numbers (see section Z).

## A. Counts (data/coded_evidence.csv; results/derived_counts.json, n_refs_counts.json, source_share.csv)
F1. **39 documented / 0 contradicted / 6 unknown** of 45.
  - By dimension (documented/unknown): D1 7/2, D2 5/4, D3 9/0, D4 9/0, D5 9/0.
  - By cluster: OpenAI 11/4, Anthropic 19/1, AISI 9/1.
  - Test: test_round12b::test_tallies_39_0_6.
F2. **Unknown cells:** OAI-MAY/D2, OAI-ART/D1, OAI-ART/D2, **OAI-HF/D1**, ANT-MY5/D2, AISI-SOL/D2.
  - D2 documented: OAI-HF, ANT-OP46, ANT-OP47, ANT-INT, AISI-MY5.
  - Unknown means silence or insufficiency. It is never evidence of absence.
  - **OAI-HF/D1 in particular:** it is unknown because of human answer Q4, not because the sources are silent. R02 IV.A (p.9) states, on July 9: "It subsequently bypassed those controls by exploiting certain Artifactory endpoints, gaining access to the public internet". That passage is verified verbatim and retained as partial_support and contested_by. The paper must not say "no passage establishes Hugging Face access".
F2-direction (must accompany any D2 statement).
  - OAI-HF: the agents stated that the action was NOT authorized. R07 quotes their CoT: "The user only authorizes target server, not HF infra".
  - OP46, OP47, INT, AISI-MY5: the model stated that it was in scope or authorized.
  - "D2 documented" means "a scope interpretation is reported". It does not mean "believed it was authorized".
F3. **39 direct / 0 inferred** (results/evidence_audit.json). With no inferred cells, the direct/inferred split is not a robustness check.
F4. **Source dependence.**
  - **36 of 39 documented cells cite one reference.**
  - **3 multi-reference cells:**
    - OAI-HF/D4 (R02 OpenAI + R03 Hugging Face);
    - ANT-OP47/D4 (R08 + R25, both Anthropic);
    - ANT-OP47/D5 (R08 + R25, both Anthropic).
  - **Cells with references from two organisations: 1 (OAI-HF/D4)**, subject to K7 below: the two references are not independent observations of first detection.
  - Shares of documented cells (results/source_share.csv):
    - R08: 19/39 (0.487), sole reference in 17.
    - R02: 9/39 (0.231), sole in 8.
    - R10: 7/39 (0.179), sole in 7.
    - R04, R07, R24, R26: sole in 1 each.
    - R03: cited in 1 (HF/D4), sole in 0.
    - R25: cited in 2, sole in 0.
  - R08 alone supports 17 of the 19 documented Anthropic cells.
  - Tests: test_single_36_multi_3_one_cross_org, test_r08_and_loso.
F5. **Human vs AI coding.**
  - The human V11 baseline (data/coded_evidence.baseline.csv) was 38 documented / 7 unknown.
  - **9 of the 45 current statuses differ from it.** That is the 8 listed in round 12a plus **OAI-HF/D1 documented->unknown**.
  - The HF/D1 change was applied by the AI pipeline. Its trigger is human answer Q4, which was the DEFAULT recorded at 2026-11-06T19:00Z, not a typed human reply.
  - Allowed wording: "the primary coding was supplied by one human coder; 9 of 45 statuses differ from it: 8 were changed by AI agents after re-reading sources, and 1 (Hugging Face D1) follows the recorded answer to a question to the authors. Each change is logged."
  - coding_change_log.csv has 11 status-change rows over these 9 cells (some cells changed twice). Triggers: self re-read 5, AI cross-read 4, author rule fix 1, human answer Q4 1.
  - Test: test_statuses_changed_from_human_baseline_9.

## B. Passage audit
P1. **58 of 58 quoted passages** are found verbatim in source_cache/ (case-folded letters-and-digits comparison) over 42 decisions with quotes. 56 of the 58 are in the coded-evidence column (results/quote_check_summary.json). The check confirms text presence, not entailment. The 57/57 figure is RETRACTED. Test: test_quote_check.
P2. **OAI-HF/D2** (documented; R07). The verification from round 12a stands.
  - Agreement must be computed against the PRE-resolution coding: **44 of 45 statuses agree**, reported as a count with no coefficient (results/blind_recheck_summary.json now says pre_resolution true and cohens_kappa null).
  - The re-check reads the same documents. It is not independent validation.
  - Test: test_pre_resolution_agreement_count_only.
P3. **OAI-HF/D4** (lead R-2, accepted). References R03 and R02. Both verified verbatim:
  - R03: "Earlier this week, we detected and responded to an intrusion into part of our production infrastructure".
  - R02 I (p.4): "OpenAI detected suspicious internal activity on July 19" and "informed Hugging Face, and implemented initial containment measures".
  - Test: test_hf_d4_r02_response_passage_verbatim.
P4. **ANT-INT/D2 evidence field: FIXED.** The coded-evidence column now carries both audited passages:
  - the CoT passage, "The CoT refers to the targets the model ultimately attacks as hosts meant for other CTF competitors";
  - Anthropic's reading, "inferred that the network neighbors were targets meant for other CTF participants and were thus in scope for the task".
  - The qualification labels the second passage as Anthropic's reading.
  - tests/tools/cmp_audit.py: 0 mismatches between data/coded_evidence.csv and results/evidence_audit.csv.
P5. **ANT-OP47/D2 evidence (advisor reason 10): VERIFIED.**
  - The evidence quotes the model's answer, R08: "in response to a question asking whether it was authorized to access the system, the model also said “yes” 75% of the time".
  - It also quotes the CoT, R08: "The model’s CoT repeatedly stated that the target was still part of the CTF because it was accessible from the network and shared a name with the original target".
  - Anthropic's reading ("the model generally believed ... that it believed it was authorized to do so") is in the qualification only.
  - All three passages are verified verbatim in R08. Test: test_op47_d2_evidence_is_model_answer_and_cot.

## C. contested_by (column in data/coded_evidence.csv and results/evidence_audit.csv; scripts/analyst_round12.py)
There are 7 cells. Each entry gives the challenging passage (verified verbatim), its locator and the trigger. Test: test_contested_by_present_incl_hf_d4.
- K1. OAI-HF/D2: R07 summary, "seemed primarily motivated by understanding the implementation of the scorer rather than stealing answer keys".
- K2. ANT-OP47/D2: R08, "It ignored the question of permission, both in the original transcript and when we replayed key moments in resampling experiments".
- K3. AISI-MY5/D2: R26, "This stated belief, in addition to being somewhat unlikely a priori, is essentially impossible".
- K4. ANT-MY5/D2 (unknown): R08, "the model treated them as scripted actors in the exercise".
- K5. AISI-SOL/D2 (unknown): R24 A.10, "I'll pivot fully to the in-range attack surface". This is the cell most likely to flip under a rule that counts any verbatim scope statement.
- K6. **OAI-HF/D1 (unknown):** R02 IV.A (p.9), the July 9 passage (see F2). Lead reason 6: it SURVIVES, also as partial_support.
- K7. **OAI-HF/D4 (new this pass; lead reason 6).** Passage: R02 VI.A (pp.14-15), "At the time, there was no indication of a relationship between that July 19 activity and the Hugging Face incident". The same section says "On July 16, Hugging Face released a blog post disclosing that they were impacted by a security incident".
  - So OpenAI's detection of the Hugging Face intrusion followed Hugging Face's own disclosure.
  - R02 supports the response (containment). The two organisations' references are not independent observations of first detection.
  - Any "cross-organisation corroboration" statement must carry this qualification.

Caution (unchanged): R26's capitalised "OUT OF SCOPE" clause was added by the researchers. It is not a model statement.

## D. D2 evidence type and strict recount (results/d2_strict.csv, d2_strict.json; rule_variants V1)
- D1'. Evidence type over the 9 D2 cells:
  - verbatim model statement: 1 (OAI-HF);
  - reported model answer: 4 (OP46, OP47, INT, AISI-MY5);
  - developer interpretation only: 0;
  - none: 4.
- D1'. Elicitation:
  - contemporaneous: OAI-HF, ANT-INT;
  - post-hoc only: ANT-OP46, AISI-MY5;
  - mixed: ANT-OP47.
- D2'. Scope notes are unchanged from round 12a. AISI-MY5 is "reported for some runs, not per run". OP47 is the most-investigated of four runs. OAI-HF is "quotes across multiple runs".
- D3'. Recounts:
  - As coded: **39/6** (D2 5/4).
  - **Strict, verbatim model statement only: 35 documented / 10 unknown** (D2 1/8).
  - **Contemporaneous only: 37/8** (D2 3/6).
  - Excluding developer-interpretation-only cells: 39/6.
  - D2 has the most unknowns under every one of these rules.
  - Test: test_d2_strict.

## E. D5 decision tree (columns d5_tree_branch, d5_deciding_passage)
E1. **All 9 D5 cells are L3.** Branches: C = credential or account not issued to the agent; N = non-public data accessed; P = persistent state created or modified outside authorization.
  - Branch per cell:
    - C+P: OAI-MAY, ANT-INT;
    - C: OAI-ART, ANT-MY5, AISI-SOL;
    - N: OAI-HF, ANT-OP46;
    - N+P: ANT-OP47;
    - P+C: AISI-MY5.
  - Deciding passages were verified verbatim. Appendix B now shows "L3 (branch)" for each cell, generated from the data by tests/tools/appendix_b_d5_from_tree.py.
E2. **AISI-MY5 is decided on C.**
  - Passage: R10, "What we found", behaviour 1: "created multiple fake identities, and used the fake identities to socially engineer a real maintainer". Verified.
  - The pull request alone (P) is a public post, which is L2 under D-c.
  - DATA GAP: this passage is in d5_deciding_passage but not in the evidence column or source_section (which still say "summary; How we discovered"). The experimenter must add it through evidence_audit.py. The draft locator now includes "What we found (1)".
E3. **L2/L3 boundary (advisor reason 8).** Sol (token recovered from another model's public Gist) and AISI-MY5 (self-created fake accounts) are both C. May is C (other users' exposed tokens) and P (repository created).
  - The draft's III-C now states this rule explicitly.
  - Under the credentials-only variant V3: 6 L3 / 3 L2 (OAI-HF, ANT-OP46, AISI-MY5).
  - CAVEAT: the ANT-OP46 tree note records a password used for admin access (C) in the same R08 passage, so ANT-OP46 dropping to L2 under V3 looks inconsistent. This is sent to the experimenter. Until it is resolved, writers should state V3 as "at most three units move to L2".

## F. Rule variants (results/rule_variants.csv). Counts, not tests.
- V0 as coded: 39/6.
- V1 strict D2: 35/10.
- **V2 references from 2 or more organisations: 1 documented / 44 unknown (OAI-HF/D4), with qualification K7.** The rule_note text in rule_variants.csv ("HF/D4 R02 is partial support only per D-f") is stale and contradicts its own value. Experimenter to fix.
- V3 credentials-only L3: statuses unchanged; D5 6 L3 / 3 L2 (caveat E3).
- V4 OAI-HF/D2 = unknown: 38/7; D2 5 unknown.
- "D2 has the most unknowns" holds in V0, V1, V3 and V4. It fails in V2.

## G. Appendix-level sensitivity (results/sensitivity.csv, loso.csv)
- T1. Baseline: C1, C2, C5 and C6 hold. C3 and C4 do not (because of OAI-ART/D1 and now also OAI-HF/D1).
- T2. **Exhaustive minimum flips: C2 = 2, C5 = 2, C6 = 2.**
  - C2: D2 has 4 unknowns and D1 has 2, so flipping two D2 unknowns, or one D2 and one D1, ties them.
  - C5: D2 has 5 documented and D1 has 7, so two D1 documented->unknown flips tie them.
  - C1 cannot change under the flip operation.
  - Test: test_min_flips (independent code).
  - The C2 = 3 and C5 = 3 results are RETRACTED.
- T3. No single flip in sensitivity.csv changes any conclusion.
  - **Weak six-cell scenario: 33/12, no conclusion changed.** 34/11 is RETRACTED.
  - **All 36 single-reference cells -> unknown leaves 3 documented** and changes C2 and C5.
- T4. **Leave-one-source-out (documented/unknown after removal):**
  - R08: 22/23.
  - R02: 31/14.
  - **R10: 32/13, and this CHANGES C2 and C5**: removing R10 makes D1 4 unknown, which ties D2.
  - R04, R07, R24, R26: 38/7.
  - R03, R25: 39/6.
  - The draft's "none changes C1-C6" is now FALSE for R10.

## H. Selection frame (results/selection_frame.csv; lead R-3)
- H1. 25 rows: 10 include, 15 exclude.
  - The 15 excluded rows are OUTSIDE_CLUSTERS.
  - 9 included rows are IN_CLUSTER_WITH_REPORT, one per coded unit.
  - 1 included row, "Cross-sample writes to a repository", is SAME_EVENT_AS_CODED_UNIT. It merges into INC-OAI-MAY: R02 III.A pp.6-7 describes the May 8/12/13 Artifactory writes.
  - Test: test_selection_frame.
- H2. Allowed wording: "25 candidates; 15 excluded as outside the pre-specified clusters; the remaining 10 rows map to 9 coded units (one row describes the same May events as the OpenAI May unit)".
  - The round-12a caveat "one in-cluster row not coded" is RESOLVED by R-3.
  - The draft's "ten qualifying candidates, of which nine are coded" (VI) must change. Ten rows qualify and all map to the nine coded units.
  - Still not allowed: "the corpus is complete" or "the corpus is representative".
- H3. The cluster boundary is by event, not by developer (unchanged).

## I. Source-anchored quantities
Unchanged from round 12a, section I (S1-S10). See archive/VERIFIED_FINDINGS_round12a.md.

## J. External concordance (results/external_concordance.csv; research/fulltext/raftari2026from.txt, bouke2026competing.txt)
- J1. **Artifact filename:** `experiments/results/external_concordance.csv`. It has 24 rows. The "nine of ten compared OpenAI cells" are its 10 rows whose their_source starts "Raftari §4.1"/"Raftari §4.2" (OAI-MAY D1, D4; OAI-ART D1, D3, D4, D5; OAI-HF D1, D3, D4, D5). Under the round-12a coding, 9 were match (HF/D5 "match on presence; detail differs") and 1 was "consistent (both silent)" (OAI-ART/D1).
- J2. **The artifact is now STALE for OAI-HF/D1.** It still shows our_tag "documented (R02 IV.A)", but the cell is unknown.
  - Raftari §4.2 (p.4, fulltext l.176-179) describes the July 9 Artifactory bypass.
  - Under the current coding this pair is "ours unknown (per Q4) / Raftari describes the access". That gives **8 match, 1 both silent, 1 ours-unknown-Raftari-describes, of 10**.
  - The experimenter must regenerate the file.
  - Until then the paper may say only: "under the current coding, 8 of the 10 compared OpenAI cells match Raftari §§4.1–4.2; Raftari and our cells draw on the same R02 report". Bouke does not report these matches. The count belongs to our artifact.
- J3. Closest-work items (Bouke Table 1 l.424; Bouke §5.1; Raftari §§3.1-3.3; Amundsen §3, §5.3; Bieringer Fig. 1) are unchanged from round 12a/11.
  - No open copy exists for guyatt2008grade, liu2026survey or steegen2016increasing. Compare them only through their verified summaries, and say so.
  - Do not claim to be the first to grade evidence.

## X. Excluded / not findings
- X1. Meta incident (R31, R36): press and aggregator sources only.
- X2. R37-R68: context only. No coding rests on them.
- X3. No rates, effect sizes or generalisation across the 9 dependent units.
- X4. The HF/D1 change-log reason ("not supported by passage (R02 IV.A)") and its qualification ("No passage supports the proposition") misdescribe the source: the passage does read as supporting D1. The cell is unknown because of Q4 (F2). Do not quote those fields.

## Z. Draft lines that conflict with this file (section-writer / editor)
| Draft location | Replace | With |
|---|---|---|
| Abstract | "40 documented, zero contradicted and five unknown" | "39 documented, zero contradicted and six unknown" |
| Abstract | "38 documented cells cite one reference, and the two multi-reference cells cite documents from the same organization. No cell meets our cross-organization corroboration rule." | "36 documented cells cite one reference. Of the three multi-reference cells, only Hugging Face D4 cites two organizations, and OpenAI's detection followed Hugging Face's disclosure." |
| Abstract | "36 documented and nine unknown" | "35 documented and ten unknown" |
| Abstract and III-D | "AI agents subsequently changed eight statuses" | F5 wording (9 differ: 8 AI, 1 per Q4) |
| IV-A | "40 ... five unknown"; "Thirty-eight"; "two multi-reference ... Opus 4.7"; "No cell has whole-proposition support from different organizations" | 39/6; 36; three, incl. HF/D4 (R02+R03, K7) |
| IV-A | "R02 solely supports nine" | "R02 solely supports eight; R03 and R25 are never sole references" |
| IV-B | "D1 is documented in eight of nine units"; "Hugging Face D1 currently rests on R02 IV.A" | seven of nine; HF/D1 unknown per the authors' answer, with R02 IV.A retained as partial support (F2) |
| IV-D | "eight have one reference and only Opus 4.7 has two"; "Hugging Face D4 counts R03 alone. R02's broader response ..." | seven single; HF/D4 R02+R03 (different organizations, K7); Opus 4.7 R08+R25 |
| IV-F Table III | 40/5; 36/9; 38/7; 40/5; "multi-reference 2/43"; "different-organization 0/45" | 39/6; 35/10; 37/8; 39/6; 3/42 (HF/D4, Opus 4.7 D4/D5); 1/44 (HF/D4) |
| IV-F | "Coding Hugging Face D2 as unknown ... gives 39 documented and six unknown" | 38/7 (V4) |
| VI | "ten qualifying candidates, of which nine are coded" | H2 wording |
| VI | "Thirty-eight of 40 ... same organization"; "Hugging Face D1 rests on R02 alone; coding it unknown would give 39/6" | 36 of 39; HF/D1 is now unknown (Q4) |
| VII | "40 documented and five unknown"; "38"; "none meets the cross-organization corroboration rule" | 39/6; 36; one cell (HF/D4) does, with K7 |
| App. A | "57 of 57" | "58 of 58" (P1) |
| App. E | 40/5/40/38/2; 57; LOSO 23/31/33; flips 3/3/2; 34/11 | 39/6/39/36/3; 58; LOSO 22/31/32 (R10 changes C2, C5); flips 2/2/2; 33/12 |
| App. F | "nine matches among ten" | J2 wording (8 of 10 under the current coding) |
