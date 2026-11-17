"""Analyst round 13 (read-only): diff coded_evidence.csv vs pre-r13b snapshot, and
check draft numbers against the five result files named by the lead."""
import csv, json, os, re, sys
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rows(p):
    return list(csv.DictReader(open(os.path.join(P, p), encoding="utf-8")))
a = {(x["unit"], x["code"]): x for x in rows("data/coded_evidence.csv")}
b = {(x["unit"], x["code"]): x for x in rows("archive/coded_evidence_pre_analyst_r13b.csv")}
nd = 0
for k in a:
    for f in a[k]:
        if a[k][f] != b.get(k, {}).get(f):
            nd += 1
            print("DIFF", k, f, repr(b.get(k, {}).get(f))[:60], "->", repr(a[k][f])[:60])
print("cell-field diffs vs snapshot:", nd)
for f in ["results/rule_variants.csv", "results/table3_extra.csv"]:
    print("==", f)
    for r in rows(f):
        print(r)
for f in ["results/provenance_net.json", "results/raftari_concordance_count.json", "results/bouke_concordance_count.json"]:
    print("==", f)
    print(json.dumps(json.load(open(os.path.join(P, f))), indent=None)[:1500])
