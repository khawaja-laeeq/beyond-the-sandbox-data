"""Independent recount of the published case-study numbers and the revised proposition-level numbers.

Written from scratch for the 2026-11-12 audit. It does not import the study's scripts or the revision's build
script. Calculations read only the coded CSVs; the manuscript's published values appear only in PUBLISHED and are
used for comparison after calculation. Standard library only.
Run from the package root:  python3 -I reproducibility/independent_verify.py  [--json out.json]
"""
import csv, json, os, sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXP = os.path.join(ROOT, "original", "experiments")
FROZEN = os.path.join(EXP, "protocol", "coded_evidence_case_study_v1.0.csv")
V11 = os.path.join(ROOT, "original", "inputs", "V11_Coded_Evidence.csv")
AN = os.path.join(ROOT, "analysis")

def rd(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

M = rd(FROZEN)
DIMS = ["D1", "D2", "D3", "D4", "D5"]
key = lambda r: (r["unit"], r["code"])
refs = {key(r): [x.strip() for x in r["reference"].split(";") if x.strip()] for r in M}
st0 = {key(r): r["status"] for r in M}
# organization of each reference (publisher), defined here independently of the study's scripts
PUB = {"R01": "OpenAI", "R02": "OpenAI", "R03": "Hugging Face", "R04": "Hugging Face", "R07": "METR", "R08": "Anthropic",
       "R10": "UK AISI", "R24": "UK AISI", "R25": "Anthropic", "R26": "Anthropic"}
# partial-support assignments: (a) as stored in the frozen file; (b) as stated in the manuscript text (§III.C)
PARTIAL_STORED = {key(r): set(x for x in r["partial_support"].replace(" ", "").split(";") if x) for r in M}
PARTIAL_MS = defaultdict(set, {("INC-OAI-HF", "D4"): {"R02", "R03"}, ("INC-ANT-OP47", "D4"): {"R25"}, ("INC-ANT-OP47", "D5"): {"R25"}})

def split(st):
    c = Counter(st.values())
    return c["documented"], c["unknown"] + c["contradicted"]

def by_dim(st, s="documented"):
    return "/".join(str(sum(1 for k, v in st.items() if k[1] == d and v == s)) for d in DIMS)

res = {}
res["cells"] = len(M)
res["S0"] = split(st0)
res["S0_documented_by_dim"] = by_dim(st0)
res["S0_unknown_by_dim"] = by_dim(st0, "unknown")
res["contradicted"] = sum(v == "contradicted" for v in st0.values())

def rule(fn):
    return split({k: (v if fn(k, v) else "unknown") if v == "documented" else v for k, v in st0.items()})

row = {key(r): r for r in M}
res["S1"] = rule(lambda k, v: k[1] != "D2" or row[k]["d2_evidence_type"].startswith("verbatim"))
def whole_orgs(k, partial):
    return {PUB[x] for x in refs[k] if x not in partial[k]}
res["S2_stored_partial"] = rule(lambda k, v: len(whole_orgs(k, PARTIAL_STORED)) >= 2)
res["S2_manuscript_partial"] = rule(lambda k, v: len(whole_orgs(k, PARTIAL_MS)) >= 2)
res["S2_cells_stored"] = sorted("/".join(k) for k in st0 if st0[k] == "documented" and len(whole_orgs(k, PARTIAL_STORED)) >= 2)
res["S3_stored_partial"] = rule(lambda k, v: any(x not in PARTIAL_STORED[k] for x in refs[k]))
res["S3_manuscript_partial"] = rule(lambda k, v: any(x not in PARTIAL_MS[k] for x in refs[k]))
res["S4"] = rule(lambda k, v: k != ("INC-OAI-HF", "D2"))
res["S5"] = rule(lambda k, v: k != ("INC-OAI-HF", "D1"))
res["S7"] = rule(lambda k, v: k[1] != "D2" or row[k]["d2_elicitation"] in ("contemporaneous", "mixed"))
res["S8"] = rule(lambda k, v: k[1] != "D2" or row[k]["d2_elicitation"] == "contemporaneous")
res["S9"] = rule(lambda k, v: len(refs[k]) >= 2)
if os.path.exists(V11):
    v11 = {key(r): r["status"] for r in rd(V11)}
    s6 = dict(v11)
    s6[("INC-ANT-MY5", "D2")] = "unknown"     # the one human-requested status change (manuscript Table V)
    res["S6"] = split(s6)
    res["V11_initial"] = split(v11)
else:
    res["S6"] = "V11_Coded_Evidence.csv missing"

doc = [k for k, v in st0.items() if v == "documented"]
res["documented_single_reference"] = sum(len(refs[k]) == 1 for k in doc)
conc = {}
for r_ in sorted({x for k in doc for x in refs[k]}):
    n = sum(r_ in refs[k] for k in doc)
    sole = sum(refs[k] == [r_] for k in doc)
    conc[r_] = (n, sole)
res["concentration"] = conc
res["units_with_2plus_orgs_in_unit_refs"] = sorted(
    u for u in {k[0] for k in st0} if len({PUB.get(x, "?") for k in st0 if k[0] == u for x in refs[k]}) >= 2)

def loso(drop, partial):
    left = 0
    for k in doc:
        rem = [x for x in refs[k] if x != drop]
        whole = [x for x in rem if x not in partial[k]]
        if whole or len(rem) >= 2:
            left += 1
    return left
res["LOSO_any_ref_survives"] = {d: sum(any(x != d for x in refs[k]) for k in doc) for d in ("R08", "R02", "R10")}
res["LOSO_manuscript_rule"] = {d: loso(d, PARTIAL_MS) for d in ("R08", "R02", "R10", "R03", "R04", "R07", "R24", "R26")}

res["D2_evidence_types"] = dict(Counter(row[k]["d2_evidence_type"] for k in st0 if k[1] == "D2" and st0[k] == "documented"))
def mech(s):
    s = s.lower()
    for kw, lab in (("self-stop", "self-stop"), ("third-party removal", "third-party removal"), ("affected-party", "affected-party response"),
                    ("operator halt", "operator halt"), ("external stop", "external technical"), ("signal only", "signal only")):
        if kw in s:
            return lab
    return "other"
res["D4_mechanisms"] = dict(Counter(mech(row[k]["response_stage"]) for k in st0 if k[1] == "D4"))
br = Counter()
for k in st0:
    if k[1] == "D5":
        b = row[k]["d5_tree_branch"].split(" -> ")[0]
        for x in b.split(";"):
            if x in "CNP" and x:
                br[x] += 1
res["D5_branch_units"] = dict(br)

# ---------------- revised proposition-level counts, from the support table only
SUP = os.path.join(AN, "proposition_support.csv")
PROPS = os.path.join(AN, "atomic_propositions.csv")
DIS = os.path.join(AN, "cross_source_disagreements.csv")
if os.path.exists(SUP):
    props = rd(PROPS)
    sup = defaultdict(list)
    for r in rd(SUP):
        if r.get("secondary") == "True":   # v1.1: secondary analyses are never counted as an organization
            continue
        sup[r["proposition_id"]].append(r)
    agg = Counter()
    for p in props:
        rows = sup.get(p["proposition_id"], [])
        whole = [r for r in rows if r["relation"] in ("supports", "hedged")]
        strict = [r for r in rows if r["relation"] == "supports"]
        contra = [r for r in rows if r["relation"] == "contradicts"]
        agg["propositions"] += 1
        agg["supported_any"] += bool(whole)
        agg["unknown_no_support_row"] += not rows
        agg["with_counterevidence"] += bool(contra)
        orgs = {r["organization"] for r in whole}
        agg["two_org_agreement"] += len(orgs) >= 2
        fam = defaultdict(set)
        for r in strict:
            fam[r["organization"]].add(r["base_family"])
        o = list(fam)
        agg["independent"] += any(fam[o[i]].isdisjoint(fam[o[j]]) for i in range(len(o)) for j in range(i + 1, len(o)))
        agg["relay_only_second_org"] += (len(orgs) <= 1 and any(r["relation"] == "relays" for r in rows))
    res["revised"] = dict(agg)
    res["revised_disagreements"] = len(rd(DIS))
    res["revised_quote_rows"] = sum(len(v) for v in sup.values())

PUBLISHED = {"S0": (40, 5), "S1": (36, 9), "S2_manuscript_partial": (0, 45), "S3_manuscript_partial": (39, 6), "S4": (39, 6),
             "S5": (39, 6), "S6": (37, 8), "S7": (38, 7), "S8": (37, 8), "S9": (3, 42), "documented_single_reference": 37,
             "LOSO_manuscript_rule": {"R08": 21, "R02": 30, "R10": 33},
             "concentration": {"R08": (19, 17), "R02": (10, 9), "R10": (7, 7)},
             "D4_mechanisms": {"operator halt": 3, "external technical": 2, "third-party removal": 1, "affected-party response": 1, "self-stop": 1, "signal only": 1},
             "D5_branch_units": {"C": 7, "P": 4, "N": 2}}
cmp = []
for k, pub in PUBLISHED.items():
    got = res.get(k)
    if isinstance(pub, dict) and isinstance(got, dict):
        for kk, vv in pub.items():
            g = got.get(kk)
            g = tuple(g) if isinstance(g, (list, tuple)) else g
            cmp.append((k + ":" + kk, vv, g, vv == g))
    else:
        g = tuple(got) if isinstance(got, (list, tuple)) else got
        cmp.append((k, pub, g, pub == g))
res["comparison"] = [dict(item=a, published=b, recomputed=c, match=d) for a, b, c, d in cmp]
for a, b, c, d in cmp:
    print("%-45s published=%-28s recomputed=%-28s %s" % (a, b, c, "MATCH" if d else "DIFF"))
print(json.dumps({k: v for k, v in res.items() if k not in ("comparison",)}, indent=1, default=str))
if "--json" in sys.argv:
    json.dump(res, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1, default=str)
