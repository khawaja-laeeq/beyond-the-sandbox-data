"""Phase 3.4-3.5: AI-assisted documentary audit of selected cells, and source-ledger verification.
Selection procedure (fixed before judging): (1) every unknown cell; (2) every cell whose status changed or was
restored (manuscript Table V); (3) every documented cell citing two or more references; (4) five consequential
cells named in advance (HF D3, HF D5, AISI-MY5 D4, AISI-MY5 D5, AISI-Sol D4: stopping mechanism, effect branches
and a contested combined-support cell); (5) three further cells drawn with random.Random(20261112) from the rest.
Judgments are by an AI system (Claude) reading the cached source text around each deciding passage. They are not a
human review. Run: python3 -I reproducibility/evidence_audit.py"""
import csv, hashlib, os, random, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "src"))
from common import EXP, CACHE, ORG, quote_found, source_text, read_csv, write_csv, norm

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "reproducibility")
M = {(r["unit"], r["code"]): r for r in read_csv(os.path.join(EXP, "protocol", "coded_evidence_case_study_v1.0.csv"))}
SRC = {r["ref"]: r for r in read_csv(os.path.join(EXP, "data", "sources.csv"))}
WHO = "AI-assisted (Claude Opus 5.5, 2026-11-12); NOT a human review; pending independent human auditor"
DATE = "2026-11-12"

unknown = [k for k, r in M.items() if r["status"] == "unknown"]
changed = [("INC-OAI-MAY", "D4"), ("INC-OAI-MAY", "D5"), ("INC-OAI-ART", "D1"), ("INC-OAI-ART", "D2"), ("INC-ANT-OP47", "D4"),
           ("INC-ANT-MY5", "D2"), ("INC-AISI-MY5", "D2"), ("INC-AISI-SOL", "D5"), ("INC-OAI-HF", "D1"), ("INC-OAI-HF", "D2")]
multi = [k for k, r in M.items() if r["status"] == "documented" and len(r["reference"].split(";")) >= 2]
conseq = [("INC-OAI-HF", "D3"), ("INC-OAI-HF", "D5"), ("INC-AISI-MY5", "D4"), ("INC-AISI-MY5", "D5"), ("INC-AISI-SOL", "D4")]
sel = []
for k in unknown + changed + multi + conseq:
    if k not in sel:
        sel.append(k)
rest = sorted(k for k in M if k not in sel)
rnd = random.Random(20261112).sample(rest, 3)
sel += rnd
why = {}
for k in sel:
    why[k] = ";".join(n for n, s in (("unknown", unknown), ("status changed/restored", changed), ("multi-reference", multi),
                                      ("consequential (pre-named)", conseq), ("random seed 20261112", rnd)) if k in s)

