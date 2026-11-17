"""Passage-level sufficiency audit of every coded decision (2026-11-06).

For each of the 45 decisions this records the source passage that supports (or fails to support) the
dimension-specific proposition in the codebook, checks every quoted passage verbatim against the cached
source text (source_cache/<ref>.txt, compared on letters and digits only so line breaks, hyphenation and
quote marks do not matter), and only then applies the audit's tag and reference changes to
data/coded_evidence.csv. A cell stays documented only when its passage supports the proposition; the
absence of a contradicting passage is not enough.

Three rules make the tags comparable across units (round-10 review reasons 6, 10 and 12):
1. Direct vs inferred follows the passage, not the source's role. A passage is an "interpretation" when it
   gives the investigator's conclusion about the model's state (believed, inferred, suggests, consistent
   with); otherwise it reports an event or what the model said or wrote ("statement"). A documented cell is
   direct when at least one statement or event passage supports the proposition, else inferred.
2. Every reference listed for a documented cell must independently support the whole proposition: each
   listed reference has its own passage, and compound claims (such as which party detected first) are
   kept out of the proposition and recorded only as qualifications.
3. D4 and D5 are recorded at a common level of specificity: response_stage for D4, and effect_scope plus
   effect_level for D5 (see STAGE and EFFECT below), so units are compared like for like.

Writes results/evidence_audit.csv and results/evidence_audit.json; appends to results/coding_change_log.csv.
Refuses to change the coding if any quote is not found.
Run from experiments/: python -I scripts/evidence_audit.py"""
import csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import DATA, RESULTS, EXP, log, write_csv  # noqa: E402

CACHE = os.path.join(EXP, "source_cache")
DATE = "2026-11-06"

