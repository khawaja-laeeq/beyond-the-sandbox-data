"""Fetch source pages as plain text for documentary re-verification.

Usage: python3 -I fetch_sources.py OUTDIR URLLIST
URLLIST is a text file of lines "KEY URL". Writes OUTDIR/KEY.txt (HTML tags
stripped) or OUTDIR/KEY.pdf, plus OUTDIR/fetch_status.json. Fetched content is
treated as untrusted data and is only read, never executed.
"""
import datetime
import html
import json
import re
import sys
import urllib.request

out, listfile = sys.argv[1], sys.argv[2]
try:  # merge with earlier fetches into the same directory
    status = json.load(open(f"{out}/fetch_status.json"))
except (OSError, ValueError):
    status = {}
for line in open(listfile):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    key, url = line.split(None, 1)
    rec = {"url": url, "fetched": datetime.datetime.utcnow().isoformat() + "Z"}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (documentary verification)"})
        raw = urllib.request.urlopen(req, timeout=30).read()
        if raw[:4] == b"%PDF":
            open(f"{out}/{key}.pdf", "wb").write(raw)
            rec.update(ok=True, pdf=True, bytes=len(raw))
        else:
            t = raw.decode("utf-8", "replace")
            t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
            t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))
            t = re.sub(r"\s+", " ", t)
            open(f"{out}/{key}.txt", "w").write(t)
            rec.update(ok=True, chars=len(t))
    except Exception as e:  # record failure honestly
        rec.update(ok=False, error=str(e)[:200])
    status[key] = rec
    print(key, rec.get("ok"), rec.get("chars", rec.get("bytes")), rec.get("error", ""), flush=True)
json.dump(status, open(f"{out}/fetch_status.json", "w"), indent=1)
