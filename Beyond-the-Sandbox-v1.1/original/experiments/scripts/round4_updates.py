"""Round 4: add the 2 new scout sources (context only), flag cells the AI second coder could not check,
record the re-read of the two new disagreements, fix number_ledger N35 / N14."""
import csv, json, os

E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(E, "data")


def load(n):
    with open(os.path.join(D, n), newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def save(n, fn, rows):
    with open(os.path.join(D, n), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fn)
        w.writeheader()
        w.writerows(rows)


# sources
fn, src = load("sources.csv")
urls = {s["url"] for s in src}
n = max(int(s["ref"][1:]) for s in src)
for l in open(os.path.join(E, "..", "research", "new_sources.jsonl"), encoding="utf-8").read().strip().splitlines()[-2:]:
    d = json.loads(l)
    if d["url"] in urls:
        continue
    n += 1
    src.append({"ref": f"R{n}", "citation": f'{d["publisher"]}, “{d["title"]},” {d["date"]}.', "url": d["url"],
                "verification": f'listed by data-scout 2026-11-02 (status: {d["status"]}); NOT opened by experimenter (scout summary only); '
                                "context only, no coded row depends on it; re-check before citing any detail",
                "relevance": "secondary coverage (context)"})
save("sources.csv", fn, src)

# coded evidence: flag cells the AI second coder could not check
NOTE = {("INC-OAI-HF", "D1"): "not independently checked by AI second coder (R01 text unavailable to it; R01 403 here too)",
        ("INC-AISI-SOL", "D5"): "second coder lacked R24 text and tagged unknown; primary re-read R24 App. A.10 (anchors A28-A30) and keeps documented"}
for name in ["coded_evidence.csv", "coded_evidence_v12.csv"]:
    fn, rows = load(name)
    for r in rows:
        k = (r["unit"], r["code"])
        if k in NOTE and "not independently checked" not in r["qualification"] and "lacked R24" not in r["qualification"]:
            r["qualification"] += "; " + NOTE[k]
        if k in [("INC-ANT-OP46", "D2"), ("INC-OAI-ART", "D4")] and "round 4" not in r["change_log"]:
            r["change_log"] += "; round 4: second coder tagged unknown; re-read source, primary kept (no status change)"
    save(name, fn, rows)

# number ledger
fn, rows = load("number_ledger.csv")
for r in rows:
    if r["id"] == "N35":
        r["value"] = f"{len(src)} sources"
        r["tokens"] = str(len(src))
    if r["id"] == "N14":
        r["claim"] = "about 1% of actions flagged with CoT present (replay)"
save("number_ledger.csv", fn, rows)
print("sources", len(src))
