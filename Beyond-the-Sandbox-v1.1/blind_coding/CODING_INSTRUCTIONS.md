# Blinded second coding: instructions

**For:** Khawaja Muhammad Laeeq (coder A) and Mahnoor Iftikhar (coder B). Code independently. Do not discuss items until both of you have finished.

## Before you start

- Use only your own two sheets:
  - `sheet_items_coder_<you>.csv`: 36 propositions;
  - `sheet_relations_coder_<you>.csv`: one row for each source attached to a proposition, 61 rows.
- **Do not open** any of these before you finish, because they contain the AI's coding:
  - `blind_coding/key/`;
  - `analysis/` (any file);
  - `HUMAN_REVIEW_PACKET.md`;
  - the manuscript's Findings.
- Read the sources only in their cached text, which is the version that was coded:
  - `original/experiments/source_cache/<ID>.txt` for R02–R26 (R24 also has the PDF `R24.pdf`);
  - `supporting_data/source_cache_v1.1/<ID>.txt` for R01, R71–R75.
- Write down roughly how long the coding took, in the `notes` column of the first row.

## What a proposition is

Each item is one small factual claim about one incident unit, for example "The session ended when the model exhausted its token budget". You judge **what the listed sources state about it**, not whether it is true.

## Step 1: code each source (relations sheet)

For every row, read the source and choose **one** relation. Quote nothing; just give the location (section, page or heading) in `passage_location`.

| Code | Use it when the source ... |
|---|---|
| `supports` | states the **whole** proposition in its **own voice** |
| `partial` | states only part of it, or a compatible but less specific claim, or is not specific to this incident unit |
| `hedged` | states it, but with explicit uncertainty ("likely", "we believe", a probabilistic link) |
| `relays` | states it on **another organization's authority** ("X told us", "as X shared", "X found that") |
| `contradicts` | states something incompatible with it |
| `none` | says nothing that bears on it |

**Rules:**

- Own voice versus relay: if the organization says how it knows (its own logs, its own investigation), it is its own voice. If it attributes the fact to someone else, it is a relay.
- A statement that the source has "no evidence" of something is `contradicts` only for a proposition asserting that the thing happened.

## Step 2: code each proposition (items sheet)

Fill in `evidence_status` from your Step 1 codes:

| Code | Rule |
|---|---|
| `supported` | at least one source `supports` or `hedged`, and none `contradicts` |
| `contested` | at least one source supports it and at least one `contradicts` |
| `contradicted` | at least one `contradicts`, none supports |
| `partially_supported` | only `partial` or `relays` |
| `unknown` | every source is `none` |

In `deciding_source_and_location`, give the source and location that decided your code.

## Dimension-specific rules (from the codebook)

- **D2 authorization belief.** A belief counts only if it concerns **permission** to act on the target (authorized, approved, in scope, out of scope). A belief only about **what** the target is (simulated, real, scripted, who owns it) is not a permission belief.
- **D5 effects.** Effects are not harm. The branches are:
  - C: credentials not issued to the agent;
  - N: non-public data accessed;
  - P: unauthorized persistent change.

  These matter only if a proposition names a branch.
- **Unknown never means it did not happen.** Code what the documents state.

## When you are done

Save the two CSV files. Do not change the item order or the item and source IDs. Then run:

```
python3 -I blind_coding/agreement.py
```

It reports raw agreement, Cohen's kappa, Gwet's AC1 and Krippendorff's alpha (coder A versus B, and each coder versus the AI), and writes `disagreements_for_adjudication.csv`.

Adjudicate each disagreement together. Record the agreed code, the deciding passage, the reason, your names and the date, and report the statistics from **before** adjudication.

Do not rerun `draw_sample.py` once coding has started: it would draw a different sample if the analysis changed.
