"""Round 10 (analyst): re-point INC-OAI-ART D3/D5 anchor checks from stale R07 anchors
(A04 'spoof', A06 'message board') to R02 III.B passages already quoted in the evidence field.
No status change. Idempotent. Run: python3 experiments/scripts/round10_analyst_art.py"""
import csv
import os

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(EXP, "data")

ap = os.path.join(D, "anchor_checks.csv")
rows = list(csv.DictReader(open(ap)))
f = list(rows[0].keys())
new = [
    ("A51", "R02", "R02.txt", "use these existing credentials to obtain administrator credentials",
     "OAI-ART D3 administrator credentials obtained via Artifactory endpoint (R02 III.B p.7)"),
    ("A52", "R02", "R02.txt", "caused the instance to become unavailable late on July 4",
     "OAI-ART D5 Artifactory outage from July 4 (R02 III.B p.8)"),
    ("A53", "R02", "R02.txt", "administrator-level compromise of the Artifactory deployment",
     "OAI-ART D5 administrator-level compromise (R02 III.B p.8)"),
]
ids = {r["check_id"] for r in rows}
for n in new:
    if n[0] not in ids:
        rows.append(dict(zip(f, n)))
for r in rows:
    if r["check_id"] == "A04" and not r["supports"].startswith("SUPERSEDED"):
        r["supports"] = "SUPERSEDED round 10 (no cell cites it): " + r["supports"]
w = csv.DictWriter(open(ap, "w", newline=""), fieldnames=f)
w.writeheader()
w.writerows(rows)

cp = os.path.join(D, "coded_evidence.csv")
rows = list(csv.DictReader(open(cp)))
f = list(rows[0].keys())
tgt = {"D3": "A51", "D5": "A52;A53"}
changed = []
for r in rows:
    if r["unit"] == "INC-OAI-ART" and r["code"] in tgt and r["anchor_checks"] != tgt[r["code"]]:
        old = r["anchor_checks"]
        r["change_log"] += ("; ROUND 10 (analyst): anchor " + old + " (R07) replaced by " + tgt[r["code"]]
                            + " (R02 III.B); proposition = R02 verbatim passage; no status change")
        r["anchor_checks"] = tgt[r["code"]]
        changed.append(r["code"])
w = csv.DictWriter(open(cp, "w", newline=""), fieldnames=f)
w.writeheader()
w.writerows(rows)

lp = os.path.join(EXP, "results", "coding_change_log.csv")
why = {"D3": "(administrator credentials)", "D5": "(outage from July 4; administrator-level compromise)"}
with open(lp, "a", newline="") as fh:
    for c in changed:
        csv.writer(fh).writerow([
            "INC-OAI-ART/" + c, "documented", "documented",
            "ROUND 10 (analyst): proposition and anchor aligned with R02 III.B passage used in Appendix B "
            + why[c] + "; stale R07 anchor removed; no status change", tgt[c]])
print("changed:", changed)
