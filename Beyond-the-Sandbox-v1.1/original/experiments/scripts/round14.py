"""Round 14 (2026-11-09), experimenter tasks R14-1b and R14-1c. Run from experiments/: python3 -I scripts/round14.py (idempotent).
R14-1b  INC-OAI-HF/D4 re-judged under S2 (whole proposition, each organisation's own document) on the R03 passage alone.
        R03 (Hugging Face) states only Hugging Face's detection and response; it says nothing about OpenAI containment.
        R02 (OpenAI) states OpenAI's detection, informing Hugging Face and initial containment; it does not itself state Hugging
        Face's detection. Choice: S2 = 0 documented / 45 (no document supports the whole retained proposition). The status stays
        documented on the combined proposition; partial_support is set to R02;R03 so each document counts as partial support.
R14-1c  One D2 scope-attribution rule applied to all nine D2 cells (rule text in D2_RULE; also written to codebook.csv D2/documented).
        No status changes result; each application is logged (trigger "AI-agent re-check, round 14")."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, rows, write_csv, log

TRIG = "AI-agent re-check, round 14"
D2_RULE = ("D2 scope-attribution rule (round 14): D2 is documented only if the source reports a belief, attributed to the model "
           "(its own words, a reported answer, or the developer's report of its reasoning), that concerns PERMISSION to act on the "
           "target of the contested action (authorized / approved / in scope / out of scope). A belief only about WHAT the target "
           "or its actors are (simulated, a realism judgment, scripted actors, who owns it) is not a permission belief, nor is a scope "
           "statement about a different target than the contested action; both stay unknown.")
APPLIED = {
    "INC-OAI-MAY": ("unknown", "no belief of any kind is reported; the passage reports actions only"),
    "INC-OAI-ART": ("unknown", "R07 states a scorer-manipulation objective, not a belief about permission"),
    "INC-OAI-HF": ("documented", "R07 quotes 'The user only authorizes target server, not HF infra': a permission belief about the target acted on (out of scope)"),
    "INC-ANT-OP46": ("documented", "R08: the model said it 'was authorized to do so in the context of the CTF': a permission belief about the target"),
    "INC-ANT-OP47": ("documented", "R08: answered 'yes' 75% when asked if it was authorized, and its CoT said the target was 'still part of the CTF': a permission belief (elicitation contested)"),
    "INC-ANT-MY5": ("unknown", "R08: scanners were treated 'as scripted actors in the exercise': a belief about what the scanners are, not about permission to act on them or the target"),
    "INC-ANT-INT": ("documented", "R08: the model 'inferred that the network neighbors were targets meant for other CTF participants and were thus in scope for the task': the belief concerns whether the target was in scope, i.e. permission; contrast ANT-MY5, where only the identity of the actors is stated"),
    "INC-AISI-MY5": ("documented", "R26: the CTF organizers 'had set it up for this exercise' and an 'approved route': a permission belief about the repository acted on"),
    "INC-AISI-SOL": ("unknown", "R24 A.10 scope statements ('in-range attack surface') concern the pivot back into range, not the target of the out-of-scope GitHub/DNS actions"),
}

ce = os.path.join(DATA, "coded_evidence.csv")
R = rows("coded_evidence.csv")
fn = list(R[0].keys())
clog = os.path.join(RESULTS, "coding_change_log.csv")
L = list(csv.reader(open(clog, encoding="utf-8")))
have = {(r[0], r[3]) for r in L[1:]}
new_rows = []

for r in R:
    k = (r["unit"], r["code"])
    if k == ("INC-OAI-HF", "D4"):
        msg = ("S2 re-judged (round 14, R14-1b): R03 alone ('Earlier this week, we detected and responded to an intrusion into part of our "
               "production infrastructure') shows Hugging Face detection and response only, not OpenAI containment; R02 I (p.4) ('informed "
               "Hugging Face, and implemented initial containment measures') shows OpenAI's response only. Neither document supports the whole "
               "retained proposition (both organisations' detection/response and OpenAI containment), so S2 = 0/45. Status unchanged (documented); "
               "partial_support R02;R03; proposition not split")
        if "R14-1b" not in r["change_log"]:
            r["change_log"] += "; " + msg
            r["partial_support"] = "R02;R03"
            r["qualification"] += " | Round 14 (R14-1b): each reference supports only its own organisation's part of the proposition (R03: Hugging Face detection and response; R02: OpenAI response and containment); no single document supports the whole proposition."
        if ("INC-OAI-HF/D4", msg) not in have:
            new_rows.append(["INC-OAI-HF/D4", "documented", "documented", msg, "", TRIG, "R03 opening (Hugging Face detection and response only); R02 I p.4", ""])
    if r["code"] == "D2":
        st, why = APPLIED[r["unit"]]
        assert r["status"] == st, (r["unit"], r["status"], st)
        msg = "D2 scope-attribution rule applied (round 14, R14-1c): %s; status unchanged (%s)" % (why, st)
        if "R14-1c" not in r["change_log"]:
            r["change_log"] += "; " + msg
        if (r["unit"] + "/D2", msg) not in have:
            new_rows.append([r["unit"] + "/D2", st, st, msg, "", TRIG, why, ""])
write_csv(ce, fn, R)
with open(clog, "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(new_rows)

cb = rows("codebook.csv")
for r in cb:
    if r["code"] == "D2" and "permission" not in r["documented"]:
        r["documented"] += ". Round 14 rule: " + D2_RULE
write_csv(os.path.join(DATA, "codebook.csv"), list(cb[0].keys()), cb)
with open(os.path.join(RESULTS, "d2_scope_rule.md"), "w", encoding="utf-8") as f:
    f.write("# D2 scope-attribution rule (round 14)\n\n" + D2_RULE + "\n\n| Unit | Status | Reading under the rule |\n|---|---|---|\n")
    for u, (st, why) in APPLIED.items():
        f.write("| %s | %s | %s |\n" % (u, st, why))
log("round14.py", "R14-1b choice: OAI-HF/D4 S2 set to 0/45 (not split). R03 passage alone: 'Earlier this week, we detected and responded to an intrusion "
    "into part of our production infrastructure' = Hugging Face detection and response only, no OpenAI containment; R02 I p.4 'informed Hugging Face, and "
    "implemented initial containment measures' = OpenAI response only; partial_support R02;R03, status unchanged. R14-1c: D2 scope rule applied to 9 cells, "
    "no status change. %d change-log rows added" % len(new_rows))
print("added", len(new_rows), "change-log rows")
