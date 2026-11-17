"""Build the v1.1 45-cell matrix from the frozen v1.0 matrix plus analysis/erratum_v1.1.csv (task 3).

Run:  python3 -I analysis/src/build_matrix_v1_1.py
* v1.0 is read from original/ and never written. Its SHA-256 must equal the freeze record, or the build stops.
* Every erratum row whose fix has status 'rejected' is skipped, so rejecting one fix reverts only the cells
  and fields that fix touched. Any other status ('pending human approval', 'approved') is applied; until the
  authors approve, v1.1 is provisional and the manuscript reports v1.0 and v1.1 side by side.
* Every quoted passage in the erratum must be found in a cached source text, and every old_value must
  equal the v1.0 value, or the build exits non-zero.
Outputs: analysis/matrix_v1.1/coded_evidence_case_study_v1.1.csv, freeze_v1.1.json, erratum_applied.csv
"""
import csv, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, EXP, ANALYSIS, quote_found, read_csv, write_csv

V10 = os.path.join(EXP, "protocol", "coded_evidence_case_study_v1.0.csv")
FREEZE = os.path.join(ROOT, "supporting_data", "original_matrix", "freeze_v1.0.json")
ERRATUM = os.path.join(ANALYSIS, "erratum_v1.1.csv")
OUTDIR = os.path.join(ANALYSIS, "matrix_v1.1")
V11 = os.path.join(OUTDIR, "coded_evidence_case_study_v1.1.csv")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def add_branch(value, letter):
    head, sep, tail = value.partition(" -> ")
    branches = [b for b in head.split(";") if b and b != "-"]
    if letter not in branches:
        branches.append(letter)
    return ";".join(branches) + sep + tail


def apply(value, op, new):
    if op == "set":
        return new
    if op == "add_branch":
        return add_branch(value, new)
    if op == "append_note":
        return value + new
    if op == "none":
        return value
    raise ValueError("unknown operation " + op)


def main():
    errors = []
    v10_sha = sha(V10)
    frozen_sha = json.load(open(FREEZE))["files"]["coded_evidence_case_study_v1.0.csv"]
    if v10_sha != frozen_sha:
        sys.exit("v1.0 matrix does not match its freeze record: %s != %s" % (v10_sha, frozen_sha))
    with open(V10, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    cell = {r["unit"] + "/" + r["code"]: r for r in rows}
    er = read_csv(ERRATUM)
    status = {}
    for e in er:
        s = e["status"].strip().lower()
        if status.setdefault(e["fix_id"], s) != s:
            errors.append("fix %s has rows with different statuses" % e["fix_id"])
    rejected = {f for f, s in status.items() if s == "rejected"}
    # a fix that depends on a rejected fix is not applied either
    changed = True
    while changed:
        changed = False
        for e in er:
            if e["fix_id"] not in rejected and e["depends_on"] and set(e["depends_on"].split(";")) & rejected:
                rejected.add(e["fix_id"]); changed = True
    applied = []
    for e in er:
        if e["cell"] not in cell:
            errors.append("unknown cell " + e["cell"]); continue
        if e["field"] not in fields:
            errors.append("unknown field " + e["field"]); continue
        r = cell[e["cell"]]
        # old_value is always the v1.0 value; v1.1 values are built only from v1.0 plus the erratum
        with open(V10, encoding="utf-8", newline="") as f:
            v10_value = {x["unit"] + "/" + x["code"]: x for x in csv.DictReader(f)}[e["cell"]][e["field"]]
        if e["old_value"] != v10_value:
            errors.append("%s %s %s: old_value differs from v1.0" % (e["fix_id"], e["cell"], e["field"]))
        srcs = [s.strip() for s in e["source_id"].split(";") if s.strip()]
        for q in [q.strip() for q in e["exact_quote"].split(" | ") if q.strip()]:
            if not any(quote_found(s, q) for s in srcs):
                errors.append("%s: quote not found in %s: %s" % (e["fix_id"], e["source_id"], q[:80]))
        if e["fix_id"] in rejected:
            applied.append(dict(e, applied="no (rejected)", value_in_v1_1=r[e["field"]]))
            continue
        r[e["field"]] = apply(r[e["field"]], e["operation"], e["new_value"])
        if e["operation"] != "none":
            note = " | v1.1 %s (%s): %s" % (e["fix_id"], e["status"], e["field"])
            if note not in r["change_log"]:
                r["change_log"] += note
        applied.append(dict(e, applied="yes" if e["operation"] != "none" else "no change proposed", value_in_v1_1=r[e["field"]]))
    if errors:
        for x in errors:
            print("ERRATUM ERROR:", x)
        sys.exit(2)
    os.makedirs(OUTDIR, exist_ok=True)
    with open(V11, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    write_csv(os.path.join(OUTDIR, "erratum_applied.csv"), list(applied[0].keys()), applied)
    rec = {"version": "1.1", "built": "from v1.0 plus analysis/erratum_v1.1.csv by analysis/src/build_matrix_v1_1.py",
           "status": "provisional: every fix is AI-assisted and pending human approval unless marked approved",
           "v1.0_sha256": v10_sha, "v1.1_sha256": sha(V11),
           "fixes_applied": sorted({e["fix_id"] for e in applied if e["applied"] == "yes"}),
           "fixes_rejected": sorted(rejected), "fixes_no_change": sorted({e["fix_id"] for e in applied if e["applied"] == "no change proposed"})}
    json.dump(rec, open(os.path.join(OUTDIR, "freeze_v1.1.json"), "w"), indent=1)
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