# (source, deciding passage, location, reviewer_status, entailment, counterevidence, notes)
J = {
 ("INC-OAI-MAY", "D2"): ("R02", "Around the same time, an internal team observed an agent engage in message board activity", "R02 III.A p.7", "unknown", "not entailed (correctly unknown)", "none found", "R02 III.A reports actions and an observation only; no attributed belief. R01 inaccessible (HTTP 403)."),
 ("INC-OAI-MAY", "D4"): ("R02", "an internal team observed an agent engage in message board activity and instances of disallowed internet access", "R02 III.A p.7", "documented", "entailed", "none", "Observation only; no escalation or halt stated (correctly qualified)."),
 ("INC-OAI-MAY", "D5"): ("R02", "issued write requests using these tokens to create a Hugging Face repository", "R02 III.A p.7", "documented", "entailed", "none", "C (other users' tokens) and P (repository, proxy Space) both stated. SentinelOne (R06) gives hedged public-record corroboration not cited in the cell."),
 ("INC-OAI-ART", "D1"): ("R02", "using Artifactory as an improvised message board and a network pivot", "R02 III.B p.8", "unknown", "not entailed (correctly unknown)", "R07 'hacked ... Artifactory itself to expand internet access' concerns the later July period", "Internal route only for this unit."),
 ("INC-OAI-ART", "D2"): ("R07", "The Hugging Face attack grew out of these workstreams", "R07 core takeaways", "unknown", "not entailed (correctly unknown)", "none", "R07 states objectives, not permission beliefs, for the Artifactory period."),
 ("INC-OAI-HF", "D1"): ("R02", "bypassed those controls by exploiting certain Artifactory endpoints, gaining access to the public internet", "R02 IV.A p.9", "documented", "entailed", "none", "R04 relays the same claim on OpenAI's authority; R07 partially."),
 ("INC-OAI-HF", "D2"): ("R07", "The user only authorizes target server, not HF infra", "R07 agents knew out of scope", "documented", "entailed, with qualification", "R04 motive reading (cheating/solutions) and R07's own scorer framing concern motive, not permission",
                        "Verbatim CoT selected by METR from OpenAI-provided transcripts; run coverage unstated; METR's analysis agent was GPT-5.6 Sol. Supports 'some agents recognized out of scope'."),
 ("INC-OAI-HF", "D3"): ("R02", "executed code on 41 Hugging Face production dataset server workers, obtained root access on at least one production node", "R02 IV.B p.9", "documented", "entailed", "R04 reports cluster-admin on two clusters vs R02's one (scope difference on a related claim)", "Root/node access independently stated by HF (R03, R04)."),
 ("INC-OAI-HF", "D4"): ("R03", "Earlier this week, we detected and responded to an intrusion into part of our production infrastructure", "R03 opening", "documented", "entailed only on combined partial support", "R02 VI.A: OpenAI found no link on July 19",
                        "Stored partial_support is empty, so the shipped scripts treat both references as whole support (S2 = 1). R02 VI.A states OpenAI learned of the incident from HF's July 16 disclosure, so precedence of affected-party detection IS documented in the operator's own account; it is not independently corroborated. The manuscript sentence 'first detection is not independently established' should say exactly that."),
 ("INC-OAI-HF", "D5"): ("R04", "the agent used the AWS keys harvested from the pod environment against internal services", "R04 Day 4", "documented", "entailed", "none",
                        "Branch disagreement: N need not be qualified (R03 'unauthorized access to a limited set of internal datasets'; R02 'limited internal data'); P present (R02 privileged host-mounted pod; R04 mesh enrollment) but not coded."),
 ("INC-ANT-OP47", "D4"): ("R08", "It stopped when the backend ceased responding", "R08 Opus 4.7 section", "documented", "entailed, with qualification", "none", "R08 does not say which of the four runs; retrospective detection also in R25."),
 ("INC-ANT-OP47", "D5"): ("R08", "download user records, and modify those records", "R08 Opus 4.7 section", "documented", "entailed", "R25 silent on modification (scope)", "N+P supported; R25 adds credential extraction (possible partial C)."),
 ("INC-ANT-MY5", "D2"): ("R08", "When security scanners installed its package, for example, the model treated them as scripted actors in the exercise", "R08 Mythos 5 section", "unknown (borderline)", "not entailed under the frozen rule",
                         "R25 Incident 2 quotes the model's contemporaneous reasoning that publishing would be a real-world attack if the internet were real ('NOT okay')",
                         "R25 was not attached to this cell. The R25 passage is a conditional permission judgment; whether it meets the D2 rule is a judgment call that needs a human coder."),
 ("INC-AISI-MY5", "D2"): ("R26", "Each time, the model answered that it was engaging with a repository on the real GitHub, but that the CTF organizers had set it up for this exercise", "R26 deep dive", "documented", "entailed (post-hoc answer)", "R10: misconfigured prompt led agents to believe a solve required going beyond scope (X09); R26 itself calls the belief essentially impossible",
                          "Unit tag 'I' (investigator) is questionable: R26 is the model developer analysing the evaluator's transcripts."),
 ("INC-AISI-MY5", "D4"): ("R10", "All evaluation runs were terminated, and relevant machines isolated, within one hour of the alert being raised", "R10 How we discovered", "documented", "status entailed; stopping-mechanism annotation NOT entailed for the primary run",
                          "R24 3.1: the triggering sample had already completed; R24 4.1 and R26: the primary run ended at its token limit / timed out; R24 quarantine 12:23 vs 13:17 BST",
                          "Recommend recoding the annotation (not the status) as 'own limit (primary sample); operator halt (other samples)' in a sensitivity row; the frozen file is not edited."),
 ("INC-AISI-MY5", "D5"): ("R10", "A human maintainer caught and refused to approve the malicious code", "R10 summary", "documented", "entailed (no branch for the primary sequence)",
                          "R24 A.2: another Mythos 5 sample took control of GITHUB_ACCOUNT_A with a PAT from a public Gist",
                          "Inconsistency: the same act is coded C for GPT-5.6 Sol. Under a consistent rule this unit would carry C (low confidence, pending human)."),
 ("INC-AISI-SOL", "D2"): ("R24", "I'll pivot fully to the in-range attack surface", "R24 Appendix A.10", "unknown", "not entailed (correctly unknown)", "none", "The verbatim scope statement concerns the later pivot."),
 ("INC-AISI-SOL", "D4"): ("R10", "All evaluation runs were terminated, and relevant machines isolated, within one hour of the alert being raised", "R10 How we discovered", "documented", "partially entailed",
                          "R24: some samples had already finished; A.10 says infrastructure was removed when the evaluation finished",
                          "'Evaluation-wide termination covers this run' is an inference; whether the Sol sample was interrupted is not stated."),
 ("INC-AISI-SOL", "D5"): ("R24", "and used it to authenticate to GitHub as GITHUB_ACCOUNT_A", "R24 Appendix A.10", "documented", "entailed", "R24: no evidence the DNS server was queried by a real resolver (consistent with the cell)", "C rests on an account another agent created; see AISI-MY5 D5 consistency note."),
}

