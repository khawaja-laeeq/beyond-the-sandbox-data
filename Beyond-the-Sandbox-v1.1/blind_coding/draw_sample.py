"""Task 9: draw the stratified random sample for blinded human coding and write two identical BLANK sheets.

Run once:  python3 -I blind_coding/draw_sample.py
Sampling frame: the 138 propositions of v1.1 that have at least one non-secondary source attached (a coder cannot
code a proposition with no source). Stratification: 4 propositions per incident unit (9 units x 4 = 36); within
each unit the 4 dimensions are chosen so that every dimension D1-D5 is sampled 7 or 8 times overall; within each
unit x dimension stratum one proposition is drawn at random. Seed: SEED below.
The sheets show ONLY the item number, the proposition text and the source IDs. They do not show the AI's
evidence status, support relations, organizations, notes, core/added flag or proposition ID.
The key (item -> proposition ID) is written to blind_coding/key/ and is needed only by agreement.py.
"""
import csv, os, random, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "analysis", "src"))
from common import SECONDARY, read_csv

SEED = 20261113
N_PER_UNIT = 4
UNITS = ["INC-OAI-MAY", "INC-OAI-ART", "INC-OAI-HF", "INC-ANT-OP46", "INC-ANT-OP47", "INC-ANT-MY5", "INC-ANT-INT",
         "INC-AISI-MY5", "INC-AISI-SOL"]
DIMS = ["D1", "D2", "D3", "D4", "D5"]
OUT = os.path.join(ROOT, "blind_coding")


def main():
    props = read_csv(os.path.join(ROOT, "analysis", "atomic_propositions.csv"))
    sup = read_csv(os.path.join(ROOT, "analysis", "proposition_support.csv"))
    srcs = {}
    for s in sup:
        if s["source_id"] not in SECONDARY:
            srcs.setdefault(s["proposition_id"], [])
            if s["source_id"] not in srcs[s["proposition_id"]]:
                srcs[s["proposition_id"]].append(s["source_id"])
    eligible = {}
    for p in props:
        if srcs.get(p["proposition_id"]):
            eligible.setdefault((p["incident_unit"], p["dimension"]), []).append(p)
    rng = random.Random(SEED)
    dim_count = {d: 0 for d in DIMS}
    sample = []
    for u in UNITS:
        avail = [d for d in DIMS if eligible.get((u, d))]
        # prefer the dimensions sampled least so far; break ties at random
        order = sorted(avail, key=lambda d: (dim_count[d], rng.random()))
        for d in order[:N_PER_UNIT]:
            p = rng.choice(sorted(eligible[(u, d)], key=lambda x: x["proposition_id"]))
            sample.append(p); dim_count[d] += 1
    rng.shuffle(sample)   # item order carries no unit or dimension information
    key, items, rels = [], [], []
    for i, p in enumerate(sample, 1):
        iid = "Q%02d" % i
        key.append(dict(item_id=iid, proposition_id=p["proposition_id"], incident_unit=p["incident_unit"], dimension=p["dimension"]))
        items.append(dict(item_id=iid, proposition=p["atomic_proposition"], source_ids=";".join(srcs[p["proposition_id"]]),
                          evidence_status="", deciding_source_and_location="", notes=""))
        for s in srcs[p["proposition_id"]]:
            rels.append(dict(item_id=iid, source_id=s, relation="", passage_location="", notes=""))
    os.makedirs(os.path.join(OUT, "key"), exist_ok=True)

    def w(path, rows):
        with open(path, "w", encoding="utf-8", newline="") as f:
            x = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n"); x.writeheader(); x.writerows(rows)
    w(os.path.join(OUT, "key", "sample_key_DO_NOT_GIVE_TO_CODERS.csv"), key)
    for coder in ("coder_A_Laeeq", "coder_B_Iftikhar"):
        w(os.path.join(OUT, "sheet_items_%s.csv" % coder), items)
        w(os.path.join(OUT, "sheet_relations_%s.csv" % coder), rels)
    with open(os.path.join(OUT, "key", "sample_record.txt"), "w", encoding="utf-8") as f:
        f.write("seed=%d\nframe=v1.1 propositions with at least one non-secondary source: %d of %d\nper unit=%d\nper dimension=%s\nitems=%d\nsource-relation pairs=%d\n"
                % (SEED, sum(len(v) for v in eligible.values()), len(props), N_PER_UNIT, dim_count, len(items), len(rels)))
    print(open(os.path.join(OUT, "key", "sample_record.txt")).read())


if __name__ == "__main__":
    main()
