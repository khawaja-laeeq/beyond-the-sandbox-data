# Post-freeze batch v1.1 (AI-proposed, not final)

Candidate units drawn only from primary sources: AI developers' own reports and affected parties' own statements.
Searched and read 2026-11-17. The frozen v1.0 data is not modified.

- `post_freeze_batch_v1_1_proposed.csv`: 12 units x D1-D5. Every status is a single-pass AI proposal
  (`coder_status = PENDING_BLIND_DOUBLE_CODING`). Not human coded, no agreement statistic. Do not cite as coded data.
- `recount.json`: original 9 units vs these 12 vs combined 21. All OpenAI units count as one reporter group, so independent
  reporter groups rise from 3 to 6 (5 if the Wikimedia report is counted under OpenAI), not from 9 to 21.
- `candidates_primary_sweep_1.csv`: every candidate found, including those not usable yet (no primary source found or page blocked).
- `build_batch.py`: regenerates the two files above from `experiments/data/coded_evidence.csv`.

Known limits: D3 and D4 are documented for every unit partly by construction (a unit is included only if an out-of-scope action is reported).
WorkOS involves an independent researcher, not an AI developer; eligibility is undecided.
