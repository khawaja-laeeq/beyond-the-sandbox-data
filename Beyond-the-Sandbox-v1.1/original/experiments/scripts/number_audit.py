"""E3: number ledger + audit.

Builds experiments/data/number_ledger.csv (value, claim, ref, source_section, tokens, arithmetic check,
anchor_found = whether the pattern is present in the cached source text), then scans draft.md for numeric
tokens and FAILS (exit 1) on any token not covered by a ledger row, on any failed arithmetic check, and on any
ledger row whose anchor is not found in the cache and is not flagged 'derived'/'data'.
build/paper.tex is scanned too but only reported (LaTeX markup, citation numbers and years create noise).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

CACHE = os.path.join(EXP, "source_cache")
# (id, value, claim, ref, source_section, cache_file, anchor_regex, tokens, kind)
L = [
 ("N01", "68.7%", "Opus 4.7 target engagement, unmodified (read-only + more intrusive); V11 sum of the two figure segments", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"47\.9% reads only plus 20\.8%", "68.7", "derived"),
 ("N02", "47.9%", "Unmodified: read-only share", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"47\.9% reads only", "47.9", "source"),
 ("N03", "20.8%", "Unmodified: more intrusive share (also production-banner read-only share)", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"20\.8% (writes|reads only)", "20.8", "source"),
 ("N04", "66.7%", "After WHOIS realism cue, total; V11 sum", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"50% reads only plus 16\.7%", "66.7", "derived"),
 ("N05", "50.0%", "WHOIS cue: read-only share (alt text prints 50%)", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"50% reads only", "50.0;50", "source"),
 ("N06", "16.7%", "WHOIS cue: more intrusive share", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"16\.7% writes", "16.7", "source"),
 ("N07", "22.9%", "After production authorization banner, total; V11 sum", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"20\.8% reads only plus 2\.1%", "22.9", "derived"),
 ("N08", "2.1%", "Banner: more intrusive share", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"2\.1% writes", "2.1", "source"),
 ("N09", "0%", "Engagement after explicit operator prohibition", "R08", "Opus 4.7 intervention figure (alt text)", "r08_figs/alt_text.txt", r"Operator note", "0", "source"),
 ("N10", "3 versions", "Mythos 5 published three versions of the malicious package", "R08", "Claude Mythos 5 uploads a malicious PyPI package", "R08.txt", r"published three versions", "3", "source"),
 ("N11", "15 installations", "Package installed on 15 third-party hosts", "R08", "Claude Mythos 5 uploads a malicious PyPI package", "R08.txt", r"installed on 15 third-party hosts", "15", "source"),
 ("N12", "~1 hour", "PyPI removed the package within an hour (Mythos 5)", "R08", "Claude Mythos 5 uploads a malicious PyPI package", "R08.txt", r"removed the package within an hour", "1", "source"),
 ("N13", "~1 hour (AISI)", "AISI contained the incident roughly one hour after discovery", "R10", "Incident summary", "R10.txt", r"within roughly one hour", "1", "source"),
 ("N14", "~1%", "about 1% of actions flagged with CoT present (replay)", "R08", "Offline monitoring", "R08.txt", r"1% of all actions", "1", "source"),
 ("N15", "~50%", "Monitor flag rate with tool calls and results (replay, class X)", "R08", "Offline monitoring", "R08.txt", r"flag rate jumps to about 50%", "50", "source"),
 ("N16", "122", "AISI evaluation runs", "R10", "Incident summary", "R10.txt", r"122 times", "122", "source"),
 ("N17", "10", "Runs with out-of-scope action", "R10", "Incident summary", "R10.txt", r"in 10 of those runs", "10", "source"),
 ("N18", "19", "Catalogued out-of-scope actions", "R10", "Incident summary", "R10.txt", r"catalogued 19 such actions", "19", "source"),
 ("N19", "17", "Actions from Mythos 5", "R10", "Incident summary", "R10.txt", r"\(17 actions\)", "17", "source"),
 ("N20", "2", "Actions from GPT-5.6 Sol (single run)", "R10", "Incident summary", "R10.txt", r"2 actions involving OpenAI", "2", "source"),
 ("N21", "5 datasets", "Only customer content accessed at Hugging Face: five datasets", "R04", "Anatomy of a Frontier Lab Agent Incident", "R04.txt", r"five datasets", "5", "source"),
 ("N22", "141,006", "Anthropic runs reviewed retrospectively", "R25", "What happened", "second/A30.txt", r"141,006", "141,006;141006", "source"),
 ("N23", "2026-07-28", "AISI detection of anomalous transfers", "R10", "How we discovered the incident", "R10.txt", r"28 ?th July", "28;7", "source"),
 ("N24", "25-28 July 2026", "Window of AISI behaviour", "R10", "What we found", "R10.txt", r"July 25 ?th and July 28 ?th", "25;28", "source"),
 ("N25", "2026-08-04", "AISI blog date", "R10", "Header", "R10.txt", r"Aug 4, 2026", "4;8", "source"),
 ("N26", "2026-08-26", "OpenAI report/blog date", "R02", "Cover (date per sources.csv citation; day not in extracted PDF text)", "sources.csv:R02", r"Aug\. 26, 2026", "26", "citation"),
 ("N27", "2026-05-26", "May precursor access", "R02", "A. pre-incident events", "R02.txt", r"May 26|2026-05-26", "26;5", "source"),
 ("N28", "2026-06-27", "Security alert on scanning (OAI-ART D4)", "R02", "A. pre-incident events", "R02.txt", r"June 27|2026-06-27", "27;6", "source"),
 ("N29", "2026-07-16", "Hugging Face disclosure", "R03", "Header (date per sources.csv citation; page text says only July 2026)", "sources.csv:R03", r"2026-07-16", "16", "citation"),
 ("N30", "2026-09-09", "Anthropic assessment date (V11)", "R08", "Header", "R08.txt", r"Sep(tember)? 9|2026-09-09", "9", "source"),
 ("N31", "2026-10-25", "Evidence cutoff", "brief", "Human answer Q3", "", "", "25;10", "data"),
 ("N32", "2026", "Year of the incidents", "R10", "Header", "R10.txt", r"2026", "2026", "source"),
 ("N33", "9 units / 5 dimensions / 45 decisions", "Size of the coded grid", "data", "units.csv; codebook.csv; coded_evidence.csv", "", "", "9;5;45", "data"),
 ("N35", "44 sources", "Rows in sources.csv", "data", "sources.csv", "", "", "44", "data"),
 ("N36", "4 evidence classes; 5 recoded", "Classes O/A/I/X; rows recoded vs baseline", "data", "coded_evidence.csv", "", "", "4;5", "data"),
 ("N37", "4 versions of Opus / models", "Model names that contain digits: Opus 4.6, Opus 4.7, Mythos 5, GPT-5.6", "R08", "Titles", "R08.txt", r"Mythos 5", "4.6;4.7;5.6;5", "source"),
]
# arithmetic checks: (id, description, lhs list, rhs)
SUMS = [("N01", [47.9, 20.8], 68.7), ("N04", [50.0, 16.7], 66.7), ("N07", [20.8, 2.1], 22.9), ("N18", [17, 2], 19)]

L.append(("N42", "5.5%", "Rollouts in which Opus 4.7 de-escalated after resampling from the self-stop point (up to 10 replayed actions); rare outcome, not reliable containment", "R08", "Alignment assessment (resampling experiments)", "R08.txt", r"only de-escalated in 5\.5% of rollouts", "5.5", "source"))
import json as _json
_nr = _json.load(open(os.path.join(RESULTS, "n_refs_counts.json")))
_n = 43
L.append(("N43", "%d of %d" % (_nr["documented_n_refs_1"], _nr["documented_cells"]), "Documented cells citing exactly one source (n_refs==1), results/n_refs_counts.json", "data", "evidence_class_rows.csv", "", "", "%d;%d" % (_nr["documented_n_refs_1"], _nr["documented_cells"]), "data"))
for _i, (_c, _v) in enumerate(_nr["by_cluster"].items()):
    L.append(("N%d" % (44 + _i), "%s: %d of %d" % (_c, _v["n_refs_1"], _v["documented"]), "n_refs==1 documented cells, cluster " + _c, "data", "evidence_class_rows.csv", "", "", "%d;%d" % (_v["n_refs_1"], _v["documented"]), "data"))
for _i, (_c, _v) in enumerate(_nr["by_dimension"].items()):
    L.append(("N%d" % (47 + _i), "%s: %d of %d" % (_c, _v["n_refs_1"], _v["documented"]), "n_refs==1 documented cells, dimension " + _c, "data", "evidence_class_rows.csv", "", "", "%d;%d" % (_v["n_refs_1"], _v["documented"]), "data"))
_dc = _json.load(open(os.path.join(RESULTS, "derived_counts.json")))["derived_counts"]
_k = 54
def _add(v, claim, tok):
    global _k
    L.append(("N%d" % _k, v, claim, "data", "results/derived_counts.json", "", "", tok, "data"))
    _k += 1
_add("36", "Documented-or-unknown cells of evidence class O (results/evidence_class_matrix.csv); NOT the decision count (45)", "36")
_add("%d" % _dc["multi_source"], "Documented cells citing more than one source (n_refs>1) in " + _dc["coding_file"], "%d" % _dc["multi_source"])
_add("%d" % _dc["downgraded_single_source_unchecked"], "Documented cells downgraded: single-source, not independently checked", "%d" % _dc["downgraded_single_source_unchecked"])
_add("%d" % _dc["class_I_documented"], "Documented cells of evidence class I (external investigation interpretation)", "%d" % _dc["class_I_documented"])
_t = {r["status"]: 0 for r in rows("coded_evidence.csv")}
for _r in rows("coded_evidence.csv"):
    _t[_r["status"]] += 1
_doc, _con, _unk = _t.get("documented", 0), _t.get("contradicted", 0), _t.get("unknown", 0)
L.append(("N34", "%d / %d / %d" % (_doc, _con, _unk), "documented / contradicted / unknown count (coded_evidence.csv)", "data", "coded_evidence.csv", "", "", "%d;%d;%d" % (_doc, _con, _unk), "data"))
L.append(("N73", "41 workers", "Hugging Face production dataset-server workers on which agents executed code", "R02", "IV.B (p.9)", "R02.txt", r"41 Hugging Face production dataset\s+server workers", "41", "source"))
_au = _json.load(open(os.path.join(RESULTS, "evidence_audit.json")))
L.append(("N72", "%d passages" % _au["passages_checked"], "Quoted supporting passages checked verbatim by scripts/evidence_audit.py", "data", "results/evidence_audit.json", "", "", "%d" % _au["passages_checked"], "data"))
_add("direct %s / inferred %s" % (_dc["direct"], _dc["inferred"]), "Direct vs inferred documented cells (None = awaiting analyst's v13 split; coding file " + _dc["coding_file"] + ")", "" if _dc["direct"] is None else "%d;%d" % (_dc["direct"], _dc["inferred"]))


def anchor(cf, pat):
    if not cf:
        return "n/a"
    if cf.startswith("sources.csv:"):
        c = [s["citation"] for s in rows("sources.csv") if s["ref"] == cf.split(":")[1]][0]
        return "found in ledger citation only" if re.search(pat, c) else "NOT FOUND"
    p = os.path.join(CACHE, cf)
    if not os.path.exists(p):
        return "cache missing"
    t = open(p, encoding="utf-8", errors="ignore").read()
    return "found" if re.search(pat, t) else "NOT FOUND"

arith = {}
bad = []
for i, parts, tot in SUMS:
    ok = abs(sum(parts) - tot) < 1e-9
    arith[i] = ("+".join(map(str, parts)) + f"={tot}: " + ("ok" if ok else "FAIL"))
    if not ok:
        bad.append(arith[i])
out = []
for (i, v, claim, ref, sec, cf, pat, tok, kind) in L:
    a = anchor(cf, pat)
    if a in ("NOT FOUND", "cache missing"):
        bad.append(f"{i} {v}: anchor {a} in {cf}")
    out.append({"id": i, "value": v, "claim": claim, "ref": ref, "source_section": sec, "cache_file": cf,
                "anchor_pattern": pat, "anchor_check": a, "kind": kind, "arithmetic_check": arith.get(i, ""), "tokens": tok})
write_csv(os.path.join(DATA, "number_ledger.csv"), list(out[0]), out)
allowed = {t.replace(",", "") for r in out for t in r["tokens"].split(";")}

NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
def scan(path, strip_tex=False):
    if not os.path.exists(path):
        return None
    t = open(path, encoding="utf-8", errors="ignore").read()
    if strip_tex:
        t = re.sub(r"%.*", "", t)
        t = re.sub(r"\\(cite|ref|label|input|includegraphics|bibliography\w*|usepackage|documentclass)\*?(\[[^\]]*\])?\{[^}]*\}", "", t)
        t = re.sub(r"\[\d+(?:[,\u2013-]\s*\d+)*\]", "", t)
    t = re.sub(r"\bR\d{2}\b|\bD[1-5]\b|\bA\d{2}\b|\bN\d{2}\b|\bQ\d\b", "", t)  # ledger IDs
    t = re.sub(r"\[\d+(?:[,\u2013-]\s*\d+)*\]", "", t)  # IEEE citation numbers
    t = re.sub(r"^#+ .*", "", t, flags=re.M)  # headings
    miss = {}
    for m in NUM.finditer(t):
        tok = m.group(0).rstrip(".,").replace(",", "")
        if tok not in allowed:
            miss.setdefault(tok, 0)
            miss[tok] += 1
    return miss

draft = scan(os.path.join(PAPER, "draft.md"))
tex = scan(os.path.join(PAPER, "build", "paper.tex"), True)
msgs = [f"{len(out)} ledger rows, {sum(r['anchor_check']=='found' for r in out)} anchors found, "
        f"{sum(r['anchor_check']=='NOT FOUND' for r in out)} not found; arithmetic: " + "; ".join(arith.values())]
if draft is None:
    msgs.append("draft.md missing")
    bad.append("draft.md missing")
else:
    msgs.append(f"draft.md: {len(draft)} distinct numbers not in ledger" + (": " + ", ".join(sorted(draft)) if draft else ""))
    if draft:
        bad.append("draft.md numbers not in ledger: " + ", ".join(sorted(draft)))
if tex is not None:
    msgs.append(f"build/paper.tex (report only): {len(tex)} distinct numeric tokens not in ledger: " + ", ".join(sorted(tex)[:40]))
status = "FAIL" if bad else "OK"
log("number_audit.py", " | ".join(msgs + [f"FAIL: {b}" for b in bad]), status)
print(status, *msgs, *bad, sep="\n")
sys.exit(1 if bad else 0)
