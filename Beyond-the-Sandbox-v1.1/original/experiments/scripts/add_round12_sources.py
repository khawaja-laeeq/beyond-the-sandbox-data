"""Round 12: add every URL in research/new_sources.jsonl not yet in sources.csv as a context-only row.
Not opened by the experimenter (scout summary only); no coded row cites them. Rows dated after the
2026-10-25 cutoff are marked as outside the study window. Idempotent."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *
have = rows("sources.csv")
urls = {s["url"].rstrip("/") for s in have}
n = max(int(s["ref"][1:]) for s in have)
new = []
for l in open(os.path.join(PAPER, "research", "new_sources.jsonl"), encoding="utf-8"):
    if not l.strip():
        continue
    d = json.loads(l)
    u = d["url"].rstrip("/")
    if u in urls:
        continue
    urls.add(u)
    n += 1
    late = (d.get("date") or "") > "2026-10-25"
    new.append({"ref": "R%d" % n,
                "citation": "%s, “%s,” %s." % (d.get("publisher", ""), d["title"], d.get("date") or "n.d."),
                "url": d["url"],
                "verification": "listed by data-scout " + (d.get("checked") or "2026-11-06")[:10] + "; NOT opened by experimenter (scout summary only); context only, "
                                "no coded row depends on it; re-check before citing any detail"
                                + ("; dated after the 2026-10-25 cutoff, outside the study window" if late else ""),
                "relevance": "context (%s); units: %s" % (d.get("type", ""), ",".join(d.get("units", [])))})
with open(os.path.join(DATA, "sources.csv"), "a", newline="", encoding="utf-8") as f:
    csv.DictWriter(f, fieldnames=["ref", "citation", "url", "verification", "relevance"]).writerows(new)
print("added", [r["ref"] for r in new])
