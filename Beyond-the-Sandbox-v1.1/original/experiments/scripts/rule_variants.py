"""Round 12 (plan D-e): recount the tags under the coding-rule choices a reader could question, and say which
abstract claims change. Reads data/coded_evidence.csv; writes results/rule_variants.csv and rule_variants.json.
Variants: V0 baseline | V1 strict D2 (D2 documented only for a verbatim model statement) |
V2 independent corroboration only (>=2 references from different organisations, each supporting the whole proposition) |
V3 credentials-only L3 boundary for D5 | V4 HF/D2 = unknown.
Counts only; the classification choices below are the experimenter's and are written to rule_variants.json.
Run: python -I scripts/rule_variants.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, rows, write_csv, log, DIMS

ORG = {"R01": "OpenAI", "R02": "OpenAI", "R03": "Hugging Face", "R04": "Hugging Face", "R07": "METR", "R08": "Anthropic",
       "R10": "UK AISI", "R24": "UK AISI", "R25": "Anthropic", "R26": "Anthropic"}
# D2 documented cells whose deciding passage is a verbatim quotation of the model's own words
VERBATIM_D2 = {"INC-OAI-HF"}   # R07: "The user only authorizes target server, not HF infra" (agent CoT, quoted)
# other documented D2 cells: reported model answer (paraphrase/statistic): OP46, OP47, INT, AISI-MY5
# L3 under the credentials-only boundary: the D5 passage shows credentials/accounts the agent was not issued
# round 13: built from the d5_tree_branch field of coded_evidence.csv, not from a hand-typed list (see below)

base = rows("coded_evidence.csv")


def claims(status, refs, lv):
    doc = [k for k, s in status.items() if s == "documented"]
    unk = [k for k, s in status.items() if s != "documented"]
    dd = {d: sum(1 for k in doc if k[1] == d) for d in DIMS}
    ud = {d: sum(1 for k in unk if k[1] == d) for d in DIMS}
    nref = lambda k: len(refs[k].split(";"))
    single_ref = [k for k in doc if nref(k) == 1]
    multi_org = [k for k in doc if len({ORG[r] for r in refs[k].split(";")}) >= 2]
    ant = [k for k in doc if k[0].startswith("INC-ANT")]
    r08 = [k for k in ant if refs[k] == "R08"]
    d5u = {k[0] for k in doc if k[1] == "D5"}
    return {
        "documented": len(doc), "unknown": len(unk),
        "documented_by_dim_D1-D5": "/".join(str(dd[d]) for d in DIMS),
        "unknown_by_dim_D1-D5": "/".join(str(ud[d]) for d in DIMS),
        "D2_has_most_unknowns": ud["D2"] > max(v for d, v in ud.items() if d != "D2"),
        "D2_least_documented": dd["D2"] < min(v for d, v in dd.items() if d != "D2"),
        "single_reference_cells": len(single_ref),
        "documented_left_after_dropping_single_reference_cells": len(doc) - len(single_ref),
        "anthropic_cells_documented": len(ant),
        "anthropic_cells_resting_on_R08_alone": len(r08),
        "cells_with_references_from_2plus_organisations": len(multi_org),
        "D5_units_L1/L2/L3": "/".join(str(sum(1 for u in d5u if lv.get(u) == l)) for l in ("L1", "L2", "L3")),
    }


status0 = {(r["unit"], r["code"]): r["status"] for r in base}
refs0 = {(r["unit"], r["code"]): r["reference"] for r in base}
lv0 = {r["unit"]: r["effect_level"] for r in base if r["code"] == "D5" and r["status"] == "documented"}
br0 = {r["unit"]: r["d5_tree_branch"].split(" -> ")[0] for r in base if r["code"] == "D5" and r["status"] == "documented"}
CRED_ONLY_L3 = sorted(u for u, b in br0.items() if "C" in b.split(";"))   # V3: a credential/account (C) branch
EFFECT_ONLY_L3 = sorted(u for u, b in br0.items() if set(b.split(";")) & {"N", "P"})   # V3b: non-public data or persistent state
lv3 = {u: ("L3" if u in CRED_ONLY_L3 else "L2") for u in lv0}
lv3b = {u: ("L3" if u in EFFECT_ONLY_L3 else "L2") for u in lv0}
V = [("V0 baseline (round-13 coding)", dict(status0), lv0, "as coded")]
s = dict(status0)
for k in s:
    if k[1] == "D2" and s[k] == "documented" and k[0] not in VERBATIM_D2:
        s[k] = "unknown"
V.append(("V1 strict D2 (verbatim model statement only)", s, lv0,
          "D2 documented only for OAI-HF (quoted agent CoT); OP46, OP47, INT, AISI-MY5 are reported answers or paraphrased CoT -> unknown"))
partial0 = {(r["unit"], r["code"]): [x for x in r["partial_support"].replace(" ", "").split(";") if x] for r in base}
# round 14 (R14-1b): references listed in partial_support (support only part of the proposition) do not count toward S2
s = {k: ("documented" if (v == "documented" and len({ORG[r] for r in refs0[k].split(";") if r not in partial0[k]}) >= 2) else "unknown")
     for k, v in status0.items()}
V.append(("V2 independent corroboration only", s, lv0,
          "documented only with references from >=2 organisations (R08+R25 are both Anthropic; HF/D4 R02+R03 are OpenAI and Hugging Face but each supports only its own part of the proposition, so since round 14 neither counts as whole support and S2 = 0 documented). Reports disclosure structure, not evidence quality"))
V.append(("V3 credentials-only L3 boundary", dict(status0), lv3,
          "D5 status unchanged; L3 only where the unit's D5 branch field contains C (credential or account of another party): " + ", ".join(CRED_ONLY_L3)))
V.append(("V3b effect-only L3 boundary", dict(status0), lv3b,
          "D5 status unchanged; L3 only where the branch field contains N (non-public data) or P (persistent state): " + ", ".join(EFFECT_ONLY_L3)))
s = dict(status0)
s[("INC-OAI-HF", "D2")] = "unknown"
V.append(("V4 OAI-HF/D2 = unknown", s, lv0, "the blind re-check challenge withdrawn"))

s = dict(status0)
s[("INC-OAI-HF", "D1")] = "unknown"
V.append(("V5 OAI-HF/D1 = unknown (round-12 coding)", s, lv0, "the Q4-based exception: R02 IV.A treated as not supporting D1"))

# V3c (analyst, round 13): effect-only boundary rebuilt from the coded D3 AND D5 passages rather than the branch field.
# Hand reading of each quoted passage (ANALYSIS.md round 13): P also for INC-ANT-MY5 (D3: package 'installed on 15
# third-party hosts' = persistent state on systems the agent was not authorized for); INC-OAI-HF N is qualified (the
# passage does not say the datasets were non-public), so HF is L2 here.
EFFECT_ONLY_L3_PASSAGES = ["INC-ANT-INT", "INC-ANT-MY5", "INC-ANT-OP46", "INC-ANT-OP47", "INC-OAI-MAY"]
V.append(("V3c effect-only L3 from D3/D5 passages (analyst)", dict(status0),
          {u: ("L3" if u in EFFECT_ONLY_L3_PASSAGES else "L2") for u in lv0},
          "as V3b (which already carries INC-ANT-MY5 as P) but drops only INC-OAI-HF (N qualified, passage does not say non-public):" + ", ".join(EFFECT_ONLY_L3_PASSAGES)))

# V6 (analyst, round 13): V11 human coding plus only the cell-specific changes a human asked for.
# laeeq 2026-11-05 (chat.jsonl, priority 1): re-tag Mythos 5 D2 (the documented one, INC-ANT-MY5) and HF D1;
# answers.md Q4 (HF/D1 unknown) is superseded by Q5 (HF/D1 documented on R02). Net: V11 with INC-ANT-MY5/D2 unknown.
# References are V11's. D5 levels did not exist in V11 (agent-introduced), so the D5 column is n/a.
import csv as _csv
v11 = list(_csv.DictReader(open(os.path.join(DATA, "..", "..", "inputs", "V11_Coded_Evidence.csv"), encoding="utf-8")))
s6 = {(r["unit"], r["code"]): r["status"] for r in v11}
refs6 = {(r["unit"], r["code"]): r["reference"] for r in v11}
s6[("INC-ANT-MY5", "D2")] = "unknown"
s6[("INC-OAI-HF", "D1")] = "documented"
V6 = ("V6 V11 human coding + human-requested changes only", s6, {},
      "V11 statuses and references; human cell-specific changes only: INC-ANT-MY5/D2 -> unknown (laeeq 2026-11-05); INC-OAI-HF/D1 documented (Q4 superseded by Q5; net no change). All other changes (round-1 re-reads, audits, D2 rules, D5 levels) were made by AI agents and are excluded")

res = [claims(st, refs0, lv) for _, st, lv, _ in V]
V.append(V6)
res.append(claims(s6, refs6, {}))
res[-1]["D5_units_L1/L2/L3"] = "n/a (no levels in V11)"
out = []
for (name, st, lv, note), c in zip(V, res):
    ch = [k for k in c if c[k] != res[0][k]]
    out.append({"variant": name, "rule_note": note, **c, "claims_that_change_vs_V0": "; ".join(ch) or "none"})
write_csv(os.path.join(RESULTS, "rule_variants.csv"), list(out[0].keys()), out)
json.dump({"variants": out, "classification_choices": {"org_map": ORG, "verbatim_D2_units": sorted(VERBATIM_D2),
          "credentials_only_L3_units": CRED_ONLY_L3, "effect_only_L3_units": EFFECT_ONLY_L3, "effect_only_L3_units_from_passages": EFFECT_ONLY_L3_PASSAGES}}, open(os.path.join(RESULTS, "rule_variants.json"), "w"), indent=1)
log("rule_variants.py", "%d variants written to rule_variants.csv" % len(out))
for o in out:
    print(o["variant"], "|", o["documented"], "/", o["unknown"], "| doc", o["documented_by_dim_D1-D5"], "unk", o["unknown_by_dim_D1-D5"],
          "| D5 L1/2/3", o["D5_units_L1/L2/L3"], "| changes:", o["claims_that_change_vs_V0"])