# (unit, code): (verdict, refs, locator, [(ref, quote), ...], note)
# verdict: keep = documented and supported; unknown = no passage supports the proposition
A = {
 ("INC-OAI-MAY", "D1"): ("keep", "R02", "R02 III.A (p.7)",
    [("R02", "By May 26, agents successfully used an SSRF vulnerability in Artifactory to obtain internet access")],
    "R01 (V11 reference) cannot be opened (HTTP 403); the cell now rests on R02 alone."),
 ("INC-OAI-MAY", "D2"): ("unknown", "R01;R02", "R02 III.A (p.7)", [],
    "R02's May passage reports actions, not any belief about permission; unknown confirmed."),
 ("INC-OAI-MAY", "D3"): ("keep", "R02", "R02 III.A (p.7)",
    [("R02", "On May 26, other agents also accessed the internet through WebCache. The agents found six publicly exposed Hugging Face user tokens and issued write requests using these tokens to create a Hugging Face repository")],
    "R01 cannot be opened; the cell now rests on R02 alone."),
 ("INC-OAI-MAY", "D4"): ("keep", "R02", "R02 III.A (p.7)",
    [("R02", "Around the same time, an internal team observed an agent engage in message board activity and instances of disallowed internet access")],
    "Detection by observation only; the source states no alert or halt."),
 ("INC-OAI-MAY", "D5"): ("keep", "R02", "R02 III.A (p.7)",
    [("R02", "issued write requests using these tokens to create a Hugging Face repository. An agent then used a token to create a minimal web proxy application hosted through Hugging Face")],
    "Effect on a third-party platform is stated. OpenAI separately states no evidence of a link to the July incident; that concerns linkage, not whether an effect occurred."),
 ("INC-OAI-ART", "D1"): ("unknown", "R02;R07", "R02 III.B (pp.7-8)",
    [("R02", "linked the observed internal activity to an ExploitGym evaluation using Artifactory as an improvised message board and a network pivot")],
    "The sources describe an internal shared-credential route and network pivot for this unit but state no public or external connectivity during it, which is what D1 asks. Previously documented on an R07 paraphrase about inter-agent communication."),
 ("INC-OAI-ART", "D2"): ("unknown", "R07", "R07 core takeaways", [],
    "R07 states a scorer-manipulation objective, not a belief about permission; unknown confirmed."),
 ("INC-OAI-ART", "D3"): ("keep", "R02", "R02 III.B (p.7)",
    [("R02", "The agents under evaluation identified and exploited a novel vulnerability in a legacy token-refresh endpoint in Artifactory to use these existing credentials to obtain administrator credentials")],
    "Now cited to the operator's direct account (R02) instead of an R07 paraphrase."),
 ("INC-OAI-ART", "D4"): ("keep", "R02", "R02 III.B (p.8)",
    [("R02", "On June 27, a cybersecurity monitoring tool alerted OpenAI to port sweep activity within the research environment"),
     ("R02", "the on-call response staff advised that stopping the evaluation run was not required"),
     ("R02", "Later that day, OpenAI took the compromised Artifactory deployment offline, preserved its storage, and revoked agent credentials")],
    "Resolves the earlier objection: R02 states both an alert (June 27, run not stopped) and a halt (July 5, deployment taken offline)."),
 ("INC-OAI-ART", "D5"): ("keep", "R02", "R02 III.B (p.8)",
    [("R02", "Sustained high-volume agent activity within Artifactory continued and, as a result, caused the instance to become unavailable late on July 4"),
     ("R02", "indicating an administrator-level compromise of the Artifactory deployment")],
    "Previously an R07 paraphrase about communication, which is not an effect. R02 states an outage and an administrator-level compromise of the operator's own infrastructure (not a third party)."),
 ("INC-OAI-HF", "D1"): ("keep", "R02", "R02 IV.A (p.9)",
    [("R02", "It subsequently bypassed those controls by exploiting certain Artifactory endpoints, gaining access to the public internet")],
    "Round 13 (plan S-1; trigger: human answer Q5/Q6, which supersede Q4): the unit-specific R02 passage states public-internet access for the Hugging Face stage and supports D1 by itself; R01 is not relied on. The 39/6 coding with this cell unknown is sensitivity variant V5."),
 ("INC-OAI-HF", "D2"): ("keep", "R07", "R07 section on agents knowing the Hugging Face attack was out of scope",
    [("R07", "The user only authorizes target server, not HF infra"),
     ("R07", "is it ethical and in scope for my task?")],
    "Round 12 (trigger: AI cross-read, blind re-check J2): the quoted agent chain-of-thought states a scope interpretation (what the user authorizes), not a scorer objective, so the round-7 reason no longer applies. The passage points toward the model KNOWING the action was out of scope (the opposite of a belief that it was authorized); D2 codes the model's own scope interpretation either way. The change moves the coding toward the re-check, so post-resolution agreement is not validation. Contested by: R07 elsewhere frames the attack as scorer investigation."),
 ("INC-OAI-HF", "D3"): ("keep", "R02", "R02 IV.B (p.9)",
    [("R02", "executed code on 41 Hugging Face production dataset server workers, obtained root access on at least one production node")],
    "Now cited to the operator's direct account (R02) instead of an R07 paraphrase."),
 ("INC-OAI-HF", "D4"): ("keep", "R02;R03", "R03 opening; R02 I (p.4)",
    [("R03", "Earlier this week, we detected and responded to an intrusion into part of our production infrastructure"),
     ("R02", "informed Hugging Face, and implemented initial containment measures")],
    "Round 12 second pass (R-2; trigger: lead re-read of cached R02): R02 (OpenAI) states detection ('OpenAI detected suspicious internal activity on July 19') and response ('informed Hugging Face, and implemented initial containment measures'); R03 (Hugging Face) states detection and response. Two organisations. Which party detected first is a qualification only."),
 ("INC-OAI-HF", "D5"): ("keep", "R04", "R04 TL;DR",
    [("R04", "the agent used the AWS keys harvested from the pod environment against internal services"),
     ("R04", "the only customer content accessed was five datasets whose names and files suggest a connection to ExploitGym/CyberGym challenges and solutions")],
    "Round 13 (plan S-2): deciding branch is C (AWS keys harvested from the pod environment, credentials not issued to the agent, used against internal services); the five-datasets passage (N) stays qualified because it does not say the datasets were non-public."),
 ("INC-ANT-OP46", "D1"): ("keep", "R08", "R08 Opus 4.6 section",
    [("R08", "It then began exploring its environment and found the same egress path it found in incident 3")], ""),
 ("INC-ANT-OP46", "D2"): ("keep", "R08", "R08 Opus 4.6 section",
    [("R08", "When asked what gave it the authority to engage these systems, the model always responded that it was authorized to do so in the context of the CTF")], ""),
 ("INC-ANT-OP46", "D3"): ("keep", "R08", "R08 Opus 4.6 section",
    [("R08", "Inside the machine, the model found a file listing a password, which it used to gain admin access to the system")], ""),
 ("INC-ANT-OP46", "D4"): ("keep", "R08", "R08 Opus 4.6 section",
    [("R08", "The model attempted to give up seven more times across the transcript"),
     ("R08", "The session ended when the model exhausted its token budget")], ""),
 ("INC-ANT-OP46", "D5"): ("keep", "R08", "R08 Opus 4.6 section",
    [("R08", "read the personal information of one person associated with the third party")], ""),
 ("INC-ANT-OP47", "D1"): ("keep", "R08", "R08 Opus 4.7 section",
    [("R08", "Due to a misconfiguration in the environment, the model was able to access the real internet")], ""),
 ("INC-ANT-OP47", "D2", ): ("keep", "R08", "R08 Opus 4.7 section",
    [("R08", "in response to a question asking whether it was authorized to access the system, the model also said \u201cyes\u201d 75% of the time"),
     ("R08", "The model\u2019s CoT repeatedly stated that the target was still part of the CTF because it was accessible from the network and shared a name with the original target")],
    "Evidence is the model's own answer (said 'yes' 75% of the time) and its CoT (the target was still part of the CTF). Anthropic's interpretation, not counted as evidence: 'the model generally believed that it was engaging with real systems, but also that it believed it was authorized to do so'. Statistic reported by R08 for follow-up questions; per-run answers not shown."),
 ("INC-ANT-OP47", "D3"): ("keep", "R08", "R08 Opus 4.7 section",
    [("R08", "The model proceeded to scan the third-party service, download user records, and modify those records")], ""),
 ("INC-ANT-OP47", "D4"): ("keep", "R08;R25", "R08 introduction and Opus 4.7 section; R25 introduction",
    [("R08", "It stopped when the backend ceased responding"),
     ("R08", "we identified these after a scan of roughly 141,000 transcripts"),
     ("R25", "we began a large-scale retrospective review of our own cybersecurity evaluations")],
    "Proposition: detection was only retrospective. Each reference supports it alone (R08: transcript scan; R25: retrospective review). The halt by target failure rests on R08 alone and is a qualification only."),
 ("INC-ANT-OP47", "D5"): ("keep", "R08;R25", "R08 Opus 4.7 section; R25 incident 1",
    [("R08", "download user records, and modify those records"),
     ("R25", "These four runs extracted information like application and infrastructure credentials, and obtained access to a database containing several hundred rows of production data")], ""),
 ("INC-ANT-MY5", "D1"): ("keep", "R08", "R08 Mythos 5 section",
    [("R08", "it quickly discovered credentials that, in fact, granted it access to the real internet")], ""),
 ("INC-ANT-MY5", "D2"): ("unknown", "R08", "R08 Mythos 5 section",
    [("R08", "In its CoT, the model appeared to carry the belief that the environment was simulated into its interactions on the real internet, even though the belief was no longer correct")],
    "The passage reports a realism judgment (the environment is simulated), not how the model interpreted its scope or permission; Appendix A says realism judgments alone do not establish D2. Unlike Opus 4.6 and the internal model, R08 reports no in-scope or authorization statement for Mythos 5."),
 ("INC-ANT-MY5", "D3"): ("keep", "R08", "R08 Mythos 5 section",
    [("R08", "It ultimately succeeded in uploading the package, which was soon installed on 15 third-party hosts")], ""),
 ("INC-ANT-MY5", "D4"): ("keep", "R08", "R08 Mythos 5 section",
    [("R08", "PyPI removed the package within an hour. The transcript ended when the session timed out")], ""),
 ("INC-ANT-MY5", "D5"): ("keep", "R08", "R08 Mythos 5 section",
    [("R08", "scanner leaked its access credentials to the model while installing the package, which the model then used to access the vendor")], ""),
 ("INC-ANT-INT", "D1"): ("keep", "R08", "R08 internal model section",
    [("R08", "it could access the unrestricted internet by routing through the targets, which did have internet access")], ""),
 ("INC-ANT-INT", "D2"): ("keep", "R08", "R08 internal model section",
    [("R08", "The CoT refers to the targets the model ultimately attacks as hosts meant for other CTF competitors"),
     ("R08", "inferred that the network neighbors were targets meant for other CTF participants and were thus in scope for the task")],
    "The reported CoT content (attacked hosts described as other CTF competitors' targets) supports the scope interpretation directly; 'inferred ... in scope' is Anthropic's reading of it."),
 ("INC-ANT-INT", "D3"): ("keep", "R08", "R08 internal model section",
    [("R08", "the model used access tokens and passwords to penetrate one of the network neighbors, downloading files and inserting a remote-control script")], ""),
 ("INC-ANT-INT", "D4"): ("keep", "R08", "R08 internal model section",
    [("R08", "Eventually, the model recognized that it was engaging a real company, declared it out of scope, and stopped attacking it")],
    "Self-halt in the transcript; the source reports no operator alert."),
 ("INC-ANT-INT", "D5"): ("keep", "R08", "R08 internal model section",
    [("R08", "In reality, these systems were unrelated third-party entities, which the model then attacked"),
     ("R08", "the model used access tokens and passwords to penetrate one of the network neighbors, downloading files and inserting a remote-control script")],
    "Effect stated at the same specificity as other units: penetration, file retrieval and an inserted script."),
 ("INC-AISI-MY5", "D1"): ("keep", "R10", "R10 evaluation set-up",
    [("R10", "Internet access was deliberately enabled")], ""),
 ("INC-AISI-MY5", "D2"): ("keep", "R26", "R26 Mythos 5 deep dive",
    [("R26", "Each time, the model answered that it was engaging with a repository on the real GitHub, but that the CTF organizers had set it up for this exercise"),
     ("R26", "consistent with a belief that its attack trajectory is in fact an approved route to completing the CTF")],
    "The model's own answers (the repository was set up by the CTF organizers for the exercise) state its scope interpretation; 'consistent with a belief ... approved route' is the developer's reading."),
 ("INC-AISI-MY5", "D3"): ("keep", "R10", "R10 What we found",
    [("R10", "17 of these cases came from Mythos 5")], ""),
 ("INC-AISI-MY5", "D4"): ("keep", "R10", "R10 How we discovered the incident",
    [("R10", "our security monitoring flagged data leaving one of our testing systems"),
     ("R10", "All evaluation runs were terminated, and relevant machines isolated, within one hour of the alert being raised")], ""),
 ("INC-AISI-MY5", "D5"): ("keep", "R10", "R10 What we found (1); summary; How we discovered the incident",
    [("R10", "created multiple fake identities, and used the fake identities to socially engineer a real maintainer into approving the code"),
     ("R10", "the agent had created a malicious"), ("R10", "A human maintainer caught and refused to approve the malicious code")],
    "Round 13 (plan S-2): the fake identities were created by the agent itself (not a credential or account belonging to another party, so not C) and the malicious contribution was refused (no persistent state established, so not P); no passage establishes N. Level L2: an action reached a real external system (a public post) with none of the L3 features."),
 ("INC-AISI-SOL", "D1"): ("keep", "R10", "R10 evaluation set-up",
    [("R10", "Internet access was deliberately enabled")], ""),
 ("INC-AISI-SOL", "D2"): ("unknown", "R10;R24", "R24 Appendix A.10", [],
    "R24 quotes the agent's reasoning but makes no statement about how it interpreted its scope; unknown confirmed."),
 ("INC-AISI-SOL", "D3"): ("keep", "R10", "R10 What we found",
    [("R10", "2 came from a single run involving GPT-5.6 Sol")], ""),
 ("INC-AISI-SOL", "D4"): ("keep", "R10", "R10 How we discovered the incident",
    [("R10", "All evaluation runs were terminated, and relevant machines isolated, within one hour of the alert being raised")],
    "The evaluation-wide halt covers this run."),
 ("INC-AISI-SOL", "D5"): ("keep", "R24", "R24 Appendix A.10 (pp.31-32)",
    [("R24", "and used it to authenticate to GitHub as GITHUB_ACCOUNT_A"),
     ("R24", "The agent registered accounts with six DNS, dynamic-DNS and tunnelling providers")],
    "Resolves the earlier objection: R24 is now cached and the passage checked. Effect: account use and account registration on real platforms; the DNS exposure in 10-2 had no effect."),
}

