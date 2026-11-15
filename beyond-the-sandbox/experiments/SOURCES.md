# Source texts

The study codes passages from 70 public documents (`data/sources.csv`, refs R01–R70).
Their text belongs to the publishers (OpenAI, Anthropic, UK AISI and others), so this package does **not**
include our cached copies (`source_cache/`).

`source_manifest.csv` lists, for every source: its URL, the file we cached, that file's sha256 and size, when it
was fetched, and a text-quality note. 62 sources had a cached copy; these did not: R01, R18, R43, R51, R53, R55, R57, R67.

## Rebuilding the cache

    python -X utf8 scripts/fetch_sources.py   # see its docstring; writes source_cache/<ref>.txt

Run from `experiments/`. Web pages change and some sites block automated clients, so a fresh copy may not match
the sha256 in the manifest; the Wayback Machine (web.archive.org) often holds a copy from near the fetch date.
With `source_cache/` present, `reproduce_all.py` also runs the four scripts that check quoted passages against
the source texts (`analyst_round12`, `round9`, `analyst_round13g`, `quote_check_summary`). Without it they are
skipped and their shipped outputs in `results/` stand.
