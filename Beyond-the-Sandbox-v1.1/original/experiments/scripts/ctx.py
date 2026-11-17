"""Analyst helper (round 11 blind re-check): print context windows around a regex in a cached source text.
Usage: python3 -I scripts/ctx.py <file> <regex> [window=300] [max=8]"""
import re
import sys

t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
pat = sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 300
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 8
for m in list(re.finditer(pat, t, re.I))[:mx]:
    print("@%d:" % m.start(), t[max(0, m.start() - w):m.end() + w].replace("\n", " "))
    print("---")
