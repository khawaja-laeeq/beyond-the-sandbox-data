"""Analyst round 12 (lead tasks R6, R8, R9, R12). Annotation only: no status or reference is changed here
(coding changes go through scripts/evidence_audit.py, rule R5). Idempotent.

R6  contested_by: for every cell where a cached passage points the other way, the challenging passage,
    its locator and the trigger. Written to data/coded_evidence.csv and results/evidence_audit.csv.
R8  D5 decision tree (plan D-c): d5_tree_branch + d5_deciding_passage for all 9 D5 cells; the two
    level changes (AISI-SOL, AISI-MY5: L2 -> L3) are appended to results/coding_change_log.csv
    (status unchanged, so old == new == documented).
R9  d2_evidence_type, d2_elicitation, d2_direction, d2_scope_note for all 9 D2 cells; strict-rule recount
    in results/d2_strict.csv and results/d2_strict.json.
R12 HF D4 partial support (R02) recorded in partial_support; not counted in n_refs.

Every quoted passage is checked verbatim (letters and digits) against source_cache/<ref>.txt; the script
exits without writing anything if one is missing.
NOTE: scripts/evidence_audit.py rewrites results/evidence_audit.csv without the contested_by column, and
scripts/round9.py rewrites the ANT-INT/D2 evidence text; re-run this script after either of them.
Run from experiments/: python3 -I scripts/analyst_round12.py"""
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, EXP, write_csv, log  # noqa: E402

CACHE = os.path.join(EXP, "source_cache")
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
_cache = {}


