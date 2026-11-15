"""E5: evidence class (O/A/I/X) x claim type (dimension). Class is provenance, not a quality rank.

Per-row columns are derived mechanically from sources.csv 'relevance':
  directness  = direct if any cited ref is a 'primary incident account' or 'external investigation', else indirect
  independence= 'beyond operator' if the row cites a ref whose relevance is not an operator/primary disclosure
                (external investigation, secondary aggregator) or its class is A/I; else 'operator only'
These are descriptive labels derived from the ledger text, not new judgements about the sources.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

cod, srcs = rows("coded_evidence.csv"), rows("sources.csv")
rel = {s["ref"]: s["relevance"] for s in srcs}
CLS = ["O", "A", "I", "X"]
detail = []
for r in cod:
    refs = [x for x in r["reference"].split(";") if x]
    rels = [rel[x] for x in refs]
    direct = any(v.startswith(("primary incident", "external investigation")) for v in rels)
    indep = r["evidence_class"] in ("A", "I") or any(v.startswith(("external investigation", "secondary")) for v in rels)
    detail.append({"unit": r["unit"], "code": r["code"], "status": r["status"], "evidence_class": r["evidence_class"],
                   "n_refs": len(refs), "refs": r["reference"],
                   "directness": "direct" if direct else "indirect",
                   "independence": "beyond operator" if indep else "operator only"})
write_csv(os.path.join(RESULTS, "evidence_class_rows.csv"), list(detail[0]), detail)
tab = []
for c in CLS:
    sel = [d for d in detail if d["evidence_class"] == c]
    row = {"class": c, **{d: sum(1 for x in sel if x["code"] == d) for d in DIMS}, "total": len(sel),
           "direct": sum(x["directness"] == "direct" for x in sel),
           "beyond_operator": sum(x["independence"] == "beyond operator" for x in sel)}
    tab.append(row)
tab.append({"class": "all", **{d: sum(1 for x in detail if x["code"] == d) for d in DIMS}, "total": len(detail),
            "direct": sum(x["directness"] == "direct" for x in detail),
            "beyond_operator": sum(x["independence"] == "beyond operator" for x in detail)})
write_csv(os.path.join(RESULTS, "evidence_class_matrix.csv"), list(tab[0]), tab)
names = {"O": "O operator disclosure", "A": "A affected-party report", "I": "I external investigation", "X": "X replay/benchmark"}
tex = [r"\begin{tabular}{lrrrrrr}", r"\toprule", "Class & " + " & ".join(DIMS) + r" & Total \\", r"\midrule"]
for t in tab:
    lab = names.get(t["class"], "All rows")
    tex.append(lab + " & " + " & ".join(str(t[d]) for d in DIMS) + f' & {t["total"]}' + r" \\")
tex += [r"\bottomrule", r"\end{tabular}"]
open(os.path.join(RESULTS, "evidence_class_matrix.tex"), "w").write("\n".join(tex) + "\n")
log("evidence_class_matrix.py", "wrote results/evidence_class_matrix.csv|tex and evidence_class_rows.csv; class counts "
    + ", ".join(f'{t["class"]}={t["total"]}' for t in tab) + "; class X is 0 coded rows (replay results appear only in qualifications)")
for t in tab:
    print(t)
