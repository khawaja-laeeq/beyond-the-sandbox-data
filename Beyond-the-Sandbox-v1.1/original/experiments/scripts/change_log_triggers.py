"""Round 11 (lead task, reason 9): add 'trigger', 'trigger_evidence' and 'blind_recheck_agrees' columns to
results/coding_change_log.csv. Idempotent: existing values in these columns are recomputed; no row is removed.

trigger categories (lead-scientist): self re-read | AI cross-read | author rule fix 2026-11-06.
Only rows whose old != new status get a trigger; other rows get 'n/a (no status change)'.
blind_recheck_agrees compares the row's NEW status with results/blind_recheck.csv (analyst AI re-check, round 11).
Note: every agent in this pipeline, including the primary coder, is an AI agent; 'self re-read' means the coding
party re-read sources without an outside objection. Evidence for each attribution is given in trigger_evidence.
Run from experiments/: python3 -I scripts/change_log_triggers.py
"""
import csv
import os

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(EXP, "results", "coding_change_log.csv")
BL = os.path.join(EXP, "results", "blind_recheck.csv")

TRIG = {
    "INC-OAI-MAY/D4": ("self re-read", "round 1: R02 reopened; change_log 'RECODED unknown->documented (round 1)'"),
    "INC-OAI-MAY/D5": ("self re-read", "round 1: R02 reopened; change_log 'RECODED unknown->documented (round 1)'"),
    "INC-ANT-OP47/D4": ("self re-read", "round 1: R08 reopened and R25 newly added"),
    "INC-AISI-MY5/D2": ("self re-read", "round 1: newly added source R26"),
    "INC-AISI-SOL/D5": ("self re-read", "round 1: newly added source R24 (later AI cross-read objection, round 3, kept the tag)"),
    "INC-OAI-ART/D2": ("AI cross-read", "reviewer R2 objection (comms/logs/round_4/reviewer-R2.log) applied as 'D2 rule (analyst)' in scripts/make_v13.py, promoted round 7"),
    "INC-OAI-HF/D2|documented|unknown": ("AI cross-read", "reviewer R2 objection (comms/logs/round_4/reviewer-R2.log) applied as 'D2 rule (analyst)' in scripts/make_v13.py, promoted round 7"),
    "INC-ANT-MY5/D2": ("AI cross-read", "round 8 recode (LOG.md round 8) after analyst open issue on simulation vs permission belief (ANALYSIS.md round 7/8)"),
    "INC-OAI-HF/D2|unknown|documented": ("AI cross-read", "round-11 blind re-check J2 (R07 agent CoT); lead decision D-a, round 12; applied via scripts/evidence_audit.py"),
    "INC-OAI-HF/D1|unknown|documented": ("human answer Q5/Q6 (supersedes Q4)", "answers.md Q5 (keep documented on R02) and Q6 (preserve the supplied data); plan.md Round 13 S-1; applied via scripts/evidence_audit.py"),
    "INC-OAI-HF/D1|documented|unknown": ("human answer Q4", "answers.md Q4: the Hugging Face D1 cell stays unknown; lead R-1, round 12; applied via scripts/evidence_audit.py"),
    "INC-OAI-ART/D1": ("author rule fix 2026-11-06", "passage-level audit rule P2 (scripts/evidence_audit.py), 2026-11-06"),
}


def main():
    rows = list(csv.DictReader(open(LOG, newline="", encoding="utf-8")))
    base = [c for c in rows[0].keys() if c not in ("trigger", "trigger_evidence", "blind_recheck_agrees")]
    blind = {}
    if os.path.exists(BL):
        blind = {r["unit"] + "/" + r["code"]: r["blind_status"] for r in csv.DictReader(open(BL, encoding="utf-8"))}
    unmapped = []
    for r in rows:
        if r["old"] != r["new"]:
            t = TRIG.get("%s|%s|%s" % (r["row"], r["old"], r["new"])) or TRIG.get(r["row"])
            if t is None:
                unmapped.append(r["row"])
                t = ("UNATTRIBUTED", "no evidence found")
            r["trigger"], r["trigger_evidence"] = t
            b = blind.get(r["row"])
            r["blind_recheck_agrees"] = "" if b is None else ("yes" if b == r["new"] else "no (blind: %s)" % b)
        else:
            r["trigger"], r["trigger_evidence"], r["blind_recheck_agrees"] = "n/a (no status change)", "", ""
    with open(LOG, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, base + ["trigger", "trigger_evidence", "blind_recheck_agrees"])
        w.writeheader()
        w.writerows(rows)
    ch = [r for r in rows if r["old"] != r["new"]]
    print("status-change rows:", len(ch), "unique cells:", len({r["row"] for r in ch}), "unmapped:", unmapped)
    for r in ch:
        print(r["row"], r["old"], "->", r["new"], "|", r["trigger"], "| blind agrees:", r["blind_recheck_agrees"])


if __name__ == "__main__":
    main()
