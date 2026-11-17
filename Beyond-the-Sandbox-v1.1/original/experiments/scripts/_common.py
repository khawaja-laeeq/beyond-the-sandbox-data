"""Shared paths and CSV loaders for the documentary scripts (standard library only)."""
import csv, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.abspath(os.path.join(HERE, ".."))
PAPER = os.path.abspath(os.path.join(EXP, ".."))
DATA = os.path.join(EXP, "data")
RESULTS = os.path.join(EXP, "results")
FIGS = os.path.join(EXP, "figures")
for d in (RESULTS, FIGS):
    os.makedirs(d, exist_ok=True)

DIMS = ["D1", "D2", "D3", "D4", "D5"]
CLUSTERS = ["OpenAI", "Anthropic", "AISI"]


def rows(name, folder=DATA):
    with open(os.path.join(folder, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(data)


def log(script, msg, status="OK"):
    """Append one entry to results/run_log.md."""
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    p = os.path.join(RESULTS, "run_log.md")
    new = not os.path.exists(p)
    with open(p, "a", encoding="utf-8") as f:
        if new:
            f.write("# Run log (scripts in experiments/scripts/)\n\n")
        f.write(f"- {ts} `{script}` [{status}] {msg}\n")


def stage_cat(text):
    """H1 category of a coded response_stage / Appendix B D4 stage label (keyword rules, first match; round 14)."""
    t = text.lower()
    for key, cat in (("signal only", "signal only"), ("operator halt", "operator halt"), ("external stop", "external technical"),
                     ("token-budget", "external technical"), ("third-party", "third party"), ("affected-party", "affected party"),
                     ("self-stop", "self")):
        if key in t:
            return cat
    return "unclassified" if text.strip() and text.strip() != "—" else ""
