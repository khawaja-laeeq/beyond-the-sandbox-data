"""Analyst, round 13 (lead tasks for advisor reasons 5, 11, 12). Reads data/coded_evidence.csv,
inputs/V11_Coded_Evidence.csv, data/units.csv and results/coding_change_log.csv. Writes:
  results/change_provenance.csv  every change since the V11 baseline CSV, with trigger class human / lead / AI-agent
  results/org_structure.csv      per unit: organisations with a corpus document; per cell: organisations giving whole
                                 and partial support
  results/appendix_e_flips.csv   selected propositions, admissible operation, ALL minimal flip sets by cell ID, and the
                                 weak-support scenario's cell IDs
Counts only, no statistics. Run from experiments/: python3 -I scripts/analyst_round13.py"""
import csv, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, write_csv, log, DIMS

INPUTS = os.path.join(DATA, "..", "..", "inputs")
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8")))
cur = rd(os.path.join(DATA, "coded_evidence.csv"))
v11 = {(r["unit"], r["code"]): r for r in rd(os.path.join(INPUTS, "V11_Coded_Evidence.csv"))}
units = {r["unit"]: r for r in rd(os.path.join(DATA, "units.csv"))}
clog = rd(os.path.join(RESULTS, "coding_change_log.csv"))
ORG = {"R01": "OpenAI", "R02": "OpenAI", "R03": "Hugging Face", "R04": "Hugging Face", "R07": "METR",
       "R08": "Anthropic", "R10": "UK AISI", "R24": "UK AISI", "R25": "Anthropic", "R26": "Anthropic"}
key = lambda r: "%s/%s" % (r["unit"], r["code"])
refs = lambda s: [x for x in s.split(";") if x]

# ---------------------------------------------------------------- 1. change provenance
HUMAN_0511 = "laeeq 2026-11-05 (chat.jsonl line 6, priority 1): 're-tag ... Mythos 5 D2 ... and Hugging Face D1'"
HUMAN_RULE = "laeeq 2026-11-05 priority 1 general rule 're-tag anything the passage does not support' (cell judgement by an AI agent)"


def classify(row, trig):
    t = trig.lower()
    if row == "INC-ANT-MY5/D2":
        return "human", HUMAN_0511 + "; applied by AI agent in round 8"
    if t.startswith("human answer q4"):
        return "human", "answers.md Q4 (default answer recorded at deadline, not actively chosen) + " + HUMAN_0511
    if t.startswith("human answer q5"):
        return "human", "answers.md Q5/Q6 (default answers recorded at deadline, not actively chosen); lead plan S-1"
    if t.startswith("author rule fix 2026-11-06"):
        return "AI-agent", HUMAN_RULE
    if "lead decision" in row.lower() or "lead" in t:
        return "lead", ""
    if t == "self re-read":
        return "AI-agent", "agent re-read of reopened/new sources, round 1"
    if t == "ai cross-read":
        return "AI-agent", "AI reviewer / AI re-check objection"
    return "AI-agent", ""


prov, seen = [], set()
for e in clog:
    if e["old"] == e["new"]:
        continue
    sig = (e["row"], e["old"], e["new"], e["trigger"])
    dup = sig in seen
    seen.add(sig)
    cls, note = classify(e["row"], e["trigger"])
    if "lead decision D-a" in e["trigger_evidence"]:
        cls, note = "lead", "lead decision D-a (round 12) on the AI blind re-check J2; moves the coding toward the re-check"
    prov.append(dict(cell=e["row"], change_type="status", old=e["old"], new=e["new"], trigger=e["trigger"],
                     trigger_class=cls, trigger_note=note + ("; DUPLICATE log row of the same event" if dup else ""),
                     evidence=e["trigger_evidence"][:300]))
