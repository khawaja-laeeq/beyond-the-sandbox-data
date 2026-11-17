"""Analyst round 13 (read-only): check remaining draft numbers (baseline 38/7, unquoted cells,
org_structure units with 2 orgs, Appendix E 220/56 minimal sets, weak-support 34/11, R05 label)."""
import csv, json, os, collections
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rows(p):
    return list(csv.DictReader(open(os.path.join(P, p), encoding="utf-8")))
print("baseline", collections.Counter(x["status"] for x in rows("data/coded_evidence.baseline.csv")))
q = json.load(open(os.path.join(P, "results/quote_check_summary.json")))
quoted = set((x["unit"], x["code"]) for x in q["quotes"])
print("no quote", [(x["unit"], x["code"], x["status"]) for x in rows("data/coded_evidence.csv") if (x["unit"], x["code"]) not in quoted])
o = rows("results/org_structure.csv")
print("org cols", list(o[0].keys()))
for r in o[:3]:
    print(r)
f = rows("results/appendix_e_flips.csv")
print("flips cols", list(f[0].keys()), len(f))
for k in list(f[0].keys()):
    vals = collections.Counter(r[k] for r in f)
    if len(vals) < 15:
        print(k, dict(vals))
qual = json.load(open(os.path.join(P, "source_cache/quality.json")))
print("R05", str(qual.get("R05", qual))[:300])
