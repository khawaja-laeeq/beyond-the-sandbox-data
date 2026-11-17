"""Task 1: lock every number in the manuscript to the data. Exits non-zero on any mismatch or untagged number.

Run:  python3 -I analysis/src/check_numbers.py [manuscript.md]   -> analysis/number_check_report.csv

How numbers are tagged in manuscript/revised_manuscript.md (HTML comments; pandoc drops them from the DOCX):
  22<!--n:v10['cross_org_agreement']-->   a COUNTED number. The expression is evaluated over the data files
                                          (namespace below) and must equal the number written in the text.
  75%<!--q:R08-->                         a QUOTED number taken from a source. The number as written must occur in
                                          that source's cached text (checked against the cache, not the data files).
  three<!--x:reason-->                    a STRUCTURAL number that is not a count of coded data (e.g. 'four research
                                          questions'). Allowed, but listed in the report with its reason.
Spelled-out numbers (one ... ninety-nine) are handled like digits.
Any digit sequence that is untagged must match an exemption pattern (identifiers such as R02, D1, S0, A10, X07, E08,
dates, years, citation brackets, section labels, version labels, times inside quoted passages are NOT exempt: tag
them with q:). The References section, YAML front matter and code blocks are not checked.
Namespace: v10, v11 (revised_summary.json for v1.0 and v1.1); c10, c11 (cell_level_results.json); s10, s11 (sensitivity
rows by rule label, ints); er (erratum: n_fixes, n_rows, applied, no_change); ns (n_rows, n_cand, by_source);
a10 (A10 rows); len, sum, abs, round, sorted, set.
"""
import csv, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, ANALYSIS, read_csv, source_text, norm
import new_source_rows as NS

MS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "manuscript", "revised_manuscript.md")
WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
                                    "fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90})
WORD_RE = r"(?:(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)(?:-(?:one|two|three|four|five|six|seven|eight|nine))?|" \
          r"zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen)"
NUM_RE = r"(?:\d{1,2}:\d{2}|\d[\d,]*(?:\.\d+)?%?|" + WORD_RE + r")"
TAGGED = re.compile(r"(?<![\w.\-])(" + NUM_RE + r")<!--([nqx]):(.*?)-->", re.I)
MONTHS = r"(?:Jan(?:uary|\.)?|Feb(?:ruary|\.)?|Mar(?:ch|\.)?|Apr(?:il|\.)?|May|June?|July?|Aug(?:ust|\.)?|Sept?(?:ember|\.)?|Oct(?:ober|\.)?|Nov(?:ember|\.)?|Dec(?:ember|\.)?)"
EXEMPT = [r"\[\d+, (?:Table \d+, )?§+[^\]]*\]", r"\b\d{1,2}[–-]\d{1,2} " + MONTHS, r"\b(?:R|D|S|W|A|X|E|N|C|RQ|L|Q)\d+[a-z]?\b", r"\bv\d\.\d\b", r"\b20[12]\d\b", r"\[\d+\](?:[–-]\[\d+\])?", r"\[\d+(?:, \d+)*\]",
          r"\b\d{1,2} " + MONTHS, MONTHS + r" \d{1,2}\b", r"\bIV-[A-I]\b", r"§+\s?[\d.–, ]+", r"\bpp?\.\s?\d+(?:[–-]\d+)?",
          r"\b[0-9a-f]{8}…", r"Python 3\.\d+", r"matplotlib 3\.\d+\.\d+", r"\b(?:HF|MAY|ART|OP46|OP47|AMY5|INT|AISIMY5|SOL)-D\d-\d+\b",
          r"\bD[1-5]–D[1-5]\b", r"\b[SWA]\d+–[SWA]\d+\b", r"\bGPT-5\.\d\b", r"\bOpus 4\.\d\b", r"\bMythos 5\b", r"\bR\d\d–R\d\d\b",
          r"\bL[1-3]\b", r"seed \d+", r"\b1\.[01]\b", r"SHA-256", r"\bTable \d+", r"\bFigure \d+",
          r"\[\d+, (?:Table \d+, )?§+[^\]]*\]"]   # pinpoint citations such as [4, §§3.2, 4–5] and [5, Table 1, §4]
# Spelled-out 'one', 'two' and 'zero' are too often ordinary words ('one organization', 'two organizations', 'a
# published zero'); counts written with them are tagged by hand and checked like any other tagged number.
GENERIC_WORDS = {"one", "two", "zero"}


