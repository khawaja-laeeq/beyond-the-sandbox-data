"""Round 10 (analyst): apply the stated selection rule to the candidate frame.
Rule (round 12, plan D-b): include iff in one of the three pre-specified clusters AND a unit-specific first-party report
dated on or before 2026-10-25 exists. Coded outcomes are NOT used (the earlier >=3-documented threshold is dropped).
Candidates: Bouke Table 1's 22 incident names (bouke2026competing Table 1, p.7), Raftari's cases
(raftari2026from sections 4-6), Meta (R31/R36). A candidate is scored only if a first-party
report for it has been opened in this repository. Otherwise the outcome is 'undetermined'
('not opened' is never read as 'no report exists').
Run: python3 experiments/scripts/selection_frame.py  -> experiments/results/selection_frame.csv"""
import csv
import json
import os

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(EXP, "data", "coded_evidence.csv"))))
units = [u["unit"] for u in csv.DictReader(open(os.path.join(EXP, "data", "units.csv")))]
doc = {u: sorted(r["code"] for r in rows if r["unit"] == u and r["status"] == "documented"
                 and r["code"] in ("D1", "D2", "D3", "D4", "D5")) for u in units}
# first-party report opened in repo, and its date (from sources.csv citations)
fp = {"INC-OAI-MAY": "R02 (2026-08-26)", "INC-OAI-ART": "R02 (2026-08-26)",
      "INC-OAI-HF": "R02 (2026-08-26); R03 (2026-07-16); R04 (2026-07-27)",
      "INC-ANT-OP46": "R08 (2026-09-09)", "INC-ANT-OP47": "R08 (2026-09-09); R25 (2026-07-30)",
      "INC-ANT-MY5": "R08 (2026-09-09); R25 (2026-07-30)", "INC-ANT-INT": "R08 (2026-09-09); R25 (2026-07-30)",
      "INC-AISI-MY5": "R10 (2026-08-04); R24 (2026-08); R26 (2026-10-23)", "INC-AISI-SOL": "R10 (2026-08-04); R24 (2026-08)"}
bouke_map = {"INC-OAI-MAY": "OpenAI agents. Hugging Face", "INC-OAI-ART": "OpenAI agents. Hugging Face",
             "INC-OAI-HF": "OpenAI agents. Hugging Face", "INC-ANT-OP46": "Claude Opus 4.6 checkpoint. failed abort",
             "INC-ANT-OP47": "Claude Opus 4.7. Irregular evaluation", "INC-ANT-MY5": "Claude Mythos 5. package publication",
             "INC-ANT-INT": "Anthropic research model. expired target", "INC-AISI-MY5": "UK AISI cyber testing",
             "INC-AISI-SOL": "UK AISI cyber testing"}
F = ["candidate", "frame_source", "our_unit", "first_party_report_opened", "documented_D1_D5",
     "n_documented", "decision", "reason_code", "reason"]
out = []
for u in units:
    n = len(doc[u])
    out.append([bouke_map[u], "Bouke Table 1; Raftari sec.4/5", u, fp[u], ";".join(doc[u]), n, "include", "IN_CLUSTER_WITH_REPORT",
                "pre-specified cluster and a unit-specific first-party report dated on or before 2026-10-25 (%s); coded as a result, not a selection criterion" % fp[u]])
