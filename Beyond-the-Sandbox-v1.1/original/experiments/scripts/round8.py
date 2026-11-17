"""Round 8 recodes (in place on data/coded_evidence.csv) + results/sufficiency_review.csv.
Run: python3 -I scripts/round8.py   (idempotent)"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS
p = os.path.join(DATA, "coded_evidence.csv")
rd = csv.DictReader(open(p, encoding="utf-8")); fn = rd.fieldnames; rows = list(rd)
for r in rows:
    k = (r["unit"], r["code"])
    if k == ("INC-ANT-MY5", "D2") and r["status"] == "documented":
        r["status"] = "unknown"
        r["evidence"] = "R08 reports biased simulation reasoning (a belief about the environment being a simulation); it states no belief about permission or authorization scope"
        r["claim_strength"] = "n/a (unknown)"; r["support_type"] = "n/a"
        r["change_log"] += "; RECODED documented->unknown (round 8): R08 (cached) reports a simulation belief, not a permission belief; codebook D2 requires a stated authorization interpretation, so the source is silent on D2"
    if k == ("INC-OAI-HF", "D1") and "round 8" not in r["change_log"]:
        r["reference"] = "R01;R02"
        r["evidence"] = "R02 section IV.A (cached): agents gained access to the public internet on July 8 via Artifactory, initially reaching a public bug-tracking page; July 10-13 they used exposed Hugging Face user credentials to reach the Hugging Face environment"
        r["source_section"] = "R02 sections IV.A-B (pp.8-9); R01 not reachable (HTTP 403)"
        r["claim_strength"] = "multi-source"; r["not_independently_checked"] = "no"
        r["change_log"] += "; round 8: status kept documented; passage supplied from cached R02 IV.A and R02 added as reference, so the cell no longer rests on unreachable R01 alone"
    if k == ("INC-AISI-SOL", "D5") and "round 8" not in r["change_log"]:
        r["claim_strength"] = "single-source"; r["not_independently_checked"] = "no"
        r["change_log"] += "; round 8: R24 fetched and cached (source_cache/R24.pdf, R24.txt); Event 10-1 (PAT recovered from public Gist, used to authenticate to GitHub) and Event 10-2 (DNS server exposed through public tunnel, no resolver queried it, infrastructure removed automatically) verified in text; status kept, now single-source and checked"
w = csv.DictWriter(open(p, "w", newline="", encoding="utf-8"), fieldnames=fn); w.writeheader(); w.writerows(rows)

cache = {f.split(".")[0] for f in os.listdir(os.path.join(os.path.dirname(DATA), "source_cache"))}
out = []
for r in rows:
    refs = [x for x in r["reference"].split(";") if x]
    cached = [x for x in refs if x in cache]
    if r["status"] == "unknown":
        suff = "n/a: silence (no positive statement required)"
    elif len(refs) > 1 and cached:
        suff = "sufficient: multi-source, at least one source in local cache"
    elif cached:
        suff = "sufficient on single source in local cache; no independent corroboration"
    else:
        suff = "not independently re-read: no cited source in local cache (coded from earlier reading)"
    out.append({"unit": r["unit"], "code": r["code"], "status": r["status"], "references": r["reference"],
                "n_refs": len(refs), "refs_in_cache": ";".join(cached) or "none", "support_type": r["support_type"],
                "sufficiency": suff})
with open(os.path.join(RESULTS, "sufficiency_review.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), sum(r["status"] == "documented" for r in rows))
