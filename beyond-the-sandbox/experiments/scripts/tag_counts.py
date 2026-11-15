"""E2: descriptive status counts by dimension and by cluster (counts only, no rates/tests)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

units, cod = rows("units.csv"), rows("coded_evidence.csv")
cl = {u["unit"]: u["cluster"] for u in units}
STAT = ["documented", "contradicted", "unknown"]
out = []
def add(kind, key, sel):
    c = {s: sum(1 for r in sel if r["status"] == s) for s in STAT}
    out.append({"by": kind, "group": key, **c, "total": len(sel)})
for d in DIMS:
    add("dimension", d, [r for r in cod if r["code"] == d])
for c in CLUSTERS:
    add("cluster", c, [r for r in cod if cl[r["unit"]] == c])
for c in CLUSTERS:
    for d in DIMS:
        add("cluster x dimension", f"{c}/{d}", [r for r in cod if cl[r["unit"]] == c and r["code"] == d])
add("all", "all", cod)
write_csv(os.path.join(RESULTS, "tag_counts.csv"), ["by", "group"] + STAT + ["total"], out)
u = [r for r in out if r["by"] == "all"][0]
log("tag_counts.py", f"wrote results/tag_counts.csv; overall documented={u['documented']}, contradicted={u['contradicted']}, unknown={u['unknown']} of {u['total']} (counts; units within a cluster are dependent)")
for r in out:
    if r["by"] in ("dimension", "cluster", "all"):
        print(r)
