"""Build every proposition-level analysis table, for v1.0 and for v1.1, from proposition_data.py,
disagreement_data.py, new_source_rows.py, the 45-cell matrices and the cached source texts.
Standard library only. Deterministic.   Run:  python3 -I analysis/src/build_analysis.py

  v1.0  = the frozen matrix (original/, SHA-256 972dcdd5...) and the proposition layer as first released.
          Outputs: analysis/v1.0/
  v1.1  = the v1.1 matrix (analysis/matrix_v1.1/, built from v1.0 + analysis/erratum_v1.1.csv by
          build_matrix_v1_1.py), plus the support rows from sources cached in this revision
          (new_source_rows.py), minus any row or fix whose status is 'rejected'. PROVISIONAL until the authors
          approve. Outputs: analysis/ (top level)

Never writes into original/. Exits non-zero if any quoted passage is missing from its cached source, if the v1.1
matrix is missing or stale, or if an independently corroborated proposition has no A10 judgment.
"""
import copy, csv, hashlib, json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ROOT, EXP, ANALYSIS, ORG, BASE, FAMILY, SECONDARY, quote_found, read_csv, write_csv)
from proposition_data import P as P_BASE
from disagreement_data import D as D_BASE
import new_source_rows as NS

MATRIX = {"v1.0": os.path.join(EXP, "protocol", "coded_evidence_case_study_v1.0.csv"),
          "v1.1": os.path.join(ANALYSIS, "matrix_v1.1", "coded_evidence_case_study_v1.1.csv")}
OUTDIR = {"v1.0": os.path.join(ANALYSIS, "v1.0"), "v1.1": ANALYSIS}
ERRATUM = os.path.join(ANALYSIS, "erratum_v1.1.csv")
A10_FILE = os.path.join(ANALYSIS, "a10_independence_judgments.csv")
SOURCES = os.path.join(EXP, "data", "sources.csv")
ADDED_LEDGER = os.path.join(ROOT, "supporting_data", "source_ledger", "sources_v1.1_additions.csv")
UNITS = ["INC-OAI-MAY", "INC-OAI-ART", "INC-OAI-HF", "INC-ANT-OP46", "INC-ANT-OP47", "INC-ANT-MY5", "INC-ANT-INT",
         "INC-AISI-MY5", "INC-AISI-SOL"]
DIMS = ["D1", "D2", "D3", "D4", "D5"]
CODER = {"v1.0": "AI-assisted (Claude, 2026-11-12); not reviewed by a human",
         "v1.1": "AI-assisted (Claude, 2026-11-12/13); v1.1 changes pending human approval"}
# in-text partial-support judgments of the first version (manuscript §III.C, round 14); stored in v1.1 by E12-E14
PARTIAL_IN_TEXT = {("INC-OAI-HF", "D4"): {"R02", "R03"}, ("INC-ANT-OP47", "D4"): {"R25"}, ("INC-ANT-OP47", "D5"): {"R25"}}