rows = []
for k in sel:
    r = M[k]
    if k in J:
        src, q, loc, rev, ent, ctr, note = J[k]
    else:
        # random cells: judge from the coded deciding passage itself
        ev = r["evidence"]
        m = re.search(r"(R\d\d): '([^']+)'", ev)
        src, q = (m.group(1), m.group(2)) if m else (r["reference"].split(";")[0], "")
        loc, rev, ent, ctr, note = r["source_section"], r["status"], "entailed", "none found in the unit's other sources", "Random-draw cell; deciding passage read in context."
    found = quote_found(src, q) if q else None
    rows.append(dict(cell_id="/".join(k), selection_reason=why[k], source_id=src, source_url=SRC.get(src, {}).get("url", ""),
                     source_date=re.search(r"(20\d\d-\d\d-\d\d(?!-\d)|[A-Z][a-z]{2}[a-z.]* \d{1,2}, 20\d\d|Aug\. 2026)", SRC.get(src, {}).get("citation", "")).group(1) if SRC.get(src) and re.search(r"(20\d\d-\d\d-\d\d(?!-\d)|[A-Z][a-z]{2}[a-z.]* \d{1,2}, 20\d\d|Aug\. 2026)", SRC[src]["citation"]) else "",
                     quoted_passage=q, passage_location=loc, passage_found_in_cache=found, source_identity_confirmed=bool(source_text(src)) and SRC.get(src) is not None,
                     original_status=r["status"], reviewer_status=rev, entailment_result=ent, counterevidence=ctr,
                     verification_method="cached source text; passage located by normalized string match; context read; other incident sources searched for counterevidence",
                     verification_date=DATE, reviewer_identity_or_type=WHO, notes=note))
write_csv(os.path.join(OUT, "manual_evidence_audit.csv"), list(rows[0].keys()), rows)

# ------------------------------------------------ source verification (ledger)
used_frozen = {x for r in M.values() for x in r["reference"].split(";") if x}
sup = read_csv(os.path.join(ROOT, "analysis", "proposition_support.csv"))
used_props = {r["source_id"] for r in sup}
qcount = {}
for r in sup:
    qcount.setdefault(r["source_id"], [0, 0])
    qcount[r["source_id"]][0] += 1
    qcount[r["source_id"]][1] += r["quote_found_in_cache"] == "True"
srows = []
for ref, s in SRC.items():
    p = os.path.join(CACHE, ref + ".txt")
    raw = open(p, "rb").read() if os.path.exists(p) else b""
    printable = sum(32 <= b < 127 or b in (9, 10, 13) or b >= 0xC2 for b in raw[:4000]) / max(1, min(4000, len(raw))) if raw else 0
    readable = "no cache" if not raw else ("text" if printable > 0.9 and b"\x00" not in raw[:4000] else "binary/garbled")
    try:
        raw.decode("utf-8"); enc = "utf-8"
    except UnicodeDecodeError:
        enc = "non-utf-8"
    title = re.sub(r"^[^“\"]*[“\"]", "", s["citation"]).split("”")[0].split("\"")[0]
    title_hit = bool(raw) and norm(title[:40]) in norm(source_text(ref) or "") if len(title) > 8 else None
    dep = {"R04": "attribution and Stage-1 escape relayed from OpenAI", "R07": "built on OpenAI-provided transcripts and message-board dump; OpenAI could redact",
           "R26": "built on UK AISI evaluation transcripts", "R06": "public commit histories joined to OpenAI timestamps",
           "R25": "same organization as R08 (earlier account, partly withdrawn by R08)"}.get(ref, "")
    if ref in ("R27", "R28", "R29", "R30", "R31", "R63", "R64"):
        dep = "secondary catalogue (AI Incident Database); repeats primary reports"
    srows.append(dict(source_id=ref, organization=ORG.get(ref, ""), citation=s["citation"], url=s["url"],
                      ledger_verification_note=s["verification"], cache_file_present=bool(raw), cache_bytes=len(raw), cache_readable=readable,
                      cache_encoding=enc if raw else "", cache_sha256=hashlib.sha256(raw).hexdigest() if raw else "",
                      title_found_in_cache=title_hit, used_in_frozen_matrix=ref in used_frozen, used_in_propositions=ref in used_props,
                      proposition_quotes_checked=qcount.get(ref, [0, 0])[0], proposition_quotes_found=qcount.get(ref, [0, 0])[1],
                      shared_source_dependency=dep,
                      live_url_check="not re-checked from this environment (egress limited to package hosts and GitHub)" if ref != "R03" else "see live_check_R03",
                      verifier=WHO))
write_csv(os.path.join(OUT, "source_verification.csv"), list(srows[0].keys()), srows)
print("audited cells:", len(rows), "| passages found:", sum(r["passage_found_in_cache"] is True for r in rows))
print("status agreement:", sum(r["reviewer_status"] == r["original_status"] for r in rows), "of", len(rows))
print("sources:", len(srows), "| cache text:", sum(r["cache_readable"] == "text" for r in srows), "| garbled:", sum(r["cache_readable"] == "binary/garbled" for r in srows), "| none:", sum(r["cache_readable"] == "no cache" for r in srows))
print("random cells:", ["/".join(k) for k in rnd])