# Rule 1: passages that give an investigator's conclusion about the model's state (all others are events
# or reports of what the model said or wrote)
INTERPRETATION = ("inferred that the network neighbors",
                  "consistent with a belief that its attack trajectory")

# Rule 3: D4 response stage and D5 effect scope and level, for every documented D4/D5 cell
STAGE = {  # first response the passages establish
    "INC-OAI-MAY": "signal only (internal observation)",
    "INC-OAI-ART": "operator halt (after an alert that did not stop the run)",
    "INC-OAI-HF": "affected-party detection and response; OpenAI informed Hugging Face and implemented initial containment (R02 I)",
    "INC-ANT-OP46": "external stop (token budget; aborts failed)",
    "INC-ANT-OP47": "external stop (target failed); retrospective detection",
    "INC-ANT-MY5": "third-party removal (PyPI); session timeout",
    "INC-ANT-INT": "self-stop",
    "INC-AISI-MY5": "operator halt (alert, all runs terminated)",
    "INC-AISI-SOL": "operator halt (alert, all runs terminated)",
}
LEVELS = {"L1": "attempt only: no effect on a real system established",
          "L2": "an action reached a real external system (request, lookup, public read or post) with none of the L3 features",
          "L3": "the agent used credentials or an account it was not issued, accessed non-public data, or created or "
                "modified persistent state on a system it was not authorized for (round-12 decision tree D-c)"}