for r in cur:
    k = (r["unit"], r["code"])
    if r["reference"] != v11[k]["reference"]:
        cl = r["change_log"]
        cls = "lead" if "R-2" in cl and r["code"] == "D4" else "AI-agent"
        note = "lead R-2 re-read of cached R02 (round 12)" if cls == "lead" else (
            "round 1 re-read / new source" if ("(round 1)" in cl or "(re-read" in cl) else
            "later agent re-read, passage audit or reference alignment (round and reason in the evidence column)")
        prov.append(dict(cell=key(r), change_type="reference", old=v11[k]["reference"], new=r["reference"], trigger="see change_log field",
                         trigger_class=cls, trigger_note=note, evidence=cl[:300]))
# D5 levels: not in V11 (no effect levels); introduced by the agents (plan D-c, round 12) and revised under plan S-2
for r in cur:
    if r["code"] == "D5" and r["status"] == "documented":
        prov.append(dict(cell=key(r), change_type="D5 effect level (new field)", old="(no level in V11)", new=r["effect_level"],
                         trigger="lead plan D-c (round 12) decision tree; plan S-2 (round 13) branch definitions",
                         trigger_class="lead", trigger_note="levels and branches assigned by AI agents; no human coded levels",
                         evidence=r["d5_tree_branch"][:300]))
for e in clog:
    if e["old"] == e["new"] and ("S-2" in (e["reason"] or "") or "S-2" in (e["trigger"] or "")):  # last row may be short
        prov.append(dict(cell=e["row"], change_type="D5 level/branch (round 13 S-2)", old="", new="", trigger=e["trigger"],
                         trigger_class="lead", trigger_note="plan S-2 rule; applied by AI agent", evidence=e["reason"][:300]))
write_csv(os.path.join(RESULTS, "change_provenance.csv"), list(prov[0].keys()), prov)

# ---------------------------------------------------------------- 2. organisation structure
org = []
for u, ur in units.items():
    cells = [r for r in cur if r["unit"] == u]
    corpus = set(refs(ur["core_sources"])) | {x for r in cells for x in refs(r["reference"])}
    orgs = sorted({ORG[x] for x in corpus})
    for r in cells:
        ev = r["evidence"]
        partial = [x for x in refs(r["partial_support"].replace(" ", ""))] if r["partial_support"] else []
        # round 14 (R14-1b): a reference listed in partial_support supports only part of the proposition, so it is not whole support
        sup = [x for x in refs(r["reference"]) if (x + ":") in ev and x not in partial] if r["status"] == "documented" else []
        org.append(dict(unit=u, cluster=ur["cluster"], unit_corpus_documents=";".join(sorted(corpus)),
                        unit_organisations=";".join(orgs), n_unit_organisations=len(orgs), cell=key(r), status=r["status"],
                        whole_support_orgs=";".join(sorted({ORG[x] for x in sup})), n_whole_support_orgs=len({ORG[x] for x in sup}),
                        partial_support_orgs=";".join(sorted({ORG[x] for x in partial if x in ORG})),
                        n_partial_support_orgs=len({ORG[x] for x in partial if x in ORG}),
                        cell_could_meet_V2=len(orgs) >= 2))
write_csv(os.path.join(RESULTS, "org_structure.csv"), list(org[0].keys()), org)

# ---------------------------------------------------------------- 3. Appendix E flips
UC = {u: r["cluster"] for u, r in units.items()}
base = {key(r): r["status"] for r in cur}


def concl(st):  # identical definitions to scripts/sensitivity.py conclusions()
    unks = [k for k, s in st.items() if s == "unknown"]
    pdim = {d: sum(1 for k in unks if k.endswith("/" + d)) for d in DIMS}
    top = sorted(pdim.values(), reverse=True)
    ddim = {d: sum(1 for k, s in st.items() if k.endswith("/" + d) and s == "documented") for d in DIMS}
    return {"C1_no_contradicted": not any(s == "contradicted" for s in st.values()),
            "C2_D2_has_most_unknown": pdim["D2"] == top[0] and top[0] > 0 and top[0] > top[1],
            "C3_all_gaps_in_D2": len(unks) > 0 and all(k.endswith("/D2") for k in unks),
            "C4_D1_D3_D4_D5_documented_in_all_units": all(ddim[d] == len(UC) for d in ("D1", "D3", "D4", "D5")),
            "C5_D2_least_documented_dimension": ddim["D2"] == min(ddim.values()) and sum(v == ddim["D2"] for v in ddim.values()) == 1,
            "C6_gaps_in_at_least_two_clusters": len({UC[k.split("/")[0]] for k in unks}) >= 2}


