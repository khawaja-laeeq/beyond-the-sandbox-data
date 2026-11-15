"""Round 14 (R14-1a). Run from experiments/: python3 -I scripts/stop_d2_profile.py
H1: who or what stopped the activity (D4 response_stage), H2: D2 direction x elicitation x contested_by.
Variants: V0 baseline coding | V1 strict D2 (D2 documented only for a verbatim model statement; D4 unchanged) |
V6 V11 coding + human-requested changes only. V11 (inputs/V11_Coded_Evidence.csv) has only status and evidence text, so every
category under V6 is labelled "AI-read from V11 evidence" (hand-assigned below, not computed); items V11 does not say are
reported as 'not stated in V11 evidence'.
Writes results/stop_agent.csv, results/d2_profile.csv, results/stop_d2_counts.json."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, PAPER, rows, write_csv, log, stage_cat

CATS = ["operator halt", "external technical", "third party", "affected party", "self", "signal only"]


R = rows("coded_evidence.csv")
cm = {(r["unit"], r["code"]): r for r in R}
units = [u["unit"] for u in rows("units.csv")]
v11 = {(r["unit"], r["code"]): r for r in csv.DictReader(open(os.path.join(PAPER, "inputs", "V11_Coded_Evidence.csv"), encoding="utf-8"))}

# V6 categories read by the experimenter (an AI) from the V11 evidence text of the D4 and D2 cells
AI = "AI-read from V11 evidence"
V6_STOP = {
    "INC-OAI-ART": "not stated in V11 evidence",       # 'Security alert and continuing evaluation described by operator': no stop is stated
    "INC-OAI-HF": "affected party",                    # 'Affected-party disclosure preceded operator attribution'
    "INC-ANT-OP46": "external technical",              # 'run ended on token budget'
    "INC-ANT-MY5": "third party",                       # 'PyPI removed package within one hour'
    "INC-ANT-INT": "self",                             # 'Model recognized out of scope and stopped itself'
    "INC-AISI-MY5": "operator halt",                   # 'evaluation stopped and isolated within hour'
    "INC-AISI-SOL": "operator halt",                   # 'Same institutional Tor alert and response' (read as the same evaluation-wide halt)
}
V6_D2 = {   # direction read from V11 evidence; V11 has no elicitation or contested field
    "INC-OAI-ART": "no permission belief stated",       # 'Agents coordinated toward scorer manipulation'
    "INC-OAI-HF": "no permission belief stated",        # 'METR interprets attacks as scorer investigation'
    "INC-ANT-OP46": "in scope",                         # 'Model believed external target part of CTF'
    "INC-ANT-OP47": "in scope",                         # 'Recognized real target but assumed authorized'
    "INC-ANT-INT": "no permission belief stated",       # 'Assumed simulated replica, later recognized real company'
}

stop, d2 = [], []
for var in ("V0", "V1", "V6"):
    for u in units:
        c = cm[(u, "D4")]
        if var == "V6":
            st = v11[(u, "D4")]["status"]
            cat = V6_STOP.get(u, "") if st == "documented" else ""
            stop.append(dict(variant=var, unit=u, d4_status=st, stop_category=cat if st == "documented" else "(unknown: not counted)",
                             basis=AI if st == "documented" else "V11 status", text=v11[(u, "D4")]["evidence"]))
        else:
            cat = stage_cat(c["response_stage"]) if c["status"] == "documented" else ""
            stop.append(dict(variant=var, unit=u, d4_status=c["status"], stop_category=cat or "(unknown: not counted)",
                             basis="coded response_stage field", text=c["response_stage"]))
    for u in units:
        c = cm[(u, "D2")]
        if var == "V6":
            st = {**{k: v["status"] for k, v in v11.items()}, ("INC-ANT-MY5", "D2"): "unknown"}[(u, "D2")]
            if st != "documented":
                continue
            d2.append(dict(variant=var, unit=u, direction=V6_D2[u], elicitation="not coded in V11", evidence_type="not coded in V11",
                           contested="not coded in V11", basis=AI + " (direction); V11 has no elicitation or contested field",
                           text=v11[(u, "D2")]["evidence"]))
            continue
        if c["status"] != "documented":
            continue
        if var == "V1" and c["d2_evidence_type"] != "verbatim model statement":
            continue
        direction = "out of scope (not authorized)" if c["d2_direction"].startswith("not authorized") else "in scope (authorized)"
        d2.append(dict(variant=var, unit=u, direction=direction, elicitation=c["d2_elicitation"], evidence_type=c["d2_evidence_type"],
                       contested="yes" if c["contested_by"] else "no", basis="coded d2_* and contested_by fields", text=c["d2_direction"]))

write_csv(os.path.join(RESULTS, "stop_agent.csv"), list(stop[0].keys()), stop)
write_csv(os.path.join(RESULTS, "d2_profile.csv"), list(d2[0].keys()), d2)


def tally(items, key):
    out = {}
    for i in items:
        out[i[key]] = out.get(i[key], 0) + 1
    return out


counts = {"labels": {"V6": AI + " for every category; V11 has only status and evidence text"}}
for var in ("V0", "V1", "V6"):
    s = [r for r in stop if r["variant"] == var and r["d4_status"] == "documented"]
    d = [r for r in d2 if r["variant"] == var]
    counts[var] = {"H1_n_units_with_D4_documented": len(s),
                   "H1_stop_category": {c: sum(1 for r in s if r["stop_category"] == c) for c in CATS + ["not stated in V11 evidence", "unclassified"] if any(r["stop_category"] == c for r in s)},
                   "H2_n_D2_documented": len(d), "H2_direction": tally(d, "direction"), "H2_elicitation": tally(d, "elicitation"),
                   "H2_evidence_type": tally(d, "evidence_type"), "H2_contested": tally(d, "contested"),
                   "H2_elicitation_x_evidence_type": {"%s | %s" % (k, e): sum(1 for r in d if r["elicitation"] == k and r["evidence_type"] == e) for k, e in
                                                      sorted({(r["elicitation"], r["evidence_type"]) for r in d})}}
exp = {"H1": {"operator halt": 3, "external technical": 2, "third party": 1, "affected party": 1, "self": 1, "signal only": 1},
       "H2_direction_in_scope": 4, "H2_direction_out_of_scope": 1, "H2_contemporaneous_verbatim": 1, "H2_post_hoc": 2, "H2_mixed": 1, "H2_contested": 3}
v0 = counts["V0"]
diff = []
if v0["H1_stop_category"] != exp["H1"]:
    diff.append("H1 differs: %s" % v0["H1_stop_category"])
if v0["H2_direction"].get("in scope (authorized)") != 4 or v0["H2_direction"].get("out of scope (not authorized)") != 1:
    diff.append("H2 direction differs: %s" % v0["H2_direction"])
if v0["H2_elicitation_x_evidence_type"].get("contemporaneous | verbatim model statement") != 1:
    diff.append("contemporaneous verbatim differs")
if v0["H2_elicitation"].get("post-hoc follow-up question") != 2 or v0["H2_elicitation"].get("mixed") != 1:
    diff.append("post-hoc/mixed differ")
if v0["H2_contested"].get("yes") != 3:
    diff.append("contested differs")
counts["lead_expectation"] = exp
counts["differences_from_lead_expectation"] = diff or ["none on the listed items"]
counts["note"] = ("The lead's elicitation list (1 contemporaneous verbatim + 2 post-hoc + 1 mixed) sums to 4, but 5 D2 cells are documented under V0: "
                  "the fifth is INC-ANT-INT, contemporaneous but a reported (paraphrased CoT) answer, not a verbatim statement. "
                  "Under V6 (MY5/D2 unknown) the documented D2 cells are OAI-ART, OAI-HF, OP46, OP47, INT, and V11 gives neither elicitation nor contested status; "
                  "V6 D4 has 7 documented units (MAY and OP47 are unknown in V11), and ART has no stop stated in the V11 evidence.")
json.dump(counts, open(os.path.join(RESULTS, "stop_d2_counts.json"), "w"), indent=1)
log("stop_d2_profile.py", "stop_agent.csv (%d rows), d2_profile.csv (%d rows), stop_d2_counts.json; differences: %s" % (len(stop), len(d2), "; ".join(counts["differences_from_lead_expectation"])))
print(json.dumps(counts, indent=1))