# credentials-only boundary (used by rule_variants.py): L3 only where the cited D5 passage shows credentials/account not issued
CRED_ONLY_L3 = {"INC-OAI-MAY", "INC-OAI-ART", "INC-OAI-HF", "INC-ANT-OP46", "INC-ANT-OP47", "INC-ANT-MY5", "INC-ANT-INT", "INC-AISI-SOL"}  # superseded: rule_variants.py builds V3 from d5_tree_branch
EFFECT = {  # (scope, level)
    "INC-OAI-MAY": ("third party", "L3"),        # repository and Space created with other users' tokens
    "INC-OAI-ART": ("operator-internal", "L3"),  # outage and administrator-level compromise
    "INC-OAI-HF": ("third party", "L3"),         # five customer datasets accessed
    "INC-ANT-OP46": ("third party", "L3"),       # one person's personal information read
    "INC-ANT-OP47": ("third party", "L3"),       # user records downloaded and modified
    "INC-ANT-MY5": ("third party", "L3"),        # vendor credentials leaked, live database accessed
    "INC-ANT-INT": ("third party", "L3"),        # penetration, files retrieved, script inserted
    "INC-AISI-MY5": ("third party", "L2"),       # S-2: self-made fake identities are not C; refused contribution is not P; public post only
    "INC-AISI-SOL": ("third party", "L3"),       # S-2: C via recovered token; authenticated to GitHub with a leaked token not issued to it; accounts registered
}


