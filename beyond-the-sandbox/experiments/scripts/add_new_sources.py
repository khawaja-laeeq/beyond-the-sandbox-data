"""Append the 7 round-3 scout sources (last 7 lines of research/new_sources.jsonl) to sources.csv as context-only rows.
They were NOT opened by the experimenter (scout summary only), so no coded row cites them."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

p = os.path.join(DATA, "sources.csv")
have = rows("sources.csv")
urls = {s["url"] for s in have}
lines = open(os.path.join(PAPER, "research", "new_sources.jsonl"), encoding="utf-8").read().strip().splitlines()[-7:]
n = int(have[-1]["ref"][1:])
kind = {"coverage": "secondary coverage (context)", "investigation": "secondary analysis (context)",
        "comparable-incident": "comparable incident (context)"}
new = []
for l in lines:
    d = json.loads(l)
    if d["url"] in urls:
        continue
    n += 1
    new.append({"ref": f"R{n}", "citation": f'{d["publisher"]}, “{d["title"]},” {d["date"]}.', "url": d["url"],
                "verification": "listed by data-scout 2026-11-02; NOT opened by experimenter this round (scout summary only); "
                                "context only, no coded row depends on it; re-check before citing any detail",
                "relevance": kind.get(d["type"], "context")})
with open(p, "a", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["ref", "citation", "url", "verification", "relevance"])
    w.writerows(new)
print("added", [r["ref"] for r in new])
