"""Analyst round 13 (§Z4): read-only check of the post-Z-1 draft against
provenance_net.json, rule_variants.csv, table3_extra.csv and appendix_e_flips.csv.
Writes nothing to data/. Prints each expected draft string, whether it was found,
and every occurrence of "33/12" with its context.
Run from experiments/:  python -I scripts/analyst_round13j.py
"""
import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
draft = (HERE.parent / "draft.md").read_text()
flat = re.sub(r"\s+", " ", draft)

rv = {r["variant"].split()[0]: r for r in csv.DictReader(open(HERE / "results/rule_variants.csv"))}
t3 = {r["rule"]: r for r in csv.DictReader(open(HERE / "results/table3_extra.csv"))}
pn = json.load(open(HERE / "results/provenance_net.json"))
fl = list(csv.DictReader(open(HERE / "results/appendix_e_flips.csv")))

for k, r in rv.items():
    print(k, r["documented"], r["unknown"], r["documented_by_dim_D1-D5"], r["unknown_by_dim_D1-D5"],
          r["D2_has_most_unknowns"], r["single_reference_cells"],
          r["cells_with_references_from_2plus_organisations"], r["D5_units_L1/L2/L3"])

S = {"V0": "S0", "V1": "S1", "V2": "S2", "V3": "S3", "V3b": "S3b", "V3c": "S3c", "V4": "S4", "V5": "S5", "V6": "S6"}
checks = []
# Table III rows: "| S? ... | d/u | L |"
for v, s in S.items():
    r = rv[v]
    m = re.search(r"\|\s*" + re.escape(s) + r" [^|]*\|\s*([0-9]+/[0-9]+)\s*\|\s*([^|]+?)\s*\|", draft)
    got = m.groups() if m else None
    lv = r["D5_units_L1/L2/L3"]
    exp_l = lv if lv not in ("0/0/0",) and v not in ("V2", "V6") else "—"
    ok = bool(m) and got[0] == f"{r['documented']}/{r['unknown']}" and (got[1] == exp_l or (v in ("V2", "V6") and got[1] == "—"))
    checks.append((f"Table III {s}", f"{r['documented']}/{r['unknown']} {exp_l}", got, ok))
for rule, label in [("D2 contemporaneous or mixed", "D2 contemporaneous or mixed"),
                    ("D2 strictly contemporaneous", "D2 strictly contemporaneous"),
                    ("Retain multi-reference cells only", "Retain multi-reference cells")]:
    r = t3[rule]
    m = re.search(r"\|\s*" + re.escape(label) + r"[^|]*\|\s*([0-9]+/[0-9]+)\s*\|", draft)
    got = m.group(1) if m else None
    checks.append((f"Table III {label}", f"{r['documented']}/{r['unknown']}", got, got == f"{r['documented']}/{r['unknown']}"))

# provenance_net
words = {7: "seven", 1: "one", 2: "Two", 8: "Eight"}
checks.append(("prov: 8 of 45 differ", "Eight of the 45", None, "Eight of the 45 current statuses differ" in flat
               and len(pn["net_changes"]) == 8))
checks.append(("prov: 7 AI-agent", pn["net_AI_agent"], None, "seven were changed by AI agents" in flat and pn["net_AI_agent"] == 7))
checks.append(("prov: 1 human", pn["net_human_requested"], None, "one at the author’s explicit request" in flat and pn["net_human_requested"] == 1))
checks.append(("prov: 2 restored", len(pn["restored_cells"]), None, "Two further cells were changed and later restored" in flat and len(pn["restored_cells"]) == 2))
checks.append(("prov: l.234 seven net", 7, None, "Seven net status changes were made by AI agents" in flat))

# appendix_e_flips
def row(prop, op):
    return [r for r in fl if r["proposition"].startswith(prop) and r["operation"].startswith(op)]
c2b = row("C2", "both")[0]; c2d = row("C2", "documented")[0]; c6b = row("C6", "both")[0]
weak = [r for r in fl if r["proposition"].startswith("weak-support scenario (")][0]
weakch = [r for r in fl if r["proposition"].startswith("weak-support scenario: propositions")][0]
checks.append(("AppE C2/C5 3 flips, 220 / 56", (c2b["min_flips"], c2b["n_minimal_sets"], c2d["n_minimal_sets"]), None,
               c2b["min_flips"] == "3" and "C2 and C5 require three flips" in flat and "220 minimal sets" in flat and "56 when only" in flat
               and c2b["n_minimal_sets"] == "220" and c2d["n_minimal_sets"] == "56"))
checks.append(("AppE C6 2 flips", c6b["min_flips"], None, c6b["min_flips"] == "2" and "C6 requires two flips" in flat))
checks.append(("AppE weak 34/11, none changed", (weak["documented_after"], weak["unknown_after"], weakch["cells"]), None,
               weak["documented_after"] == "34" and weak["unknown_after"] == "11" and weakch["cells"] == "none"
               and "34 documented and 11 unknown decisions" in flat and "no tracked proposition changes" in flat))
names = {"INC-OAI-MAY/D4": "OpenAI May D4", "INC-OAI-ART/D5": "Artifactory D5", "INC-ANT-OP46/D2": "Opus 4.6 D2",
         "INC-ANT-INT/D2": "Anthropic internal-model D2", "INC-AISI-SOL/D4": "AISI Sol D4", "INC-AISI-SOL/D5": "AISI Sol D5"}
checks.append(("AppE weak cell list", weak["cells"], None, all(names[c] in flat for c in weak["cells"].split(";"))
               and set(weak["cells"].split(";")) == set(names)))

bad = 0
for name, exp, got, ok in checks:
    bad += not ok
    print(("OK  " if ok else "FAIL"), name, "| expected:", exp, "| draft:", got)
print("numeric mismatches:", bad, "of", len(checks))

print("\n'33/12' occurrences:")
for m in re.finditer(r"33/12|33 documented", flat):
    print("  ...", flat[max(0, m.start() - 160): m.end() + 40], "...")
