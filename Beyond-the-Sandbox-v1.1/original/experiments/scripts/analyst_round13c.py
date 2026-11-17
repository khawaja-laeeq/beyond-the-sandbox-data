"""Analyst round 13 (fourth pass, 2026-11-08 ~19:50Z). Run from experiments/: python3 -I scripts/analyst_round13c.py
READ-ONLY on data/ and on the other result files. Recomputes, independently of analyst_round12.py and rule_variants.py,
straight from data/coded_evidence.csv:
  results/table3_extra.csv            -- the four Table III rows that are not in rule_variants.csv (D/U, D/U by
                                         dimension, D5 L1/L2/L3), plus S0 as a control row
  results/raftari_concordance_count.json -- count of the Raftari §4.1/§4.2 rows in results/external_concordance.csv
  results/provenance_net.json         -- net status changes vs V11 by trigger class, from results/change_provenance.csv
"""
import csv, os, json, sys
from collections import Counter, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, write_csv, log  # noqa: E402

DIMS = ["D1", "D2", "D3", "D4", "D5"]
R = list(csv.DictReader(open(os.path.join(DATA, "coded_evidence.csv"), encoding="utf-8")))
assert len(R) == 45 and len({(r["unit"], r["code"]) for r in R}) == 45


def nrefs(r):
    return len([x for x in r["reference"].split(";") if x.strip()])


RULES = OrderedDict([
    ("S0 baseline (control)", lambda r: r["status"] == "documented"),
    ("D2 contemporaneous or mixed",
     lambda r: r["status"] == "documented" and (r["code"] != "D2" or r["d2_elicitation"] in ("contemporaneous", "mixed"))),
    ("D2 strictly contemporaneous",
     lambda r: r["status"] == "documented" and (r["code"] != "D2" or r["d2_elicitation"] == "contemporaneous")),
    ("Exclude developer-interpretation-only D2",
     lambda r: r["status"] == "documented" and (r["code"] != "D2" or r["d2_evidence_type"] != "developer interpretation only")),
    ("Retain multi-reference cells only", lambda r: r["status"] == "documented" and nrefs(r) >= 2),
])

out = []
for name, keep in RULES.items():
    doc = [r for r in R if keep(r)]
    bydim = Counter(r["code"] for r in doc)
    d2 = sorted(r["unit"] for r in doc if r["code"] == "D2")
    d5 = [r for r in doc if r["code"] == "D5"]
    if len(d5) == 9:
        lv = Counter(r["effect_level"] for r in d5)
        lev = "%d/%d/%d" % (lv["L1"], lv["L2"], lv["L3"])
    else:
        lev = "n/a (%d of 9 D5 cells documented; levels do not sum to nine)" % len(d5)
    um = Counter(r["code"] for r in R if not keep(r))
    out.append({"rule": name, "documented": len(doc), "unknown": 45 - len(doc),
                "documented_by_dim_D1-D5": "/".join(str(bydim[d]) for d in DIMS),
                "unknown_by_dim_D1-D5": "/".join(str(um[d]) for d in DIMS),
                "D2_documented_units": ";".join(d2),
                "multi_reference_documented_cells": ";".join("%s/%s" % (r["unit"], r["code"]) for r in doc if nrefs(r) >= 2)
                if name.startswith("Retain") else "",
                "D2_has_most_unknowns": um["D2"] == max(um.values()) and list(um.values()).count(um["D2"]) == 1,
                "D5_L1/L2/L3": lev})
write_csv(os.path.join(RESULTS, "table3_extra.csv"), list(out[0].keys()), out)

# ---- Raftari concordance ----
C = list(csv.DictReader(open(os.path.join(RESULTS, "external_concordance.csv"), encoding="utf-8")))
raf = [c for c in C if "Raftari §4.1" in c["comparison"] or "Raftari §4.2" in c["comparison"]]
cnt = Counter("match" if c["match_diverge"].startswith("match") else c["match_diverge"] for c in raf)
other_raf = [c for c in C if "Raftari" in c["comparison"] and c not in raf]
rj = {"source_file": "results/external_concordance.csv",
      "rule": "rows whose comparison column names 'Raftari §4.1' or 'Raftari §4.2' (OpenAI units)",
      "n_rows": len(raf), "counts": dict(cnt),
      "rows": ["%s %s: %s" % (c["unit"], c["comparison"].split(" vs ")[0], c["match_diverge"]) for c in raf],
      "other_raftari_rows_not_counted": ["%s %s: %s" % (c["unit"], c["comparison"], c["match_diverge"]) for c in other_raf],
      "caveat": "Raftari §§4.1-4.2 cites the same OpenAI report (R02) we code from; agreement is not independent validation."}
json.dump(rj, open(os.path.join(RESULTS, "raftari_concordance_count.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---- provenance net changes ----
P = [p for p in csv.DictReader(open(os.path.join(RESULTS, "change_provenance.csv"), encoding="utf-8"))
     if p["change_type"] == "status" and "DUPLICATE" not in p["trigger_note"]]
first, last, cls = {}, {}, {}
for p in P:
    first.setdefault(p["cell"], p["old"])
    last[p["cell"]] = p["new"]
    cls.setdefault(p["cell"], []).append(p["trigger_class"])
net = {c: (first[c], last[c], cls[c]) for c in first if first[c] != last[c]}
restored = sorted(c for c in first if first[c] == last[c])
cur = {"%s/%s" % (r["unit"], r["code"]): r["status"] for r in R}
assert all(cur[c] == v[1] for c, v in net.items()), "provenance final state disagrees with coded_evidence.csv"
pj = {"source_file": "results/change_provenance.csv (status rows, duplicate log row dropped)",
      "status_events": len(P),
      "net_changes": {c: "%s->%s (%s)" % (v[0], v[1], ",".join(v[2])) for c, v in sorted(net.items())},
      "net_AI_agent": sum(1 for v in net.values() if v[2] == ["AI-agent"]),
      "net_human_requested": sum(1 for v in net.values() if "human" in v[2]),
      "restored_cells": {c: ",".join(cls[c]) for c in restored},
      "final_state_matches_coded_evidence": True}
json.dump(pj, open(os.path.join(RESULTS, "provenance_net.json"), "w", encoding="utf-8"), indent=1)
log("analyst_round13c.py", "table3_extra %s; raftari %s; provenance net AI %d human %d restored %d" % (
    [(o["rule"], o["documented"], o["unknown"], o["D5_L1/L2/L3"]) for o in out], dict(cnt),
    pj["net_AI_agent"], pj["net_human_requested"], len(restored)))
for o in out:
    print(o)
print(json.dumps(rj, indent=1, ensure_ascii=False))
print(json.dumps(pj, indent=1))
