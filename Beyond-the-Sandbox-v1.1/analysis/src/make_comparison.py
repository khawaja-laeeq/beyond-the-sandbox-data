"""Task 4: list every value that differs between v1.0 and v1.1 -> analysis/v1.0_vs_v1.1_comparison.csv
Reads only generated outputs (run build_matrix_v1_1.py, build_analysis.py and cell_recount.py first)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ANALYSIS, EXP, read_csv, write_csv

V10M = os.path.join(EXP, "protocol", "coded_evidence_case_study_v1.0.csv")
V11M = os.path.join(ANALYSIS, "matrix_v1.1", "coded_evidence_case_study_v1.1.csv")


def flat(prefix, v, out):
    if isinstance(v, dict):
        for k, x in v.items():
            flat(prefix + "." + str(k), x, out)
    else:
        out[prefix] = v


def main():
    rows = []
    applied = read_csv(os.path.join(ANALYSIS, "matrix_v1.1", "erratum_applied.csv"))
    cause = {}
    for e in applied:
        cause.setdefault((e["cell"], e["field"]), []).append(e["fix_id"])
    m10 = {r["unit"] + "/" + r["code"]: r for r in read_csv(V10M)}
    m11 = {r["unit"] + "/" + r["code"]: r for r in read_csv(V11M)}
    for c in m10:
        for f in m10[c]:
            if f != "change_log" and m10[c][f] != m11[c][f]:
                rows.append(dict(level="matrix cell field", item=c, measure=f, v1_0=m10[c][f], v1_1=m11[c][f],
                                 cause=";".join(cause.get((c, f), ["?"]))))
    cl = json.load(open(os.path.join(ANALYSIS, "cell_level_results.json"), encoding="utf-8"))
    a, b = {}, {}
    flat("cell", cl["v1.0"], a); flat("cell", cl["v1.1"], b)
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            rows.append(dict(level="cell-level measure", item=k, measure=k.split(".", 1)[1], v1_0=json.dumps(a.get(k)),
                             v1_1=json.dumps(b.get(k)), cause="v1.1 matrix (erratum)"))
    s10 = json.load(open(os.path.join(ANALYSIS, "v1.0", "revised_summary.json"), encoding="utf-8"))
    s11 = json.load(open(os.path.join(ANALYSIS, "revised_summary.json"), encoding="utf-8"))
    a, b = {}, {}
    flat("propositions", {k: v for k, v in s10.items() if k not in ("coder", "version", "matrix_sha256")}, a)
    flat("propositions", {k: v for k, v in s11.items() if k not in ("coder", "version", "matrix_sha256")}, b)
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            rows.append(dict(level="proposition-level measure", item=k, measure=k.split(".", 1)[1], v1_0=json.dumps(a.get(k)),
                             v1_1=json.dumps(b.get(k)), cause="new-source rows and/or erratum (core set, AMY5-D2-0)"))
    for fn, key in (("atomic_sensitivity_results.csv", "rule"),):
        r10 = {r[key]: r for r in read_csv(os.path.join(ANALYSIS, "v1.0", fn))}
        r11 = {r[key]: r for r in read_csv(os.path.join(ANALYSIS, fn))}
        for k in r10:
            for f in ("propositions_counted", "supported", "unknown", "two_plus_organizations", "independent_corroboration", "with_counterevidence"):
                if r10[k][f] != r11[k][f]:
                    rows.append(dict(level="sensitivity rule", item=k, measure=f, v1_0=r10[k][f], v1_1=r11[k][f], cause="recomputed from v1.1"))
    c10 = {r["proposition_id"]: r for r in read_csv(os.path.join(ANALYSIS, "v1.0", "proposition_corroboration.csv"))}
    c11 = {r["proposition_id"]: r for r in read_csv(os.path.join(ANALYSIS, "proposition_corroboration.csv"))}
    for pid in c10:
        for f in ("core_or_added", "evidence_status", "orgs_whole_support", "cross_org_agreement", "independent_corroboration",
                  "independent_corroboration_a10", "shared_upstream_only", "different_parts_only", "repeated_reporting_only",
                  "contradicted_by"):
            if c10[pid].get(f) != c11[pid].get(f):
                rows.append(dict(level="proposition", item=pid, measure=f, v1_0=c10[pid].get(f, ""), v1_1=c11[pid].get(f, ""),
                                 cause="see proposition_support.csv rows added_in=v1.1, and erratum core additions"))
    d10 = {(r["unit"], r["branch"]): r for r in read_csv(os.path.join(ANALYSIS, "v1.0", "d5_branch_support.csv"))}
    d11 = {(r["unit"], r["branch"]): r for r in read_csv(os.path.join(ANALYSIS, "d5_branch_support.csv"))}
    for k in d10:
        for f in ("in_frozen_branches", "organizations"):
            if d10[k][f] != d11[k][f]:
                rows.append(dict(level="D5 branch (Table III)", item="%s %s" % k, measure=f, v1_0=d10[k][f], v1_1=d11[k][f], cause="erratum / new-source rows"))
    write_csv(os.path.join(ANALYSIS, "v1.0_vs_v1.1_comparison.csv"), ["level", "item", "measure", "v1_0", "v1_1", "cause"], rows)
    from collections import Counter
    print(len(rows), "differences:", dict(Counter(r["level"] for r in rows)))


if __name__ == "__main__":
    main()
