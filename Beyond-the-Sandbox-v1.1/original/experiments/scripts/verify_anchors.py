"""Deterministic anchor check: for each row of experiments/data/anchor_checks.csv, search the
cached source text (experiments/source_cache/, fetched by fetch_sources.py) for the regex and
record hit count and a short excerpt. Writes experiments/results/anchor_check.json.
Standard library only. Run: python3 experiments/scripts/verify_anchors.py"""
import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
CACHE = os.path.join(EXP, "source_cache")
SPECIAL = {"A18": "r08_raw_alt"}  # figure alt text lives in raw HTML, not stripped text

rows, out = list(csv.DictReader(open(os.path.join(EXP, "data", "anchor_checks.csv")))), []
for r in rows:
    path = os.path.join(CACHE, r["cache_file"])
    rec = {k: r[k] for k in ("check_id", "ref", "pattern", "supports")}
    if r["check_id"] in SPECIAL:
        path = os.path.join(CACHE, "r08_figs", "alt_text.txt")
    if not os.path.exists(path):
        rec.update(hits=None, note="cache file missing")
    else:
        t = re.sub(r"\s+", " ", open(path, encoding="utf-8", errors="replace").read())
        ms = list(re.finditer(r["pattern"], t, re.I))
        rec["hits"] = len(ms)
        if ms:
            m = ms[0]
            rec["excerpt"] = t[max(0, m.start() - 120):m.end() + 120]
    out.append(rec)
os.makedirs(os.path.join(EXP, "results"), exist_ok=True)
json.dump(out, open(os.path.join(EXP, "results", "anchor_check.json"), "w"), indent=1)
for rec in out:
    print(rec["check_id"], rec["ref"], rec["hits"], "|", rec["supports"])
