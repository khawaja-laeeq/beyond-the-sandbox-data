"""Analyst round 14 (R14-2). Independent recount; does not use _common.stage_cat or stop_d2_profile.py logic.
Run from experiments/: python3 -I scripts/analyst_round14.py
Reads data/coded_evidence.csv, data/units.csv, data/sources.csv, ../inputs/V11_Coded_Evidence.csv, source_cache/*.txt.
Writes ONLY results/analyst_r14_h1h2.json, results/analyst_r14_cnp.csv, results/analyst_r14_s2.json (no data edits)."""
import csv, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(HERE, *a)
R = list(csv.DictReader(open(P("data", "coded_evidence.csv"), encoding="utf-8")))
cm = {(r["unit"], r["code"]): r for r in R}
units = [u["unit"] for u in csv.DictReader(open(P("data", "units.csv"), encoding="utf-8"))]
v11 = {(r["unit"], r["code"]): r for r in csv.DictReader(open(P("..", "inputs", "V11_Coded_Evidence.csv"), encoding="utf-8"))}


def stop_cat(t):  # analyst's own keyword classifier on the response_stage text
    t = t.lower()
    if t.startswith("signal only"): return "signal only (no stop)"
    if "operator halt" in t: return "operator halt"
    if "self-stop" in t: return "self"
    if "affected-party" in t: return "affected party"
    if "third-party" in t: return "third party"
    if "external stop" in t: return "external technical"
    return "UNCLASSIFIED"


def tally(xs):
    o = {}
    for x in xs: o[x] = o.get(x, 0) + 1
    return dict(sorted(o.items()))


out = {}
for var in ("V0", "V1"):  # V1 changes only D2, so D4 is identical to V0
    d4 = {u: stop_cat(cm[(u, "D4")]["response_stage"]) for u in units if cm[(u, "D4")]["status"] == "documented"}
    d2 = [cm[(u, "D2")] for u in units if cm[(u, "D2")]["status"] == "documented"
          and (var == "V0" or cm[(u, "D2")]["d2_evidence_type"] == "verbatim model statement")]
    out[var] = dict(n_D4=len(d4), H1=tally(d4.values()), H1_units=d4, n_D2=len(d2),
                    direction=tally("out" if r["d2_direction"].startswith("not authorized") else "in" for r in d2),
                    elicitation=tally(r["d2_elicitation"] for r in d2), evidence_type=tally(r["d2_evidence_type"] for r in d2),
                    contested=tally("yes" if r["contested_by"].strip() else "no" for r in d2), D2_units=[r["unit"] for r in d2])
v6 = {k: r["status"] for k, r in v11.items()}; v6[("INC-ANT-MY5", "D2")] = "unknown"
out["V6"] = dict(D4_documented=[u for u in units if v6[(u, "D4")] == "documented"],
                 D2_documented=[u for u in units if v6[(u, "D2")] == "documented"],
                 D2_evidence={u: v11[(u, "D2")]["evidence"] for u in units if v6[(u, "D2")] == "documented"},
                 D4_evidence={u: v11[(u, "D4")]["evidence"] for u in units if v6[(u, "D4")] == "documented"})
json.dump(out, open(P("results", "analyst_r14_h1h2.json"), "w"), indent=1)

# S2: stored partial_support vs the R14-1b judgement applied in memory (HF/D4 partial_support R02;R03)
ORG = {s["ref"]: s["citation"].split(",")[0].split("“")[0].strip() for s in csv.DictReader(open(P("data", "sources.csv"), encoding="utf-8"))}
ORG["R04"] = "Hugging Face"; ORG["R07"] = "METR"


def s2(partial_override):
    n = []
    for k, r in cm.items():
        part = partial_override.get(k, r["partial_support"]).replace(" ", "").split(";")
        whole = {ORG[x] for x in r["reference"].split(";") if x and x not in part}
        if r["status"] == "documented" and len(whole) >= 2: n.append("%s/%s" % k)
    return n


s2o = dict(stored_partial_support_HF_D4=cm[("INC-OAI-HF", "D4")]["partial_support"],
           S2_documented_from_stored_data=s2({}), S2_documented_with_R14_1b_applied=s2({("INC-OAI-HF", "D4"): "R02;R03"}))
json.dump(s2o, open(P("results", "analyst_r14_s2.json"), "w"), indent=1)

# C/N/P branch presence per unit, with verbatim check of the deciding passage in the cached source
rows = []
for u in units:
    r = cm[(u, "D5")]; br = r["d5_tree_branch"].split("->")[0].strip()
    present = set(x.strip() for x in br.split(";")) if br not in ("-", "") else set()
    m = re.match(r"(R\d+[a-z]?): '(.*)'", r["d5_deciding_passage"].strip())
    ref, q = (m.group(1), m.group(2)) if m else ("", "")
    src = open(P("source_cache", ref + ".txt"), encoding="utf-8", errors="ignore").read() if ref and os.path.exists(P("source_cache", ref + ".txt")) else ""
    norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).lower()
    rows.append(dict(unit=u, d5_status=r["status"], C="yes" if "C" in present else "no", N="yes" if "N" in present else "no",
                     P="yes" if "P" in present else "no", qualified="N qualified" if u == "INC-OAI-HF" else "",
                     deciding_ref=ref, deciding_passage=q, passage_verbatim_in_cache="yes" if q and norm(q) in norm(src) else "NO",
                     branch_note=r["d5_tree_branch"]))
with open(P("results", "analyst_r14_cnp.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(json.dumps(out, indent=1)); print(json.dumps(s2o, indent=1))
for x in rows: print(x["unit"], x["C"], x["N"], x["P"], x["deciding_ref"], x["passage_verbatim_in_cache"])
