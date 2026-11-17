"""Task 9: agreement between the two blinded human coders, and between each coder and the AI coding.

Run AFTER both coders have filled their sheets:   python3 -I blind_coding/agreement.py
Reads: blind_coding/sheet_items_coder_*.csv, sheet_relations_coder_*.csv (filled), the key in blind_coding/key/,
and the AI coding in analysis/ (v1.1). Writes: blind_coding/agreement_results.csv and
blind_coding/disagreements_for_adjudication.csv (with blank adjudication columns).
Statistics, computed separately for item-level evidence status and source-level relation:
  raw agreement; Cohen's kappa (Cohen 1960); Gwet's AC1 (Gwet 2008), with the full category set as q;
  Krippendorff's alpha (nominal, 2 coders) as a cross-check.
Only rows coded by both parties are compared; the number compared is reported.
Standard library only.
"""
import csv, os, sys
from collections import Counter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BC = os.path.join(ROOT, "blind_coding")
STATUS = ["supported", "partially_supported", "unknown", "contested", "contradicted"]
RELATION = ["supports", "partial", "hedged", "relays", "contradicts", "none"]
CODERS = {"A": "coder_A_Laeeq", "B": "coder_B_Iftikhar"}


def rd(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def clean(v):
    return v.strip().lower().replace(" ", "_").replace("-", "_") if v else ""


def stats(pairs, cats):
    """pairs: list of (code1, code2). Returns raw agreement, Cohen's kappa, Gwet's AC1, Krippendorff's alpha."""
    n = len(pairs)
    if n == 0:
        return dict(n=0, raw=None, kappa=None, ac1=None, alpha=None)
    pa = sum(a == b for a, b in pairs) / n
    c1, c2 = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe_k = sum((c1[k] / n) * (c2[k] / n) for k in cats)
    kappa = (pa - pe_k) / (1 - pe_k) if pe_k < 1 else None
    q = len(cats)
    pi = {k: (c1[k] + c2[k]) / (2 * n) for k in cats}
    pe_g = sum(pi[k] * (1 - pi[k]) for k in cats) / (q - 1)
    ac1 = (pa - pe_g) / (1 - pe_g) if pe_g < 1 else None
    # Krippendorff's alpha, nominal, two coders, no missing values
    tot = Counter(a for a, _ in pairs) + Counter(b for _, b in pairs)
    N = 2 * n
    do = sum(a != b for a, b in pairs) * 2 / N
    de = sum(tot[k] * tot[m] for k in tot for m in tot if k != m) / (N * (N - 1))
    alpha = 1 - do / de if de > 0 else None
    r = lambda x: None if x is None else round(x, 4)
    return dict(n=n, raw=r(pa), kappa=r(kappa), ac1=r(ac1), alpha=r(alpha))


def main():
    key = {r["item_id"]: r for r in rd(os.path.join(BC, "key", "sample_key_DO_NOT_GIVE_TO_CODERS.csv"))}
    ai_status = {r["proposition_id"]: r["evidence_status"] for r in rd(os.path.join(ROOT, "analysis", "atomic_propositions.csv"))}
    ai_rel = {}
    for r in rd(os.path.join(ROOT, "analysis", "proposition_support.csv")):
        ai_rel[(r["proposition_id"], r["source_id"])] = r["relation"]
    st, rel = {"AI": {}}, {"AI": {}}
    for iid, k in key.items():
        st["AI"][iid] = ai_status[k["proposition_id"]]
    for x in rd(os.path.join(BC, "sheet_relations_%s.csv" % CODERS["A"])):
        rel["AI"][(x["item_id"], x["source_id"])] = ai_rel.get((key[x["item_id"]]["proposition_id"], x["source_id"]), "none")
    problems = []
    for c, name in CODERS.items():
        st[c] = {r["item_id"]: clean(r["evidence_status"]) for r in rd(os.path.join(BC, "sheet_items_%s.csv" % name)) if clean(r["evidence_status"])}
        rel[c] = {(r["item_id"], r["source_id"]): clean(r["relation"]) for r in rd(os.path.join(BC, "sheet_relations_%s.csv" % name)) if clean(r["relation"])}
        problems += ["%s: invalid status %r" % (c, v) for v in set(st[c].values()) if v not in STATUS]
        problems += ["%s: invalid relation %r" % (c, v) for v in set(rel[c].values()) if v not in RELATION]
    if problems:
        sys.exit("Fix the sheets first:\n  " + "\n  ".join(problems))
    if not st["A"] or not st["B"]:
        sys.exit("The sheets are not filled in yet (coder A: %d items, coder B: %d items). Nothing computed." % (len(st["A"]), len(st["B"])))
    out = []
    for a, b in (("A", "B"), ("A", "AI"), ("B", "AI")):
        for level, data, cats in (("evidence_status (item)", st, STATUS), ("relation (source x item)", rel, RELATION)):
            common = sorted(set(data[a]) & set(data[b]))
            s = stats([(data[a][k], data[b][k]) for k in common], cats)
            out.append(dict(comparison="%s vs %s" % (a, b), level=level, n_compared=s["n"], raw_agreement=s["raw"],
                            cohens_kappa=s["kappa"], gwets_ac1=s["ac1"], krippendorffs_alpha=s["alpha"]))
    with open(os.path.join(BC, "agreement_results.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(out)
    dis = []
    for iid in sorted(set(st["A"]) & set(st["B"])):
        if st["A"][iid] != st["B"][iid]:
            dis.append(dict(item_id=iid, proposition_id=key[iid]["proposition_id"], level="evidence_status", source_id="",
                            coder_A=st["A"][iid], coder_B=st["B"][iid], ai=st["AI"][iid], adjudicated_code="", deciding_passage="", reason="", adjudicator="", date=""))
    for k in sorted(set(rel["A"]) & set(rel["B"])):
        if rel["A"][k] != rel["B"][k]:
            dis.append(dict(item_id=k[0], proposition_id=key[k[0]]["proposition_id"], level="relation", source_id=k[1],
                            coder_A=rel["A"][k], coder_B=rel["B"][k], ai=rel["AI"].get(k, "none"), adjudicated_code="", deciding_passage="", reason="", adjudicator="", date=""))
    cols = ["item_id", "proposition_id", "level", "source_id", "coder_A", "coder_B", "ai", "adjudicated_code", "deciding_passage", "reason", "adjudicator", "date"]
    with open(os.path.join(BC, "disagreements_for_adjudication.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(dis)
    for r in out:
        print(r)
    print(len(dis), "disagreements between the two human coders written for adjudication")


if __name__ == "__main__":
    main()
