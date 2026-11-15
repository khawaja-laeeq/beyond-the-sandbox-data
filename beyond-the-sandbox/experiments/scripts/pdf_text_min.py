"""Minimal stdlib PDF text extractor (fallback when pypdf is missing): pdf_text_min.py IN.pdf OUT.txt
Inflates FlateDecode streams and pulls text from Tj/TJ operators; ToUnicode maps are NOT applied,
so output may be garbled for subset fonts. Read-only on input."""
import re
import sys
import zlib

raw = open(sys.argv[1], "rb").read()
out = []
for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
    try:
        d = zlib.decompress(m.group(1))
    except Exception:
        continue
    if b"BT" not in d:
        continue
    out.append("\n[[stream]]")
    for t in re.finditer(rb"\[(.*?)\]\s*TJ|\((.*?)(?<!\\)\)\s*Tj", d, re.S):
        s = t.group(1) or t.group(2)
        parts = re.findall(rb"\((.*?)(?<!\\)\)", s) if t.group(1) else [s]
        out.append("".join(p.decode("latin-1") for p in parts))
open(sys.argv[2], "w").write("\n".join(out))
print(len(out), "chunks")
