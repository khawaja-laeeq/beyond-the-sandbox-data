"""Run original/experiments/scripts/reproduce_all.py with Python's UTF-8 mode, without editing original/.

Why: on Windows the default text encoding is cp1252, and two original scripts (selection_frame, analyst_round13j)
open UTF-8 files without naming the encoding, so they fail there; on Linux (where the package was built) UTF-8 is the
default and they pass. reproduce_all.py starts each script as [sys.executable, "-I", script], and -I ignores the
PYTHONUTF8 environment variable, so this wrapper inserts "-X utf8" into those child commands instead.
Usage (from original/):  python -X utf8 -I ../reproducibility/run_original_utf8.py
"""
import os, runpy, subprocess, sys

_run = subprocess.run


def run_utf8(cmd, *a, **k):
    if isinstance(cmd, list) and cmd and cmd[0] == sys.executable and "-X" not in cmd:
        cmd = [cmd[0], "-X", "utf8"] + cmd[1:]
    return _run(cmd, *a, **k)


subprocess.run = run_utf8
sys.argv = ["reproduce_all.py"]
runpy.run_path(os.path.join(os.getcwd(), "experiments", "scripts", "reproduce_all.py"), run_name="__main__")
