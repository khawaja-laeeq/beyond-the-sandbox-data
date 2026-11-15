"""Recompute single-source / multi-source / direct-vs-inferred counts and the
"conclusions that change when single-source or inferred cells are discounted" table.
Reads data/coded_evidence_v13.csv if it exists (analyst's recode; any column whose values include
'direct' and 'inferred' is used as the direct/inferred split), else data/coded_evidence.csv (the split is then
reported as unavailable, never guessed). Writes results/discount_table.csv, results/derived_counts.json.
Run: python3 -I scripts/discount_table.py"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, DIMS, log

v13 = os.path.join(DATA, "coded_evidence_v13.csv")
src_file = "coded_evidence_v13.csv" if os.path.exists(v13) else "coded_evidence.csv"
with open(os.path.join(DATA, src_file), newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
units = {r["unit"]: r["cluster"] for r in csv.DictReader(open(os.path.join(DATA, "units.csv")))}

# support_type is the split column (a coding where no cell is inferred still has a split: all direct)
split_col = "support_type" if "support_type" in rows[0] else None
for c in ([] if split_col else rows[0]):
    vals = {r[c].strip().lower() for r in rows}
    if {"direct", "inferred"} <= vals:
        split_col = c
for r in rows:
    r["_n"] = len([x for x in r["reference"].split(";") if x])
    r["_doc"] = r["status"] == "documented"
    r["_single"] = r["_doc"] and r["_n"] == 1
    r["_multi"] = r["_doc"] and r["_n"] > 1
    r["_inferred"] = bool(split_col) and r["_doc"] and r[split_col].strip().lower() == "inferred"
    r["_direct"] = bool(split_col) and r["_doc"] and r[split_col].strip().lower() == "direct"
    r["_strong"] = r["_doc"] and r["_multi"] and not r["_inferred"]  # multi-source and not inferred
    r["_I"] = r["_doc"] and r["evidence_class"] == "I"

doc = [r for r in rows if r["_doc"]]
dc = {"coding_file": src_file, "split_column": split_col, "cells": len(rows), "documented": len(doc),
      "unknown": sum(r["status"] == "unknown" for r in rows), "contradicted": sum(r["status"] == "contradicted" for r in rows),
      "n_refs_1": sum(r["_single"] for r in doc), "multi_source": sum(r["_multi"] for r in doc),
      "downgraded_single_source_unchecked": sum(r.get("claim_strength", "").startswith("downgraded") for r in doc),
      "direct": sum(r["_direct"] for r in doc) if split_col else None,
      "inferred": sum(r["_inferred"] for r in doc) if split_col else None,
      "class_I_documented": sum(r["_I"] for r in doc),
      "multi_source_and_not_inferred": sum(r["_strong"] for r in doc) if split_col else None}

DESC = {"D1": "Technical access to external connectivity is documented", "D2": "Authorization interpretation is documented",
        "D3": "Out-of-scope external action is documented", "D4": "Detection/response is documented",
        "D5": "Confirmed real-world impact is documented"}
table = []


def line(name, sel):
    n = len(sel)
    table.append({"conclusion": name, "cells": n,
                  "documented_as_coded": sum(r["_doc"] for r in sel),
                  "after_dropping_single_source": sum(r["_doc"] and not r["_single"] for r in sel),
                  "after_dropping_class_I_interpretation": sum(r["_doc"] and not r["_I"] for r in sel),
                  "after_dropping_inferred": sum(r["_doc"] and not r["_inferred"] for r in sel) if split_col else "n/a (no v13 split yet)",
                  "after_dropping_single_source_and_inferred": sum(r["_strong"] for r in sel) if split_col else "n/a (no v13 split yet)"})


for d in DIMS:
    line("%s: %s (all 9 units)" % (d, DESC[d]), [r for r in rows if r["code"] == d])
for cl in ("OpenAI", "Anthropic", "AISI"):
    line("Cluster %s: all documented cells" % cl, [r for r in rows if units[r["unit"]] == cl])
line("All 45 cells", rows)
for t in table:
    t["changes"] = "yes" if (t["after_dropping_single_source"] != t["documented_as_coded"]) else "no"

with open(os.path.join(RESULTS, "discount_table.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, list(table[0]))
    w.writeheader()
    w.writerows(table)
json.dump({"derived_counts": dc, "discount_table": table}, open(os.path.join(RESULTS, "derived_counts.json"), "w"), indent=1)
print(json.dumps(dc, indent=1))
for t in table:
    print(t)
log("discount_table.py", json.dumps(dc))
