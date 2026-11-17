"""Round 9 (2026-11-06). Run from experiments/: python3 -I scripts/round9.py  (idempotent)
1. INC-ANT-INT/D2: evidence text rewritten to the R08 scope statement (status unchanged: documented).
2. Adds the 3 newest data-scout sources (context rows, not opened).
3. Rewrites change-log rows that referred to a second coder; adds round-8/9 rows.
4. Writes results/audit_trail.csv for every decision (from evidence_audit.csv + coded_evidence.csv).
5. Checks draft Appendix B refs == coded_evidence.csv refs -> results/appendix_b_check.csv."""
import csv, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

ce = os.path.join(DATA, "coded_evidence.csv")
R = rows("coded_evidence.csv")
fn = list(R[0].keys())
Q = "inferred that the network neighbors were targets meant for other CTF participants and were thus in scope for the task"
for r in R:
    if r["unit"] == "INC-ANT-INT" and r["code"] == "D2":
        # round 12: evidence/qualification text is owned by evidence_audit.py (audit passages); not overwritten here
        note = ("ROUND 9: kept documented; evidence text rewritten to the scope statement quoted from R08 internal model section "
                "(the simulation-only paraphrase was not a permission belief). Contrast ANT-MY5/D2, recoded to unknown because R08 gives only a simulation belief there.")
        if "ROUND 9" not in r["change_log"]:
            r["change_log"] += "; " + note
for r in R:
    if r["unit"] == "INC-OAI-ART" and r["code"] == "D1" and r["reference"] == "R07":
        r["reference"] = "R02;R07"  # audit passage is R02 III.B; unknown cell, no documented count changes
        r["change_log"] += "; ROUND 9: reference field aligned with audit (R02 passage examined, R07 earlier source)"
write_csv(ce, fn, R)

# 2. sources
have = rows("sources.csv"); urls = {s["url"] for s in have}; n = int(have[-1]["ref"][1:]); new = []
for l in open(os.path.join(PAPER, "research", "new_sources.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    if d.get("checked", "").startswith("2026-11-06") and d["url"] not in urls:
        n += 1
        new.append({"ref": "R%d" % n, "citation": "%s, “%s,” %s." % (d["publisher"], d["title"], d["date"]), "url": d["url"],
                    "verification": "listed by data-scout 2026-11-06 (status: %s); NOT opened by experimenter (scout summary only); context only, no coded row depends on it" % d.get("status"),
                    "relevance": "comparable incident (context)" if d["type"] == "comparable-incident" else "secondary coverage (context)"})
if new:
    with open(os.path.join(DATA, "sources.csv"), "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["ref", "citation", "url", "verification", "relevance"]).writerows(new)
print("sources added", [r["ref"] for r in new])

# 3. change log
p = os.path.join(RESULTS, "coding_change_log.csv")
L = list(csv.reader(open(p, encoding="utf-8")))
out = [L[0]]
for row in L[1:]:
    if row[0].startswith(("DISAGREEMENT", "SUPERSEDED")):
        u = row[0].split(" ", 1)[1]
        row = [u, row[1], row[2], "Earlier AI cross-read objection (no second coder; no agreement statistic). Resolved by the passage-level audit 2026-11-06: tag unchanged; see results/evidence_audit.csv for the deciding passage.", row[4]]
    out.append(row)
if not any(r[0] == "INC-ANT-INT/D2" for r in out):
    out.append(["INC-ANT-INT/D2", "documented", "documented", "ROUND 9: kept; evidence rewritten to R08 scope statement: '%s'" % Q, ""])
if not any(r[0] == "INC-ANT-MY5/D2" and "round 8" in r[3] for r in out):
    out.append(["INC-ANT-MY5/D2", "documented", "unknown", "RECODED documented->unknown (round 8): R08 reports a simulation belief, not a permission belief", ""])
if not any(r[0] == "INC-OAI-HF/D1" and "round 8" in r[3] for r in out):
    out.append(["INC-OAI-HF/D1", "documented", "documented", "Round 8: kept; R02 IV.A added (R01 HTTP 403)", ""])
seen = set(); ded = []
for r in out:
    if tuple(r) not in seen:
        seen.add(tuple(r)); ded.append(r)
csv.writer(open(p, "w", newline="", encoding="utf-8")).writerows(ded)

# 4. audit trail
ea = {(r["unit"], r["code"]): r for r in rows("evidence_audit.csv", RESULTS)}
cache = os.path.join(EXP, "source_cache")
tr = []
for r in R:
    a = ea[(r["unit"], r["code"])]
    refs = [x for x in r["reference"].split(";") if x]
    cached = [x for x in refs if os.path.exists(os.path.join(cache, x + ".txt"))]
    tr.append(dict(unit=r["unit"], code=r["code"], status=r["status"], references=r["reference"], cached_refs=";".join(cached),
                   uncached_refs=";".join(x for x in refs if x not in cached), locator=a["locator"], quotes_found=a["passages_found_verbatim"],
                   passages=a["passages"], note=a["note"]))
write_csv(os.path.join(RESULTS, "audit_trail.csv"), list(tr[0]), tr)

# 5. appendix B check
name = {"INC-OAI-MAY": "OpenAI May", "INC-OAI-ART": "OpenAI Artifactory", "INC-OAI-HF": "OpenAI Hugging Face", "INC-ANT-OP46": "Anthropic Opus 4.6",
        "INC-ANT-OP47": "Anthropic Opus 4.7", "INC-ANT-MY5": "Anthropic Mythos 5", "INC-ANT-INT": "Anthropic internal model",
        "INC-AISI-MY5": "AISI Mythos 5", "INC-AISI-SOL": "AISI Sol"}
inv = {v: k for k, v in name.items()}
txt = open(os.path.join(PAPER, "draft.md"), encoding="utf-8").read()
sec = txt.split("## Appendix B.")[1].split("## Appendix C.")[0]
chk = []; cm = {(r["unit"], r["code"]): r for r in R}; seen = set()
for line in sec.splitlines():
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) >= 7 and c[0] in inv and re.fullmatch(r"D[1-5]", c[1]):
        k = (inv[c[0]], c[1]); seen.add(k)
        # last column holds the citations "[@R02; @R07], locator"; read only @-prefixed keys (locators may name refs too)
        d = set(re.findall(r"@(R\d+)", c[-1])); s = set(x for x in cm[k]["reference"].split(";") if x)
        chk.append(dict(unit=k[0], code=k[1], draft_refs=";".join(sorted(d)), csv_refs=";".join(sorted(s)), equal="yes" if d == s else "NO"))
for k in cm:
    if k not in seen:
        chk.append(dict(unit=k[0], code=k[1], draft_refs="(row missing)", csv_refs=cm[k]["reference"], equal="NO"))
write_csv(os.path.join(RESULTS, "appendix_b_check.csv"), list(chk[0]), chk)
bad = [c for c in chk if c["equal"] != "yes"]
print("appendix B rows", len(chk), "mismatches", len(bad))
for b in bad:
    print(b)
log("round9.py", "ANT-INT/D2 text, sources, change log, audit_trail (45), appendix_b_check (%d mismatches)" % len(bad))
