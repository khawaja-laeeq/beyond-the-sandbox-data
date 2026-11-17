"""Round 5: (1) claim_strength column + downgrade of the two not-independently-checked cells,
(2) single agreement JSON (full 45, 43-cell sensitivity, per-dimension kappa, bootstrap CI, decision count),
(3) n_refs==1 documented-cell counts. Run from experiments/: python3 -I scripts/round5.py"""
import csv, json, random
from collections import Counter
D, R = "data/", "results/"
DOWN = {("INC-OAI-HF", "D1"): "R01 only; R01 unreachable (HTTP 403) and the AI second coder had no R01 text, so this cell rests on the primary coder's reading of a single source",
        ("INC-AISI-SOL", "D5"): "R24 only; the AI second coder had no R24 text and tagged unknown, so this cell rests on the primary coder's re-read of a single source (App. A.10)"}
rows = list(csv.DictReader(open(D + "coded_evidence.csv", encoding="utf-8")))
fn = list(rows[0])
if "claim_strength" not in fn:
    fn.append("claim_strength")
for r in rows:
    k = (r["unit"], r["code"])
    nref = len([x for x in r["reference"].split(";") if x])
    if k in DOWN:
        r["claim_strength"] = "downgraded: single-source, not independently checked"
        tag = "DOWNGRADED claim strength (round 5, status unchanged): " + DOWN[k]
        if "DOWNGRADED claim strength" not in r["change_log"]:
            r["change_log"] = (r["change_log"] + "; " if r["change_log"] else "") + tag
    elif r["status"] == "documented":
        r["claim_strength"] = "single-source" if nref == 1 else "multi-source"
    else:
        r["claim_strength"] = "n/a (unknown)"
for name in ("coded_evidence.csv", "coded_evidence_v12.csv"):
    with open(D + name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fn)
        w.writeheader()
        w.writerows(rows)
with open(R + "claim_strength_log.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["row", "status", "claim_strength", "reason"])
    for k, v in DOWN.items():
        w.writerow(["/".join(k), "documented", "downgraded", v])


def rd(p):
    return {(r["unit"], r["code"]): r["status"] for r in csv.DictReader(open(D + p))}


prim, sec = rd("coded_evidence.csv"), rd("second_coding.csv")


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def st(keys):
    a = [prim[k] for k in keys]
    b = [sec[k] for k in keys]
    k = kappa(a, b)
    ag = sum(x == y for x, y in zip(a, b))
    return {"n": len(keys), "agree": ag, "percent_agreement": round(100 * ag / len(keys), 1),
            "kappa": None if k is None else round(k, 3)}


keys = sorted(k for k in prim if k in sec)
skip = set(DOWN)
random.seed(0)


def boot(ks, B=2000):
    v = []
    for _ in range(B):
        s = [random.choice(ks) for _ in ks]
        k = kappa([prim[x] for x in s], [sec[x] for x in s])
        if k is not None:
            v.append(k)
    v.sort()
    return {"B": B, "seed": 0, "valid_resamples": len(v),
            "ci95": [round(v[int(.025 * len(v))], 3), round(v[int(.975 * len(v)) - 1], 3)],
            "note": "percentile bootstrap over cells; degenerate resamples (kappa undefined) dropped"}


sens = [k for k in keys if k not in skip]
dims = sorted({c for _, c in keys})
full = st(keys)
agr = {"label": "AI-assisted second coding (codex), not an independent human coder",
       "decision_count": len(prim), "units": len({u for u, _ in prim}), "dimensions": len(dims),
       "full_set": dict(full, bootstrap=boot(keys)),
       "sensitivity_excluding_unchecked": dict(st(sens), excluded=["/".join(k) for k in sorted(skip)], bootstrap=boot(sens)),
       "per_dimension": {d: st([k for k in keys if k[1] == d]) for d in dims},
       "per_dimension_note": "n=9 per dimension; kappa is None where both coders are constant. Descriptive only.",
       "disagreements": [["/".join(k), prim[k], sec[k]] for k in keys if prim[k] != sec[k]],
       "primary_unknown": sum(prim[k] == "unknown" for k in keys),
       "second_unknown": sum(sec[k] == "unknown" for k in keys),
       "min_kappa_threshold": 0.6, "threshold_met_full_set": (full["kappa"] or 0) >= 0.6}
json.dump(agr, open(R + "agreement.json", "w"), indent=1)

cl = {r["unit"]: r["cluster"] for r in csv.DictReader(open(D + "units.csv"))}
er = list(csv.DictReader(open(R + "evidence_class_rows.csv")))
doc = [r for r in er if r["status"] == "documented"]
one = [r for r in doc if r["n_refs"] == "1"]
nr = {"documented_cells": len(doc), "documented_n_refs_1": len(one),
      "by_cluster": {c: {"documented": sum(cl[r["unit"]] == c for r in doc),
                         "n_refs_1": sum(cl[r["unit"]] == c for r in one)} for c in sorted(set(cl.values()))},
      "by_dimension": {d: {"documented": sum(r["code"] == d for r in doc),
                           "n_refs_1": sum(r["code"] == d for r in one)} for d in dims},
      "single_source_cells": ["%s/%s" % (r["unit"], r["code"]) for r in one]}
json.dump(nr, open(R + "n_refs_counts.json", "w"), indent=1)
print(json.dumps({"agr": {k: agr[k] for k in ("decision_count", "full_set", "sensitivity_excluding_unchecked", "per_dimension")}, "nr": nr}, indent=1))
