"""Analyst round 13 (third pass, 2026-11-08 ~19:20Z). Run from experiments/: python3 -I scripts/analyst_round13b.py
READ-ONLY on data/. Writes:
  results/appendix_b_check.csv  -- regenerated: draft Appendix B vs data/coded_evidence.csv, now also status,
                                   D5 level and D5 branch letters (the old file checked references only)
  results/t5_variant_check.csv  -- T-5 headline claims (a)-(d) recomputed independently under V0, V1, V6 (+V2)
  results/single_flip_check.csv -- every single-cell flip and which propositions C1-C6 it changes
"""
import csv, os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, PAPER, write_csv, log, stage_cat  # noqa: E402

DIMS = ["D1", "D2", "D3", "D4", "D5"]
R = list(csv.DictReader(open(os.path.join(DATA, "coded_evidence.csv"), encoding="utf-8")))
units = {u["unit"]: u["cluster"] for u in csv.DictReader(open(os.path.join(DATA, "units.csv"), encoding="utf-8"))}
cm = {(r["unit"], r["code"]): r for r in R}
assert len(cm) == 45

# ---------------- 1. Appendix B: refs + status + level + branch ----------------
name = {"INC-OAI-MAY": "OpenAI May", "INC-OAI-ART": "OpenAI Artifactory", "INC-OAI-HF": "OpenAI Hugging Face",
        "INC-ANT-OP46": "Anthropic Opus 4.6", "INC-ANT-OP47": "Anthropic Opus 4.7", "INC-ANT-MY5": "Anthropic Mythos 5",
        "INC-ANT-INT": "Anthropic internal model", "INC-AISI-MY5": "AISI Mythos 5", "INC-AISI-SOL": "AISI Sol"}
inv = {v: k for k, v in name.items()}
txt = open(os.path.join(PAPER, "draft.md"), encoding="utf-8").read()
sec = txt.split("## Appendix B.")[1].split("## Appendix C.")[0]
SMAP = {"D": "documented", "U": "unknown", "C": "contradicted"}


def letters(s):
    return set(re.findall(r"\b([CNP])\b", s))


chk, seen = [], set()
for line in sec.splitlines():
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) >= 7 and c[0] in inv and re.fullmatch(r"D[1-5]", c[1]):
        k = (inv[c[0]], c[1]); seen.add(k); r = cm[k]
        d_refs = set(re.findall(r"@(R\d+)", c[-1])); s_refs = set(x for x in r["reference"].split(";") if x)
        d_stat = SMAP.get(c[2].split("/")[0].strip(), "?")
        d_lvl = (re.match(r"L[123]", c[5]) or [""])[0] if c[1] == "D5" else ""
        s_lvl = r["effect_level"] if c[1] == "D5" else ""
        s_br = r["d5_tree_branch"].split("->")[0] if c[1] == "D5" else ""
        d_br = letters(c[5].split("(")[1]) if (c[1] == "D5" and "(" in c[5]) else set()
        row = dict(unit=k[0], code=k[1], draft_refs=";".join(sorted(d_refs)), csv_refs=";".join(sorted(s_refs)),
                   equal="yes" if (d_refs and d_refs == s_refs) else "NO",
                   draft_status=d_stat, csv_status=r["status"], status_equal="yes" if d_stat == r["status"] else "NO",
                   draft_level=d_lvl, csv_level=s_lvl, level_equal="yes" if d_lvl == s_lvl else "NO",
                   draft_branch=";".join(sorted(d_br)), csv_branch=";".join(sorted(letters(s_br))),
                   branch_equal="yes" if d_br == letters(s_br) else "NO")
        # round 14 (R14-1d): D4 stage category (draft label vs coded response_stage, both mapped by _common.stage_cat)
        d_stg = stage_cat(c[4]) if c[1] == "D4" else ""
        s_stg = stage_cat(r["response_stage"]) if c[1] == "D4" else ""
        row.update(draft_stage=d_stg, csv_stage=s_stg, stage_equal="yes" if d_stg == s_stg else "NO")
        chk.append(row)
for k in cm:
    if k not in seen:
        chk.append(dict(unit=k[0], code=k[1], draft_refs="(row missing)", csv_refs=cm[k]["reference"], equal="NO",
                        draft_status="", csv_status=cm[k]["status"], status_equal="NO", draft_level="", csv_level="",
                        level_equal="NO", draft_branch="", csv_branch="", branch_equal="NO",
                        draft_stage="", csv_stage="", stage_equal="NO"))
write_csv(os.path.join(RESULTS, "appendix_b_check.csv"), list(chk[0]), chk)
bsum = {f: sum(r[f] == "yes" for r in chk) for f in ("equal", "status_equal", "level_equal", "branch_equal", "stage_equal")}
bsum["rows"] = len(chk); bsum["empty_draft_refs"] = sum(1 for r in chk if not r["draft_refs"])
print("appendix B", bsum)
for r in chk:
    if "NO" in (r["equal"], r["status_equal"], r["level_equal"], r["branch_equal"], r["stage_equal"]):
        print("  MISMATCH", r)