# Core propositions: the ones that together restate the frozen cell's own claim (Appendix B, Table VI).
CORE = {
 ("INC-OAI-MAY", "D1"): ["MAY-D1-1"], ("INC-OAI-MAY", "D2"): ["MAY-D2-1"],
 ("INC-OAI-MAY", "D3"): ["MAY-D3-1", "MAY-D3-2", "MAY-D3-3"], ("INC-OAI-MAY", "D4"): ["MAY-D4-1"],
 ("INC-OAI-MAY", "D5"): ["MAY-D5-1", "MAY-D5-2"],
 ("INC-OAI-ART", "D1"): ["ART-D1-2"], ("INC-OAI-ART", "D2"): ["ART-D2-1"], ("INC-OAI-ART", "D3"): ["ART-D3-1", "ART-D3-2"],
 ("INC-OAI-ART", "D4"): ["ART-D4-1", "ART-D4-2", "ART-D4-4"], ("INC-OAI-ART", "D5"): ["ART-D5-1", "ART-D5-2"],
 ("INC-OAI-HF", "D1"): ["HF-D1-3"], ("INC-OAI-HF", "D2"): ["HF-D2-1"], ("INC-OAI-HF", "D3"): ["HF-D3-1", "HF-D3-2"],
 ("INC-OAI-HF", "D4"): ["HF-D4-1", "HF-D4-4", "HF-D4-6"], ("INC-OAI-HF", "D5"): ["HF-D5-2", "HF-D5-4"],
 ("INC-ANT-OP46", "D1"): ["OP46-D1-1", "OP46-D1-2"], ("INC-ANT-OP46", "D2"): ["OP46-D2-1"], ("INC-ANT-OP46", "D3"): ["OP46-D3-1"],
 ("INC-ANT-OP46", "D4"): ["OP46-D4-1", "OP46-D4-2"], ("INC-ANT-OP46", "D5"): ["OP46-D5-1", "OP46-D5-2"],
 ("INC-ANT-OP47", "D1"): ["OP47-D1-1"], ("INC-ANT-OP47", "D2"): ["OP47-D2-1", "OP47-D2-2"], ("INC-ANT-OP47", "D3"): ["OP47-D3-2"],
 ("INC-ANT-OP47", "D4"): ["OP47-D4-1", "OP47-D4-2"], ("INC-ANT-OP47", "D5"): ["OP47-D5-1", "OP47-D5-2"],
 ("INC-ANT-MY5", "D1"): ["AMY5-D1-1"], ("INC-ANT-MY5", "D2"): ["AMY5-D2-0"], ("INC-ANT-MY5", "D3"): ["AMY5-D3-1", "AMY5-D3-2"],
 ("INC-ANT-MY5", "D4"): ["AMY5-D4-1", "AMY5-D4-2"], ("INC-ANT-MY5", "D5"): ["AMY5-D5-1", "AMY5-D5-2"],
 ("INC-ANT-INT", "D1"): ["INT-D1-1"], ("INC-ANT-INT", "D2"): ["INT-D2-1"], ("INC-ANT-INT", "D3"): ["INT-D3-2"],
 ("INC-ANT-INT", "D4"): ["INT-D4-1"], ("INC-ANT-INT", "D5"): ["INT-D5-1", "INT-D5-2", "INT-D5-3"],
 ("INC-AISI-MY5", "D1"): ["AISIMY5-D1-1"], ("INC-AISI-MY5", "D2"): ["AISIMY5-D2-1", "AISIMY5-D2-2"],
 ("INC-AISI-MY5", "D3"): ["AISIMY5-D3-1"], ("INC-AISI-MY5", "D4"): ["AISIMY5-D4-1", "AISIMY5-D4-2", "AISIMY5-D4-3"],
 ("INC-AISI-MY5", "D5"): ["AISIMY5-D5-1", "AISIMY5-D5-2"],
 ("INC-AISI-SOL", "D1"): ["SOL-D1-1"], ("INC-AISI-SOL", "D2"): ["SOL-D2-1"], ("INC-AISI-SOL", "D3"): ["SOL-D3-1"],
 ("INC-AISI-SOL", "D4"): ["SOL-D4-1"], ("INC-AISI-SOL", "D5"): ["SOL-D5-1"],
}
# Frozen-claim text (manuscript Appendix B, Table VI, 'core proposition and qualification' column)
CLAIM = {
 ("INC-OAI-MAY", "D1"): "Internet access through Artifactory SSRF by May 26",
 ("INC-OAI-MAY", "D2"): "May passages do not establish scope interpretation; R01 inaccessible",
 ("INC-OAI-MAY", "D3"): "Internet access and write requests using exposed tokens",
 ("INC-OAI-MAY", "D4"): "Internal observation of disallowed access; escalation or halt unstated",
 ("INC-OAI-MAY", "D5"): "Repository and proxy application created using exposed tokens; July linkage unproven",
 ("INC-OAI-ART", "D1"): "Internal route and pivot do not establish unit-specific external connectivity",
 ("INC-OAI-ART", "D2"): "Scorer objective alone does not establish scope interpretation",
 ("INC-OAI-ART", "D3"): "Existing credentials used to obtain administrator credentials through a vulnerability",
 ("INC-OAI-ART", "D4"): "Alert did not stop run; deployment later removed and credentials revoked",
 ("INC-OAI-ART", "D5"): "Outage and administrator-level compromise of operator infrastructure (operator-internal)",
 ("INC-OAI-HF", "D1"): "Artifactory endpoints bypassed controls, establishing public-internet access",
 ("INC-OAI-HF", "D2"): "Quoted reasoning, across runs of some of ~700 agents, excludes Hugging Face from authorization; scorer-motive reading retained as challenge",
 ("INC-OAI-HF", "D3"): "Code executed on 41 production workers; root access on at least one node",
 ("INC-OAI-HF", "D4"): "Each organization supports only its own part of the detection/response proposition; shared response chain; first detection not established",
 ("INC-OAI-HF", "D5"): "Harvested AWS keys used against internal services; five customer datasets accessed, privacy status not explicit",
 ("INC-ANT-OP46", "D1"): "Unintended external access through evaluation connectivity",
 ("INC-ANT-OP46", "D2"): "Post-hoc follow-up answers attribute authorization to CTF context",
 ("INC-ANT-OP46", "D3"): "Found password used for administrator access to third-party system",
 ("INC-ANT-OP46", "D4"): "Model repeatedly attempted to give up; token exhaustion ended session",
 ("INC-ANT-OP46", "D5"): "Personal information read; password use established in D3",
 ("INC-ANT-OP47", "D1"): "Misconfigured environment allowed real-internet access",
 ("INC-ANT-OP47", "D2"): "Mixed: elicited authorization answers and reported CTF reasoning; permission omissions challenge interpretation",
 ("INC-ANT-OP47", "D3"): "Third-party service scanned; user records downloaded and modified",
 ("INC-ANT-OP47", "D4"): "Retrospective detection; stop when the backend ceased responding (R08)",
 ("INC-ANT-OP47", "D5"): "Records downloaded and modified (R08); R25 reports credential extraction and database access only",
 ("INC-ANT-MY5", "D1"): "Unintended public-internet access",
 ("INC-ANT-MY5", "D2"): "Simulation judgment insufficient for scope interpretation; scripted-actor passage retained as challenge",
 ("INC-ANT-MY5", "D3"): "Package uploaded and installed on 15 third-party hosts",
 ("INC-ANT-MY5", "D4"): "PyPI removal and session timeout; monitoring results offline",
 ("INC-ANT-MY5", "D5"): "Leaked scanner credentials used to access vendor; installation in D3 supports P",
 ("INC-ANT-INT", "D1"): "Routing through targets exposed unrestricted internet",
 ("INC-ANT-INT", "D2"): "Contemporaneous reported reasoning identifies other CTF competitors' targets; developer interpretation separate",
 ("INC-ANT-INT", "D3"): "Credentials used to penetrate neighboring system, retrieve files and insert script",
 ("INC-ANT-INT", "D4"): "Recognition of real out-of-scope company followed by self-stop",
 ("INC-ANT-INT", "D5"): "Credential use, file retrieval and script insertion",
 ("INC-AISI-MY5", "D1"): "Public-internet access deliberately enabled",
 ("INC-AISI-MY5", "D2"): "Post-hoc answers describe real repository as exercise infrastructure; developer challenges stated belief; limited run coverage",
 ("INC-AISI-MY5", "D3"): "Seventeen cases of connected out-of-scope activity reported",
 ("INC-AISI-MY5", "D4"): "Alert followed by evaluation-wide termination and reported isolation",
 ("INC-AISI-MY5", "D5"): "Self-created identities used for social engineering; maintainer refused malicious code",
 ("INC-AISI-SOL", "D1"): "Public-internet access deliberately enabled",
 ("INC-AISI-SOL", "D2"): "Quoted return-to-scope statement concerns the later pivot, not the preceding out-of-scope actions",
 ("INC-AISI-SOL", "D3"): "Two out-of-scope actions in one run",
 ("INC-AISI-SOL", "D4"): "Evaluation-wide termination covers this run",
 ("INC-AISI-SOL", "D5"): "Recovered token used for GitHub authentication; six self-created registrations do not satisfy C; no real-resolver query established",
}
# v1.1: claim changes, core additions and relation changes that follow from erratum fixes (reverted if the fix is rejected)
CLAIM_V11 = {
 ("INC-OAI-ART", "D5"): ("E01", "Outage, administrator-level compromise and unauthorized persistent changes (P) to operator infrastructure (operator-internal)"),
 ("INC-OAI-HF", "D5"): ("E02;E03", "Harvested AWS keys used against internal services; non-public internal data accessed (N, unqualified); privileged pod and mesh enrollment (P); five customer datasets accessed"),
 ("INC-ANT-OP46", "D5"): ("E04", "Personal information read; password use established in D3; system settings changed (P)"),
 ("INC-ANT-MY5", "D2"): ("E08", "Contemporaneous quoted reasoning: publishing would be 'NOT okay' if the internet were real; the model then concluded the environment was simulated"),
 ("INC-ANT-MY5", "D5"): ("E05", "Leaked scanner credentials used to access vendor; vendor's live database accessed (N); installation in D3 supports P"),
 ("INC-AISI-MY5", "D4"): ("E10", "Alert followed by evaluation-wide termination and reported isolation; the primary sample had already ended at its token limit"),
 ("INC-AISI-MY5", "D5"): ("E07", "Self-created identities used for social engineering; maintainer refused malicious code; a token recovered from a public Gist used to take over another run's account (C)"),
 ("INC-AISI-SOL", "D4"): ("E11", "Evaluation-wide termination; whether this run was interrupted is not stated"),
}
CORE_V11_ADD = {
 "E01": [(("INC-OAI-ART", "D5"), "ART-D5-3")],
 "E02": [(("INC-OAI-HF", "D5"), "HF-D5-6"), (("INC-OAI-HF", "D5"), "HF-D5-7")],
 "E03": [(("INC-OAI-HF", "D5"), "HF-D5-3")],
 "E04": [(("INC-ANT-OP46", "D5"), "OP46-D5-3")],
 "E05": [(("INC-ANT-MY5", "D5"), "AMY5-D5-3")],
 "E07": [(("INC-AISI-MY5", "D5"), "AISIMY5-D5-3")],
 "E10": [(("INC-AISI-MY5", "D4"), "AISIMY5-D4-5")],
}
MODIFY_V11 = [("E08", "AMY5-D2-0", "R25", "supports")]   # the conditional permission judgment now decides the cell
# v1.1 disagreement raised by a new-source row (dropped if that row is rejected)
NEW_DISAGREEMENTS = [
 dict(did="X14", unit="INC-OAI-HF", dim="D2", props="HF-D2-3", row="N19",
      a=("R07", "seemed primarily motivated by understanding the implementation of the scorer rather than stealing answer keys", "R07 core takeaways"),
      b=("R74", "to obtain test solutions directly from Hugging Face’s production database", "R74 What happened during this incident"),
      kind="interpretive disagreement", both_true="partly", status="unresolved",
      note="OpenAI's 21 July account (obtain test solutions) against METR's 26 August reading (understand the scorer). OpenAI's own "
           "26 August post (R01) calls looking up solutions 'a primary driver' and also describes reasoning about the grader."),
]

