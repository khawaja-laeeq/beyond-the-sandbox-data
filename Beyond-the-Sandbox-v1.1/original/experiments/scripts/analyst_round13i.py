"""Analyst round 13 (pass 9): read-only recount of reference-support numbers in draft Sec. III
(R08 19/17, R02 10/9, R10 sole 7; 37 single / 3 multi; three units with two organisations;
quote-check 60/60, 58 in coded column, 42/45 decisions) from data and result files.
Run from experiments/:  python -I scripts/analyst_round13i.py
"""
import csv, collections, json, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(HERE, "data/coded_evidence.csv"), encoding="utf-8")))
print("columns:", list(rows[0].keys()))
refcol = [c for c in rows[0] if c.lower() in ("reference", "refs", "references", "source_ids", "sources", "ref_ids")]
print("ref column:", refcol)
rc = refcol[0]
doc = [r for r in rows if r["status"] == "documented"]


def refs(r):
    return [x.strip() for x in r[rc].replace(",", ";").split(";") if x.strip()]


sup, sole = collections.Counter(), collections.Counter()
for r in doc:
    rs = refs(r)
    for x in set(rs):
        sup[x] += 1
    if len(set(rs)) == 1:
        sole[rs[0]] += 1
print("support:", sup.most_common(6))
print("sole support:", sole.most_common(6))
print("single-ref:", sum(len(set(refs(r))) == 1 for r in doc), "multi-ref:", sum(len(set(refs(r))) > 1 for r in doc))
o = list(csv.DictReader(open(os.path.join(HERE, "results/org_structure.csv"), encoding="utf-8")))
print("units with >=2 organisations:", sorted({r["unit"] for r in o if int(r["n_unit_organisations"]) >= 2}))
q = json.load(open(os.path.join(HERE, "results/quote_check_summary.json"), encoding="utf-8"))
print("quote summary:", {k: v for k, v in q.items() if not isinstance(v, (list, dict))})
