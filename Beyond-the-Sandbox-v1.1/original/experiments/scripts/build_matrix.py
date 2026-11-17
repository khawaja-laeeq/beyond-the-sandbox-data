"""E1: 9x5 status heatmap (PDF+PNG) and LaTeX table. Run with the repo .venv python (matplotlib)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

units, cod, book = rows("units.csv"), rows("coded_evidence.csv"), rows("codebook.csv")
st = {(r["unit"], r["code"]): r["status"] for r in cod}
code = {"documented": 0, "contradicted": 1, "unknown": 2}
colors = ["#2a7f62", "#c0392b", "#d9d9d9"]
order = sorted(units, key=lambda u: (CLUSTERS.index(u["cluster"]), 0))  # stable: keeps register order within cluster
grid = [[code[st[(u["unit"], d)]] for d in DIMS] for u in order]

fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.imshow(grid, cmap=ListedColormap(colors), vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(5))
ax.set_xticklabels([f'{b["code"]}\n{b["dimension"].replace(" / ", "/")}' for b in book], fontsize=7)
ax.xaxis.tick_top()
ax.set_yticks(range(len(order)))
ax.set_yticklabels([f'{u["cluster"]}: {u["label"]}' for u in order], fontsize=8)
for i, row in enumerate(grid):
    for j, v in enumerate(row):
        ax.text(j, i, ["doc.", "contr.", "unk."][v], ha="center", va="center", fontsize=7,
                color="white" if v < 2 else "black")
ax.set_xticks([x - .5 for x in range(6)], minor=True)
ax.set_yticks([y - .5 for y in range(len(order) + 1)], minor=True)
ax.grid(which="minor", color="white", linewidth=1.5)
ax.tick_params(which="both", length=0)
# cluster separators
bounds = [i for i in range(1, len(order)) if order[i]["cluster"] != order[i - 1]["cluster"]]
for b in bounds:
    ax.axhline(b - .5, color="black", linewidth=2)
ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(colors, ["documented", "contradicted", "unknown"])],
          loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "coding_matrix.pdf"))
fig.savefig(os.path.join(FIGS, "coding_matrix.png"), dpi=200)

abbr = {"documented": "D", "contradicted": "C", "unknown": "U"}
lines = [r"\begin{tabular}{llccccc}", r"\toprule",
         "Cluster & Unit & " + " & ".join(b["code"] for b in book) + r" \\", r"\midrule"]
for i, u in enumerate(order):
    if i and u["cluster"] != order[i - 1]["cluster"]:
        lines.append(r"\midrule")
    lines.append(f'{u["cluster"] if i == 0 or u["cluster"] != order[i-1]["cluster"] else ""} & {u["label"]} & '
                 + " & ".join(abbr[st[(u["unit"], d)]] for d in DIMS) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}"]
open(os.path.join(RESULTS, "coding_matrix_table.tex"), "w").write("\n".join(lines) + "\n")
n = {k: sum(v == c for r in grid for v in r) for k, c in code.items()}
log("build_matrix.py", f"wrote figures/coding_matrix.pdf|png and results/coding_matrix_table.tex; counts {n}")
print(n)