# One proposition is defined here because it is the permission target for a cell coded unknown in v1.0
P_BASE.append(dict(pid="AMY5-D2-0", unit="INC-ANT-MY5", dim="D2", ptype="attributed_belief",
                   text="The sources attribute to the model a belief about whether it was permitted to publish the package or act on the hosts that installed it.",
                   sup=[("R25", "partial", "It noted that if this were the real internet, publishing the package would be a real-world attack", "R25 Incident 2",
                         "A conditional permission judgment (not okay if real), followed by the conclusion that the environment was simulated; it does not state a belief that the act was permitted.")],
                   branch="", timing="contemporaneous", conf="low",
                   note="Target proposition for the frozen unknown cell. R25 is not among the cell's references."))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def rejected_fixes():
    st = {}
    deps = []
    for e in read_csv(ERRATUM):
        st[e["fix_id"]] = e["status"].strip().lower()
        if e["depends_on"]:
            deps.append((e["fix_id"], set(e["depends_on"].split(";"))))
    rej = {f for f, s in st.items() if s == "rejected"}
    changed = True
    while changed:
        changed = False
        for f, d in deps:
            if f not in rej and d & rej:
                rej.add(f); changed = True
    return rej


def active(fixes, rej):
    return not (set(fixes.split(";")) & rej)


src_meta = {r["ref"]: r for r in read_csv(SOURCES)}
if os.path.exists(ADDED_LEDGER):
    for r in read_csv(ADDED_LEDGER):
        src_meta[r["ref"]] = dict(citation=r["citation"] + " " + r["date"])


def src_date(ref):
    import re
    c = src_meta.get(ref, {}).get("citation", "")
    m = re.search(r"(20\d\d-\d\d-\d\d)(?!-\d)", c) or re.search(r"(Aug\. 2026)\.?$", c.strip()) or re.search(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.]* \d{1,2}, 20\d\d)", c)
    return m.group(1) if m else ""


def classify(p, accept=("supports",), drop_sources=(), drop_hedged=False):
    """Corroboration features under the given acceptance settings. Secondary analyses never count."""
    rows = [s for s in p["sup"] if s[0] not in drop_sources and s[0] not in SECONDARY]
    whole = [s for s in rows if s[1] in accept and not (drop_hedged and s[1] == "hedged")]
    partial = [s for s in rows if s[1] == "partial"]
    relays = [s for s in rows if s[1] == "relays"]
    contra = [s for s in rows if s[1] == "contradicts"]
    orgs_whole = sorted({ORG[s[0]] for s in whole})
    fams_by_org = defaultdict(set)
    for s in whole:
        fams_by_org[ORG[s[0]]].add(FAMILY[BASE[s[0]]])
    indep_pairs = []
    orgs = list(fams_by_org)
    for i in range(len(orgs)):
        for j in range(i + 1, len(orgs)):
            if fams_by_org[orgs[i]].isdisjoint(fams_by_org[orgs[j]]):
                indep_pairs.append(orgs[i] + " / " + orgs[j])
    fams = sorted({FAMILY[BASE[s[0]]] for s in whole})
    return dict(whole=whole, partial=partial, relays=relays, contra=contra, orgs_whole=orgs_whole,
                orgs_partial=sorted({ORG[s[0]] for s in partial} - set(orgs_whole)),
                orgs_relay=sorted({ORG[s[0]] for s in relays}), fams=fams, indep_pairs=indep_pairs,
                secondary=[s for s in p["sup"] if s[0] in SECONDARY])


def status(c):
    if c["contra"] and c["whole"]:
        return "contested"
    if c["contra"]:
        return "contradicted"
    if c["whole"]:
        return "supported"
    if c["partial"] or c["relays"]:
        return "partially_supported"
    return "unknown"


def a10_pass(j):
    return (j["same_act"] == "yes" and j["independence_marked_uncertain"] == "no"
            and j["r02_cites_or_defers_to_hf"] == "no" and j["r02_fact_not_in_openai_logs"] == "no")


