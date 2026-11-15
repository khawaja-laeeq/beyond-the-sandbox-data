"""Print part of a cached source text: show_source.py FILE [ANCHOR] [LEN] or with
--grep PATTERN to print short windows around each regex match."""
import re
import sys

t = open(sys.argv[1]).read()
if len(sys.argv) > 2 and sys.argv[2] == "--grep":
    w = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    for m in re.finditer(sys.argv[3], t, re.I):
        print("...", t[max(0, m.start() - w):m.end() + w], "...\n")
else:
    anchor = sys.argv[2] if len(sys.argv) > 2 else ""
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    i = t.find(anchor) if anchor else 0
    print(t[max(0, i):i + n])