# ---------------- 2. T-5 claims per variant ----------------
def per_dim(st):
    return {d: (sum(1 for k, s in st.items() if k[1] == d and s == "documented"),
                sum(1 for k, s in st.items() if k[1] == d and s == "unknown")) for d in DIMS}


V0 = {k: r["status"] for k, r in cm.items()}
V1 = dict(V0)
for k, r in cm.items():
    if k[1] == "D2" and r["status"] == "documented" and r["d2_evidence_type"] != "verbatim model statement":
        V1[k] = "unknown"
v11 = {(r["unit"], r["code"]): r["status"] for r in
       csv.DictReader(open(os.path.join(PAPER, "inputs", "V11_Coded_Evidence.csv"), encoding="utf-8"))}
V6 = dict(v11); V6[("INC-ANT-MY5", "D2")] = "unknown"  # only human cell-specific change (laeeq 2026-11-05); Q4 superseded by Q5

ORG = {}
for s in csv.DictReader(open(os.path.join(DATA, "sources.csv"), encoding="utf-8")):
    ORG[s["ref"]] = s["citation"].split(",")[0].split("“")[0].strip()
ORG["R04"] = "Hugging Face"; ORG["R07"] = "METR"  # R04 author string is "Hugging Face security researchers"; R07 on metr.org
V2 = {k: ("documented" if r["status"] == "documented" and
          len({ORG[x] for x in r["reference"].split(";") if x and x not in r["partial_support"].replace(" ", "").split(";")}) >= 2
          else "unknown") for k, r in cm.items()}   # round 14 (R14-1b): partial-support references are not whole support

out = []
for vn, st in (("V0", V0), ("V1", V1), ("V6", V6), ("V2", V2)):
    pdm = per_dim(st); un = {d: pdm[d][1] for d in DIMS}
    top = max(un.values())
    a = un["D2"] == top and sum(v == top for v in un.values()) == 1 and top > 0
    b = pdm["D3"] == (9, 0) and pdm["D4"] == (9, 0)
    c = pdm["D1"] == (8, 1)
    docs = sorted(f"{k[0]}/{k[1]}" for k, s in st.items() if s == "documented")
    out.append(dict(variant=vn, documented=sum(s == "documented" for s in st.values()),
                    unknown=sum(s == "unknown" for s in st.values()),
                    **{f"{d}_doc/unk": f"{pdm[d][0]}/{pdm[d][1]}" for d in DIMS},
                    a_D2_most_unknowns="holds" if a else "fails",
                    b_D3_D4_9of9="holds" if b else "fails",
                    c_D1_8of1="holds" if c else "fails",
                    d_V2_1of45_HF_D4=("holds" if docs == ["INC-OAI-HF/D4"] else "fails") if vn == "V2" else "n/a",
                    documented_cells_if_le3=";".join(docs) if len(docs) <= 3 else ""))
write_csv(os.path.join(RESULTS, "t5_variant_check.csv"), list(out[0]), out)
for o in out:
    print(o)


# ---------------- 3. single-flip check (same proposition definitions as sensitivity.py) ----------------
def props(st):
    unks = [k for k, s in st.items() if s == "unknown"]
    pd = {d: sum(1 for k in unks if k[1] == d) for d in DIMS}
    top = sorted(pd.values(), reverse=True)
    dd = {d: sum(1 for k, s in st.items() if k[1] == d and s == "documented") for d in DIMS}
    return {"C1": not any(s == "contradicted" for s in st.values()),
            "C2": pd["D2"] == top[0] and top[0] > 0 and top[0] > top[1],
            "C3": len(unks) > 0 and all(k[1] == "D2" for k in unks),
            "C4": all(dd[d] == len(units) for d in ("D1", "D3", "D4", "D5")),
            "C5": dd["D2"] == min(dd.values()) and sum(v == dd["D2"] for v in dd.values()) == 1,
            "C6": len({units[k[0]] for k in unks}) >= 2}


base = props(V0); sf = []
for k in cm:
    st = dict(V0); st[k] = "unknown" if V0[k] == "documented" else "documented"
    p = props(st); ch = [c for c in base if p[c] != base[c]]
    sf.append(dict(cell=f"{k[0]}/{k[1]}", from_=V0[k], to=st[k], changed=";".join(ch)))
write_csv(os.path.join(RESULTS, "single_flip_check.csv"), list(sf[0]), sf)
chg = [s for s in sf if s["changed"]]
print("baseline props", base)
print("single flips that change a proposition:", chg)
log("analyst_round13b.py", "appendix_b_check %s; t5 variants %s; single flips changing a proposition %d"
    % (json.dumps(bsum), [(o["variant"], o["a_D2_most_unknowns"], o["b_D3_D4_9of9"], o["c_D1_8of1"]) for o in out], len(chg)))