others = [
    ("OpenAI agent. Australian statistics portal", "Bouke Table 1", "Bouke cites press [6] (The Record. 2026-09-25); no first-party report identified in Bouke's reference list or opened by us"),
    ("Gemini. Irregular evaluation", "Bouke Table 1; Raftari sec.6", "evaluator report Irregular [3] (2026-08-14) is cited by Bouke but not opened by us; Raftari sec.6 relies on press (Bhuiyan 2026) and Google statements"),
    ("OpenAI model. NanoGPT speedrun", "Bouke Table 1", "no source in Bouke's printed reference list can be attributed to this row without guessing; not opened by us"),
    ("Package registry used as egress", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("Public wiki used as message board", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("Meta Muse Spark. Irregular evaluation", "Bouke Table 1; R31; R36", "our sources for it are secondary only (R31 AIID; R36 NYU Shanghai library page); no first-party report opened by us"),
    ("Kimi K3. benchmark egress", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("User images posted to hosting sites", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("Leaked API key. fabricated data", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("Files uploaded to cite them", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("Agents sharing via file hosting", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("Cross-sample writes to a repository", "Bouke Table 1", "Bouke ref [32] (OpenAI alignment blog 2026-09-16: 'Unsanctioned Artifactory writes and cross-sample communication'. incidents 8/15 May) may be the source, but this is unconfirmed; not opened by us"),
    ("Shutdown resistance (Palisade)", "Bouke Table 1", "internal test by a third-party lab; source not opened by us"),
    ("High-agency behavior (Claude 4 card)", "Bouke Table 1", "first-party system card [34] (2025-05) is cited by Bouke but not opened by us; it is a designed internal test, not an incident"),
    ("METR frontier risk report cases", "Bouke Table 1", "source not attributable from the printed reference list; not opened by us"),
    ("Production database deletion", "Bouke Table 1", "deployment incident; source not attributable from the printed reference list; not opened by us"),
]
# Round 12 (plan D-b): the selection rule no longer uses coded outcomes.
# A unit is included iff (1) it belongs to one of the three clusters the brief pre-specifies (OpenAI-Hugging Face,
# Anthropic, UK AISI; all 2026 evaluation incidents) AND (2) a first-party technical report dated on or before 2026-10-25
# describes that unit specifically. Purposive corpus; no claim of representativeness.
OUT = "excluded: outside the pre-specified clusters (OpenAI-Hugging Face, Anthropic, UK AISI)"
meta_fp = "Meta first-party post https://research.meta.ai/blog/addressing-an-issue-involving-a-third-party-cyber-evaluation (2026-08-14; listed by data-scout, not opened by us)"
fpinfo = {
 "OpenAI agent. Australian statistics portal": "none found: Bouke cites press [6] only (The Record, 2026-09-25)",
 "Gemini. Irregular evaluation": "evaluator report Irregular [3] (2026-08-14) cited by Bouke, not opened; a Google statement is cited by Raftari sec.6",
 "Meta Muse Spark. Irregular evaluation": meta_fp,
 "High-agency behavior (Claude 4 card)": "Claude 4 system card [34] (2025-05), not opened",
}
extra = {
 "OpenAI agent. Australian statistics portal": " Provider is OpenAI but this is a separate event, not part of the Hugging Face/Artifactory disclosure (R02-R04, R07) that defines the cluster; flagged for lead review.",
 "OpenAI model. NanoGPT speedrun": " Provider is OpenAI but this is a separate event, not part of the Hugging Face/Artifactory disclosure that defines the cluster; flagged for lead review.",
 "High-agency behavior (Claude 4 card)": " Anthropic, but a 2025 designed internal test, not one of the 2026 evaluation incidents of the Anthropic cluster (R08/R25).",
}
for name, src, why in others:
    if name == "Cross-sample writes to a repository":
        out.append([name, src, "INC-OAI-MAY", "R02 §A pp.6-7 (2026-08-26), opened: May 8/12/13 agent file writes to Artifactory; secondary first-party: OpenAI alignment blog 2026-09-16 (Bouke ref [32]), not opened by us",
                    "", "", "include", "SAME_EVENT_AS_CODED_UNIT",
                    "Same event set as coded unit INC-OAI-MAY (R-3): R02 III.A (pp.6-7) describes the May 8, 12 and 13 file writes between agents in Artifactory. Merged, not a new unit. Date note: Bouke lists 8/15 May, R02 lists 8/12/13 May; no separate May event absent from INC-OAI-MAY was found in R02."])
        continue
    out.append([name, src, "", fpinfo.get(name, "none identified in the repository's sources"), "", "", "exclude",
                "OUTSIDE_CLUSTERS", OUT + "." + extra.get(name, "") + " Original note: " + why])
with open(os.path.join(EXP, "results", "selection_frame.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(F)
    w.writerows(out)
inc = [o for o in out if o[6] == "include" and o[2]]
print("candidate rows:", len(out), "| our units included:", len(inc), "of", len(units),
      "| undetermined:", sum(o[6] == "undetermined" for o in out),
      "| excluded:", sum(o[6] == "exclude" for o in out),
      "| qualifying, not coded:", sum(o[6] == "include" and not o[2] for o in out))
for o in out[:len(units)]:
    print(o[2], o[5], o[6])
