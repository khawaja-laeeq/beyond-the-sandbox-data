"""Second clean run (Phase 3.6). Copies the deliverable tree to a fresh temporary directory, runs every step with
the interpreter given on the command line, and writes machine-readable results. It never edits original/.
Usage (from the deliverable root):
    python3 -m venv /tmp/venv_clean && /tmp/venv_clean/bin/pip install matplotlib==<ver>   # optional figure only
    /tmp/venv_clean/bin/python -I reproducibility/clean_run.py reproducibility/clean_run_results.json
"""
import hashlib, json, os, platform, shutil, subprocess, sys, tempfile, time

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(SRC, "reproducibility", "clean_run_results.json")

def tree_hash(d):
    h = {}
    for root, _, files in os.walk(d):
        for f in sorted(files):
            p = os.path.join(root, f)
            h[os.path.relpath(p, d)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h

work = tempfile.mkdtemp(prefix="bts_clean_")
for sub in ("original", "analysis", "reproducibility", "supporting_data", "manuscript"):
    shutil.copytree(os.path.join(SRC, sub), os.path.join(work, sub), ignore=shutil.ignore_patterns("__pycache__", "runs", "superseded"))
# analysis outputs are regenerated; delete them so the run must recreate them. Stored inputs (the erratum and the A10
# judgments, both edited by humans) are kept.
INPUTS = {"erratum_v1.1.csv", "a10_independence_judgments.csv"}
for f in os.listdir(os.path.join(work, "analysis")):
    if f.endswith((".csv", ".json", ".png")) and f not in INPUTS:
        os.remove(os.path.join(work, "analysis", f))
for d in ("v1.0", "matrix_v1.1"):
    shutil.rmtree(os.path.join(work, "analysis", d), ignore_errors=True)
for f in ("manual_evidence_audit.csv", "source_verification.csv", "independent_verify_results.json"):
    p = os.path.join(work, "reproducibility", f)
    if os.path.exists(p):
        os.remove(p)

orig_before = tree_hash(os.path.join(work, "original"))
ref_checksums = {}
for line in open(os.path.join(SRC, "reproducibility", "original_checksums.sha256")):
    h, p = line.strip().split("  ", 1)
    ref_checksums[os.path.normpath(p)] = h
orig_matches_snapshot = all(orig_before.get(os.path.normpath(p)) == h for p, h in ref_checksums.items())

py = sys.executable
steps = [
    ("reproduce_all (original package)" + (" via UTF-8 wrapper (Windows)" if os.name == "nt" else ""),
     ([py, "-X", "utf8", "-I", os.path.join(work, "reproducibility", "run_original_utf8.py")] if os.name == "nt"
      else [py, "-I", "experiments/scripts/reproduce_all.py"]), os.path.join(work, "original")),
    ("build_matrix_v1_1 (v1.0 + erratum)", [py, "-I", "analysis/src/build_matrix_v1_1.py"], work),
    ("build_analysis (propositions, v1.0 and v1.1)", [py, "-I", "analysis/src/build_analysis.py"], work),
    ("cell_recount (S0-S9, LOO, mechanisms)", [py, "-I", "analysis/src/cell_recount.py"], work),
    ("make_comparison (v1.0 vs v1.1)", [py, "-I", "analysis/src/make_comparison.py"], work),
    ("check_numbers (manuscript locked to data)", [py, "-I", "analysis/src/check_numbers.py"], work),
    ("prior_work table", [py, "-I", "analysis/src/prior_work.py"], work),
    ("independent_verify", [py, "-I", "reproducibility/independent_verify.py", "--json", "reproducibility/independent_verify_results.json"], work),
    ("evidence_audit + source_verification", [py, "-I", "reproducibility/evidence_audit.py"], work),
]
results = []
for name, cmd, cwd in steps:
    t = time.time()
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
    results.append(dict(step=name, command=" ".join(cmd[1:]), exit_code=r.returncode, seconds=round(time.time() - t, 2),
                        stdout_tail=r.stdout.strip().splitlines()[-25:], stderr_tail=r.stderr.strip().splitlines()[-10:]))

orig_after = tree_hash(os.path.join(work, "original"))
changed = sorted(k for k in orig_before if orig_before[k] != orig_after.get(k))
data_changed = [k for k in changed if k.startswith(os.path.join("experiments", "data")) or k.startswith(os.path.join("experiments", "protocol"))]
iv = json.load(open(os.path.join(work, "reproducibility", "independent_verify_results.json")))
summ = json.load(open(os.path.join(work, "analysis", "revised_summary.json")))
gen = {}
for sub in ("", "v1.0", "matrix_v1.1"):
    for f in sorted(os.listdir(os.path.join(work, "analysis", sub))):
        if f.endswith((".csv", ".json")) and f not in INPUTS:
            rel = os.path.join(sub, f) if sub else f
            gen[rel] = hashlib.sha256(open(os.path.join(work, "analysis", rel), "rb").read()).hexdigest()
committed = {f: hashlib.sha256(open(os.path.join(SRC, "analysis", f), "rb").read()).hexdigest()
             for f in gen if os.path.exists(os.path.join(SRC, "analysis", f))}
try:
    import matplotlib
    mpl = matplotlib.__version__
except Exception:
    mpl = None
res = dict(
    run_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), platform=platform.platform(), python=platform.python_version(),
    interpreter=py, matplotlib=mpl, workdir=work, steps=results,
    all_steps_exit_zero=all(s["exit_code"] == 0 for s in results),
    original_tree_matches_snapshot_before_run=orig_matches_snapshot,
    original_files_changed_by_run=changed, coded_data_or_protocol_changed=data_changed,
    generated_analysis_identical_to_committed=all(gen[f] == committed.get(f) for f in gen),
    analysis_hash_mismatches=[f for f in gen if gen[f] != committed.get(f)],
    published_value_checks=iv["comparison"], published_values_all_match=all(c["match"] for c in iv["comparison"]),
    revised_headline=dict((k, summ[k]) for k in ("total_propositions", "supported", "contested", "unknown", "partially_supported", "contradicted",
                                                 "cross_org_agreement", "independent_corroboration", "shared_upstream_only", "repeated_reporting_only",
                                                 "with_explicit_counterevidence", "disagreements_total")),
    note="A computational recount. It is not an independent scientific replication and does not validate documentary judgments.")
json.dump(res, open(out_path, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("steps", "published_value_checks")}, indent=1))
for s in results:
    print("%-40s exit=%d  %.1fs" % (s["step"], s["exit_code"], s["seconds"]))
sys.exit(0 if res["all_steps_exit_zero"] and not data_changed else 1)
