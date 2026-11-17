"""Shared helpers for the revision analysis. Standard library only (Python >= 3.10)."""
import csv, os, re, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ORIG = os.path.join(ROOT, "original")
EXP = os.path.join(ORIG, "experiments")
CACHE = os.path.join(EXP, "source_cache")
# v1.1 (2026-11-13): sources cached in this revision. Never written into original/. A file here takes
# precedence over the original cache (R05's original cache file is a garbled binary capture).
CACHE_V11 = os.path.join(ROOT, "supporting_data", "source_cache_v1.1")
ANALYSIS = os.path.join(ROOT, "analysis")

# Organization that published each incident source (publisher attribution rule; see manuscript §III.F)
ORG = {"R01": "OpenAI", "R02": "OpenAI", "R05": "OpenAI", "R03": "Hugging Face", "R04": "Hugging Face",
       "R06": "SentinelOne", "R07": "METR", "R08": "Anthropic", "R09": "Anthropic", "R25": "Anthropic",
       "R26": "Anthropic", "R10": "UK AISI", "R24": "UK AISI",
       "R27": "AIID", "R28": "AIID", "R29": "AIID", "R30": "AIID",
       # v1.1 additions (supporting_data/source_ledger/sources_v1.1_additions.csv)
       "R71": "OpenAI", "R74": "OpenAI", "R72": "JFrog", "R75": "Irregular",
       "R73": "Alazab & Waheed (secondary analysis)"}
# Secondary analyses: recorded with their quotes, but never counted as an organization under any rule
# (task 2: 'treat it as secondary analysis, not as an organization's own records').
SECONDARY = {"R73"}
# Default evidence base (the record the source's statements are drawn from). Two sources share a base when
# their statements derive from the same upstream records, whoever publishes them.
BASE = {"R02": "OpenAI internal records", "R07": "OpenAI internal records (provided to METR)",
        "R03": "Hugging Face platform records", "R04": "Hugging Face platform records",
        "R06": "Public Hugging Face commit histories joined to OpenAI chronology",
        "R08": "Anthropic evaluation transcripts", "R25": "Anthropic evaluation transcripts",
        "R10": "UK AISI evaluation records", "R24": "UK AISI evaluation records",
        "R26": "UK AISI evaluation records (transcripts analysed by Anthropic)",
        # v1.1 additions
        "R01": "OpenAI internal records", "R05": "OpenAI internal records", "R74": "OpenAI internal records",
        "R71": "UK AISI evaluation records (as reported to OpenAI by UK AISI)",
        "R72": "JFrog product-security records (incident facts from OpenAI's disclosure to JFrog)",
        "R75": "Irregular evaluation-environment records",
        "R73": "Secondary synthesis of published disclosures and press"}
# Base family: bases in the same family are NOT independent of each other
FAMILY = {"OpenAI internal records": "OAI", "OpenAI internal records (provided to METR)": "OAI",
          "Hugging Face platform records": "HF", "Public Hugging Face commit histories joined to OpenAI chronology": "PUB",
          "Anthropic evaluation transcripts": "ANT", "UK AISI evaluation records": "AISI",
          "UK AISI evaluation records (transcripts analysed by Anthropic)": "AISI",
          "UK AISI evaluation records (as reported to OpenAI by UK AISI)": "AISI",
          "JFrog product-security records (incident facts from OpenAI's disclosure to JFrog)": "JFROG",
          "Irregular evaluation-environment records": "IRR",
          "Secondary synthesis of published disclosures and press": "SEC"}
NONUTF8 = {"R24": "cp1252"}


def norm(s):
    s = unicodedata.normalize("NFKC", s).casefold()
    return re.sub(r"[^0-9a-z]+", "", s)


_cache = {}
def source_text(ref):
    if ref not in _cache:
        p = os.path.join(CACHE_V11, ref + ".txt")
        if not os.path.exists(p):
            p = os.path.join(CACHE, ref + ".txt")
        if not os.path.exists(p):
            _cache[ref] = None
        else:
            raw = open(p, "rb").read()
            enc = NONUTF8.get(ref, "utf-8")
            t = raw.decode(enc, errors="replace")
            t = t.replace("&#x27;", "'").replace("&quot;", '"').replace("&amp;", "&")
            _cache[ref] = t
    return _cache[ref]


def quote_found(ref, quote):
    t = source_text(ref)
    if t is None:
        return None
    return norm(quote) in norm(t)


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fields, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