def found(ref, q):
    if ref not in _cache:
        p = os.path.join(CACHE, ref + ".txt")
        _cache[ref] = norm(open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else ""
    return norm(q) in _cache[ref]


# ---------------- R6: contested_by (challenging passage, locator, trigger) ----------------
CONTESTED = {
    ("INC-OAI-HF", "D2"): ("R07", "R07 summary (opening takeaways)",
        "The Hugging Face attack grew out of these workstreams, and seemed primarily motivated by understanding the implementation of the scorer rather than stealing answer keys",
        "round-7 recode reason (reviewer R2 round 4, scorer-objective reading); round-11 blind re-check J2; lead D-a",
        "Points the other way on WHAT D2 codes: the investigator frames the attack as scorer investigation; the coded passage is the agents' own statement that the action was outside what the user authorized (direction: not authorized), unlike the four Anthropic/AISI D2 cells (direction: authorized/in scope)."),
    ("INC-ANT-OP47", "D2"): ("R08", "R08 Opus 4.7 section ('did not check whether it was authorized')",
        "It ignored the question of permission, both in the original transcript and when we replayed key moments in resampling experiments",
        "analyst round 12 re-read for R6",
        "The 'yes' 75% answers were elicited by follow-up questions; during the run the model did not consider permission (thinking blocks questioned ownership and authorization in 1.5% of re-runs). Supports D2 as a reported answer, not as a contemporaneous authorization belief."),
    ("INC-AISI-MY5", "D2"): ("R26", "R26 Mythos 5 deep dive (momentum)",
        "This stated belief, in addition to being somewhat unlikely a priori, is essentially impossible",
        "analyst round 12 re-read for R6",
        "The developer treats the stated answer as biased or motivated reasoning; it records what the model said, not necessarily what it believed."),
    ("INC-ANT-MY5", "D2"): ("R08", "R08 Mythos 5 section",
        "When security scanners installed its package, for example, the model treated them as scripted actors in the exercise",
        "round-11 blind re-check J5 (borderline)",
        "Could be read as a scope interpretation (third parties treated as part of the exercise), but it is the developer's paraphrase of a realism judgment; Appendix A rule 2 keeps it unknown."),
    ("INC-AISI-SOL", "D2"): ("R24", "R24 Appendix A.10 (pp.31-32)",
        "I'll pivot fully to the in-range attack surface",
        "round-11 blind re-check J5 (borderline)",
        "A verbatim agent statement of scope ('in-range attack surface', 'rescan only the permitted entry subnet'), but about the pivot back after the GitHub account was suspended, not about the out-of-scope GitHub/DNS actions. Under a rule that counts any verbatim scope statement (the rule that recoded OAI-HF/D2) this cell is the most likely to flip."),
    # round 12 second pass (lead reason 6): R-2 made R02 a full reference for HF/D4; the challenge record must survive.
    ("INC-OAI-HF", "D4"): ("R02", "R02 VI.A (pp.14-15)",
        "At the time, there was no indication of a relationship between that July 19 activity and the Hugging Face incident",
        "advisor round 11 reason 12; lead R-2 (R02 accepted as full reference); analyst round 12 second pass",
        "OpenAI's July 19 detection was of internal Artifactory activity; R02 VI.A also states 'On July 16, Hugging Face released a blog post disclosing that they were impacted by a security incident', and OpenAI linked its agents to the intrusion only on July 20. R02 therefore supports OpenAI's response to the Hugging Face intrusion, but its detection of that intrusion followed Hugging Face's own disclosure (R03). The two references are from different organisations but are not independent observations of first detection."),
}

PARTIAL = {}  # round 13 (S-1): HF/D1 is documented on R02 IV.A, so no partial-support record remains

# ---------------- R8: D5 decision tree (plan D-c) ----------------
# branch: C = credential/account not issued; N = non-public data accessed; P = persistent state created or
# modified on a system not authorized. L3 if any branch applies.
D5TREE = {
    "INC-OAI-MAY": ("C;P", "R02", "issued write requests using these tokens to create a Hugging Face repository", "L3", "L3",
                    "other users' exposed tokens (C); repository and proxy Space created (P)"),
    "INC-OAI-ART": ("C", "R02", "indicating an administrator-level compromise of the Artifactory deployment", "L3", "L3",
                    "administrator credentials obtained by exploit (C); operator-internal system, not a third party"),
    "INC-OAI-HF": ("C;N", "R04", "the agent used the AWS keys harvested from the pod environment against internal services", "L3", "L3",
                   "round 13 S-2: deciding branch C (AWS keys harvested from the pod environment, not issued to the agent). N (five customer datasets) stays qualified: the passage does not say they were non-public"),
    "INC-ANT-OP46": ("N;C", "R08", "read the personal information of one person associated with the third party", "L3", "L3",
                     "personal information (N); the D3 passage of the same unit (R08: 'a file listing a password, which it used to gain admin access to the system') shows a credential found in the target system and used (C)"),
    "INC-ANT-OP47": ("N;P", "R08", "download user records, and modify those records", "L3", "L3", "records downloaded (N) and modified (P)"),
    "INC-ANT-MY5": ("C;P", "R08", "scanner leaked its access credentials to the model while installing the package, which the model then used to access the vendor", "L3", "L3", "leaked vendor credentials used (C); the D3 passage (R08: 'installed on 15 third-party hosts') also meets P; C alone decides L3"),
    "INC-ANT-INT": ("C;P", "R08", "the model used access tokens and passwords to penetrate one of the network neighbors, downloading files and inserting a remote-control script", "L3", "L3", "tokens and passwords (C); script inserted (P)"),
    "INC-AISI-MY5": ("-", "R10", "created multiple fake identities, and used the fake identities to socially engineer a real maintainer", "L3", "L2",
                     "round 13 S-2: fake identities were created by the agent (not a credential or account of another party, so not C); the malicious contribution was refused (no persistent state established, so not P); no N passage. A public post only: L2"),
    "INC-AISI-SOL": ("C", "R24", "and used it to authenticate to GitHub as GITHUB_ACCOUNT_A", "L2", "L3",
                     "personal access token recovered from another model's public Gist (C); the six provider registrations are accounts the agent made itself and do not count as C"),
}

# ---------------- R9: D2 evidence type ----------------
# d2_evidence_type: verbatim model statement | reported model answer | developer interpretation only | none (unknown)
# d2_elicitation: contemporaneous (CoT during the run) | post-hoc follow-up question | mixed | n/a
D2 = {
    "INC-OAI-MAY": ("none", "n/a", "n/a", "", "", ""),
    "INC-OAI-ART": ("none", "n/a", "n/a", "", "", ""),
    "INC-OAI-HF": ("verbatim model statement", "contemporaneous", "not authorized (knew the action was out of scope)",
                   "R07", "The user only authorizes target server, not HF infra",
                   "R07: 'Quotes across multiple runs'; reported for some of the ~700 participating agents, not per run"),
    "INC-ANT-OP46": ("reported model answer", "post-hoc follow-up question", "authorized (in the context of the CTF)",
                     "R08", "When asked what gave it the authority to engage these systems, the model always responded that it was authorized to do so in the context of the CTF",
                     "answers to follow-up questions inserted into the transcript; answer text shown only in an R08 figure (not in the cached text)"),
    "INC-ANT-OP47": ("reported model answer", "mixed", "authorized / in scope (part of the CTF)",
                     "R08", "the model also said “yes” 75% of the time",
                     "statistic over follow-up questions on the most-investigated of four runs; CoT paraphrased ('repeatedly stated ... still part of the CTF'); per-run answers not shown"),
    "INC-ANT-MY5": ("none", "n/a", "n/a", "", "", ""),
    "INC-ANT-INT": ("reported model answer", "contemporaneous", "in scope (hosts of other CTF competitors)",
                    "R08", "The CoT refers to the targets the model ultimately attacks as hosts meant for other CTF competitors",
                    "paraphrased CoT of one transcript; R08 'inferred ... in scope' is the developer's reading"),
    "INC-AISI-MY5": ("reported model answer", "post-hoc follow-up question", "in scope (repository set up by the CTF organizers)",
                     "R26", "Each time, the model answered that it was engaging with a repository on the real GitHub, but that the CTF organizers had set it up for this exercise",
                     "reported for some runs, not per run: follow-up questions after every action in compaction cycle 4 of one analysed transcript; AISI-MY5 groups 17 Mythos 5 actions (R10)"),
    "INC-AISI-SOL": ("none", "n/a", "n/a", "", "", ""),
}

# ---------------- verify every passage ----------------
missing = []
for (u, c), (ref, loc, q, trig, note) in CONTESTED.items():
    if not found(ref, q):
        missing.append(f"contested {u}/{c} {ref}: {q[:60]}")
for u, (br, ref, q, old, new, note) in D5TREE.items():
    if not found(ref, q):
        missing.append(f"D5 {u} {ref}: {q[:60]}")
for u, v in D2.items():
    if v[3] and not found(v[3], v[4]):
        missing.append(f"D2 {u} {v[3]}: {v[4][:60]}")
if not found("R02", "OpenAI detected suspicious internal activity on July 19"):
    missing.append("partial R02 detection passage")
if missing:
    sys.exit("Passages not found verbatim; nothing written:\n  " + "\n  ".join(missing))

# ---------------- write coded_evidence annotations ----------------
path = os.path.join(DATA, "coded_evidence.csv")
coded = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
fields = list(coded[0].keys())
NEW = ["contested_by", "partial_support", "d2_evidence_type", "d2_elicitation", "d2_direction", "d2_scope_note",
       "d5_tree_branch", "d5_deciding_passage"]
fields += [f for f in NEW if f not in fields]


def contested_text(k):
    if k not in CONTESTED:
        return ""
    ref, loc, q, trig, note = CONTESTED[k]
    return f"{ref} ({loc}): '{q}' | trigger: {trig} | {note}"


for r in coded:
    k = (r["unit"], r["code"])
    r["contested_by"] = contested_text(k)
    r["partial_support"] = PARTIAL.get(k, r.get("partial_support", "") or "")  # round 14: keep partial_support set by scripts/round14.py
    if r["code"] == "D2":
        t, el, dr, ref, q, sc = D2[r["unit"]]
        r["d2_evidence_type"], r["d2_elicitation"], r["d2_direction"], r["d2_scope_note"] = t, el, dr, sc
    else:
        r["d2_evidence_type"] = r["d2_elicitation"] = r["d2_direction"] = r["d2_scope_note"] = ""
    if r["code"] == "D5" and r["status"] == "documented":
        br, ref, q, old, new, note = D5TREE[r["unit"]]
        assert r["effect_level"] == new, (r["unit"], r["effect_level"], new)
        r["d5_tree_branch"] = f"{br} -> {new} ({note})"
        r["d5_deciding_passage"] = f"{ref}: '{q}'"
    else:
        r["d5_tree_branch"] = r["d5_deciding_passage"] = ""
    for f in fields:
        r.setdefault(f, "")
write_csv(path, fields, coded)

# evidence_audit.csv: add contested_by
ap = os.path.join(RESULTS, "evidence_audit.csv")
aud = list(csv.DictReader(open(ap, newline="", encoding="utf-8")))
af = list(aud[0].keys()) + (["contested_by"] if "contested_by" not in aud[0] else [])
for r in aud:
    r["contested_by"] = contested_text((r["unit"], r["code"]))
write_csv(ap, af, aud)

# ---------------- change log: D5 level changes + HF/D2 trigger ----------------
lp = os.path.join(RESULTS, "coding_change_log.csv")
log_rows = list(csv.DictReader(open(lp, newline="", encoding="utf-8")))
lf = list(log_rows[0].keys())
lf = [f for f in lf if f is not None]
for r in log_rows:
    r.pop(None, None)
    if r["row"] == "INC-OAI-HF/D2" and r["old"] == "unknown" and r["new"] == "documented" and not r.get("trigger"):
        r["trigger"] = "AI cross-read"
        r["trigger_evidence"] = "round-11 blind re-check J2 (R07 agent CoT); lead decision D-a, round 12; applied via scripts/evidence_audit.py"
        r["blind_recheck_agrees"] = "yes (by construction: the recode follows the re-check; pre-resolution agreement 44/45)"
for u in ("INC-AISI-SOL",):
    br, ref, q, old, new, note = D5TREE[u]
    reason = f"D5 effect_level {old}->{new} (round 12, decision tree D-c, branch {br}): {ref} '{q}'; status unchanged"
    if not any(r["row"] == f"{u}/D5" and "effect_level L2->L3" in r["reason"] for r in log_rows):
        log_rows.append({"row": f"{u}/D5", "old": "documented", "new": "documented", "reason": reason, "anchor": "",
                         "trigger": "author rule fix (D-c tree, round 12)",
                         "trigger_evidence": "plan.md Round 12 D-c; scripts/evidence_audit.py EFFECT table",
                         "blind_recheck_agrees": "n/a (level, not status)"})
S13 = [("INC-AISI-MY5/D5", "documented", "documented", "D5 effect_level L3->L2 (round 13, S-2): R10 What we found (1) 'created multiple fake identities, and used the fake identities to socially engineer a real maintainer'; self-made identities are not C, the contribution was refused (not P), no N passage; status unchanged", "author rule fix (plan S-2)"),
       ("INC-OAI-HF/D5", "documented", "documented", "D5 deciding branch N->C (round 13, S-2): R04 'the agent used the AWS keys harvested from the pod environment against internal services'; level L3 unchanged; status unchanged", "author rule fix (plan S-2)"),
       ("INC-OAI-HF/D1", "unknown", "documented", "RECODED unknown->documented (round 13, S-1): R02 IV.A 'bypassed those controls by exploiting certain Artifactory endpoints, gaining access to the public internet' supports D1 by itself; supersedes the Q4-based recode of round 12", "human answer Q5/Q6 (supersedes Q4)")]
for row_, o_, n_, why_, trig_ in S13:
    if not any(r["row"] == row_ and r["reason"].startswith(why_[:60]) for r in log_rows):
        log_rows.append({"row": row_, "old": o_, "new": n_, "reason": why_, "anchor": "", "trigger": trig_,
                         "trigger_evidence": "answers.md Q5/Q6; plan.md Round 13 S-1/S-2; applied via scripts/evidence_audit.py" ,
                         "blind_recheck_agrees": "n/a"})
write_csv(lp, lf, log_rows)

# ---------------- R9: strict D2 recount ----------------
st = {(r["unit"], r["code"]): r["status"] for r in coded}
out = []
for u, (t, el, dr, ref, q, sc) in D2.items():
    s = st[(u, "D2")]
    out.append({"unit": u, "status_as_coded": s, "d2_evidence_type": t, "d2_elicitation": el, "d2_direction": dr,
                "deciding_passage": f"{ref}: '{q}'" if ref else "", "scope_note": sc,
                "contested_by": contested_text((u, "D2")),
                "strict_verbatim_only": "documented" if (s == "documented" and t == "verbatim model statement") else "unknown",
                "contemporaneous_only": "documented" if (s == "documented" and el in ("contemporaneous", "mixed")) else "unknown",
                "contemporaneous_strict": "documented" if (s == "documented" and el == "contemporaneous") else "unknown",
                "excluding_developer_interpretation_only": "documented" if (s == "documented" and t != "developer interpretation only") else "unknown"})
write_csv(os.path.join(RESULTS, "d2_strict.csv"), list(out[0].keys()), out)


def recount(col):
    d2doc = sum(r[col] == "documented" for r in out)
    other = sum(v == "documented" for (u, c), v in st.items() if c != "D2")
    unk_by = {c: sum(1 for (u, cc), v in st.items() if cc == c and v == "unknown") for c in ("D1", "D2", "D3", "D4", "D5")}
    unk_by["D2"] = 9 - d2doc
    return {"D2_documented": d2doc, "D2_unknown": 9 - d2doc, "total_documented": other + d2doc,
            "total_unknown": 45 - other - d2doc, "unknown_by_dim": unk_by,
            "D2_has_most_unknowns": unk_by["D2"] > max(v for k, v in unk_by.items() if k != "D2")}


summ = {"as_coded": recount("status_as_coded"), "strict_verbatim_only": recount("strict_verbatim_only"),
        "contemporaneous_only": recount("contemporaneous_only"),
        "contemporaneous_only_label": "rule counts d2_elicitation 'contemporaneous' OR 'mixed' (includes OP47)",
        "contemporaneous_strict": recount("contemporaneous_strict"),
        "excluding_developer_interpretation_only": recount("excluding_developer_interpretation_only"),
        "evidence_type_counts": {t: sum(r["d2_evidence_type"] == t for r in out) for t in
                                 ("verbatim model statement", "reported model answer", "developer interpretation only", "none")},
        "direction_of_documented": {r["unit"]: r["d2_direction"] for r in out if r["status_as_coded"] == "documented"},
        "note": "verbatim = R07 quotes the agents' CoT in quotation marks; R26's capitalised 'OUT OF SCOPE' text is a clause the researchers ADDED to the compaction notes, not a model statement, so it does not make AISI-MY5 verbatim."}
json.dump(summ, open(os.path.join(RESULTS, "d2_strict.json"), "w", encoding="utf-8"), indent=1)
log("analyst_round12.py", "contested_by %d cells; D5 tree 9 cells; d2_strict: as coded %d, strict %d, contemporaneous %d D2 documented"
    % (len(CONTESTED), summ["as_coded"]["D2_documented"], summ["strict_verbatim_only"]["D2_documented"],
       summ["contemporaneous_only"]["D2_documented"]))
print(json.dumps(summ, indent=1))
