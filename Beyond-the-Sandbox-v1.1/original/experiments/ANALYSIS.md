# Analysis log (analyst)

## 2026-11-06 round 11 (newest first)
- Protocol check (lib/protocol.py beyond-the-sandbox): PASS, 39/0/6, no failures. Warnings: single coder by design; R01/R05 403; 36 sources not re-verified.
- Blind entailment re-check (lead task, reason 3). Judged all 45 cells from Appendix A, codebook.csv, the Appendix B propositions and source_cache/ before opening tags or notes. Output: results/blind_recheck.csv (scripts/blind_recheck_build.py; all 45 deciding quotes found verbatim). Result 40 D / 5 U / 0 C, all documented cells direct. Compared with scripts/blind_recheck_compare.py: 44/45 agree, kappa 0.897 (bootstrap 95% CI 0.56-1.00, n = 45). Limits: AI re-check, not strictly blind (the analyst had seen the tags), same sources. It is not a human second coder.
- Disagreement OAI-HF/D2: R07 quotes the agents' own CoT ("The user only authorizes target server, not HF infra"; "is it ethical and in scope for my task?"). The round-7 unknown recode rested on reading R07 as a scorer objective only. The archived codex coder also had it documented. Sent to the experimenter; F2 "no OpenAI unit" is marked challenged.
- Direct/inferred: data 39/0 (evidence_audit.json, coded_evidence.csv). The draft still says 37/2 (l.84, 112, 146, 272, 276, 385; Table III asterisks; Table IV inferred column). Draft l.84 contradicts R08 (R08 does report the model's own authorization answers and CoT). F3' retracted. The editor's request to regenerate evidence_audit.json "to show 37/2" was refused: that would change data to match the paper.
- Quote check rerun (scripts/quote_check_summary.py): 56/56 (was 52/52). Draft l.236, 388 and the Appendix E table (l.403) are stale.
- Table V vs T5: matches (C2 4, C3 1, C4 1, C5 4, C6 2, C1 cannot change). §IV-G eight-cell scenario (31/14) and Table IV inferred column are stale; current results/sensitivity.csv gives six weak cells, all six -> 33/12, no change; discount inferred column = 39.
- Change log: added trigger / trigger_evidence / blind_recheck_agrees (scripts/change_log_triggers.py). 9 status changes: self re-read 5, AI cross-read 3, author rule fix 1; the re-check agrees with 8/9.
- Selection frame: 25 rows; 9 include (MET), 16 undetermined (NO_SOURCE_ENTRY), 0 excluded.
- ART D3/D5 in coded_evidence.csv already match Appendix B (R02 III.B); no edit needed, and coded_evidence.csv was not edited (lead instruction).
- Tests: tests/test_round11_analyst.py (6 tests, PASS); the round-10 37/2 test is marked xfail(strict) as superseded. 12 passed, 1 xfailed.
- Side note for the experimenter: R3 effect levels put AISI-SOL/D5 at L2, but its deciding passage is authentication to a GitHub account with a leaked token, which the L3 definition ("accounts ... accessed") covers. AISI-MY5 created fake accounts, which is also borderline L2/L3. Check this.

## 2026-11-05 round 8 (newest first)
- protocol/documentary PASS; tallies 40/0/5; derived_counts consistent. Draft still says 41/36/35.
- Verified R02 (HF/D1) and R08 (MY5/D2 recode). ANT-INT/D2 also a simulation belief (open).
- audit_trail has 5 rows; sufficiency_review is automatic; change-log RULE not rewritten; figures predate recode.
- Not done: re-run sensitivity; reopen R24.

## 2026-11-02 round 3
- Ran protocol.py (PASS) and documentary.py (kappa 0.789, agreement 0.978, AI coder, 5 recodes vs baseline). Re-ran consistency.py and number_audit.py: both OK.
- Re-read cached sources: R10 122/10/19 and 17+2 verbatim; R08 monitor ~1% (CoT present) vs ~50% (CoT stripped) is one replay under two conditions; OP46 abort, CTF belief, token budget verbatim; OAI-MAY D5 text states linkage unproven, and D5 codes an effect, so it is correct as coded.
- Wrote data/coded_evidence_v12.csv (identical to coded_evidence.csv; the five recodes were already applied) and results/coding_change_log.csv via scripts/make_change_log.py. No further code changes: no source contradicts any code.
- Open issues: (1) number_ledger N35 says 35 sources but sources.csv has 42; (2) N14 claim text should state "about 1% of actions flagged, CoT present" neutrally; (3) draft.md is a stub, so no draft claims could be challenged and the draft number audit is vacuous until a draft exists; (4) OAI-HF D1 rests on R01 alone, which returned 403, so it is unverified this round; (5) kappa depends on rare cells, so report raw agreement too.
- Not done: did not open R37-R42 or fetch live primary URLs; relied on the cache.

## 2026-11-02 round 4
- protocol.py FAIL (kappa 0.542; draft '36 decisions' vs 45). documentary.py agrees. Re-ran agreement.py (n=45, 42/45, 0.542), consistency.py OK (44 sources), number_audit.py: draft has 0.789, 0.978, 36, 42, 5.5 not in ledger.
- Corrected VERIFIED_FINDINGS header (wrongly said PASS), source count 42->44; added section E (single-source cells HF D1/R01, Sol D5/R24; agreement wording).
- v12 rows HF/D1 and SOL/D5 still status=documented with no downgrade/change-log row; requested from experimenter.
- Draft still has [CITATION NEEDED]/[RESULT PENDING] throughout (lines 13,34,88,196,279,283) - not submission-ready. Did not re-open R01 (403).

## 2026-11-05 round 5
- protocol.py and documentary.py FAIL (kappa 0.542; n=45). Read agreement.json: values match; bootstrap CI [0,1] uninformative.
- Checked v12: only OAI-HF/D1 (R01) and AISI-SOL/D5 (R24) are sole-R01/R24 cells; both carry the downgrade. MAY D1/D3 cite R01+R02 (multi-source).
- Verified source passages in cache: R02 'on-call response staff advised that stopping the evaluation run was not required'; R08 'stated that it believed this third party was part of the CTF'; A30 'used it to authenticate to GitHub'. Wrote results/decision_rule.md, appended 3 quoted disagreement rows to coding_change_log.csv, agreement paragraph drafted.
- n_refs_counts: 37/43 single-source, contradicts draft 'only two'.
- Not done: did not re-run all scripts, did not audit new ledger rows (N42), R01 still 403.

## 2026-11-05 round 6
- protocol.py FAIL: brief says single coder, no kappa; draft reports kappa. documentary.py runs. Withheld all kappa findings from VERIFIED_FINDINGS (K0).
- Checked second_coding.csv directly: disagreements are SOL/D5, ART/D4, MAY/D5; OP46/D2 and MAY/D4 now agree. Corrected my J4 (K1). disagreements.csv and the change log (SUPERSEDED row) now consistent; Appendix B / draft not re-checked this round.
- quote_check.json: 0 NOT_FOUND (K2). Wrote scripts/make_v13.py and data/coded_evidence_v13.csv: D2 recodes ART, HF; support_type direct/inferred; not_independently_checked flag; ran, counts 36/5/4 (K3).
- Not done: passage-support review of primary cells; derived_counts/discount_table not regenerated on v13; draft.md not re-read for markers.

## 2026-11-05 round 7
- protocol.py and documentary.py PASS (41/0/4). Warnings: R01/R05/R43 403, R06 429, R18 no link.
- Spot-checked R02 cache: May tokens (lines 256-260) and "advised that stopping the evaluation run was not required" (284-286) support MAY/D5 and ART/D4. R24 and R01 not in cache, so SOL/D5 and HF/D1 cannot be checked. R08 gives only a simulation belief for MY5/D2.
- Wrote results/audit_trail.csv (5 rows only). The 45-cell audit and sufficiency_review.csv are NOT done. VERIFIED_FINDINGS section H added. sensitivity.csv read, not re-run. draft.md not re-read this round.

## 2026-11-06 round 9 (analyst)
Checked: `python3 lib/protocol.py beyond-the-sandbox` PASS (45 decisions, 39/0/6); tag_counts.csv matches VERIFIED_FINDINGS F1-F4 (cluster 11/19/9 documented; D2 4 documented, 5 unknown). Audit rows read: ANT-INT/D2 (R08: "inferred that the network neighbors were targets meant for other CTF participants and were thus in scope for the task"), AISI-MY5/D4 (R10 only, 2/2 passages; no R24 ref in coded_evidence, so the Appendix B "R10+R24" must be changed to R10), OAI-HF/D3 (R02 IV.B: code on 41 production dataset-server workers, root on at least one node), OAI-ART/D3 and D5 (R02 III.B, p.7-8, quotes verbatim in audit). Passage review now covers 45/45 decisions (52 passages), not 3/45.
Open issues: (1) ANT-INT/D2 is "direct" but AISI-MY5/D2 (also a developer's reading of model reasoning) is "inferred": the direct/inferred rule is not applied consistently; the rule should be stated as: direct = quoted passage reports an event or the model's own stated reasoning; inferred = the source's interpretation of unstated model belief. Under it, INT/D2 quote (model "inferred") is borderline. (2) Sensitivity does not include INT/D2 flip alone? T2 lists it; fine. (3) Single coder, no agreement statistic; audit verdicts are by the same coder (not independent validation).
Not checked: figures not regenerated (need approval).

## 2026-11-06 round 10 (analyst)
- protocol.py PASS (45 decisions, 39/0/6; warnings: R18 no link; R01/R05/R06/R43/R51/R53/R55 did not load). documentary.py runs; there is no second_coding.csv in data/ (single coder by design, Q2), so no kappa.
- New independent tests experiments/tests/test_round10_analyst.py, 7/7 PASS. They check the tallies 45/39/6, direct/inferred 37/2, single-source 36, R08 citing/sole 19/17, minimum flips C2=4 and C6=2 (my own brute force, not the project script), R02 passages for ART D3/D5 and HF D3 in the cache, and the selection-frame counts.
- The experimenter's direct/inferred recode is confirmed (OP47/D2 inferred). The draft is stale: "38 directly supported ... one inferred" (l.380), "one inferred decision" (l.191), "seven narrow or contested cells", 38/32 rows (l.200-208). These must become 37/2, eight cells, 31 documented.
- OAI-ART D3/D5: the evidence field already quoted R02, but the anchor_checks field still pointed to R07 anchors (A04 spoof, A06 message board). These were the stale propositions the advisor flagged. I added A51-A53 (R02; 1 hit each), re-pointed the cells, marked A04 SUPERSEDED, and logged 2 rows in coding_change_log.csv (scripts/round10_analyst_art.py). No status change.
- Section-writer premise corrected: the token-refresh mechanism (R02 III.B p.7) and the HF root access (R02 IV.B p.9) are verbatim in R02. They are supported, not unsupported. Omitting them is allowed; calling them unsupported is not.
- Built results/external_concordance.csv (25 rows; Bouke Table 1 mostly unaligned because of the interleaved extraction; HF row and Bouke §5.1 prose compared; Raftari §4-5 compared) and results/selection_frame.csv (scripts/selection_frame.py). See VERIFIED_FINDINGS G, H, I.
- Weak points still open: the sensitivity conclusions were chosen by the authors; the all-single-source scenario overturns C2 and C5; the selection rule was stated post hoc and OAI-ART is exactly at its threshold; the coder is also the auditor; 16 candidate incidents were not assessed.

## 2026-11-06 round 12 (analyst)
- protocol.py: FAIL. The only failure is the draft's decision table, which still has HF/D2 = unknown and HF/D4 = R02;R03. The data pass. documentary.py: no second_coding.csv (single coder, Q2).
- Re-ran quote_check_summary.py. The file was stale at 56; it now gives 57/57 (42 decisions with quotes; R07 2 new). evidence_audit.json also gives 57/57.
- New tests/test_round12_analyst.py: 12/12 PASS. Independent recomputation of:
  - 40/0/5, by dimension and by cluster;
  - 40 direct;
  - 38 single-reference / 2 multi-reference (OP47 D4/D5);
  - R08 19/17;
  - LOSO R08 23, R02 31, R10 33;
  - minimum flips C2 = 3, C5 = 3, C6 = 2 (C2 and C5 were 4);
  - pre-resolution agreement 44/45, kappa 0.897 (internal);
  - D5 all L3, logged;
  - d2_strict 36/9 and 38/7;
  - contested_by on 6 cells;
  - selection 25 = 10 include + 15 exclude;
  - 8 statuses changed from the human V11 baseline.
- 7 old tests in test_round10/11 are now strict xfail with the reason "SUPERSEDED round 12". They were kept, not deleted. Suite: 17 passed, 8 xfailed.
- New scripts/analyst_round12.py. It is idempotent, annotation only, and exits if any passage is missing. It does the following:
  - adds contested_by, partial_support, d2_evidence_type/elicitation/direction/scope_note and d5_tree_branch/deciding_passage to coded_evidence.csv;
  - adds contested_by to evidence_audit.csv;
  - writes results/d2_strict.csv/.json;
  - appends the AISI-SOL and AISI-MY5 D5 L2->L3 rows to coding_change_log.csv;
  - fills the missing trigger on the round-12 HF/D2 log row.
  - Backups are in archive/*_pre_analyst_r12.csv.
- Verified HF/D2 against R07 (agents' CoT verbatim). Agreed with the recode under codebook D2 (any reported scope interpretation). Flagged that its direction (not authorized) is the opposite of the other four documented D2 cells.
- Verified HF/D1 on R02 IV.A alone. Noted the literal conflict with human Q4 ("stays unknown").
- Checked HF/D4 (D-f). R02 also states a response ("informed Hugging Face, and implemented initial containment measures"), so "R02 = detection only" is true of the displayed quote, not of R02. Recorded this in contested_by and sent it to the lead. The conservative R03-only coding is kept.
- D5 tree: agree with 9/9 L3. AISI-MY5 is better decided on R10 "created multiple fake identities" (C) than on the pull request, which D-c's L2 "post" wording makes ambiguous. OAI-HF L3 rests on "customer content", and the passage does not state that it was private.
- D2 evidence types: 1 verbatim (HF) and 4 reported model answers. Two of the reported cells (OP46, AISI-MY5) rest only on post-hoc follow-up answers.
  - Trap avoided: R26's "is OUT OF SCOPE" text is a researcher-inserted compaction clause, not a model statement.
  - Contested passages found for OP47/D2 ("ignored the question of permission") and AISI-MY5/D2 ("essentially impossible").
- Problems found:
  1. round9.py overwrote the ANT-INT/D2 evidence after evidence_audit.py (tests/tools/cmp_audit.py, 1 mismatch).
  2. blind_recheck_summary.json now reports a post-resolution 45/45, kappa 1.0, and calls the primary coder human.
  3. The selection frame includes one in-cluster row that is not coded (D-b done-criterion unmet).
  4. The draft is entirely round-11 stale: 39/6, 36/3, L2 for AISI, C2 = 4, 33/12, 22/23, "one human coder made the primary coding".
- Not checked: figures (not regenerated by me), PDF build.

## 2026-11-06 round 12, second pass (analyst): after the lead's R-1/R-2/R-3 and the experimenter's rebuild

### Recount and tests
- Protocol at the start was FAIL on two draft-table rows (HF/D1 said D while the data say U; HF/D4 cited R03 while the data cite R02;R03). The analyst fixed both rows (Table II, Appendix B) and re-ran the check: **PASS** at 22:45Z.
- Independent recount (tests/tools/recount_r12.py): 39 documented / 6 unknown, 39 direct, 36 single-reference, 3 multi-reference (HF/D4 R02;R03, OP47/D4 and OP47/D5 R08;R25). These agree with derived_counts.json and n_refs_counts.json.
- tests/tools/cmp_audit.py: 0 mismatches. The ANT-INT/D2 overwrite defect is fixed.
- New tests/test_round12b_analyst.py holds the current expectations: 15/15 pass.
- The 16 stale 40/5 assertions in rounds 11 and 12 are marked as strict xfail "SUPERSEDED round 12 second pass" by tests/tools/mark_superseded_r12b.py. No test was deleted.
- Three round-10/11 strict xfails pass again now that the counts are back at 39/6 and 36. They are made non-strict.
- Suite: 19 passed, 18 xfailed, 3 xpassed.

### Lead task (1): contested_by on HF/D1, D2 and D4
- HF/D1 and HF/D2 were present.
- **HF/D4 was missing.** R-2 promoted R02 to a full reference, and the old challenge text went with it.
- Added in scripts/analyst_round12.py. Passage: R02 VI.A pp.14-15, "At the time, there was no indication of a relationship between that July 19 activity and the Hugging Face incident". It sits alongside "On July 16, Hugging Face released a blog post disclosing ..."; both were verified verbatim.
- Re-ran the script. tests/tools/coding_hash.py shows that status, reference, evidence and effect_level are unchanged (annotation only).
- The R02 July 9 passage ("It subsequently bypassed those controls by exploiting certain Artifactory endpoints ...", R02 IV.A, fulltext l.326-331) is kept as partial_support for HF/D1. Verified.

### Lead task (2): D5 column and III-C text
- Appendix B D5 cells were regenerated from d5_tree_branch as "L3 (branch)" by tests/tools/appendix_b_d5_from_tree.py.
- AISI-MY5's locator now includes R10 "What we found (1)", where "created multiple fake identities, and used the fake identities to socially engineer a real maintainer" occurs (verified; offset 8468 of the normalised text, under the "What we found" heading).
- The III-C (draft §III.C) D5 text now states the C/N/P branches and that recovered tokens (Sol) and self-created impersonation accounts (AISI-MY5) are both C. This addresses advisor reason 8.
- Data gap: the AISI-MY5/D5 evidence and source_section do not yet carry the fake-identity passage. Sent to the experimenter.

### Lead task (3): OP47/D2
- The evidence field quotes the model's answer ("yes" 75%) and the CoT. Anthropic's "generally believed" reading is in the qualification only. All three passages were verified verbatim in R08. No fix needed.

### Section-writer request
- The concordance artifact is results/external_concordance.csv (Raftari §4.1/§4.2 rows).
- It is stale for HF/D1: our_tag still says documented. Under the current coding it is 8 match / 1 both silent / 1 ours-unknown, of 10.
- ANT-INT/D2: the evidence field now matches the audited passages (cmp_audit 0).

### New issues
1. Removing R10 (LOSO) now changes C2 and C5 (32/13). The draft says no LOSO removal changes any conclusion.
2. Minimum flips fall to C2 = 2, C5 = 2 and C6 = 2.
3. rule_variants V2 rule_note is stale ("R02 partial support only") although its value is 1.
4. The V3 credentials-only variant moves ANT-OP46 to L2, but its tree note records a password used for admin access (C). This looks inconsistent.
5. The HF/D1 qualification and change-log reason say "No passage supports the proposition", which misdescribes R02. The cell is unknown because of Q4 (a default answer).
6. The response_stage for HF/D4 is still "affected-party detection and response" only, although R02 now supports OpenAI's containment.
7. The draft text outside the tables is still at 40/5 (full replacement list in VERIFIED_FINDINGS.md section Z).

- Not checked: PDF build and page count after these edits; figures.

## 2026-11-08 — Round 13 (analyst)

### Checks of the experimenter's round-13 work
- **Protocol** (`python3 lib/protocol.py beyond-the-sandbox`, 18:13Z): **FAIL**, one failure. The draft decision table has HF/D1 = unknown; the data say documented. `lib/documentary.py` gives the same result. The result files agree with the data.
- **Re-runs**: rule_variants.py, sensitivity.py and analyst_round13.py re-run from coded_evidence.csv. The experimenter's numbers reproduce:
  - 40/0/5 (D1 8/1, D2 5/4);
  - V1 36/9; V2 1/44; V3 0/2/7; V3b 0/4/5; V4 39/6; V5 39/6;
  - weak-support scenario 34/11; LOSO shows no change.
- **appendix_b_check.csv**: 45/45 equal=yes, and draft_refs is non-empty in all rows. This closes advisor reason 3 (references only).
- **Quotes**: 60/60 verbatim, covering 42 of the 45 decisions. The 3 decisions without a quote are unknown D2 cells. I re-checked the HF/D1 R02 IV.A quote myself by normalised matching (a line break sits inside the passage), along with R08 "installed on 15 third-party hosts" and R04 "harvested from the pod environment".
- **pytest**: 26 passed, 24 xfailed, 9 xpassed. The new tests/test_round13_analyst.py has 8 tests, all passing; they are independent recounts.
- **V3 from passages (lead task, reason 6)**: I read every coded D3 and D5 passage for type-C credential use myself. C appears in 7 units (MAY, ART, HF, OP46, ANT-MY5, INT, SOL), giving 0/2/7, the same as the branch field.
- **V3b check**: the branch field omits P for ANT-MY5, whose D3 passage ("installed on 15 third-party hosts") is P under S-2. It also counts HF on an N that is qualified. Read from the passages, the effect-only boundary gives the same 0/4/5 but a different set of units. I added it as V3c in rule_variants.py.
- **S-2 outcome**: AISI-MY5 is L2. The draft still calls its mapping "interpretive" and lists it as L3 (P+C). That text is stale.

### New result files (lead tasks)
- **V6** (reason 5; rule_variants.py) is V11 plus only the cell-specific human requests: ANT-MY5/D2 set to unknown (laeeq 2026-11-05), and HF/D1 net unchanged (Q4 then Q5). The result is **37/8**, with D1 9/0, D2 5/4, D4 7/2 and D5 7/2. D2-most-unknown still holds.
- **change_provenance.csv** (reason 5):
  - 12 distinct status events: human 3, lead 1, AI-agent 8. There is also 1 duplicate log row.
  - 16 reference changes.
  - 9 D5 level rows plus 2 S-2 rows. All levels were assigned by AI agents; V11 has no levels.
  - Net: 8 of 45 statuses differ from V11. 7 were changed by AI agents (one of them under the human's general passage rule) and 1 was requested by the human.
  - Classification choice: "author rule fix 2026-11-06" is classed AI-agent, because the rule was the human's but the judgement on the cell was an agent's. Human Q4 and Q5 answers are marked as defaults.
- **org_structure.csv** (reason 11):
  - Only 3 of 9 units have corpus documents from two or more organisations (OAI-ART, OAI-HF, AISI-MY5).
  - Only HF/D4 has whole support from two organisations.
  - partial_support is empty in all 45 cells, so partial-support counts are 0 everywhere.
  - V2 measures disclosure structure.
- **appendix_e_flips.csv** (reason 12): C1–C6 under both operations, with every minimal flip set:
  - C2 and C5: 3 flips (220 sets in both directions; 56 with documented→unknown only);
  - C6: 2 flips, exactly one set (ANT-MY5/D2 + AISI-SOL/D2);
  - C3 and C4: false at baseline, 1 flip (ART/D1);
  - C1: cannot change;
  - weak-support scenario: 6 cells listed, 34/11.

### Round-12 open issues
- Issues 1–4 and 6: resolved.
- Issue 5: resolved (the HF/D1 qualification is rewritten).
- Issue 7: the draft is still stale, now at round-12 numbers (39/6, 0/0/9, 0/3/6, 33/12, two flips). The full replacement list is in VERIFIED_FINDINGS.md section Z.

### Not checked
- PDF build and page count.
- Figures, including source_concentration.png, after the 40/5 change.
- selection_frame was not re-derived.

## 2026-11-08 round 13, analyst second pass (after the experimenter's 18:30Z message)
- `python3 lib/protocol.py beyond-the-sandbox` (18:34Z): FAIL, with one failure: draft Appendix B says INC-OAI-HF/D1 is unknown, but coded_evidence.csv says documented. The data are right (R02 IV.A passage found in source_cache/R02.txt; Q5/Q6). Only the draft is wrong. lib/documentary.py gives the same result. The single-coder warning is expected (Q2).
- Independent recount from coded_evidence.csv (my own csv code, not the scripts): 40/5; D1 8/1; D2 5/4; D5 baseline 0/1/8; V3 (C in branch) 0/2/7; V3b (N or P in branch) 0/3/6; V3b without HF's qualified N gives 0/4/5, which equals V3c. All match rule_variants.csv.
- Experimenter item 1 (ANT-MY5/D5 branch C;P): verified. "installed on 15 third-party hosts" appears verbatim in R08.txt. Level stays L3 because C decides. V3b changes from 0/4/5 to 0/3/6. In VERIFIED_FINDINGS, E3/E4/F/Z are updated and the old V3b 0/4/5 is retracted. Problem found: the V3c rule_note in rule_variants.csv still says "adds INC-ANT-MY5", which is no longer true now that V3b includes it. The count is correct; the note is out of date. Sent to the experimenter.
- Experimenter item 2 (two HF/D1 change-log rows): accepted. change_provenance.csv flags one row as DUPLICATE. test_provenance_classes counts 12 events excluding that row and passes.
- Experimenter item 3 (partial_support empty in all 45 cells): accepted. It is consistent with F5/V2 and stated as a limitation in VERIFIED_FINDINGS §F.
- External concordance: the 10 Raftari OpenAI rows recounted give 9 match (HF/D5 matches on presence only) and 1 where both are silent. Raftari §4.2 p.4 spot-checked in research/fulltext/raftari2026from.txt ("used Artifactory endpoints to bypass outbound network controls"). The draft's "eight of ten" is out of date.
- Tests: test_round13_analyst.py::test_v3b_v3c hardcoded 0/4/5 and failed. It is rewritten to recompute V3b from the branch field (it now asserts 0/3/6, and V3c = V3b minus HF = 0/4/5). Suite: 26 passed, 24 xfailed, 9 xpassed.
- Draft check: draft.md is still entirely at round 12 (39/6, 0/0/9, "credentials-only 0/3/6 with HF/OP46/AISI-MY5 to L2", 35/10, "eight of ten", HF/D1 "recorded author decision" at lines 5, 78, 102, 114, 138, 158, 172-178, 199, 217, 225, 265, 354). It must not go out until it follows VERIFIED_FINDINGS §Z.

## 2026-11-08 round 13, analyst third pass (after the experimenter's 18:40Z message)
- `python3 lib/protocol.py beyond-the-sandbox` (18:44Z): **FAIL**, with the same single failure as before: draft Appendix B lists INC-OAI-HF/D1 as unknown, but coded_evidence.csv says documented. Tallies: 40/5, D1 8/1, D2 5/4. This failure is in the draft only. The result files pass, so no finding is withheld because of it.
- Experimenter's V3c rule_note fix: verified. The note in rule_variants.py and rule_variants.csv now says V3c drops only INC-OAI-HF. Its unit list is INT, ANT-MY5, OP46, OP47, MAY (5 L3, so 0/4/5). V3b lists 6 units including HF (0/3/6). Re-running `python -I scripts/rule_variants.py` reproduces V3c 0/4/5, V5 39/6 and V6 37/8. VERIFIED_FINDINGS E4 is updated to remove the stale-note caveat.
- pytest: 26 passed, 24 xfailed, 9 xpassed (unchanged).
- Draft: still at round 12. Line 78 and the line 265 row say HF/D1 is unknown under a "recorded author decision". Line 158 and lines 172-178 give 39/6, 0/0/9, 35/10, "0/3/6 with HF/OP46/AISI-MY5". Line 354 says "eight of ten". It conflicts with VERIFIED_FINDINGS §Z. This is the only reason the protocol fails.
- Not checked: PDF build, figures.

## 2026-11-08 round 13, analyst fourth pass (after the protocol 18:47Z task and the experimenter's 18:49Z message)
- `python3 lib/protocol.py beyond-the-sandbox` (18:53Z): **FAIL**, the same single failure. The draft table says INC-OAI-HF/D1 is unknown; coded_evidence.csv says documented. `lib/documentary.py` gives the same result, and its tallies are 40/5 (D1 8/1, D2 5/4). The failure is in draft.md only, which was last modified at 17:49Z, before the round-13 recodes. No result file fails, so no finding is withheld. VERIFIED_FINDINGS keeps the "no draft text goes out" gate.
- The experimenter reported no data changes. Confirmed: coded_evidence.csv was last modified at 18:30Z and the result files at 18:45Z, the same as in the third pass.
- HF/D1 quote re-checked in source_cache/R02.txt l.329-331. The context (l.325-331) is the July 9 ExploitGym agent that precedes "B. ... Hugging Face compromise", so the passage is specific to this unit. R08 "a file listing a password, which it used to gain admin access to the system" (the OP46 C branch) is verbatim.
- Independent recount (my own code): 40/5. D5 is 0/1/8, with AISI-MY5 at L2. V3 is 0/2/7 and V3b is 0/3/6. LOSO: R08 23/22, R02 31/14, R10 33/12, R04 39/6, R03/R25 40/5. All match the result files.
- New caveat: the "contemporaneous-only 38/7" count includes OP47, whose d2_elicitation is "mixed". Strictly contemporaneous gives D2 2/7 and 37/8 in total. Added to VERIFIED_FINDINGS §D.
- pytest: 26 passed, 24 xfailed, 9 xpassed (unchanged).
- Draft: 10 occurrences of "39 documented"/"39/6" remain. §Z of VERIFIED_FINDINGS is the replacement list.
- Not checked: PDF build, figures.

## 2026-11-08 round 13, analyst fifth pass (after the 19:01–19:14Z inbox)
- `python3 lib/protocol.py beyond-the-sandbox` (19:17Z): **PASS**, 0 failures (40/5; D1 8/1, D2 5/4, D3–D5 9/0). lib/documentary.py agrees. The draft-only HF/D1 failure is resolved by the editor's revision (draft.md 19:06Z). The gate in VERIFIED_FINDINGS is lifted.
- Experimenter (contemporaneous_strict): ran `python3 -I scripts/analyst_round12.py` after snapshotting data/coded_evidence.csv and results/coding_change_log.csv to archive/*_pre_analyst_r13b.csv. A diff after the run showed 0 changed cells and an identical change log (the script is idempotent). d2_strict.json now has `contemporaneous_strict`: D2 2/7 (OAI-HF, INT), 37/8 in total, D2 still has the most unknowns. `contemporaneous_only` stays 3/6, 38/7, and its label notes that it includes "mixed". Confirmed.
- Editor (appendix_b_check.csv): the old file on disk (18:26Z) was already 45/45 yes with non-empty refs. The advisor's empty/NO copy came from an earlier draft and parser. I regenerated it with the new read-only scripts/analyst_round13b.py, adding status, D5 level and D5 branch columns: 45/45 on all four comparisons, against draft.md 19:06Z.
- Lead (T-5 per variant): recomputed V0, V1, V6 and V2 independently (results/t5_variant_check.csv).
  - (a) holds under V0, V1 and V6 and fails under V2.
  - (b) and (c) hold under V0 and V1 and fail under V6: D4 7/2, D1 9/0.
  - (d) V2 = 1/44, and the one documented cell is HF/D4.
  - Written to VERIFIED_FINDINGS §F-T5.
- Section-writer (Appendix E): "no single flip changes any proposition" in VERIFIED_FINDINGS §G was internally inconsistent. RETRACTED. results/single_flip_check.csv (all 45 flips) shows exactly one, OAI-ART/D1 → documented, which changes C3 and C4. I also re-derived, in new tests, the weak-support 34/11 with no change and the single C6 2-flip set (ANT-MY5/D2 + AISI-SOL/D2). The draft's Appendix E text (l.393–395) matches.
- Section-writer (supply flips / org rows): appendix_e_flips.csv (562 rows: every minimal set per proposition and operation, plus the weak-support rows) and org_structure.csv (45 rows) are both in results/. Summarised in the message, not pasted in full.
- Side check: R26 is Anthropic ("An alignment assessment of the UK AISI cybertesting incident"), so org_structure's AISI-MY5 two-organisation label (UK AISI + Anthropic) is right.
- Draft vs VERIFIED_FINDINGS: every round-13 §Z item is resolved (abstract, Table III, provenance wording, AISI-MY5 L2, LOSO 23/31/33, 60/60 quotes, Q4/Q5 disclosure at l.90). D1/D4/D5 "all nine" claims are already scoped to "S0 and S1" (l.152, 168, 174).
- pytest: 33 passed, 24 xfailed, 9 xpassed. The new test_round13b_analyst.py (5) and test_round13c_analyst.py (2) all pass.
- Still open (not analyst-fixable): advisor reasons 5/10 (no independent human second coder; human Q2 keeps the single-coder limitation) and 9/11 (D5 and V2 have little discriminating power). These are handled as stated limitations, not as findings.
- Not checked: PDF build, figures.

## 2026-11-08 ~19:50Z, round 13, fourth pass (analyst)
- Protocol `python3 lib/protocol.py beyond-the-sandbox` (19:44Z): **PASS**, 0 failures; 40/5; D1 8/1, D2 5/4, D3–D5 9/0. Warnings unchanged (single coder by design; unreachable/insufficient sources not quoted).
- Editor + lead U-4 (Table III rows with no CSV): new read-only script `scripts/analyst_round13c.py` recomputes them from data/coded_evidence.csv into **results/table3_extra.csv**: D2 contemporaneous-or-mixed 38/7 (0/1/8), strictly contemporaneous 37/8 (0/1/8), developer-interpretation-only exclusion 40/5 (no-op, 0 cells in class; 0/1/8), multi-reference 3/42 (HF/D4, OP47/D4, OP47/D5; levels not reported). All four equal draft Table III l.199–202 and d2_strict.json / n_refs_counts.json. No row needs cutting. Also re-checked S0–S6 rows vs rule_variants.csv: all match (S3 L2 = OP47, AISI-MY5; S3b L2 = ART, AISI-MY5, SOL).
- Lead (draft l.232): results/change_provenance.csv → results/provenance_net.json: 12 status events (duplicate dropped); net 7 AI-agent, 1 human-requested (ANT-MY5/D2), 2 restored (HF/D1, HF/D2); final states asserted equal to coded_evidence.csv. l.232 supported.
- Section-writer (Raftari locator): results/raftari_concordance_count.json (from results/external_concordance.csv): 10 §4.1/§4.2 rows, 9 match (HF/D5 = "match on presence; detail differs"), 1 consistent-both-silent (ART/D1). Spot-checked against research/fulltext/raftari2026from.txt §4.1–4.2 p.4: quotes agree. Raftari is full text; it cites R02, so concordance is not independent.
- Experimenter: re-ran analyst_round13b.py: Appendix B 45/45 on refs/status/level/branch, 0 empty draft refs (advisor reason 3 resolved on disk). pytest: 40 passed, 24 xfailed, 9 xpassed (new tests/test_round13d_analyst.py 7/7).
- Advisor reasons 6 and 8 are resolved in the current coding (HF and OP46 carry C; AISI-MY5 is L2). Reasons 5/10 (no human second coder) and 9/11 (low discrimination of D5/V2) remain stated limitations.
- Not checked: PDF build, figures.

## 2026-11-08 ~20:10Z, round 13, sixth pass (analyst)
- Protocol `python3 lib/protocol.py beyond-the-sandbox`: PASS, 0 failures, 40/5; lib/documentary.py consistent (second_coder null, single coder by design per Q2; 8 changes vs baseline listed).
- Lead W-2: new read-only scripts/analyst_round13e.py -> results/bouke_concordance_count.json: 11 Bouke rows, match 4 (2 Table 1, 2 §5.1 prose), not_comparable 2, unaligned 5. Equals the lead's count. Spot-checked bouke2026competing.txt l.424-436 (Table 1 p.7, interleaved extraction confirmed) and l.359-365 (§5.1 p.6 quotes). Added VERIFIED_FINDINGS §J2; test tests/test_round13e_analyst.py.
- Experimenter final check reproduced: analyst_round13b.py -> appendix_b_check.csv 45 rows with refs/status/level/branch columns; pytest 41 passed, 24 xfailed, 9 xpassed, 0 failures.
- Editor: Table III caption cites table3_extra.csv; rows verified last pass. Accepted.
- Source-quality side check: quality.json rates R05 "partial (1021 words)", but source_cache/R05.txt is undecoded binary from an HTTP 403 (fetch_status.json R05 ok=false). R05 is effectively insufficient. The draft (l.242, l.344 "HTTP 403") is correct and no cell relies on R05. quality.json is mislabeled for R05 (reported to data-scout/experimenter).
- Draft l.421 "No detailed Bouke table-cell concordance is reported" is now out of date if the section-writer adopts J2. Either wording is acceptable, but the numbers must be 11: 4/2/5.
- Not checked: PDF build, figures.

## 2026-11-08 ~20:25Z, round 13, seventh pass (analyst; post-X-1 replacement draft 20:16Z)
- Protocol `python3 lib/protocol.py beyond-the-sandbox` (20:23:23Z): PASS, 0 failures, 40/5, 70 sources; warnings unchanged (single coder by design per Q2; unreachable/insufficient sources not quoted). lib/documentary.py consistent (second_coder null; 8 changes vs baseline).
- coded_evidence.csv mtime 20:21:28Z: diffed against archive/coded_evidence_pre_analyst_r13b.csv with the new read-only scripts/analyst_round13f.py: 0 cell-field differences (no recode).
- Editor (appendix_b_check.csv): regenerated with analyst_round13b.py against draft.md 20:16Z: 45 rows, equal/status/level/branch all 45 yes, 0 empty draft_refs. Advisor reason 3 resolved on disk.
- Lead (post-X-1 number check): every draft number traced to rule_variants.csv, table3_extra.csv, provenance_net.json and bouke_concordance_count.json, plus the auxiliary files listed in VERIFIED_FINDINGS §Z2 (new scripts/analyst_round13g.py). 0 numeric mismatches. The draft makes no numerical Raftari claim, so raftari_concordance_count.json (10: 9/1) is not contradicted. Two wording notes go to the section-writer: protocol timestamp 20:11:15Z vs latest 20:23:23Z, and the S3 rule text at l.178 vs the V3 rule_note.
- Experimenter (X-3): reproduced pytest 41 passed / 24 xfailed / 9 xpassed / 0 failed. R05 stays "insufficient" in quality.json after a fresh documentary.py run; no revert.
- Not checked: PDF build, figures.

## 2026-11-08 ~22:00Z, round 13, ninth pass (analyst; draft.md 20:33:19Z after Y-1)
- Protocol (21:57:33Z): PASS, 0 failures, 40/5, 70 sources. lib/documentary.py gives the same result (second_coder null; 8 changes vs baseline; single coder by design per Q2).
- Lead (reasons 5/12): every draft number is traced to change_provenance/provenance_net.json, rule_variants.csv, table3_extra.csv, bouke_concordance_count.json and raftari_concordance_count.json. **0 mismatches.**
  - Support and organisation counts were recomputed independently with the new read-only scripts/analyst_round13i.py.
  - Appendix E was rebuilt from coded_evidence.csv with scripts/analyst_round13h.py: C2/C5 3 flips (220 / 56 sets), C6 2, C3/C4 1, C1 >4, single flip ART/D1 only, weak-support 34/11 with no proposition change. All equal appendix_e_flips.csv.
  - The draft states the proposition table, the flip operation, the search bound and the six named cells in full. Advisor reason 12 is addressed. 33/12 appears only as superseded. Details are in VERIFIED_FINDINGS §Z3.
- Experimenter (Y-3): pytest reproduced, 41 passed / 24 xfailed / 9 xpassed / 0 failed. R05 quality.json is back to "partial" (archive copy).
  - R05.txt is still 53 KB of undecoded or compressed binary, so the label is wrong. R05 stays effectively insufficient. 0 cells cite it, and the draft says HTTP 403. §X4 updated.
  - Recommended fix in fetch/quality: decompress the archive response, or add a printable-ratio guard. The documentary checker is not edited.
- Editor: no numbers changed. Confirmed by the 0-mismatch trace above.
- Still open (stated limitations, not fixable by the analyst):
  - no independent human second coder (reasons 5/10; Q2);
  - low discriminating power of D5/S2 (reasons 9/11).
- Not checked: PDF build, figures.

## 2026-11-08 ~22:30Z — analyst, round 13 (post-Z-1 re-check, §Z4)
- Protocol: PASS, 0 failures, 40/5 (22:23:36Z). documentary.py: exit 0, same tallies, no second coder, so no kappa.
- Coded data: 0 cell-field differences against the r13b snapshot (13f). The 22:16Z mtime is not a recode.
- Re-ran 13i and 13h. Their output is the same as in Z3.
- Wrote and ran scripts/analyst_round13j.py (read-only). It checks the draft against provenance_net, rule_variants, table3_extra and appendix_e_flips: 0 of 21 numeric checks mismatch. "33/12" appears only as superseded (l.403).
- pytest 41 passed / 24 xfailed / 9 xpassed / 0 failed.
- Inbox: editor said no numbers changed, and 13j confirms it. Data-scout said R05 is a local decode issue; 0 cells cite R05. The experimenter's Z-3 report reproduces, and documentary.py is now confirmed by the analyst.
- Open items, not fixable by the analyst: no human second coder (reasons 5/10); D5/S2 discriminating power (reasons 9/11).

## 2026-11-08 ~22:45Z — analyst, round 13 (post-AA-2/AA-3 re-check, §Z5)
- Protocol: PASS, failures []. documentary.py: no second coder, so no kappa (Q2).
- coded_evidence.csv mtime 22:39:05Z. 13f finds 0 cell-field differences against the r13b snapshot, so there was no recode.
- 13b re-run: Appendix B 45/45 equal on refs, status, level and branch; 0 empty draft_refs. This reproduces the experimenter's AA-3 result.
- 13j re-run on draft.md 22:34:39Z: 0 of 21 numeric mismatches. "33/12" appears once, only as superseded (Appendix E).
- pytest run on the analyst side: 41 passed / 24 xfailed / 9 xpassed / 0 failed.
- Inbox: lead (reasons 5/6/12) done, 0 mismatches. Experimenter (AA-3 plus pytest) reproduced. Editor (Table VII caption only) needs no number change, and 13j agrees.
- Not checked: PDF build, figures. Still open: reasons 5/10 and 9/11, which are stated limitations.

## 2026-11-08 ~23:00Z — analyst, round 13 (closing re-check, §Z6)
- Protocol `python3 lib/protocol.py beyond-the-sandbox`: pass true, failures []. documentary.py: second_coder null, so no kappa (Q2). experiments/data/second_coding.csv does not exist.
- coded_evidence.csv mtime 22:39:05Z, unchanged since §Z5. 13f: 0 cell-field diffs vs the r13b snapshot.
- draft.md changed at 22:53:31Z after §Z5, so I re-ran 13j: 0 of 21 numeric mismatches. "33/12" appears only as superseded (Appendix E: "replace the earlier 33/12 scenario"; 34/11 is the current figure).
- 13b re-run: Appendix B 45/45 equal on refs, status, level and branch; 0 empty draft_refs. Variants V0 40/5, V1 36/9, V6 37/8, V2 1/44 (HF D4): the same as the findings.
- pytest (analyst side): 41 passed / 24 xfailed / 9 xpassed / 0 failed. This matches the experimenter's report.
- Inbox: lead says reasons 5/6/12 are closed and asks for no recoding (none done). The experimenter's pytest result reproduces.
- VERIFIED_FINDINGS.md content needs no change; nothing retracted. Still open, as stated limitations: no human second coder (reasons 5/10); low discriminating power of D5 (reasons 9/11).
- Not checked: PDF build, figures.

## 2026-11-08 ~23:20Z — analyst, round 13 (CC-1 / CC-2, §Z7)
- CC-1 line diff, 23:05Z vs 22:53Z draft: **not possible**. No copy of the 22:53Z draft exists. build/paper.tex and reproducibility_package.zip were rebuilt from the current draft at 23:05:20Z, git commands were denied in this session, and §Z6 recorded no hash or snapshot. **The number of changed lines is unverified.** I do not claim 0. Fix: keep a copy (or hash) of draft.md before each edit, e.g. as archive/draft_<time>.md.
- Content checks on draft.md 23:05:20Z instead:
  - 13j: 0 of 21 numeric mismatches. All Table III rows, provenance 8/7/1/2 and Appendix E 3/220/56, 2, 34/11 with six cells match.
  - "33/12" appears once, only as "replace the earlier 33/12 scenario".
  - 13b: Appendix B 45/45 equal on refs, status, level and branch; 0 empty draft_refs.
- Protocol (23:19:43Z): pass true, failures []. coded_evidence.csv mtime 23:17:26Z, but 13f finds 0 cell-field diffs (checker rewrite, no recode).
- CC-2 (experimenter): reproduced protocol PASS and Appendix B 45/45. My pytest run: 41 passed / 24 xfailed / 9 xpassed / 0 failed. I did not wait for the documentary.py re-run to finish. Its last output matches §Z6 (8 changes vs baseline, reproduced null), and there is no second_coding.csv, so there is no kappa (Q2).
- Still open (stated limitations): no human second coder (reasons 5/10); low discriminating power of D5/S2 (reasons 9/11).
- Addendum ~23:25Z: the documentary.py re-run finished, exit 0. Output matches §Z6: 8 changes vs baseline, reproduced null, no second coder, so no kappa (Q2).
- Addendum 2, ~23:30Z (editor answer, lead DD-1, experimenter DD-3):
  - **Diff baseline recorded (DD-1).** draft.md = experiments/archive/draft_20261108T2330Z.md, sha256 d3cba77553b27d32c6a1ba1842c15562a8fd47eb15cd6552d5dfbbf09f48cd37. I checked both files with sha256sum and the hashes are identical. From now on, any draft change is diffed against this file.
  - **CC-1 re-run on the current draft** (draft.md mtime 23:24:11Z, i.e. the editor's archive copy; the editor's 23:23:05Z write is the same content):
    - 13j: 0 of 21 numeric mismatches. "33/12" appears only at l.403, as superseded.
    - 13b: V0 40/5, V1 36/9, V6 37/8, V2 1/44.
    - appendix_b_check.csv (23:27Z): 45/45 yes on refs, status, level and branch; 0 empty draft_refs.
    - 13f: 0 cell-field diffs (coded_evidence.csv mtime 23:17:26Z).
  - Protocol (23:26:59Z): PASS, 45 decisions, 70 sources.
  - pytest: 41 passed / 24 xfailed / 9 xpassed / 0 failed.
  - DD-3 (experimenter): the draft hash is unchanged, and the experimenter's statement reproduces.
  - The 22:53Z→23:05Z line diff from the earlier CC-1 is still unrecoverable, and I still do not claim it is 0. Every later diff can now be checked against the baseline above.
  - Still open (stated limitations): no human second coder (reasons 5/10); low discriminating power of D5 (reasons 9/11).
  - Not checked: PDF build, figures.
  - documentary.py (background run started ~23:26Z) finished with exit 0. Its output is the same as §Z6: 8 changes vs baseline, reproduced null, no second coder, so no kappa (Q2).

## 2026-11-08 ~23:50Z — analyst, round 13 (EE-2, editor CC-1 request, section-writer request; §Z8 of VERIFIED_FINDINGS)
- draft.md sha256 is 5915d4f372d5… This is the editor's edit. It is NOT yet the EE-1 (revert) state, so the diff below is against the 23:30Z baseline (archive/draft_20261108T2330Z.md).
- Diff vs baseline. Expected kept hunks are present: l.34, l.120, l.178, l.195, l.216, l.367, l.381. **Unexpected hunks:**
  - l.44 (new "limited to the supplied verified summaries");
  - l.46 (the Greenblatt/CaMeL specifics replaced by summary-only text);
  - l.242–245 (Source access paragraph rewritten; it adds "Supporting abstracts … were not available" and drops the Abstract locators);
  - l.330 ("supplied protocol report");
  - l.362 (Table VII caption "supplied");
  - l.381: besides the kept last sentence, "supplied" ×2 and "checked manuscript".
- **The l.44/46/242–244 changes are false.** greenblatt2023ai.txt p.1 Abstract and debenedetti2025defeating.txt p.1 Abstract contain exactly the pre-edit claims: GPT-4 untrusted, GPT-3.5 trusted, trusted editing and untrusted monitoring on programming problems; 77% vs 84% in AgentDojo. These should be reverted under EE-1.
- EE-2: V3 0/2/7 (L2: OP47, AISI-MY5; L3 includes OAI-HF via its R04 D5 passage and OP46 via its R08 D3 passage) matches the new l.178 definition. PASS.
- 13j: 0/21 numeric mismatches. Protocol PASS (23:46:36Z). documentary.py PASS, no kappa (Q2). 13f: 0 cell diffs. round9 Appendix B: 45/45, 0 mismatches. No documented cell rests on an insufficient source or only on partial sources.
- pytest not run (venv python needs approval; no pytest in system python). The data are unchanged since the 23:30Z 41/24/9/0 run.
- These results apply to sha 5915d4f3 only. They must be re-run after EE-1.
- Still open (stated limitations): no human second coder (reasons 5/10); low discriminating power of D5 and S2 (reasons 9/11).

## 2026-11-09 ~00:20Z — analyst, round 13 (FF-2, editor V3/EE-2 request, section-writer request, experimenter EE-1; §Z9 of VERIFIED_FINDINGS)
- draft.md sha256 is 6b6a5813…032afe9, the post-EE-1 state, identical to archive/draft_20261108T2359Z.md.
- Diff against the 23:30Z baseline: exactly 7 hunks, at l.34/120/178/195/216/368/382.
  - l.44, l.46 and l.242–245 are identical to the baseline. The §Z8 false edits are reverted.
- Protocol: PASS (00:19:01Z). documentary.py: PASS, no second coder, no kappa.
- Coded data: 13f finds 0 cell diffs. 13j finds 0/21 numeric mismatches.
- Issue found: the experimenter's round9 rewrite of appendix_b_check.csv has only the reference columns. This broke test_round13b (KeyError status_equal) and left the l.382 status/level/branch claim without a file behind it.
  - Re-ran analyst_round13b.py: 45/45 on all four fields.
  - pytest: 41 passed / 24 xfailed / 9 xpassed / 0 failed.
  - Asked the experimenter not to overwrite the four-field file with the refs-only one.
- EE-2: V3 0/2/7 is consistent with the l.178 text. I re-read the R04 and R08 credential quotes in source_cache.
- Still open (stated limitations): no human second coder (reasons 5/10); low discriminating power of D5 and S2 (reasons 9/11). These are wording limits, not number errors.
- Not checked: PDF build, figures.

## 2026-11-09 ~00:36Z — analyst, round 13 (GG-3, lead-scientist; experimenter GG-3 note)
- draft.md sha256 is 6b6a5813…032afe9, the same as archive/draft_20261108T2359Z.md. There is no draft change since FF-2, so nothing needs a diff.
- Protocol: PASS (00:34:54Z), no failures. Its warnings are unchanged: unverified sources, links blocked from this machine, sources with no usable text, single coder.
- results/appendix_b_check.csv still has all four fields: 45 rows and 0 "no" values in any *_equal column. So it was not overwritten again after FF-2.
  - Advisor round_12 reason 3 ("draft_refs empty, equal=NO") describes the earlier refs-only or broken file. It does not describe the current file.
- pytest experiments/tests: 41 passed / 24 xfailed / 9 xpassed / 0 failed. Identical to FF-2.
- No change to VERIFIED_FINDINGS. §Z9 stands.
- Still open: these are interpretation and validation issues, not number errors, and re-running does not fix them.
  - No human second coder (reasons 5/10).
  - The D5 branch for AISI Mythos 5 (reason 8).
  - The credentials-only framing in Table III (reason 6).
  - The HF D1 decision taken under Q4 (reason 4).
  - Appendix E thresholds can't be reconstructed (reason 12).
- Addendum ~00:40Z: this round's documentary.py run finished. It passes with no failures and says single coder by design, so there is no kappa.

## 2026-11-09 ~00:45Z — analyst, round 13 (editor advisor-point-3 request; lead HH-3; experimenter HH-3; §Z10)
- draft.md sha256 is 6b6a5813, the same as archive/draft_20261108T2359Z.md. There is no draft change, so no diff is needed (HH-3).
- I regenerated appendix_b_check.csv with analyst_round13b.py (00:44:36Z).
  - Result: 45/45 on refs, status, D5 level and D5 branch; 0 empty draft_refs. An independent CSV read confirms it.
  - Advisor reason 3 refers to a stale file. The l.382 45/45 claim is supported, but only as a manuscript-vs-data consistency check.
- HF D1 is documented in the data and in the draft, so advisor reason 4's premise is stale. Artifactory D1 is the only unknown D1.
- Protocol: PASS. documentary.py: exit 0, no kappa (single coder, Q2). pytest: 41/24/9/0.
- Still open (interpretation limits, not number errors): no human second coder (5/10); AISI-MY5 D5 branch (8); credentials-only framing (6); Appendix E reconstructibility (12).

## 2026-11-09 ~01:45Z — analyst round 14 (R14-2; experimenter R14 result)
- Draft sha 6b6a5813 is unchanged, so the freeze holds and I did not need the 13b/13j diff re-run. Protocol: failures []. pytest 41/24/9/0. documentary.py: single coder, no second_coding (Q2), so no kappa.
- New independent script, scripts/analyst_round14.py (writes only analyst_r14_* files):
  - H1 V0/V1 3/2/1/1/1/1 matches stop_agent.csv. V6: 7 units, operator 2, matches.
  - H2 V0 4 in / 1 out, 2/2/1 elicitation, 1 verbatim, 3 contested: matches. V1: only HF. V6: 5 cells, 2 in scope / 3 no permission belief (AI-read): matches.
- Issue: two operator halts are one AISI alert, so "operator halt most common" is not allowed.
- Issue: the D2 in-scope headline is V0 only. It fails under V1 and V6.
- Issue: V6's D2 documented cells (3 of 5) do not meet the round-14 D2 rule.
- C/N/P table built; 9/9 deciding passages are verbatim in the cache. R08 INT/MY5 and R07 HF D2 quotes are verbatim.
- **Defect:** HF/D4 partial_support is empty in coded_evidence.csv, even though the change_log claims R02;R03. rule_variants V2 still says 1/44 while its note says 0. The idempotency guard in round14.py skips the assignment. The S2 = 0/45 claim is not reflected in the results, so it is withheld from VERIFIED_FINDINGS (R14-S2) until fixed.
- Housekeeping: my background protocol run left a stray output file at the repo root, experiments_tmp_proto_r14.txt (protocol stdout). I did not delete it.
