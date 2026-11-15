"""Print cells where primary, baseline and second coder differ (read-only helper)."""
import csv, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def rd(n):
    return {(r["unit"], r["code"]): r["status"] for r in csv.DictReader(open(os.path.join(D, n)))}


p, s, b = rd("coded_evidence.csv"), rd("second_coding.csv"), rd("coded_evidence.baseline.csv")
print(len(p), len(s), len(b))
for k in sorted(p):
    if p[k] != s.get(k) or p[k] != b.get(k):
        print(k, "prim", p[k], "sec", s.get(k), "base", b.get(k))