b = concl(base)
doc = [k for k, s in base.items() if s == "documented"]
allk = list(base)
OPS = {"both directions": ("flip any cell documented<->unknown", allk), "documented->unknown only": ("flip documented cells to unknown", doc)}
fl = []
for cn in b:
    for dname, (opdesc, pool) in OPS.items():
        found = None
        for k in range(1, 5):
            sets = []
            for combo in itertools.combinations(pool, k):
                st = dict(base)
                for x in combo:
                    st[x] = "unknown" if base[x] == "documented" else "documented"
                if concl(st)[cn] != b[cn]:
                    sets.append(combo)
            if sets:
                found = (k, sets)
                break
        if not found:
            fl.append(dict(proposition=cn, baseline_value=b[cn], operation=dname + ": " + opdesc, min_flips=">4",
                           n_minimal_sets=0, flip_set_index="", cells="", documented_after="", unknown_after=""))
            continue
        k, sets = found
        for i, combo in enumerate(sets, 1):
            nd = sum(1 for x in allk if (base[x] == "documented") != (x in combo))
            fl.append(dict(proposition=cn, baseline_value=b[cn], operation=dname + ": " + opdesc, min_flips=k,
                           n_minimal_sets=len(sets), flip_set_index=i, cells=";".join(combo), documented_after=nd, unknown_after=45 - nd))
CONTESTED = {"INC-ANT-INT/D2", "INC-ANT-OP46/D2", "INC-AISI-SOL/D5", "INC-OAI-MAY/D4", "INC-OAI-ART/D5", "INC-AISI-SOL/D4"}
weak = [key(r) for r in cur if r["status"] == "documented" and (r["support_type"] == "inferred" or r["claim_strength"].startswith("downgraded") or key(r) in CONTESTED)]
st = dict(base)
for x in weak:
    st[x] = "unknown"
cw = concl(st)
nd = sum(s == "documented" for s in st.values())
fl.append(dict(proposition="weak-support scenario (sensitivity.py definition: support inferred, claim strength downgraded, or the 6 contested cells)",
               baseline_value="", operation="all weak documented->unknown", min_flips=len(weak), n_minimal_sets="", flip_set_index="",
               cells=";".join(weak), documented_after=nd, unknown_after=45 - nd))
fl.append(dict(proposition="weak-support scenario: propositions changed", baseline_value="", operation="", min_flips="", n_minimal_sets="",
               flip_set_index="", cells=";".join(c for c in b if cw[c] != b[c]) or "none", documented_after="", unknown_after=""))
write_csv(os.path.join(RESULTS, "appendix_e_flips.csv"), list(fl[0].keys()), fl)
log("analyst_round13.py", "change_provenance %d rows, org_structure %d rows, appendix_e_flips %d rows" % (len(prov), len(org), len(fl)))

from collections import Counter
print("provenance status changes by class:", Counter(p["trigger_class"] for p in prov if p["change_type"] == "status"))
print("provenance all rows by class:", Counter(p["trigger_class"] for p in prov))
print("units with >=2 orgs:", sorted({o["unit"] for o in org if o["n_unit_organisations"] >= 2}))
print("cells with >=2 whole-support orgs:", [o["cell"] for o in org if o["n_whole_support_orgs"] >= 2])
for cn in b:
    for dname in OPS:
        r = [x for x in fl if x["proposition"] == cn and x["operation"].startswith(dname)]
        print(cn, b[cn], "|", dname, "| min", r[0]["min_flips"], "| sets", r[0]["n_minimal_sets"], "|", r[0]["cells"] if len(r) <= 3 else "e.g. " + r[0]["cells"])
print("weak:", weak, nd, 45 - nd, [c for c in b if cw[c] != b[c]])
