"""Figure 1: support for the 138 atomic propositions by incident unit, v1.0 and v1.1 side by side.
Reads analysis/v1.0/ and analysis/ breakdown tables. Needs matplotlib (only this script does).
Run:  python3 -I analysis/src/make_figures.py   -> analysis/fig_proposition_support_by_unit.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ANALYSIS, read_csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LABEL = {"INC-OAI-MAY": "OpenAI May", "INC-OAI-ART": "Artifactory", "INC-OAI-HF": "Hugging Face",
         "INC-ANT-OP46": "Opus 4.6", "INC-ANT-OP47": "Opus 4.7", "INC-ANT-MY5": "Anthropic Mythos 5",
         "INC-ANT-INT": "Internal model", "INC-AISI-MY5": "AISI Mythos 5", "INC-AISI-SOL": "AISI Sol"}
SERIES = [("independent", "Independent corroboration (current rule)", "#1b5e20"),
          ("shared", "Two organizations, shared records", "#66bb6a"),
          ("single", "One organization", "#90a4ae"),
          ("weak", "Partial, contested or contradicted", "#ffb74d"),
          ("unknown", "Unknown", "#e0e0e0")]


def series(folder):
    """One category per proposition, so each bar sums to the unit's proposition count."""
    counts = {u: dict(unit=LABEL[u], independent=0, shared=0, single=0, weak=0, unknown=0) for u in LABEL}
    for r in read_csv(os.path.join(folder, "proposition_corroboration.csv")):
        u = r["parent_cell_id"].split("/")[0]
        if r["independent_corroboration"] == "True":
            k = "independent"
        elif r["cross_org_agreement"] == "True":
            k = "shared"
        elif r["evidence_status"] == "supported":
            k = "single"
        elif r["evidence_status"] == "unknown":
            k = "unknown"
        else:
            k = "weak"
        counts[u][k] += 1
    return [counts[u] for u in LABEL]


def main():
    data = {"v1.0 (frozen)": series(os.path.join(ANALYSIS, "v1.0")), "v1.1 (provisional, pending author approval)": series(ANALYSIS)}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    for ax, (title, rows) in zip(axes, data.items()):
        units = [r["unit"] for r in rows][::-1]
        left = [0] * len(rows)
        for key, lab, col in SERIES:
            vals = [r[key] for r in rows][::-1]
            ax.barh(units, vals, left=left, color=col, label=lab, edgecolor="white", linewidth=0.5)
            left = [a + b for a, b in zip(left, vals)]
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Atomic propositions")
        ax.spines[["top", "right"]].set_visible(False)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8, frameon=False)
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    p = os.path.join(ANALYSIS, "fig_proposition_support_by_unit.png")
    fig.savefig(p, dpi=200, metadata={"Software": None})
    print("wrote", p)


if __name__ == "__main__":
    main()
