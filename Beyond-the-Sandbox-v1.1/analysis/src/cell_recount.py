"""Cell-level recount for v1.0 and v1.1 from STORED data only (task 3/4): Table I, S0-S9, leave-one-source-out,
stopping mechanisms and D5 branch counts. Standard library only.
Run:  python3 -I analysis/src/cell_recount.py      -> analysis/cell_level_results.json, analysis/table1_v1.0.csv,
                                                      analysis/table1_v1.1.csv
In v1.0 the partial-support judgments of S2, S3 and leave-one-out existed only in the manuscript text; they are
reproduced here twice: from the stored column (empty) and with the in-text judgments. In v1.1 they are stored
(erratum E12-E14), so the two coincide.
"""
import csv, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, EXP, ANALYSIS, ORG, read_csv, write_csv

MATRIX = {"v1.0": os.path.join(EXP, "protocol", "coded_evidence_case_study_v1.0.csv"),
          "v1.1": os.path.join(ANALYSIS, "matrix_v1.1", "coded_evidence_case_study_v1.1.csv")}
V11_HUMAN = os.path.join(ROOT, "original", "inputs", "V11_Coded_Evidence.csv")
UNITS = ["INC-OAI-MAY", "INC-OAI-ART", "INC-OAI-HF", "INC-ANT-OP46", "INC-ANT-OP47", "INC-ANT-MY5", "INC-ANT-INT",
         "INC-AISI-MY5", "INC-AISI-SOL"]
LABEL = {"INC-OAI-MAY": "OpenAI May", "INC-OAI-ART": "OpenAI Artifactory", "INC-OAI-HF": "OpenAI Hugging Face",
         "INC-ANT-OP46": "Anthropic Opus 4.6", "INC-ANT-OP47": "Anthropic Opus 4.7", "INC-ANT-MY5": "Anthropic Mythos 5",
         "INC-ANT-INT": "Anthropic internal model", "INC-AISI-MY5": "AISI Mythos 5", "INC-AISI-SOL": "AISI Sol"}
DIMS = ["D1", "D2", "D3", "D4", "D5"]
PARTIAL_IN_TEXT = {("INC-OAI-HF", "D4"): {"R02", "R03"}, ("INC-ANT-OP47", "D4"): {"R25"}, ("INC-ANT-OP47", "D5"): {"R25"}}
MECH = (("self-stop", "Self-stop"), ("third-party removal", "Third party"), ("affected-party", "Affected party"),
        ("operator halt", "Operator halt"), ("external stop", "External technical"), ("signal only", "Signal only"))


def mech(s):
    s = s.lower()
    for kw, lab in MECH:
        if kw in s:
            return lab
    return "other"