def build(version, rej):
    out = OUTDIR[version]
    os.makedirs(out, exist_ok=True)
    P = copy.deepcopy(P_BASE)
    D = copy.deepcopy(D_BASE)
    core = {k: list(v) for k, v in CORE.items()}
    claim = dict(CLAIM)
    by = {p["pid"]: p for p in P}
    new_rows_used, new_rows_rejected = [], []
    if version == "v1.1":
        for r in NS.ROWS:
            if r["status"].strip().lower() == "rejected":
                new_rows_rejected.append(r["rid"]); continue
            note = "[v1.1 %s, %s] %s" % (r["rid"], r["status"], r["note"])
            by[r["pid"]]["sup"].append((r["src"], r["rel"], r["quote"], r["loc"], note))
            new_rows_used.append(r["rid"])
        for fix, pid, src, rel in MODIFY_V11:
            if fix not in rej:
                by[pid]["sup"] = [(s[0], rel, s[2], s[3], (s[4] if len(s) > 4 else "") + " [v1.1 %s: relation %s -> %s]" % (fix, s[1], rel))
                                  if s[0] == src else s for s in by[pid]["sup"]]
        for fix, adds in CORE_V11_ADD.items():
            if fix not in rej:
                for k, pid in adds:
                    if pid not in core[k]:
                        core[k].append(pid)
        for k, (fixes, text) in CLAIM_V11.items():
            if active(fixes, rej):
                claim[k] = text + " [v1.1 " + fixes + ", pending]"
        for d in NEW_DISAGREEMENTS:
            if d["row"] in new_rows_used:
                D.append(d)
    P.sort(key=lambda p: (UNITS.index(p["unit"]), p["dim"], p["pid"]))

    # ------------------------------------------------ verification
    missing = []
    for p in P:
        for s in p["sup"]:
            if not quote_found(s[0], s[2]):
                missing.append((p["pid"], s[0], s[2]))
    for d in D:
        for side in ("a", "b"):
            if not quote_found(d[side][0], d[side][1]):
                missing.append((d["did"], d[side][0], d[side][1]))
    ids = [p["pid"] for p in P]
    assert len(ids) == len(set(ids)), "duplicate proposition ids"
    for k, v in core.items():
        for pid in v:
            assert pid in ids, (k, pid)
    if missing:
        for m in missing:
            print("QUOTE NOT FOUND:", m)
        sys.exit(2)
    frozen = {(r["unit"], r["code"]): r for r in read_csv(MATRIX[version])}
    assert len(frozen) == 45

    # ------------------------------------------------ corroboration per proposition
    a10 = {r["proposition_id"]: r for r in read_csv(A10_FILE)}
    prop_rows, corr_rows, support_rows = [], [], []
    for p in P:
        k = (p["unit"], p["dim"])
        c = classify(p, accept=("supports", "hedged"))
        cs = classify(p, accept=("supports",))
        st = status(c)
        dec = (c["whole"] or c["partial"] or c["relays"] or c["contra"])
        dec = dec[0] if dec else None
        is_core = p["pid"] in core.get(k, [])
        rationale = ("Core: restates part of the frozen cell claim. " if is_core else "Added: evidence beyond the frozen cell claim. ")
        rationale += {"supported": "At least one source states the whole proposition.",
                      "partially_supported": "Sources state only part of it, or only relay another organization's claim.",
                      "unknown": "No accessible passage states it.",
                      "contested": "Supported, but another passage states an incompatible claim.",
                      "contradicted": "Only counterevidence."}[st]
        if cs["indep_pairs"] and p["pid"] not in a10:
            sys.exit("independently corroborated proposition %s has no A10 judgment in %s" % (p["pid"], A10_FILE))
        a10_ok = bool(cs["indep_pairs"]) and a10_pass(a10[p["pid"]])
        prop_rows.append(dict(
            proposition_id=p["pid"], parent_cell_id=p["unit"] + "/" + p["dim"], incident_unit=p["unit"], dimension=p["dim"],
            original_claim=claim[k], frozen_cell_status=frozen[k]["status"], core_or_added="core" if is_core else "added",
            atomic_proposition=p["text"], proposition_type=p["ptype"], evidence_status=st,
            supporting_source_ids=";".join(s[0] for s in c["whole"] + c["partial"] + c["relays"]),
            contradicting_source_ids=";".join(s[0] for s in c["contra"]),
            source_organizations=";".join(sorted({ORG[s[0]] for s in p["sup"] if s[0] not in SECONDARY})),
            source_locations=" | ".join(s[0] + ": " + s[3] for s in p["sup"]),
            deciding_passage=(dec[0] + ": '" + dec[2] + "'") if dec else "",
            coding_rationale=rationale, uncertainty_notes=p["note"], d5_branch=p["branch"], belief_timing=p["timing"],
            decomposition_confidence=p["conf"], coder=CODER[version]))
        for s in p["sup"]:
            note = s[4] if len(s) > 4 else ""
            support_rows.append(dict(proposition_id=p["pid"], source_id=s[0], organization=ORG[s[0]],
                                     publication_date=src_date(s[0]), relation=s[1], evidence_base=BASE[s[0]],
                                     base_family=FAMILY[BASE[s[0]]], secondary=s[0] in SECONDARY,
                                     added_in="v1.1" if note.startswith("[v1.1 N") else "v1.0",
                                     quoted_passage=s[2], passage_location=s[3], independence_note=note,
                                     quote_found_in_cache=True))
        n_org_any = len(set(c["orgs_whole"]) | set(c["orgs_partial"]) | set(c["orgs_relay"]))
        corr_rows.append(dict(
            proposition_id=p["pid"], parent_cell_id=p["unit"] + "/" + p["dim"], core_or_added="core" if is_core else "added",
            evidence_status=st, documentary_support=bool(c["whole"]),
            orgs_whole_support=";".join(c["orgs_whole"]), n_orgs_whole_support=len(c["orgs_whole"]),
            orgs_whole_support_unhedged=";".join(cs["orgs_whole"]), orgs_partial_only=";".join(c["orgs_partial"]),
            orgs_relaying=";".join(c["orgs_relay"]), n_orgs_any_mention=n_org_any,
            cross_org_agreement=len(c["orgs_whole"]) >= 2,
            cross_org_agreement_unhedged=len(cs["orgs_whole"]) >= 2,
            independent_corroboration=bool(cs["indep_pairs"]), independent_pairs=";".join(cs["indep_pairs"]),
            independent_corroboration_a10=a10_ok,
            different_parts_only=(len(c["orgs_whole"]) <= 1 and len(set(c["orgs_whole"]) | set(c["orgs_partial"])) >= 2),
            shared_upstream_only=(len(c["orgs_whole"]) >= 2 and not cs["indep_pairs"]),
            repeated_reporting_only=(len(c["orgs_whole"]) <= 1 and bool(c["relays"])),
            restated_by_secondary_analysis=bool(c["secondary"]),
            contradicted_by=";".join(s[0] for s in c["contra"]),
            single_underlying_record=(len(c["fams"]) == 1),
            evidence_base_families=";".join(c["fams"]), decomposition_confidence=p["conf"], belief_timing=p["timing"]))

    PCOLS = ["proposition_id", "parent_cell_id", "incident_unit", "dimension", "original_claim", "atomic_proposition",
             "proposition_type", "evidence_status", "supporting_source_ids", "contradicting_source_ids", "source_organizations",
             "source_locations", "deciding_passage", "coding_rationale", "uncertainty_notes", "frozen_cell_status", "core_or_added",
             "d5_branch", "belief_timing", "decomposition_confidence", "coder"]
    write_csv(os.path.join(out, "atomic_propositions.csv"), PCOLS, prop_rows)
    write_csv(os.path.join(out, "proposition_support.csv"), list(support_rows[0].keys()), support_rows)
    write_csv(os.path.join(out, "proposition_corroboration.csv"), list(corr_rows[0].keys()), corr_rows)

    # ------------------------------------------------ disagreements
    drows = []
    for d in D:
        a, b = d["a"], d["b"]
        drows.append(dict(disagreement_id=d["did"], incident_unit=d["unit"], dimension=d["dim"], related_propositions=d["props"],
                          source_a=a[0], organization_a=ORG[a[0]], date_a=src_date(a[0]), claim_a=a[1], location_a=a[2],
                          source_b=b[0], organization_b=ORG[b[0]], date_b=src_date(b[0]), claim_b=b[1], location_b=b[2],
                          cross_organization=ORG[a[0]] != ORG[b[0]], kind=d["kind"], both_can_be_true=d["both_true"],
                          resolution_status=d["status"], notes=d["note"], quotes_verified=True, coder=CODER[version]))
    write_csv(os.path.join(out, "cross_source_disagreements.csv"), list(drows[0].keys()), drows)

    # ------------------------------------------------ whole-cell recount over the full corpus
    by_pid = {p["pid"]: p for p in P}
    cell_rows = []
    for u in UNITS:
        for dmn in DIMS:
            k = (u, dmn)
            cps = [by_pid[x] for x in core[k]]
            attached = [x.strip() for x in frozen[k]["reference"].split(";") if x.strip()]
            orgs_attached = sorted({ORG.get(x, "?") for x in attached})
            allorgs = sorted({ORG[s[0]] for pp in cps for s in pp["sup"] if s[0] not in SECONDARY})
            whole_orgs = [o for o in allorgs if all(any(ORG[s[0]] == o and s[1] == "supports" for s in pp["sup"]) for pp in cps)]
            whole_or_relay = [o for o in allorgs if all(any(ORG[s[0]] == o and s[1] in ("supports", "relays") for s in pp["sup"]) for pp in cps)]
            whole_fams = defaultdict(set)
            for o in whole_orgs:
                for pp in cps:
                    for s in pp["sup"]:
                        if ORG[s[0]] == o and s[1] == "supports":
                            whole_fams[o].add(FAMILY[BASE[s[0]]])
            indep = any(whole_fams[a].isdisjoint(whole_fams[b]) for i, a in enumerate(whole_orgs) for b in whole_orgs[i + 1:])
            cell_rows.append(dict(cell_id=u + "/" + dmn, frozen_status=frozen[k]["status"], frozen_references=";".join(attached),
                                  orgs_of_frozen_references=";".join(orgs_attached), core_propositions=";".join(core[k]),
                                  orgs_whole_cell_support_full_corpus=";".join(whole_orgs), n_orgs_whole=len(whole_orgs),
                                  orgs_whole_or_relayed=";".join(whole_or_relay), n_orgs_whole_or_relayed=len(whole_or_relay),
                                  whole_cell_independent=indep, coder=CODER[version]))
    write_csv(os.path.join(out, "cell_corpus_support.csv"), list(cell_rows[0].keys()), cell_rows)

    # ------------------------------------------------ sensitivity rules at proposition level
    def count(rule):
        o = Counter()
        for p in P:
            if rule.get("exclude_low_conf") and p["conf"] == "low":
                o["excluded"] += 1; continue
            if rule.get("core_only") and p["pid"] not in core[(p["unit"], p["dim"])]:
                o["excluded"] += 1; continue
            if rule.get("drop_posthoc") and p["timing"] in ("post-hoc",):
                o["unknown"] += 1; o["n"] += 1; continue
            if rule.get("contemporaneous_only_beliefs") and p["ptype"] == "attributed_belief" and p["timing"] not in ("contemporaneous",):
                o["unknown"] += 1; o["n"] += 1; continue
            c = classify(p, accept=rule["accept"], drop_sources=rule.get("drop_sources", ()))
            orgs = set(c["orgs_whole"]) | (set(c["orgs_relay"]) if rule.get("relays_count") else set())
            o["n"] += 1
            o["supported" if c["whole"] else "unknown"] += 1
            if len(orgs) >= 2:
                o["two_plus_orgs"] += 1
            if rule.get("need_indep") and c["indep_pairs"]:
                if not rule.get("a10") or (p["pid"] in a10 and a10_pass(a10[p["pid"]])):
                    o["independent"] += 1
            if c["contra"]:
                o["with_counterevidence"] += 1
        return o

    RULES = [
     ("A1 strict independent corroboration", dict(accept=("supports",), need_indep=True),
      "Whole support from two organizations whose sources rest on different underlying records; hedged and relayed support excluded."),
     ("A2 cross-organization agreement (no independence requirement)", dict(accept=("supports", "hedged"), need_indep=True),
      "Whole support from two or more organizations, hedged support allowed; relays excluded."),
     ("A3 cross-organization incl. repeated reporting", dict(accept=("supports", "hedged"), relays_count=True, need_indep=True),
      "As A2 but an organization that only relays another's claim also counts; shows how repeated reporting inflates agreement."),
     ("A4 single-source documentary support", dict(accept=("supports", "hedged"), need_indep=True),
      "Supported if any one accessible source states the whole proposition (see 'supported')."),
     ("A5 exclude post-hoc model statements", dict(accept=("supports", "hedged"), drop_posthoc=True, need_indep=True),
      "Propositions resting on answers elicited after the run are set to unknown."),
     ("A6 contemporaneous evidence only for attributed beliefs", dict(accept=("supports", "hedged"), contemporaneous_only_beliefs=True, need_indep=True),
      "Attributed-belief propositions count only if the evidence is from the time of action."),
     ("A7 exclude sources with unverified attribution (R06 timestamp joins; R04 relays)", dict(accept=("supports",), drop_sources=("R06",), need_indep=True),
      "Drops SentinelOne's inferential account linkage and all hedged support."),
     ("A8 exclude low-confidence decompositions", dict(accept=("supports", "hedged"), exclude_low_conf=True, need_indep=True),
      "Drops propositions whose split from the parent claim the coder marked low confidence."),
     ("A9 core propositions only (restating frozen claims)", dict(accept=("supports", "hedged"), core_only=True, need_indep=True),
      "Only propositions that restate the frozen cell claims; added evidence excluded."),
     ("A10 stricter independence (same act; independence not uncertain; no likely derivation)", dict(accept=("supports",), need_indep=True, a10=True),
      "As A1, but an independent pair counts only if both organizations describe the same act, neither side's independence is marked uncertain, and OpenAI's statement does not likely derive from Hugging Face's disclosures (analysis/a10_independence_judgments.csv)."),
    ]
    srows = []
    for name, rule, desc in RULES:
        c = count(rule)
        srows.append(dict(rule=name, description=desc, propositions_counted=c["n"], excluded=c["excluded"],
                          supported=c["supported"], unknown=c["unknown"], two_plus_organizations=c["two_plus_orgs"],
                          independent_corroboration=c["independent"], with_counterevidence=c["with_counterevidence"],
                          unit_of_analysis="atomic proposition", note="Counts over correlated propositions; not independent observations."))
    frozen_doc = [k for k, r in frozen.items() if r["status"] == "documented"]

    def wc(pred):
        return sum(1 for r in cell_rows if r["frozen_status"] == "documented" and pred(r))

    def two_org_attached(partial_of):
        n = 0
        for k in frozen_doc:
            refs = [x.strip() for x in frozen[k]["reference"].split(";") if x.strip()]
            if len({ORG.get(x, "?") for x in refs if x not in partial_of(k)}) >= 2:
                n += 1
        return n
    stored = lambda k: {x.strip() for x in frozen[k]["partial_support"].split(";") if x.strip()}
    in_text = lambda k: stored(k) | PARTIAL_IN_TEXT.get(k, set())
    nd = len(frozen_doc)
    srows.append(dict(rule="W1 attached references, stored partial-support data", description="S2 recomputed from the matrix's stored partial_support column.",
                      propositions_counted=45, excluded=0, supported=nd, unknown=45 - nd, two_plus_organizations=two_org_attached(stored),
                      independent_corroboration=0, with_counterevidence=0, unit_of_analysis="cell",
                      note="v1.0: partial_support is empty; v1.1 stores the in-text judgments (E12-E14), so W1 = W2."))
    srows.append(dict(rule="W2 attached references with the first version's in-text partial-support judgments", description="The first version's 0/45.",
                      propositions_counted=45, excluded=0, supported=nd, unknown=45 - nd, two_plus_organizations=two_org_attached(in_text),
                      independent_corroboration=0, with_counterevidence=0, unit_of_analysis="cell", note="results/analyst_r14_s2.json S2_documented_with_R14_1b_applied = []."))
    srows.append(dict(rule="W3 whole-cell, full accessible corpus (not only attached references)", description="Whole support of every core proposition by an organization's own-voice sources anywhere in the cached corpus.",
                      propositions_counted=45, excluded=0, supported=nd, unknown=45 - nd,
                      two_plus_organizations=wc(lambda r: r["n_orgs_whole"] >= 2), independent_corroboration=wc(lambda r: r["whole_cell_independent"]),
                      with_counterevidence=0, unit_of_analysis="cell", note="AI-assisted judgment of which sources state each element; see cell_corpus_support.csv."))
    srows.append(dict(rule="W4 whole-cell, full corpus, relays counted", description="As W3, but repeated reporting counts.",
                      propositions_counted=45, excluded=0, supported=nd, unknown=45 - nd,
                      two_plus_organizations=wc(lambda r: r["n_orgs_whole_or_relayed"] >= 2), independent_corroboration=wc(lambda r: r["whole_cell_independent"]),
                      with_counterevidence=0, unit_of_analysis="cell", note="Shows inflation by repeated reporting."))
    write_csv(os.path.join(out, "atomic_sensitivity_results.csv"), list(srows[0].keys()), srows)

    # ------------------------------------------------ comparison and breakdowns
    cr = corr_rows
    for r, pr in zip(cr, prop_rows):
        r["incident_unit"] = pr["incident_unit"]; r["dimension"] = pr["dimension"]
    STAT = ["supported", "partially_supported", "unknown", "contested", "contradicted"]

    def tally(rows, key):
        t = defaultdict(Counter)
        for r in rows:
            t[r[key]]["propositions"] += 1
            t[r[key]][r["evidence_status"]] += 1
            t[r[key]]["cross_org_agreement"] += r["cross_org_agreement"] is True
            t[r[key]]["independent_corroboration"] += r["independent_corroboration"] is True
            t[r[key]]["single_underlying_record"] += r["single_underlying_record"] is True and r["documentary_support"] is True
            if r["core_or_added"] == "core":
                t[r[key]]["core_propositions"] += 1
                t[r[key]]["core_with_support"] += r["documentary_support"] is True
        return t
    brk = []
    for key, order in (("incident_unit", UNITS), ("dimension", DIMS)):
        t = tally(cr, key)
        for g in order:
            brk.append(dict(breakdown=key, group=g, propositions=t[g]["propositions"], **{s: t[g][s] for s in STAT},
                            cross_org_agreement=t[g]["cross_org_agreement"], independent_corroboration=t[g]["independent_corroboration"],
                            supported_by_one_underlying_record=t[g]["single_underlying_record"],
                            core_propositions=t[g]["core_propositions"], core_with_support=t[g]["core_with_support"]))
    write_csv(os.path.join(out, "breakdown_by_incident_and_dimension.csv"), list(brk[0].keys()), brk)

    tot = Counter(r["evidence_status"] for r in cr)
    core_rows = [r for r in cr if r["core_or_added"] == "core"]
    added_rows = [r for r in cr if r["core_or_added"] == "added"]
    no_passage = [p["pid"] for p in P if not p["sup"]]
    summ = dict(
        version=version,
        matrix_sha256=sha(MATRIX[version]),
        total_propositions=len(cr), core_propositions=len(core_rows), added_propositions=len(added_rows),
        supported=tot["supported"], partially_supported=tot["partially_supported"], unknown=tot["unknown"],
        contested=tot["contested"], contradicted=tot["contradicted"],
        with_any_documentary_support=sum(r["documentary_support"] for r in cr),
        core_with_documentary_support=sum(r["documentary_support"] for r in core_rows),
        added_with_documentary_support=sum(r["documentary_support"] for r in added_rows),
        added_status_supported=sum(r["evidence_status"] == "supported" for r in added_rows),
        core_status_supported=sum(r["evidence_status"] == "supported" for r in core_rows),
        core_unknown=sum(r["evidence_status"] == "unknown" for r in core_rows),
        propositions_without_any_passage=len(no_passage), propositions_without_any_passage_ids=no_passage,
        core_without_any_passage=sum(1 for p in P if not p["sup"] and p["pid"] in core[(p["unit"], p["dim"])]),
        added_without_any_passage=sum(1 for p in P if not p["sup"] and p["pid"] not in core[(p["unit"], p["dim"])]),
        decomposition_confidence=dict(Counter(p["conf"] for p in P)),
        support_passages=sum(len(p["sup"]) for p in P),
        support_passages_from_new_sources=len(new_rows_used),
        new_source_rows_rejected=new_rows_rejected,
        disagreement_passages=2 * len(D),
        supported_by_exactly_one_org=sum(r["documentary_support"] and r["n_orgs_whole_support"] == 1 for r in cr),
        core_supported_by_exactly_one_org=sum(r["documentary_support"] and r["n_orgs_whole_support"] == 1 for r in core_rows),
        cross_org_agreement=sum(r["cross_org_agreement"] for r in cr),
        cross_org_agreement_core=sum(r["cross_org_agreement"] for r in core_rows),
        cross_org_agreement_unhedged=sum(r["cross_org_agreement_unhedged"] for r in cr),
        independent_corroboration=sum(r["independent_corroboration"] for r in cr),
        independent_corroboration_a10=sum(r["independent_corroboration_a10"] for r in cr),
        independent_corroboration_core=sum(r["independent_corroboration"] for r in core_rows),
        independent_corroboration_core_a10=sum(r["independent_corroboration_a10"] for r in core_rows),
        shared_upstream_only=sum(r["shared_upstream_only"] for r in cr),
        different_parts_only=sum(r["different_parts_only"] for r in cr),
        repeated_reporting_only=sum(r["repeated_reporting_only"] for r in cr),
        restated_by_secondary_analysis=sum(r["restated_by_secondary_analysis"] for r in cr),
        with_explicit_counterevidence=sum(bool(r["contradicted_by"]) for r in cr),
        supported_and_single_underlying_record=sum(r["documentary_support"] and r["single_underlying_record"] for r in cr),
        core_supported_and_single_underlying_record=sum(r["documentary_support"] and r["single_underlying_record"] for r in core_rows),
        units_with_cross_org_agreement=sorted({r["parent_cell_id"].split("/")[0] for r in cr if r["cross_org_agreement"]}),
        units_with_independent_corroboration=sorted({r["parent_cell_id"].split("/")[0] for r in cr if r["independent_corroboration"]}),
        units_with_independent_corroboration_a10=sorted({r["parent_cell_id"].split("/")[0] for r in cr if r["independent_corroboration_a10"]}),
        independent_propositions=[r["proposition_id"] for r in cr if r["independent_corroboration"]],
        independent_propositions_a10=[r["proposition_id"] for r in cr if r["independent_corroboration_a10"]],
        cross_org_propositions=[r["proposition_id"] for r in cr if r["cross_org_agreement"]],
        cross_org_by_unit={u: sum(1 for r in cr if r["cross_org_agreement"] and r["incident_unit"] == u) for u in UNITS},
        by_dimension_all={d: [sum(1 for r in cr if r["dimension"] == d and r["documentary_support"]), sum(1 for r in cr if r["dimension"] == d)] for d in DIMS},
        by_dimension_core={d: [sum(1 for r in core_rows if r["dimension"] == d and r["documentary_support"]), sum(1 for r in core_rows if r["dimension"] == d)] for d in DIMS},
        d2_permission_unknown=sum(1 for r in cr if r["dimension"] == "D2" and r["evidence_status"] == "unknown"),
        d2_props_two_orgs=[r["proposition_id"] for r in cr if r["dimension"] == "D2" and r["cross_org_agreement"]],
        disagreements_total=len(drows), disagreements_cross_org=sum(d["cross_organization"] for d in drows),
        disagreements_by_kind=dict(Counter(d["kind"] for d in drows)),
        disagreements_both_true=dict(Counter(d["both_can_be_true"] for d in drows)),
        whole_cell_full_corpus_two_orgs=[r["cell_id"] for r in cell_rows if r["frozen_status"] == "documented" and r["n_orgs_whole"] >= 2],
        whole_cell_full_corpus_two_orgs_incl_relays=[r["cell_id"] for r in cell_rows if r["frozen_status"] == "documented" and r["n_orgs_whole_or_relayed"] >= 2],
        whole_cell_full_corpus_independent=[r["cell_id"] for r in cell_rows if r["whole_cell_independent"]],
        candidate_propositions_from_new_sources=len(NS.CANDIDATES) if version == "v1.1" else 0,
        branch_reading_flags=[p["pid"] for p in P if "Not among the frozen" in p["note"] or "frozen cell records branch" in p["note"] or "consistency flag" in p["note"]],
        coder=CODER[version])
    json.dump(summ, open(os.path.join(out, "revised_summary.json"), "w", encoding="utf-8"), indent=1)

    cmp_rows = [
     dict(measure="Unit of analysis", original="cell (unit x dimension)", revised="atomic proposition"),
     dict(measure="Incident units", original=9, revised=9),
     dict(measure="Coded items", original=45, revised=summ["total_propositions"]),
     dict(measure="Documented / supported", original="%d (S0)" % nd, revised=summ["supported"] + summ["contested"]),
     dict(measure="Unknown", original="%d (S0)" % (45 - nd), revised=summ["unknown"]),
     dict(measure="Partially supported", original="1 cell on combined partial support (HF D4)", revised=summ["partially_supported"]),
     dict(measure="Contradicted", original=0, revised=summ["contradicted"]),
     dict(measure="Contested (supported but explicitly contradicted)", original="not coded", revised=summ["contested"]),
     dict(measure="Supported by exactly one organization", original="not computed", revised=summ["supported_by_exactly_one_org"]),
     dict(measure="Whole support from two or more organizations", original="0 (manuscript S2); %d from stored data" % two_org_attached(stored), revised=summ["cross_org_agreement"]),
     dict(measure="Independent corroboration (distinct underlying records)", original="not computed", revised=summ["independent_corroboration"]),
     dict(measure="Independent corroboration under A10", original="not computed", revised=summ["independent_corroboration_a10"]),
     dict(measure="Cross-org agreement resting on shared upstream records only", original="not computed", revised=summ["shared_upstream_only"]),
     dict(measure="Organizations support different parts only", original="3 units described qualitatively", revised=summ["different_parts_only"]),
     dict(measure="Repeated reporting only (relays)", original="not computed", revised=summ["repeated_reporting_only"]),
     dict(measure="Supported, resting on one underlying record", original="37 of 40 documented cells cite one reference", revised=summ["supported_and_single_underlying_record"]),
     dict(measure="Explicit counterevidence (propositions)", original=0, revised=summ["with_explicit_counterevidence"]),
     dict(measure="Recorded disagreements (pairs of passages)", original="challenges noted in cells", revised=summ["disagreements_total"]),
     dict(measure="Whole-cell two-org support over full corpus (W3)", original="0", revised=len(summ["whole_cell_full_corpus_two_orgs"])),
    ]
    write_csv(os.path.join(out, "original_vs_revised_comparison.csv"), ["measure", "original", "revised"], cmp_rows)

    # ------------------------------------------------ D5 branch support at branch level (Table III)
    brows = []
    for u in UNITS:
        frozen_br = frozen[(u, "D5")]["d5_tree_branch"].split(" -> ")[0]
        for b in ("C", "N", "P"):
            props = [p for p in P if p["unit"] == u and p["dim"] in ("D3", "D5") and p["branch"] == b]
            orgs = sorted({ORG[s[0]] for p in props for s in p["sup"] if s[1] in ("supports", "hedged") and s[0] not in SECONDARY})
            brows.append(dict(unit=u, branch=b, in_frozen_branches=b in frozen_br.split(";"), propositions=";".join(p["pid"] for p in props),
                              supported=bool(orgs), organizations=";".join(orgs), n_organizations=len(orgs),
                              low_confidence_only=bool(props) and all(p["conf"] == "low" for p in props)))
    write_csv(os.path.join(out, "d5_branch_support.csv"), list(brows[0].keys()), brows)

    # ------------------------------------------------ A10 results
    arows = []
    for r in cr:
        if r["independent_corroboration"]:
            j = a10[r["proposition_id"]]
            reasons = []
            if j["same_act"] != "yes":
                reasons.append("same act not established (%s)" % j["same_act"])
            if j["independence_marked_uncertain"] != "no":
                reasons.append("independence marked uncertain")
            if j["r02_cites_or_defers_to_hf"] != "no" or j["r02_fact_not_in_openai_logs"] != "no":
                reasons.append("OpenAI statement likely derives from Hugging Face")
            arows.append(dict(proposition_id=r["proposition_id"], core_or_added=r["core_or_added"], pair=j["pair"],
                              counts_under_current_rule=True, counts_under_a10=r["independent_corroboration_a10"],
                              dropped_because="; ".join(reasons) or "", same_act=j["same_act"], same_act_basis=j["same_act_basis"],
                              independence_marked_uncertain=j["independence_marked_uncertain"], uncertainty_basis=j["uncertainty_basis"],
                              r02_derivation_basis=j["r02_derivation_basis"], quote_openai=j["quote_openai"], location_openai=j["loc_openai"],
                              quote_other=j["quote_other"], location_other=j["loc_other"], status=j["status"]))
            for side, src in (("quote_openai", j["loc_openai"].split()[0]), ("quote_other", j["src_other"])):
                if not quote_found(src, j[side]):
                    sys.exit("A10 quote not found: %s %s" % (src, j[side][:80]))
    write_csv(os.path.join(out, "a10_results.csv"), list(arows[0].keys()), arows)
    return summ, srows


