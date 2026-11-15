"""Round 6: add the data-scout round-6 sources (ReversingLabs, MIT Technology Review, NSFOCUS) as context rows.
Not opened by the experimenter (scout summary only); no coded cell depends on them.
Run: python3 -I scripts/add_round6_sources.py (idempotent: skips URLs already in sources.csv)"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

have = rows("sources.csv")
urls = {s["url"] for s in have}
n = int(have[-1]["ref"][1:])
lines = open(os.path.join(PAPER, "research", "new_sources.jsonl"), encoding="utf-8").read().strip().splitlines()
new = []
for l in lines:
    d = json.loads(l)
    if d.get("round") != 6 or d["url"] in urls:
        continue
    n += 1
    new.append({"ref": "R%d" % n, "citation": "%s, “%s,” %s." % (d["publisher"], d["title"], d["date"]), "url": d["url"],
                "verification": "listed by data-scout 2026-11-05 (status: %s); NOT opened by experimenter (scout summary only); "
                                "context only, no coded row depends on it; adds no positive statement beyond R02/R04/R08/R25; "
                                "re-check before citing any detail" % d.get("status"),
                "relevance": "comparable incident (context)" if d["type"] == "comparable-incident" else "secondary coverage (context)"})
with open(os.path.join(DATA, "sources.csv"), "a", newline="", encoding="utf-8") as f:
    csv.DictWriter(f, fieldnames=["ref", "citation", "url", "verification", "relevance"]).writerows(new)
print("added", [r["ref"] for r in new])
