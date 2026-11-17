"""One command that regenerates every results/ file the draft cites and prints sha256 values.
Run from anywhere:  python3 -I experiments/scripts/reproduce_all.py   (about a minute; standard library only; no network)
Order matters: round9 overwrites appendix_b_check.csv, analyst_round13b rewrites it with the extended check, so 13b follows round9.
Every script is idempotent. data/*.csv are hashed before and after: if a hash changes, the run reports it (it should not).
Scripts that need a network fetch (lib/documentary.py, source download) are NOT run here; results/quote_check_summary.json and
the source_cache/ texts are inputs."""
import hashlib, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.abspath(os.path.join(HERE, ".."))
SCRIPTS = ["analyst_round12", "round14", "rule_variants", "analyst_round13", "round9", "analyst_round13b", "analyst_round13c",
           "analyst_round13e", "analyst_round13f", "analyst_round13g", "analyst_round13h", "analyst_round13i", "analyst_round13j",
           "sensitivity", "selection_frame", "discount_table", "tag_counts", "n_refs", "evidence_class_matrix", "quote_check_summary",
           "stop_d2_profile"]


NEEDS_MATPLOTLIB = {"n_refs"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def tree(sub):
    d = os.path.join(EXP, sub)
    return {f: sha(os.path.join(d, f)) for f in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, f))}


print("python", sys.version.split()[0])
data0 = tree("data")
fails = []
for s in SCRIPTS:
    p = os.path.join(HERE, s + ".py")
    if not os.path.exists(p):
        print("%-26s MISSING" % s); fails.append(s); continue
    t = time.time()
    py = sys.executable
    if s in NEEDS_MATPLOTLIB:   # figure scripts: use the repository venv if the current interpreter lacks matplotlib
        venv = os.path.abspath(os.path.join(EXP, "..", "..", "..", ".venv", "bin", "python"))
        if os.path.exists(venv):
            py = venv
    r = subprocess.run([py, "-I", p], cwd=EXP, capture_output=True, text=True, timeout=300)
    print("%-26s rc=%d  %.1fs" % (s, r.returncode, time.time() - t))
    if r.returncode:
        fails.append(s); print("   ", (r.stderr or r.stdout).strip().splitlines()[-1:])
data1 = tree("data")
print("\ndata/ hashes unchanged by the run:", data0 == data1)
for f, h in data1.items():
    print("sha256 %s  data/%s" % (h, f))
for f, h in tree("results").items():
    if f != "run_log.md":      # run_log.md carries timestamps
        print("sha256 %s  results/%s" % (h, f))
print("\nfailed scripts:", fails or "none")
sys.exit(1 if fails or data0 != data1 else 0)
