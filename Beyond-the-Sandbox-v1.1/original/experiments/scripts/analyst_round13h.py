"""Analyst round 13 (pass 9): independent rebuild of Appendix E from data/coded_evidence.csv.
Read-only on data; writes nothing except stdout. Recomputes C1-C6, minimal flip counts and number of
minimal sets (both directions; documented->unknown only), single flips, and the six-cell weak-support
scenario named in draft.md Appendix E. Compares with results/appendix_e_flips.csv.
Run from experiments/:  python -I scripts/analyst_round13h.py
"""
import csv, itertools, os, json
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(HERE, "data/coded_evidence.csv"), encoding="utf-8")))
units = {r["unit"]: r["cluster"] for r in csv.DictReader(open(os.path.join(HERE, "data/units.csv"), encoding="utf-8"))}
base = {(r["unit"], r["code"]): r["status"] for r in rows}
DIMS = ["D1", "D2", "D3", "D4", "D5"]


def props(st):
    unk = Counter(c for (u, c), s in st.items() if s == "unknown")
    doc = Counter(c for (u, c), s in st.items() if s == "documented")
    ucells = [k for k, s in st.items() if s == "unknown"]
    return {
        "C1": all(s != "contradicted" for s in st.values()),
        "C2": all(unk["D2"] > unk[d] for d in DIMS if d != "D2"),
        "C3": all(c == "D2" for (u, c) in ucells),
        "C4": all(st[(u, d)] == "documented" for u in units for d in DIMS if d != "D2"),
        "C5": all(doc["D2"] < doc[d] for d in DIMS if d != "D2"),
        "C6": len({units[u] for (u, c) in ucells}) >= 2,
    }


def flip(st, cells):
    s = dict(st)
    for k in cells:
        s[k] = "unknown" if s[k] == "documented" else "documented"
    return s


b = props(base)
out = {"baseline_counts": dict(Counter(base.values())), "baseline": b}
allc = sorted(base)
d2u = [k for k in allc if base[k] == "documented"]
for name, pool in [("both", allc), ("doc_to_unk", d2u)]:
    res = {}
    for p in b:
        res[p] = (">4", 0)
        for n in range(1, 5):
            m = sum(1 for cs in itertools.combinations(pool, n) if props(flip(base, cs))[p] != b[p])
            if m:
                res[p] = (n, m)
                break
    out[name] = res
singles = {"%s/%s" % k: [p for p, v in props(flip(base, [k])).items() if v != b[p]] for k in allc}
out["single_flip_changes"] = {k: v for k, v in singles.items() if v}
named = [("INC-OAI-MAY", "D4"), ("INC-OAI-ART", "D5"), ("INC-ANT-OP46", "D2"), ("INC-ANT-INT", "D2"),
         ("INC-AISI-SOL", "D4"), ("INC-AISI-SOL", "D5")]
out["weak_named_all_documented"] = all(base[k] == "documented" for k in named)
ws = flip(base, named)
out["weak_counts"] = dict(Counter(ws.values()))
out["weak_props_changed"] = [p for p, v in props(ws).items() if v != b[p]]
r = {k: v for k, v in base.items()}
eg = flip(base, [("INC-OAI-MAY", "D1"), ("INC-OAI-HF", "D1"), ("INC-ANT-OP46", "D1")])
out["example_C2_after_MAY_HF_OP46_D1"] = props(eg)["C2"]
out["example_C6_after_ANTMY5_AISISOL_D2"] = props(flip(base, [("INC-ANT-MY5", "D2"), ("INC-AISI-SOL", "D2")]))["C6"]
# result file
f = list(csv.DictReader(open(os.path.join(HERE, "results/appendix_e_flips.csv"), encoding="utf-8")))
summ = sorted({(x["proposition"][:2], x["operation"][:4], x["min_flips"], x["n_minimal_sets"]) for x in f})
out["result_file_summary"] = summ
print(json.dumps(out, indent=1, default=str))
