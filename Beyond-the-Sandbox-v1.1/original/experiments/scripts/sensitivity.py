"""Sensitivity of headline count conclusions to flipping weak tags (counts only, no statistics).
Reads data/coded_evidence.csv. Scenarios flip (a) each unknown -> documented, (b) each weakly supported
documented cell (support_type inferred, claim_strength downgraded, or listed in CONTESTED: a narrow or
reviewer-contested proposition, see results/evidence_audit.csv notes) -> unknown, one at a time and all together,
plus all single-source documented cells -> unknown. Writes results/sensitivity.csv.
Run: python3 -I scripts/sensitivity.py"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, DIMS, log

rows = list(csv.DictReader(open(os.path.join(DATA, "coded_evidence.csv"), encoding="utf-8")))
units = {r["unit"]: r["cluster"] for r in csv.DictReader(open(os.path.join(DATA, "units.csv"), encoding="utf-8"))}


def key(r):
    return r["unit"] + "/" + r["code"]


def nref(r):
    return len([x for x in r["reference"].split(";") if x])


unk = [r for r in rows if r["status"] == "unknown"]
# documented cells whose proposition is narrow or was contested by reviewers (audit notes give the reason)
CONTESTED = {"INC-ANT-INT/D2", "INC-ANT-OP46/D2", "INC-AISI-SOL/D5", "INC-OAI-MAY/D4", "INC-OAI-ART/D5", "INC-AISI-SOL/D4"}
weak = [r for r in rows if r["status"] == "documented" and (r["support_type"] == "inferred" or r["claim_strength"].startswith("downgraded")
                                                            or key(r) in CONTESTED)]
single = [r for r in rows if r["status"] == "documented" and nref(r) == 1]


def conclusions(st):
    unks = [k for k, s in st.items() if s == "unknown"]
    per_dim = {d: sum(1 for k in unks if k.endswith("/" + d)) for d in DIMS}
    top = sorted(per_dim.values(), reverse=True)
    doc_dim = {d: sum(1 for k, s in st.items() if k.endswith("/" + d) and s == "documented") for d in DIMS}
    n_units = len(units)
    return {
        "documented": sum(s == "documented" for s in st.values()),
        "unknown": len(unks),
        "C1_no_contradicted": not any(s == "contradicted" for s in st.values()),
        "C2_D2_has_most_unknown": per_dim["D2"] == top[0] and top[0] > 0 and top[0] > top[1],
        "C3_all_gaps_in_D2": len(unks) > 0 and all(k.endswith("/D2") for k in unks),
        "C4_D1_D3_D4_D5_documented_in_all_units": all(doc_dim[d] == n_units for d in ("D1", "D3", "D4", "D5")),
        "C5_D2_least_documented_dimension": doc_dim["D2"] == min(doc_dim.values()) and sum(v == doc_dim["D2"] for v in doc_dim.values()) == 1,
        "C6_gaps_in_at_least_two_clusters": len({units[k.split("/")[0]] for k in unks}) >= 2,
    }


base = {key(r): r["status"] for r in rows}
b = conclusions(base)
scen = [("baseline", "none", [], None)]
for r in unk:
    scen.append(("unknown->documented, one", key(r), [key(r)], "documented"))
scen.append(("unknown->documented, all %d" % len(unk), "all unknown", [key(r) for r in unk], "documented"))
for r in weak:
    scen.append(("weak documented->unknown, one", key(r), [key(r)], "unknown"))
scen.append(("weak documented->unknown, all %d" % len(weak), "all weak", [key(r) for r in weak], "unknown"))
scen.append(("single-source documented->unknown, all %d" % len(single), "all single-source", [key(r) for r in single], "unknown"))
scen.append(("both: unknown->documented and weak->unknown", "all", [key(r) for r in unk + weak], None))

out = []
for name, target, ks, new in scen:
    st = dict(base)
    for k in ks:
        st[k] = new if new else ("documented" if base[k] == "unknown" else "unknown")
    c = conclusions(st)
    ch = [k for k in c if k.startswith("C") and c[k] != b[k]]
    out.append(dict(scenario=name, cells_flipped=target, n_flipped=len(ks), **c,
                    conclusions_changed=";".join(ch) if ch else "none"))
with open(os.path.join(RESULTS, "sensitivity.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(out[0]))
    w.writeheader()
    w.writerows(out)
for o in out:
    print(o["scenario"], "|", o["cells_flipped"], "|", o["documented"], o["unknown"], "|", o["conclusions_changed"])
log("sensitivity.py", "wrote results/sensitivity.csv (%d scenarios)" % len(out))

# ---------------- Round 10 additions ----------------
# (a) every documented cell -> unknown singly; (b) minimum flips that change each conclusion C1-C6 ->
# results/sensitivity_exhaustive.csv; (c) leave-one-source-out over every ref in data/sources.csv (a documented cell
# with no refs left becomes unknown) -> results/loso.csv; documented cells per reference -> results/source_share.csv.
import itertools
from collections import Counter

CONCL = [k for k in b if k.startswith("C")]
doc_keys = [key(r) for r in rows if r["status"] == "documented"]
all_keys = [key(r) for r in rows]

ex = []
for k in doc_keys:
    st = dict(base)
    st[k] = "unknown"
    c = conclusions(st)
    ch = [x for x in CONCL if c[x] != b[x]]
    ex.append(dict(analysis="(a) single flip documented->unknown", cells=k, n_flips=1, documented=c["documented"], unknown=c["unknown"],
                   conclusions_changed=";".join(ch) if ch else "none", min_flips="", note=""))

MAXK = 4
for cn in CONCL:
    for direction, pool in (("both directions", all_keys), ("documented->unknown only", doc_keys)):
        found_k, example = None, None
        for k in range(1, MAXK + 1):
            for combo in itertools.combinations(pool, k):
                st = dict(base)
                for x in combo:
                    st[x] = "unknown" if base[x] == "documented" else "documented"
                if conclusions(st)[cn] != b[cn]:
                    found_k, example = k, combo
                    break
            if found_k:
                break
        ex.append(dict(analysis="(b) minimum flips to change " + cn, cells=";".join(example) if example else "",
                       n_flips=found_k or "", documented="", unknown="",
                       conclusions_changed=cn if found_k else "none within %d flips" % MAXK,
                       min_flips=found_k if found_k else ">%d" % MAXK,
                       note="%s; baseline truth value %s%s" % (direction, b[cn], "; false at baseline" if not b[cn] else "")))
ex.append(dict(analysis="(b) note", cells="", n_flips="", documented="", unknown="", conclusions_changed="", min_flips="",
               note="C1 (no contradicted) cannot change by documented<->unknown flips; it needs a cell recoded contradicted. Search is exhaustive up to %d flips; '>%d' = no combination of that size changes the conclusion." % (MAXK, MAXK)))
with open(os.path.join(RESULTS, "sensitivity_exhaustive.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(ex[0]))
    w.writeheader()
    w.writerows(ex)

srcs = [r["ref"] for r in csv.DictReader(open(os.path.join(DATA, "sources.csv"), encoding="utf-8"))]
lo = []
for ref in srcs:
    st = dict(base)
    lost = []
    for r in rows:
        refs = [x for x in r["reference"].split(";") if x]
        if r["status"] == "documented" and ref in refs and len(refs) == 1:
            st[key(r)] = "unknown"
            lost.append(key(r))
    cited = sum(1 for r in rows if r["status"] == "documented" and ref in r["reference"].split(";"))
    c = conclusions(st)
    ch = [x for x in CONCL if c[x] != b[x]]
    lo.append(dict(dropped_ref=ref, documented_cells_citing=cited, cells_to_unknown=len(lost), cells_lost=";".join(lost),
                   documented_after=c["documented"], unknown_after=c["unknown"], conclusions_changed=";".join(ch) if ch else "none"))
with open(os.path.join(RESULTS, "loso.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(lo[0]))
    w.writeheader()
    w.writerows(lo)

CL = ("OpenAI", "Anthropic", "AISI")
sh = []
for ref in srcs:
    cit = [r for r in rows if r["status"] == "documented" and ref in r["reference"].split(";")]
    cc = Counter(units[r["unit"]] for r in cit)
    sole = [r for r in cit if nref(r) == 1]
    d = dict(ref=ref, documented_cells=len(cit), sole_source_cells=len(sole), share_of_documented=round(len(cit) / len(doc_keys), 3))
    for c in CL:
        d["cells_" + c] = cc.get(c, 0)
    for c in CL:
        d["sole_" + c] = sum(1 for r in sole if units[r["unit"]] == c)
    sh.append(d)
with open(os.path.join(RESULTS, "source_share.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(sh[0]))
    w.writeheader()
    w.writerows(sh)
print("baseline:", {k: b[k] for k in CONCL})
for e in ex:
    if e["analysis"].startswith("(b)"):
        print(e["analysis"], "|", e["min_flips"], "|", e["note"], "|", e["cells"])
print("(a) single flips changing something:", [(e["cells"], e["conclusions_changed"]) for e in ex if e["analysis"].startswith("(a)") and e["conclusions_changed"] != "none"])
print("LOSO with changes:", [(l["dropped_ref"], l["cells_to_unknown"], l["conclusions_changed"]) for l in lo if l["cells_to_unknown"]])
log("sensitivity.py", "wrote sensitivity_exhaustive.csv (%d rows), loso.csv (%d refs), source_share.csv" % (len(ex), len(lo)))