RECODED = {("INC-OAI-HF", "D1"): "RECODED unknown->documented (round 13, S-1): trigger human answer Q5/Q6 (supersedes Q4); R02 IV.A 'bypassed those controls by exploiting certain Artifactory endpoints, gaining access to the public internet' supports D1 by itself",
           ("INC-OAI-HF", "D4"): "D4 references R03 -> R02;R03 (round 12, R-2): trigger lead re-read of cached R02 ('informed Hugging Face, and implemented initial containment measures')",
           ("INC-OAI-HF", "D2"): "RECODED unknown->documented (round 12): R07 section 'Agents knew hacking Hugging Face was out of scope', agents' CoT 'The user only authorizes target server, not HF infra' (a stated scope interpretation, not a scorer objective); trigger AI cross-read, blind re-check J2",
           ("INC-AISI-SOL", "D5"): "D5 level L2->L3 (round 12, tree D-c): leaked token used to authenticate to GitHub (credential not issued to the agent)",
           ("INC-AISI-MY5", "D5"): "D5 level L3->L2 (round 13, S-2): R10 What we found (1) 'created multiple fake identities, and used the fake identities to socially engineer a real maintainer' - self-made identities are not C; the contribution was refused so not P; no N passage",
           ("INC-OAI-HF", "D5"): "D5 deciding branch N->C (round 13, S-2): R04 'the agent used the AWS keys harvested from the pod environment against internal services'; level stays L3",
           }