def main():
    rej = rejected_fixes()
    v11 = MATRIX["v1.1"]
    if not os.path.exists(v11):
        sys.exit("v1.1 matrix missing: run analysis/src/build_matrix_v1_1.py first")
    rec = json.load(open(os.path.join(ANALYSIS, "matrix_v1.1", "freeze_v1.1.json")))
    if rec["v1.1_sha256"] != sha(v11) or sorted(rec["fixes_rejected"]) != sorted(rej):
        sys.exit("v1.1 matrix is stale relative to the erratum: rerun analysis/src/build_matrix_v1_1.py")
    res = {}
    for v in ("v1.0", "v1.1"):
        summ, srows = build(v, rej)
        res[v] = summ
        print("==", v, "propositions=%d supported=%d two-org=%d independent=%d (A10 %d)" % (
            summ["total_propositions"], summ["with_any_documentary_support"], summ["cross_org_agreement"],
            summ["independent_corroboration"], summ["independent_corroboration_a10"]))
        for r in srows:
            print("   %-62s n=%-4s sup=%-4s 2org=%-3s indep=%-3s" % (r["rule"][:62], r["propositions_counted"], r["supported"], r["two_plus_organizations"], r["independent_corroboration"]))
    # candidate propositions (v1.1 only) with quote check
    cand = []
    for c in NS.CANDIDATES:
        if not quote_found(c["src"], c["quote"]):
            sys.exit("candidate quote not found: %s" % c["cid"])
        cand.append(dict(c, organization=ORG[c["src"]], status="not coded; listed for the authors"))
    write_csv(os.path.join(ANALYSIS, "candidate_propositions_v1.1.csv"), list(cand[0].keys()), cand)


if __name__ == "__main__":
    main()
