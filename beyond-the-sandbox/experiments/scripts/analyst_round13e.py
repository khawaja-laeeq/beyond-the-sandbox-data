"""Analyst round 13 (sixth pass, 2026-11-08 ~20:10Z). Run from experiments/: python3 -I scripts/analyst_round13e.py
READ-ONLY on data/ and results/external_concordance.csv. Mirrors the Raftari count in analyst_round13c.py:
  results/bouke_concordance_count.json -- count of rows in results/external_concordance.csv whose comparison names Bouke.
Classes: 'match*' -> match; 'not_comparable*' -> not_comparable; 'unaligned' -> unaligned.
"""
import csv, os, json, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import RESULTS, log  # noqa: E402

C = list(csv.DictReader(open(os.path.join(RESULTS, "external_concordance.csv"), encoding="utf-8")))
bk = [c for c in C if "Bouke" in c["comparison"]]


def cls(v):
    for k in ("match", "not_comparable", "unaligned"):
        if v.startswith(k):
            return k
    return v


cnt = Counter(cls(c["match_diverge"]) for c in bk)
bj = {"source_file": "results/external_concordance.csv",
      "rule": "rows whose comparison column names 'Bouke' (Table 1 p.7 rows and §5.1 p.6 prose rows)",
      "n_rows": len(bk), "counts": dict(cnt),
      "rows": ["%s %s: %s" % (c["unit"], c["comparison"], c["match_diverge"]) for c in bk],
      "match_from_table1": sum(1 for c in bk if cls(c["match_diverge"]) == "match" and c["their_source"] == "Bouke Table 1"),
      "match_from_prose": sum(1 for c in bk if cls(c["match_diverge"]) == "match" and "prose" in c["their_source"]),
      "caveat": ("Bouke Table 1 (bouke2026competing p.7) extracts with interleaved lines; rows marked unaligned are not "
                 "compared. Bouke codes the OpenAI 2026-05..07 incident as one row covering our MAY, ART and HF units, and "
                 "Bouke cites the same first-party reports we code from, so agreement is not independent validation.")}
json.dump(bj, open(os.path.join(RESULTS, "bouke_concordance_count.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
log("analyst_round13e.py", "bouke n=%d %s" % (len(bk), dict(cnt)))
print(json.dumps(bj, indent=1, ensure_ascii=False))