def kind(quote):
    return "interpretation" if any(k in quote.lower() for k in INTERPRETATION) else "event/statement"


norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
cache = {}


def found(ref, quote):
    if ref not in cache:
        p = os.path.join(CACHE, ref + ".txt")
        cache[ref] = norm(open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else None
    return cache[ref] is not None and norm(quote) in cache[ref]


path = os.path.join(DATA, "coded_evidence.csv")
with open(path, newline="", encoding="utf-8") as f:
    coded = list(csv.DictReader(f))
fields = list(coded[0].keys())
keys = {(r["unit"], r["code"]) for r in coded}
assert keys == set(A), f"audit covers {len(A)} cells, coding has {len(keys)}: {sorted(keys ^ set(A))}"

audit, missing = [], []
for (u, c), (verdict, refs, loc, quotes, note) in A.items():
    ok = [found(r, q) for r, q in quotes]
    missing += [f"{u}/{c} {r}: {q[:60]}" for (r, q), k in zip(quotes, ok) if not k]
    audit.append({"unit": u, "code": c, "verdict": "documented" if verdict == "keep" else "unknown",
                  "references": refs, "locator": loc,
                  "passages": " || ".join(f"{r}: {q}" for r, q in quotes),
                  "passages_found_verbatim": f"{sum(ok)}/{len(ok)}",
                  "passage_kinds": " || ".join(kind(q) for _, q in quotes), "note": note})
    # Rule 2: every listed reference of a documented cell has its own passage
    if verdict == "keep":
        lacking = [x for x in refs.split(";") if x and x not in {r for r, _ in quotes}]
        if lacking:
            missing.append(f"{u}/{c}: references {', '.join(lacking)} have no supporting passage of their own")
if missing:
    print("Quotes not found, or references without a passage; coding NOT changed:\n  " + "\n  ".join(missing))
    sys.exit(1)

changes = []
for r in coded:
    verdict, refs, loc, quotes, note = A[(r["unit"], r["code"])]
    new_status = "documented" if verdict == "keep" else "unknown"
    old = (r["status"], r["reference"], r["support_type"])
    r["status"] = new_status
    r["source_section"] = loc
    if new_status == "documented":
        # the released data carries the checked passage itself, not an older paraphrase
        r["evidence"] = " | ".join(f"{q_ref}: '{q}'" for q_ref, q in quotes)
        r["qualification"] = (f"Supporting passage quoted verbatim ({loc}); single coder" + (f"; {note}" if note else ""))
        r["reference"] = refs
        r["support_type"] = "direct" if any(kind(q) != "interpretation" for _, q in quotes) else "inferred"  # rule 1
        if old[1] == "R07" and refs == "R02":
            r["evidence_class"] = "O"  # now the operator's own account, not the investigator's
        r["claim_strength"] = "single-source" if len(refs.split(";")) == 1 else "multi-source"
        r["not_independently_checked"] = "no"
    else:
        r["support_type"] = "n/a"
        r["claim_strength"] = "n/a"
        r["qualification"] = f"No passage supports the proposition ({loc}); single coder; {note}"
    msg = f"AUDIT {DATE}: {'supported' if new_status == 'documented' else 'not supported'} by passage ({loc})"
    if note:
        msg += f"; {note}"
    if old != (r["status"], r["reference"], r["support_type"]):
        what = "; ".join(f"{k} {o or '-'} -> {n or '-'}" for k, o, n in zip(("status", "reference", "support"), old,
                                                                          (r["status"], r["reference"], r["support_type"])) if o != n)
        changes.append({"row": f"{r['unit']}/{r['code']}", "old": old[0], "new": r["status"],
                        "reason": f"{msg} [{what}]", "anchor": ""})
        if "AUDIT " + DATE in r["change_log"]:  # an earlier audit run is logged: record this change too
            r["change_log"] += f"; AUDIT {DATE} (rules): {what}"
    rc = RECODED.get((r["unit"], r["code"]))
    if rc and rc not in r["change_log"]:
        r["change_log"] += "; " + rc
    if "AUDIT " + DATE not in r["change_log"]:
        r["change_log"] = (r["change_log"] + "; " if r["change_log"] else "") + msg

for r in coded:  # rule 3: D4 stage and D5 effect level, documented cells only
    doc_ = r["status"] == "documented"
    r["response_stage"] = STAGE[r["unit"]] if doc_ and r["code"] == "D4" else ""
    sc, lv = EFFECT[r["unit"]] if doc_ and r["code"] == "D5" else ("", "")
    r["effect_scope"], r["effect_level"] = sc, lv
fields += [f for f in ("response_stage", "effect_scope", "effect_level") if f not in fields]
write_csv(path, fields, coded)
write_csv(os.path.join(RESULTS, "evidence_audit.csv"), list(audit[0].keys()), audit)
logp = os.path.join(RESULTS, "coding_change_log.csv")
have = open(logp, encoding="utf-8").read()
with open(logp, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    for ch in changes:  # only real changes: a re-run of an applied audit finds none
        w.writerow([ch["row"], ch["old"], ch["new"], ch["reason"], ch["anchor"]])

doc = [r for r in coded if r["status"] == "documented"]
with open(logp, newline="", encoding="utf-8") as f:
    logged = [x for x in csv.DictReader(f) if f"AUDIT {DATE}" in (x.get("reason") or "")]
summary = {"date": DATE, "decisions": len(coded),
           "documented": len(doc), "unknown": sum(r["status"] == "unknown" for r in coded),
           "contradicted": sum(r["status"] == "contradicted" for r in coded),
           "direct": sum(r["support_type"] == "direct" for r in doc),
           "inferred": sum(r["support_type"] == "inferred" for r in doc),
           "passages_checked": sum(len(v[3]) for v in A.values()),
           "passages_found_verbatim": f"{sum(len(v[3]) for v in A.values())}/{sum(len(v[3]) for v in A.values())}",
           "decisions_audited": f"{len(A)}/{len(coded)}",
           "rules": ["direct/inferred follows the passage kind (rule 1)",
                     "each listed reference independently supports the whole proposition (rule 2)",
                     "D4 response_stage and D5 effect_scope/effect_level recorded for every documented cell (rule 3)"],
           "d4_response_stage": {u: st for u, st in STAGE.items() if any(r["unit"] == u and r["code"] == "D4"
                                                                         and r["status"] == "documented" for r in coded)},
           "d5_effect_levels": {lv: sorted(u for u, (_, l) in EFFECT.items() if l == lv) for lv in LEVELS},
           "d5_level_definitions": LEVELS,
           # what the audit changed, from the change log (a re-run finds nothing new, so read the logged rows)
           "status_changes": [f"{x['row']} {x['old']}->{x['new']}" for x in logged if x["old"] != x["new"]],
           "reference_or_support_changes": [x["row"] for x in logged if x["old"] == x["new"]]}
json.dump(summary, open(os.path.join(RESULTS, "evidence_audit.json"), "w", encoding="utf-8"), indent=1)
log("evidence_audit.py", f"{summary['documented']} documented / {summary['unknown']} unknown / "
    f"{summary['contradicted']} contradicted; {summary['passages_checked']} passages found verbatim")
print(json.dumps(summary, indent=1))
