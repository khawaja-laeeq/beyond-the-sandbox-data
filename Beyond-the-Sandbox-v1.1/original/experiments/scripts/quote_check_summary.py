"""Quote check summary from the evidence audit (results/evidence_audit.csv). Re-checks every quoted passage verbatim
against source_cache/<ref>.txt (letters and digits only, case-folded, as in evidence_audit.py) and writes
results/quote_check_summary.json: total, matched, missing, per-source counts, and the full per-quote list.
Also checks that every quote in the evidence column of data/coded_evidence.csv is among the audited passages.
Run from experiments/: python3 -I scripts/quote_check_summary.py"""
import csv, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, EXP, log

CACHE = os.path.join(EXP, "source_cache")
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
cache = {}


def text(ref):
    if ref not in cache:
        p = os.path.join(CACHE, ref + ".txt")
        cache[ref] = norm(open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else None
    return cache[ref]


audit = list(csv.DictReader(open(os.path.join(RESULTS, "evidence_audit.csv"), encoding="utf-8")))
coded = {(r["unit"], r["code"]): r for r in csv.DictReader(open(os.path.join(DATA, "coded_evidence.csv"), encoding="utf-8"))}
quotes = []
for a in audit:
    if not a["passages"].strip():
        continue
    for part in a["passages"].split(" || "):
        m = re.match(r"(R\d+): (.*)$", part.strip(), re.S)
        ref, q = m.group(1), m.group(2)
        t = text(ref)
        ev = coded[(a["unit"], a["code"])]["evidence"]
        quotes.append(dict(unit=a["unit"], code=a["code"], ref=ref, locator=a["locator"], quote=q,
                           source_text_cached=t is not None, matched=bool(t is not None and norm(q) in t),
                           in_coded_evidence=norm(q) in norm(ev)))
per = {}
for q in quotes:
    d = per.setdefault(q["ref"], dict(total=0, matched=0, missing=0))
    d["total"] += 1
    d["matched" if q["matched"] else "missing"] += 1
summary = dict(method="letters and digits only, case-folded, substring of source_cache/<ref>.txt; checks the quoted words exist, not that they entail the tag",
               total=len(quotes), matched=sum(q["matched"] for q in quotes), missing=sum(not q["matched"] for q in quotes),
               quotes_in_coded_evidence_column=sum(q["in_coded_evidence"] for q in quotes),
               decisions_audited=len(audit), decisions_with_quotes=len({(q["unit"], q["code"]) for q in quotes}),
               per_source=per, quotes=quotes)
json.dump(summary, open(os.path.join(RESULTS, "quote_check_summary.json"), "w", encoding="utf-8"), indent=1)
print({k: v for k, v in summary.items() if k != "quotes"})
log("quote_check_summary.py", "total %d matched %d missing %d" % (summary["total"], summary["matched"], summary["missing"]))