def recount(path):
    M = read_csv(path)
    key = lambda r: (r["unit"], r["code"])
    row = {key(r): r for r in M}
    refs = {key(r): [x.strip() for x in r["reference"].split(";") if x.strip()] for r in M}
    st0 = {key(r): r["status"] for r in M}
    stored = {k: {x.strip() for x in row[k]["partial_support"].split(";") if x.strip()} for k in row}
    in_text = {k: stored[k] | PARTIAL_IN_TEXT.get(k, set()) for k in row}
    res = {}

    def split(st):
        c = Counter(st.values())
        return [c["documented"], c["unknown"] + c["contradicted"]]

    def rule(fn):
        return split({k: (v if fn(k, v) else "unknown") if v == "documented" else v for k, v in st0.items()})

    def whole_orgs(k, partial):
        return {ORG.get(x, x) for x in refs[k] if x not in partial[k]}
    res["S0"] = split(st0)
    res["S0_documented_by_dim"] = {d: sum(1 for k, v in st0.items() if k[1] == d and v == "documented") for d in DIMS}
    res["S0_unknown_by_dim"] = {d: sum(1 for k, v in st0.items() if k[1] == d and v != "documented") for d in DIMS}
    res["unknown_cells"] = sorted("/".join(k) for k, v in st0.items() if v != "documented")
    res["S1"] = rule(lambda k, v: k[1] != "D2" or row[k]["d2_evidence_type"].startswith("verbatim"))
    res["S2_stored"] = rule(lambda k, v: len(whole_orgs(k, stored)) >= 2)
    res["S2_in_text"] = rule(lambda k, v: len(whole_orgs(k, in_text)) >= 2)
    res["S2_cells_stored"] = sorted("/".join(k) for k in st0 if st0[k] == "documented" and len(whole_orgs(k, stored)) >= 2)
    res["S3_stored"] = rule(lambda k, v: any(x not in stored[k] for x in refs[k]))
    res["S3_in_text"] = rule(lambda k, v: any(x not in in_text[k] for x in refs[k]))
    res["S4"] = rule(lambda k, v: k != ("INC-OAI-HF", "D2"))
    res["S5"] = rule(lambda k, v: k != ("INC-OAI-HF", "D1"))
    if os.path.exists(V11_HUMAN):
        s6 = {key(r): r["status"] for r in read_csv(V11_HUMAN)}
        s6[("INC-ANT-MY5", "D2")] = "unknown"   # the one human-requested status change (first version, Table V)
        res["S6"] = split(s6)
    res["S7"] = rule(lambda k, v: k[1] != "D2" or row[k]["d2_elicitation"] in ("contemporaneous", "mixed"))
    res["S8"] = rule(lambda k, v: k[1] != "D2" or row[k]["d2_elicitation"] == "contemporaneous")
    res["S9"] = rule(lambda k, v: len(refs[k]) >= 2)
    doc = [k for k, v in st0.items() if v == "documented"]
    res["documented_single_reference"] = sum(len(refs[k]) == 1 for k in doc)
    res["concentration"] = {r_: [sum(r_ in refs[k] for k in doc), sum(refs[k] == [r_] for k in doc)] for r_ in ("R08", "R02", "R10")}

    def loso(drop, partial):
        left = 0
        for k in doc:
            rem = [x for x in refs[k] if x != drop]
            whole = [x for x in rem if x not in partial[k]]
            if whole or len(rem) >= 2:
                left += 1
        return left
    res["LOO_in_text"] = {d: loso(d, in_text) for d in ("R08", "R02", "R10")}
    res["LOO_stored"] = {d: loso(d, stored) for d in ("R08", "R02", "R10")}
    res["D2_evidence_types"] = dict(Counter(row[k]["d2_evidence_type"] for k in doc if k[1] == "D2"))
    res["D2_verbatim_contemporaneous_cells"] = sorted("/".join(k) for k in doc if k[1] == "D2" and row[k]["d2_evidence_type"].startswith("verbatim")
                                                      and row[k]["d2_elicitation"] == "contemporaneous")
    res["D4_mechanisms"] = dict(Counter(mech(row[(u, "D4")]["response_stage"]) for u in UNITS))
    res["D4_mechanism_qualified"] = sorted(u for u in UNITS if "not stated" in row[(u, "D4")]["response_stage"])
    br = Counter()
    for u in UNITS:
        for x in row[(u, "D5")]["d5_tree_branch"].split(" -> ")[0].split(";"):
            if x in ("C", "N", "P"):
                br[x] += 1
    res["D5_branch_units"] = {b: br[b] for b in ("C", "N", "P")}
    res["D5_effect_levels"] = dict(Counter(row[(u, "D5")]["effect_level"] for u in UNITS))
    res["evidence_class_counts"] = dict(Counter(r["evidence_class"] for r in M))
    t1 = []
    for u in UNITS:
        d2 = row[(u, "D2")]
        d2txt = "—" if st0[(u, "D2")] != "documented" else "%s; %s" % (d2["d2_evidence_type"], d2["d2_direction"])
        t1.append(dict(unit=LABEL[u], **{d: ("D" if st0[(u, d)] == "documented" else "U") for d in DIMS},
                       d2_evidence=d2txt, stopping_mechanism=mech(row[(u, "D4")]["response_stage"]) +
                       (" (interruption not stated)" if "not stated" in row[(u, "D4")]["response_stage"] else ""),
                       d5_branches=", ".join(x for x in row[(u, "D5")]["d5_tree_branch"].split(" -> ")[0].split(";") if x in "CNP" and x) or "none"))
    return res, t1


def main():
    out = {}
    for v, p in MATRIX.items():
        if not os.path.exists(p):
            sys.exit("missing matrix " + p)
        out[v], t1 = recount(p)
        write_csv(os.path.join(ANALYSIS, "table1_%s.csv" % v), list(t1[0].keys()), t1)
    json.dump(out, open(os.path.join(ANALYSIS, "cell_level_results.json"), "w", encoding="utf-8"), indent=1)
    for k in out["v1.0"]:
        if out["v1.0"][k] != out["v1.1"][k]:
            print("%-34s v1.0=%-40s v1.1=%s" % (k, json.dumps(out["v1.0"][k])[:40], json.dumps(out["v1.1"][k])[:80]))


if __name__ == "__main__":
    main()
