"""Report which cached source files contain each audited number pattern (helper for number_ledger)."""
import glob, os, re
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source_cache")
pats = ["68.7", "66.7", "22.9", "47.9", "50.0", "16.7", "20.8", "2.1%", r"(three|3) versions|THREE",
        r"15 (real|third)", r"installed", r"about an hour|one hour|roughly an hour|within an hour",
        r"\b122\b", r"\b19 (such|cases|actions)", r"\b17\b", r"five datasets", r"1%", r"50%", "141,006"]
files = sorted(glob.glob(base + "/*.txt") + glob.glob(base + "/second/*.txt") + glob.glob(base + "/r08_figs/*.txt"))
for p in pats:
    hits = []
    for f in files:
        t = open(f, encoding="utf-8", errors="ignore").read()
        m = re.search(p, t)
        if m:
            s = max(0, m.start() - 60)
            hits.append(os.path.basename(f) + ": " + t[s:m.end() + 60].replace("\n", " "))
    print("==", p, len(hits))
    for h in hits[:3]:
        print("   ", h)
