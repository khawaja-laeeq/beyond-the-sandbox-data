"""Fetch raw HTML of a page and list image URLs whose surrounding HTML matches a pattern.
Usage: find_figure.py URL PATTERN OUTDIR  -> downloads the matching images into OUTDIR."""
import re
import sys
import urllib.request

url, pat, out = sys.argv[1], sys.argv[2], sys.argv[3]
ua = {"User-Agent": "Mozilla/5.0 (documentary verification)"}
h = urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=30).read().decode("utf-8", "replace")
n = 0
for m in re.finditer(r"<img[^>]+>", h):
    tag = m.group(0)
    ctx = h[max(0, m.start() - 1500):m.end() + 1500]
    if not re.search(pat, tag + ctx, re.I):
        continue
    srcs = re.findall(r'(?:src|srcSet|srcset)="([^"]+)"', tag)
    alt = re.findall(r'alt="([^"]*)"', tag)
    print("ALT:", alt[:1], "SRC:", srcs[:1])
    with open(f"{out}/alt_text.txt", "a") as fa:
        fa.write((alt[0] if alt else "") + "\n")
    if srcs:
        s = html_src = srcs[0].split(" ")[0].replace("&amp;", "&")
        if s.startswith("/"):
            s = "https://www.anthropic.com" + s
        n += 1
        data = urllib.request.urlopen(urllib.request.Request(s, headers=ua), timeout=30).read()
        ext = "png" if data[:4] == b"\x89PNG" else ("webp" if data[8:12] == b"WEBP" else "jpg")
        open(f"{out}/fig{n}.{ext}", "wb").write(data)
        print("saved", f"fig{n}.{ext}", len(data))
