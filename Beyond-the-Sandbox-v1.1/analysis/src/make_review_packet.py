"""Task 10: build HUMAN_REVIEW_PACKET.md from the stored decisions (erratum, new-source rows, A10 judgments,
candidates) plus the hand-written lists below (headline sentences, framing conflicts, automatic number fixes).
Run:  python3 -I analysis/src/make_review_packet.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, ANALYSIS, ORG, read_csv
import new_source_rows as NS

HEADLINES = [  # (where, sentence in the manuscript of 12 Nov, sentence in the single-version manuscript of 13 Nov)
 ("Whole manuscript (13 Nov)", "Two versions reported side by side ('v1.0; v1.1')",
  "One version: the coded data after the erratum and both AI reviews (matrix v1.1). First-version values appear only where the text describes the first version (Sections IV-B, IV-I); every value under both matrices is in analysis/v1.0_vs_v1.1_comparison.csv."),
 ("Abstract, Findings",
  "Only 5 propositions, all about the Hugging Face intrusion, are supported by organizations drawing on different underlying records.",
  "Independent corroboration is rare and confined to the Hugging Face unit: 3–6 propositions, depending on how strictly independence is judged."),
 ("Abstract, Findings",
  "Most cross-organization agreement repeats shared records ..., and 107 of the 129 supported propositions rest on a single organization.",
  "74 of 79 core propositions have documentary support. Two or more organizations state 12 of them, and most of that agreement repeats a shared record."),
 ("Abstract, Findings",
  "Finally, the primary AISI Mythos 5 run ended at its own token limit, not by the operator halt we had coded.",
  "Containment must be read per sample: the primary AISI Mythos 5 run ended at its own token limit, not by the operator halt we had coded."),
 ("Abstract, Implication (new)", "(none)",
  "What the public can establish about an agent incident depends less on how many organizations write about it than on whether the affected party publishes its own records. We derive a disclosure checklist from the gaps."),
 ("Section I 'Why this matters' and 'Main findings in brief'; Section V-D (new)", "(none)",
  "Summaries of existing results and the actions they imply; no new data or claims beyond the findings."),
 ("Section IV-A", "Under the baseline rule S0, 40 of 45 cells are documented ... 5 are unknown.",
  "41 of 45 documented, 4 unknown (E08). The first version's 40/5 is given in Section IV-I."),
 ("Section IV-B", "Independent corroboration is rare and confined to one unit. Five propositions ...",
  "Six propositions under the plain rule (adds the dataset-processing entry point, from R01); three under A10, with the dropped propositions and reasons."),
 ("Section IV-B", "The Anthropic units have no second organization at all: Irregular and the affected companies published nothing in the corpus.",
  "No Anthropic proposition has whole support from a second organization. Irregular's statement adds partial support to five Opus 4.7 propositions. The affected companies published nothing in the corpus."),
 ("Section IV-C", "No permission-belief proposition is supported by more than one organization.",
  "One permission belief (HF-D2-1) is stated by METR and OpenAI, both from OpenAI's transcripts; no permission belief is independently corroborated."),
 ("Section IV-D", "AISI's blog says machines were isolated within one hour of the alert. Its technical report gives isolation at 12:23 or 13:17 BST against an alert at 10:56 BST.",
  "The technical report confirms termination at 11:42 BST, within one hour of the 10:56 BST alert; the discrepancy concerns isolation (12:23 vs 13:17 BST)."),
 ("Section V-B (new paragraph, 13 Nov)", "(none)",
  "By 26 September, OpenAI alone had notified over 100 organizations about activity that met its notification criteria [32]; none has published an account in this corpus. Source: R05, cached; context only, not coded."),
 ("Section VII (Conclusion)",
  "Corrected, two organizations agree on 22 of 138 propositions, but only 5, all about the Hugging Face intrusion, are corroborated from independent records.",
  "Corrected, two organizations agree on 12 of 79 core propositions, mostly on shared records. Independent corroboration is confined to the Hugging Face intrusion and amounts to 3–6 propositions, depending on how strictly independence is judged."),
]
FRAMING = [
 ("Conclusion, Section V-B bullet, Table VII row",
  "'Authorization belief remains single-organization' / 'authorization belief rests on one organization' / 'D2 single-organization'",
  "In v1.1, HF-D2-1 (agents verbalized that attacking Hugging Face was outside authorization) is stated by METR and by OpenAI (R01, new). Both draw on OpenAI's transcripts, so it is shared-record agreement, but 'single-organization' is no longer literally true for one permission-belief proposition. REWORDED at the authors' request (13 Nov): every supported permission belief rests on a single organization's records, none is independently corroborated, and the evidence is mostly post-hoc or paraphrased. (The old Conclusion said 'mostly post-hoc'; at proposition level only 3 of 21 supported D2 beliefs are post-hoc, so 'post-hoc or paraphrased' is the closer phrase, as Section V-B already had it. The data do not record verbatim versus paraphrase; check that most contemporaneous items are the developer's description rather than quotation.) Confirm the wording."),
 ("Section V-B",
  "'The affected party is the only organization in the corpus with its own records of another organization's agent.'",
  "In v1.1, Irregular (R75) describes models' actions in its own evaluation environment, i.e. it has its own records of other organizations' agents, although its statement names no model and gives only partial support. REWORDED at the authors' request (13 Nov): among the organizations that published, the affected party is the only one whose own records give whole support to claims about another organization's agent; Irregular is named, with its limits. Confirm the wording."),
 ("Section IV-C (not a framing sentence; listed for judgment)",
  "'Authorization belief ... mostly post-hoc or paraphrased'",
  "If E08 is approved, a second unit (Anthropic Mythos 5) has contemporaneous verbatim scope reasoning. 'Mostly' still holds by count; the authors may wish to check the emphasis."),
]
AUTO_FIXES = [  # task 1: automatic fixes of counted numbers (data wins), old text -> new text
 ("manuscript III-C", "a decomposition confidence: 107 high, 28 medium, 3 low.", "a decomposition confidence: 119 high, 16 medium, 3 low."),
 ("manuscript VI (Limitations)", "28 splits are medium-confidence and 3 low-confidence.", "16 splits are medium-confidence and 3 low-confidence."),
 ("reviewer_report.md, Soundness", "Decomposing cells involves judgment (28 medium and 3 low confidence splits).", "Decomposing cells involves judgment (16 medium and 3 low confidence splits)."),
 ("task brief", "'63 of 67 [added propositions] are supported'", "Confirmed for status 'supported' (63); 64 if the one contested proposition is counted. Both are now stored (added_status_supported, added_with_documentary_support). No change to data."),
]


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def main():
    L = []
    w = L.append
    w("# Human review packet (revision v1.1)\n")
    w("Generated by `analysis/src/make_review_packet.py` from the stored decision files. **Every item below is an AI decision (Claude, 12–13 November 2026).** At the authors' request, the same AI system re-checked every item against its source on 13 November 2026: it approved most, rejected erratum fix E09 and new-source rows N39, N41 and N49, and changed ten new-source relations to partial. Decisions and reasons are in `analysis/ai_second_review_2026-11-13.csv`. **This second review is not an independent check, and no human has reviewed any item.** The tick boxes below are left for the authors.\n")
    w("**How to decide.** For each item, read the quote at its location. Then:\n")
    w("- **Erratum fixes (A):** set `status` in `analysis/erratum_v1.1.csv` to `approved` or `rejected`, and rerun the pipeline (README). A rejected fix reverts only its own cells.")
    w("- **New-source rows (B):** set `status` in `analysis/src/new_source_rows.py` to `approved` or `rejected`.")
    w("- **A10 judgments (C):** edit the judgment columns in `analysis/a10_independence_judgments.csv`.")
    w("- **Headlines and framing (D, E):** these are text decisions.")
    w("- **Number check (F):** the manuscript's numbers are locked to the data by `analysis/src/check_numbers.py`; after any change the build fails until the text agrees.\n")
    er = read_csv(os.path.join(ANALYSIS, "erratum_v1.1.csv"))
    ap = {(e["fix_id"], e["field"]): e for e in read_csv(os.path.join(ANALYSIS, "matrix_v1.1", "erratum_applied.csv"))}
    w("## A. Label fixes in the 45-cell matrix (task 3; `analysis/erratum_v1.1.csv`)\n")
    seen = []
    for e in er:
        if e["fix_id"] in seen:
            continue
        seen.append(e["fix_id"])
        rows = [x for x in er if x["fix_id"] == e["fix_id"]]
        w("### %s: %s (confidence: %s)\n" % (e["fix_id"], e["cell"], e["confidence"]))
        w("- **Reason:** %s" % e["reason"])
        w("- **Source and location:** %s, %s" % (e["source_id"], e["location"]))
        for q in e["exact_quote"].split(" | "):
            w("- **Quote:** \"%s\"" % q.strip())
        for x in rows:
            v11 = ap.get((x["fix_id"], x["field"]), {}).get("value_in_v1_1", "")
            w("- **Field `%s`** (%s): v1.0 `%s` → v1.1 `%s`" % (x["field"], x["operation"], esc(x["old_value"])[:300] or "(empty)", esc(v11)[:300] or "(empty)"))
        w("- **Decision:** ☐ approve ☐ reject ☐ change to: ____\n")
    w("## B. New sources and their coding (task 2)\n")
    w("Search protocol and inclusion decisions are in `analysis/search_protocol.md`; ledger entries are in `supporting_data/source_ledger/sources_v1.1_additions.csv`; texts are in `supporting_data/source_cache_v1.1/`.\n")
    for r in read_csv(os.path.join(ROOT, "supporting_data", "source_ledger", "sources_v1.1_additions.csv")):
        w("- **%s** %s (%s; %s). Decision: *%s*. %s" % (r["ref"], r["citation"], r["date"], r["organization"], r["decision"], r["reason"]))
    w("\n**Excluded:** eight Cloud Security Alliance research notes (derivative syntheses), the OpenAI Black Hat talk (no transcript), press and blog coverage. Reasons are in the search protocol.\n")
    w("### B1. Coded rows (%d), attached only to existing propositions\n" % len(NS.ROWS))
    w("| Row | Proposition | Source | Relation | Quote | Location | Note | Decision |")
    w("|---|---|---|---|---|---|---|---|")
    for r in NS.ROWS:
        w("| %s | %s | %s | %s | \"%s\" | %s | %s | ☐ ok ☐ reject |" % (r["rid"], r["pid"], r["src"], r["rel"], esc(r["quote"]), esc(r["loc"]), esc(r["note"])))
    w("\n### B2. Candidate propositions raised by the new sources (%d), not coded or counted\n" % len(NS.CANDIDATES))
    w("| ID | Unit | Source | Quote | Location | Why it matters | Decision |")
    w("|---|---|---|---|---|---|---|")
    for c in NS.CANDIDATES:
        w("| %s | %s | %s | \"%s\" | %s | %s | ☐ add as proposition ☐ ignore |" % (c["cid"], c["unit"], c["src"], esc(c["quote"]), esc(c["loc"]), esc(c["why"])))
    w("\n## C. Stricter independence judgments, A10 (task 5; `analysis/a10_independence_judgments.csv`)\n")
    res = {r["proposition_id"]: r for r in read_csv(os.path.join(ANALYSIS, "a10_results.csv"))}
    res10 = {r["proposition_id"]: r for r in read_csv(os.path.join(ANALYSIS, "v1.0", "a10_results.csv"))}
    for j in read_csv(os.path.join(ANALYSIS, "a10_independence_judgments.csv")):
        pid = j["proposition_id"]
        r = res.get(pid) or res10.get(pid) or {}
        w("### %s: %s\n" % (pid, "counts under A10" if r.get("counts_under_a10") == "True" else "DROPPED under A10: " + r.get("dropped_because", "")))
        w("- **Pair:** %s (in v1.0: %s)" % (j["pair"], "yes" if pid in res10 else "no, v1.1 only"))
        w("- **OpenAI:** \"%s\" (%s)" % (j["quote_openai"], j["loc_openai"]))
        w("- **Other:** \"%s\" (%s)" % (j["quote_other"], j["loc_other"]))
        w("- **(a) Same act:** %s. %s" % (j["same_act"], j["same_act_basis"]))
        w("- **(b) Independence marked uncertain:** %s. %s" % (j["independence_marked_uncertain"], j["uncertainty_basis"] or "—"))
        w("- **(c) OpenAI statement likely derives from Hugging Face:** cites or defers = %s; fact not visible in OpenAI's logs = %s. %s"
          % (j["r02_cites_or_defers_to_hf"], j["r02_fact_not_in_openai_logs"], j["r02_derivation_basis"]))
        w("- **Decision:** ☐ agree ☐ disagree: ____\n")
    w("## D. Headline sentences that changed (task 4)\n")
    w("| Where | Before (manuscript of 12 Nov) | Now (v1.1 manuscript) | Decision |")
    w("|---|---|---|---|")
    for a, b, c in HEADLINES:
        w("| %s | %s | %s | ☐ ok ☐ edit |" % (esc(a), esc(b), esc(c)))
    w("\n## E. Framing conflicts (reworded at the authors' request on 13 Nov; AI-drafted wording, confirm or edit)\n")
    for a, b, c in FRAMING:
        w("- **%s:** %s. *What changed:* %s" % (a, b, c))
    w("\n## F. Number check (task 1)\n")
    w("`analysis/src/check_numbers.py` tags every number in the manuscript to a data key (`n:`), a cached source (`q:`) or a stated structural reason (`x:`). The build fails on any mismatch or untagged number; the report is `analysis/number_check_report.csv`. Automatic fixes of counted numbers (data wins):\n")
    w("| Where | Old text | New text |")
    w("|---|---|---|")
    for a, b, c in AUTO_FIXES:
        w("| %s | %s | %s |" % (esc(a), esc(b), esc(c)))
    w("\nNo counted number was found to contradict its source passage, so none was left unfixed. Quoted numbers (times, percentages, run counts) were checked against the cached sources, and none mismatched. Structural numbers (`x:` tags) are listed in the report with their reasons, for the authors to check.\n")
    w("## G. Text decisions (task 7)\n")
    w("- **References [9], [10], [24], [25], [26]** are now cited where used, not removed: [9] in Related Work and III-F, [10] in Related Work and III-D, and [24], [25], [26] wherever their sources are used. Body citations are numeric; ledger codes appear only in Table VIII.")
    w("- **The reference list grew from [1]–[28] to [1]–[32]**, because task 2 added JFrog [29], OpenAI 21 Jul [30] and Irregular [31], and OpenAI's third-party-impact update [32] (R05) was added on 13 Nov as context for the 100+ notified organizations. The brief expected [1]–[28]; the authors should confirm.")
    w("- **The Bieringer sentence** in Related Work still says the fields 'overlap'. The re-reading (`analysis/literature_candidates.md`, section 4) finds that the match is by field name, not object. A replacement sentence is drafted there, pending your reading.")
    w("- **The stale PDFs** of the previous round were moved to `manuscript/superseded/`. No new PDF was built in this round (MD and DOCX only).\n")
    open(os.path.join(ROOT, "HUMAN_REVIEW_PACKET.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote HUMAN_REVIEW_PACKET.md (%d lines)" % len(L))


if __name__ == "__main__":
    main()