def namespace():
    ld = lambda p: json.load(open(p, encoding="utf-8"))
    cl = ld(os.path.join(ANALYSIS, "cell_level_results.json"))

    def sens(folder):
        out = {}
        for r in read_csv(os.path.join(folder, "atomic_sensitivity_results.csv")):
            out[r["rule"].split()[0]] = {k: int(v) for k, v in r.items() if v.lstrip("-").isdigit()}
        return out
    er_rows = read_csv(os.path.join(ANALYSIS, "erratum_v1.1.csv"))
    applied = read_csv(os.path.join(ANALYSIS, "matrix_v1.1", "erratum_applied.csv"))
    er = dict(n_fixes=len({e["fix_id"] for e in er_rows}), n_rows=len(er_rows),
              applied=len({e["fix_id"] for e in applied if e["applied"] == "yes"}),
              no_change=len({e["fix_id"] for e in applied if e["applied"].startswith("no change")}),
              rejected=len({e["fix_id"] for e in applied if e["applied"].startswith("no (")}))
    by_source = {}
    kept = [r for r in NS.ROWS if r["status"].strip().lower() != "rejected"]   # rows actually used in v1.1
    for r in kept:
        by_source[r["src"]] = by_source.get(r["src"], 0) + 1
    ns = dict(n_rows=len(kept), n_rows_all=len(NS.ROWS), n_rejected=len(NS.ROWS) - len(kept),
              n_rel_corrected=len(getattr(NS, "REL_CORRECTIONS", {})), n_cand=len(NS.CANDIDATES), by_source=by_source,
              n_sources_added=len({r["src"] for r in NS.ROWS} | {c["src"] for c in NS.CANDIDATES}))
    def brk(folder):
        return {r["group"]: {k: int(v) for k, v in r.items() if v.isdigit()} for r in read_csv(os.path.join(folder, "breakdown_by_incident_and_dimension.csv"))}
    return dict(b10=brk(os.path.join(ANALYSIS, "v1.0")), b11=brk(ANALYSIS), v10=ld(os.path.join(ANALYSIS, "v1.0", "revised_summary.json")), v11=ld(os.path.join(ANALYSIS, "revised_summary.json")),
                c10=cl["v1.0"], c11=cl["v1.1"], s10=sens(os.path.join(ANALYSIS, "v1.0")), s11=sens(ANALYSIS), er=er, ns=ns,
                a10=read_csv(os.path.join(ANALYSIS, "a10_independence_judgments.csv")),
                len=len, sum=sum, abs=abs, round=round, sorted=sorted, set=set)


_ft = {}


def _txt(s):
    return _ft[s] if s.startswith("FT:") else (source_text(s) or "")


def value(tok):
    t = tok.lower().rstrip("%").replace(",", "")
    if t in WORDS:
        return WORDS[t]
    if "-" in t and t.split("-")[0] in WORDS:
        a, b = t.split("-")
        return WORDS[a] + WORDS[b]
    return float(t) if "." in t else int(t)


def checked_text(md):
    md = re.sub(r"\A---.*?\n---\n", lambda m: "\n" * m.group(0).count("\n"), md, flags=re.S)
    md = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), md, flags=re.S)
    i = md.find("\n# References")
    return md if i < 0 else md[:i]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ns = namespace()
    md = open(MS, encoding="utf-8").read()
    body = checked_text(md)
    rows, bad = [], 0
    spans = []
    for m in TAGGED.finditer(body):
        tok, kind, arg = m.group(1), m.group(2).lower(), m.group(3).strip()
        line = body.count("\n", 0, m.start()) + 1
        spans.append((m.start(), m.end()))
        st, exp = "ok", ""
        try:
            if kind == "n":
                exp = eval(arg, {"__builtins__": {}}, ns)
                if isinstance(exp, bool) or value(tok) != exp:
                    st = "MISMATCH"
            elif kind == "q":
                srcs = [s.strip() for s in arg.split(";")]
                for s_ in srcs:
                    if s_.startswith("FT:"):
                        _ft[s_] = open(os.path.join(ROOT, "original", "research", "fulltext", s_[3:] + ".txt"), encoding="utf-8", errors="replace").read()
                raw = tok.replace("%", "")
                found = any((_ft.get(s) if s.startswith("FT:") else source_text(s)) and (raw.lower() in _txt(s).lower() and not raw.isdigit()
                                                 or re.search(r"(?<!\d)" + re.escape(raw) + r"(?!\d)", _txt(s)))
                            for s in srcs)
                exp = "in " + arg
                if not found:
                    st = "NOT IN SOURCE"
            else:
                exp = "structural: " + arg
        except Exception as e:  # noqa: BLE001
            st, exp = "ERROR", repr(e)
        bad += st not in ("ok",)
        rows.append(dict(line=line, number=tok, tag=kind, expression=arg, expected=exp, status=st,
                         context=body[max(0, m.start() - 60):m.start()].replace("\n", " ")[-60:]))
    # untagged numbers
    masked = list(body)
    for a, b in spans:
        for i in range(a, b):
            masked[i] = " "
    masked = "".join(masked)
    masked = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), masked, flags=re.S)
    masked = re.sub(r"\(\.\./[^)]*\)|\{width=[^}]*\}|`[^`]*`", lambda m: " " * len(m.group(0)), masked)
    for pat in EXEMPT:
        masked = re.sub(pat, lambda m: " " * len(m.group(0)), masked)
    for m in re.finditer(r"(?<![\w.\-])(" + NUM_RE + r")(?![\w])", masked, re.I):
        tok = m.group(1)
        if tok.lower() in GENERIC_WORDS:
            continue
        line = masked.count("\n", 0, m.start()) + 1
        bad += 1
        rows.append(dict(line=line, number=tok, tag="", expression="", expected="", status="UNTAGGED",
                         context=body[max(0, m.start() - 60):m.start() + 20].replace("\n", " ")))
    rows.sort(key=lambda r: r["line"])
    out = os.path.join(ANALYSIS, "number_check_report.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["line", "number", "tag", "expression", "expected", "status", "context"], lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    print("numbers checked:", len(rows), dict(Counter(r["status"] for r in rows)), "->", out)
    for r in rows:
        if r["status"] != "ok":
            print("  line %s: %s [%s %s] expected %s :: %s" % (r["line"], r["number"], r["tag"], r["expression"], r["expected"], r["context"]))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
