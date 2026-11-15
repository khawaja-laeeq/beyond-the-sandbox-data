"""List hrefs in a page's raw HTML whose URL or anchor text matches a pattern.
Usage: find_links.py URL PATTERN"""
import re
import sys
import urllib.request

ua = {"User-Agent": "Mozilla/5.0 (documentary verification)"}
h = urllib.request.urlopen(urllib.request.Request(sys.argv[1], headers=ua), timeout=30).read().decode("utf-8", "replace")
seen = set()
for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', h, re.S):
    href, text = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
    text = re.sub(r"\s+", " ", text).strip()
    if re.search(sys.argv[2], href + " " + text, re.I) and href not in seen:
        seen.add(href)
        print(href, "|", text[:120])
