"""Round 11: compare the analyst's blind entailment re-check (results/blind_recheck.csv) with the primary coding
(data/coded_evidence.csv). This is an AI re-check versus the human coder, NOT agreement between independent humans.
Expected blind_recheck.csv columns: unit, code, and a status column (blind_status | status | tag | blind_tag)
with values documented / unknown / contradicted. Outputs results/blind_recheck_cells.csv and
results/blind_recheck_summary.json (raw agreement, Cohen's kappa over status categories, n, confusion).
Run: python3 -I scripts/blind_recheck_compare.py"""
import csv
import json
import os
import sys
from collections import Counter

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(EXP, "results")
src = os.path.join(R, "blind_recheck.csv")
if not os.path.exists(src):
    sys.exit("blind_recheck.csv not found at %s (analyst output pending); nothing written." % src)
rc = list(csv.DictReader(open(src)))
col = next((c for c in ("blind_status", "status", "tag", "blind_tag") if c in rc[0]), None)
if col is None:
    sys.exit("no status column in blind_recheck.csv; columns: %s" % list(rc[0]))
prim = {(r["unit"], r["code"]): r["status"].strip().lower()
        for r in csv.DictReader(open(os.path.join(EXP, "data", "coded_evidence.csv")))}
# Pre-resolution coding = the coding the blind re-check was made against (round 11): HF/D2 unknown, HF/D1 documented.
# Current coding differs from it by the resolution (HF/D2 -> documented, then HF/D1 -> unknown by human answer Q4).
prim[("INC-OAI-HF", "D2")] = "unknown"
prim[("INC-OAI-HF", "D1")] = "documented"
cells, a, b = [], [], []
for r in rc:
    k = (r["unit"], r["code"])
    if k not in prim:
        continue
    x, y = prim[k], r[col].strip().lower()
    cells.append([k[0], k[1], x, y, "match" if x == y else "mismatch"])
    a.append(x)
    b.append(y)
with open(os.path.join(R, "blind_recheck_cells.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["unit", "code", "primary_status", "blind_recheck_status", "result"])
    w.writerows(cells)
n = len(cells)
agree = sum(x == y for x, y in zip(a, b))
po = agree / n if n else None
cats = sorted(set(a) | set(b))
ca, cb = Counter(a), Counter(b)
pe = sum(ca[c] / n * cb[c] / n for c in cats) if n else None
kappa = (po - pe) / (1 - pe) if n and pe < 1 else None
out = {"comparison": "AI blind re-check (analyst) vs PRE-RESOLUTION primary coding (round 11; reported as a count only); not human-human agreement; the re-check "
       "reads the same developer documents the coder used, so it is not independent of those sources",
       "n_cells": n, "n_primary_cells": len(prim), "n_agree": agree, "n_mismatch": n - agree,
       "raw_agreement": po, "cohens_kappa": None, "pre_resolution": True, "count_statement": "%d of %d statuses agree" % (agree, n),
       "kappa_note": "not reported (round 12: count only, no kappa)",
       "confusion_primary_to_blind": {"%s->%s" % k: v for k, v in sorted(Counter(zip(a, b)).items())}}
json.dump(out, open(os.path.join(R, "blind_recheck_summary.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
