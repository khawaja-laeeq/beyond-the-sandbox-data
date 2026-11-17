"""Round 10: (1) operational direct/inferred rule applied to all 39 documented cells; (2) context-only sources R51-R56.
Rule: direct = the quoted passage reports an event, or the model's own stated reasoning/statement (said, responded,
declared, inferred, recognized). inferred = the source's interpretation of a belief the model did not state in the
quoted passage (e.g. 'consistent with a belief', 'generally believed'). Edits data/coded_evidence.csv in place.
Idempotent. Run from experiments/: python3 -I scripts/round10.py"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, log, write_csv

p = os.path.join(DATA, "coded_evidence.csv")
R = list(csv.DictReader(open(p, encoding="utf-8")))
fields = list(R[0])
RULE = ("Round 10 rule: direct = quoted passage reports an event or the model's own stated reasoning/statement; "
        "inferred = the source's interpretation of a belief the model did not state in the passage.")
INFERRED = {
    ("INC-AISI-MY5", "D2"): "R26 'consistent with a belief': source's interpretation of unstated belief",
    ("INC-ANT-OP47", "D2"): "R08 'generally believed ... believed it was authorized': developer's attribution of belief, no model statement quoted",
}
for r in R:
    k = (r["unit"], r["code"])
    if r["status"] != "documented":
        continue
    new = "inferred" if k in INFERRED else "direct"
    if r["support_type"] != new:
        why = INFERRED.get(k, "passage reports event or model statement")
        prefix = r["change_log"] + "; " if r["change_log"] else ""
        r["change_log"] = prefix + "ROUND 10 support_type " + r["support_type"] + "->" + new + ": " + why + ". " + RULE
        r["support_type"] = new
write_csv(p, fields, R)
print("inferred:", list(INFERRED))

sp = os.path.join(DATA, "sources.csv")
S = list(csv.DictReader(open(sp, encoding="utf-8")))
have = {r["url"] for r in S}
new = [
    ("Dark Reading, “When AI Agents Escape Sandboxes, Old Security Rules Apply.”", "https://www.darkreading.com/application-security/ai-agents-escape-sandboxes-old-security-rules-apply"),
    ("SC Media (Z. Karliner), “AI agents need boundaries they can’t override,” 2026-09-24.", "https://www.scworld.com/perspective/ai-agents-need-boundaries-they-cant-override"),
    ("NHI Management Group, “Agentic AI intent over identity: what the OpenAI escape reveals,” 2026-09-06.", "https://nhimg.org/articles/agentic-ai-intent-over-identity-what-the-openai-escape-reveals"),
    ("NHI Management Group, “Agentic AI sandboxes: where did the control boundary fail?” 2026-09-06.", "https://nhimg.org/community/ai-beyond-identity/agentic-ai-sandboxes-where-did-the-control-boundary-fail"),
    ("NHI Management Group, “AI agents need external controls after sandbox breakout tests,” 2026-09-06.", "https://nhimg.org/articles/ai-agents-need-external-controls-after-sandbox-breakout-tests"),
    ("UK NCSC, “Managing the cyber risk of agentic AI,” 2026-09-24.", "https://www.ncsc.gov.uk/blogs/managing-the-cyber-risk-of-agentic-ai"),
]
n = max(int(r["ref"][1:]) for r in S)
added = []
for cit, url in new:
    if url in have:
        continue
    n += 1
    added.append(dict(ref="R%02d" % n, citation=cit, url=url,
                      verification="listed by data-scout 2026-11-06; NOT opened by experimenter (scout summary only); secondary commentary on units already coded from primary sources; no coded row depends on it",
                      relevance="secondary coverage (context)"))
with open(sp, "a", newline="", encoding="utf-8") as f:
    csv.DictWriter(f, ["ref", "citation", "url", "verification", "relevance"]).writerows(added)
print("sources added", [a["ref"] for a in added])
log("round10.py", "support_type rule applied to 39 documented cells; sources added %s" % [a["ref"] for a in added])
