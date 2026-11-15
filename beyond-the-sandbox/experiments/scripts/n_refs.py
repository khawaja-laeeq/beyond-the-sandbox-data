"""n_refs==1 counts and source-concentration figure from data/coded_evidence.csv.
Writes results/n_refs_counts.json, figures/source_concentration.png. Run from experiments/ with the repo venv python."""
import csv, json, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rows = list(csv.DictReader(open("data/coded_evidence.csv", encoding="utf-8")))
cl = {r["unit"]: r["cluster"] for r in csv.DictReader(open("data/units.csv", encoding="utf-8"))}
doc = [r for r in rows if r["status"] == "documented"]
for r in doc:
    r["n"] = len([x for x in r["reference"].split(";") if x])
one = [r for r in doc if r["n"] == 1]
dims = ["D1", "D2", "D3", "D4", "D5"]
clusters = sorted(set(cl.values()))
nr = {"coding_file": "coded_evidence.csv", "documented_cells": len(doc), "documented_n_refs_1": len(one),
      "by_cluster": {c: {"documented": sum(cl[r["unit"]] == c for r in doc), "n_refs_1": sum(cl[r["unit"]] == c for r in one)} for c in clusters},
      "by_dimension": {d: {"documented": sum(r["code"] == d for r in doc), "n_refs_1": sum(r["code"] == d for r in one)} for d in dims}}
json.dump(nr, open("results/n_refs_counts.json", "w"), indent=1)
fig, ax = plt.subplots(1, 2, figsize=(8, 3))
for a, key, labs in ((ax[0], "by_cluster", clusters), (ax[1], "by_dimension", dims)):
    d = [nr[key][l]["documented"] - nr[key][l]["n_refs_1"] for l in labs]
    s = [nr[key][l]["n_refs_1"] for l in labs]
    a.bar(labs, s, label="one source"); a.bar(labs, d, bottom=s, label="2+ sources")
    a.set_title("Documented cells by " + key[3:]); a.set_ylabel("cells (counts)")
ax[0].legend()
fig.suptitle("Source concentration: %d of %d documented cells cite one source" % (len(one), len(doc)))
fig.tight_layout(); fig.savefig("figures/source_concentration.png", dpi=150)
print(nr)
