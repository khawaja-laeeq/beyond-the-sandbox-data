"""Build the draft as a venue-format PDF and check it (run.sh step `latex`, before the review panel).

draft.md -> build/paper.tex (template: templates/latex/article.tex or $LATEX_TEMPLATE)
         -> build/paper.pdf with tectonic, latexmk or pdflatex+bibtex (whichever is installed)
Checks: it compiles, no undefined citations, main-text pages (before the references) within the
limit found in brief.md ("max 4 pages", "4-page", "page limit: 8"). Writes build/latex_check.json.

  python3 lib/latex.py <paper>
Install a TeX engine once on the VM (see README):  sudo apt-get install -y latexmk texlive-latex-extra
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import literature as lit  # noqa: E402
from common import REPO, now_iso, paper_dir, read, read_jsonl  # noqa: E402

SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
MATH_RE = re.compile(r"(\$\$.+?\$\$|\\\[.+?\\\]|\$[^\s$][^$\n]*?\$|\\\(.+?\\\))", re.S)
CITE_RE = re.compile(r"\[((?:-?@[\w:.-]+[;,\s]*)+)\]")
SECTION = {1: "section", 2: "section", 3: "subsection", 4: "subsubsection"}
APPENDIX_MARK = "%%APPENDIX%%"  # appendices go after the references: they don't count toward the page limit


def escape(text):
    return "".join(SPECIAL.get(c, c) for c in text)


# Unicode that pdflatex can't typeset: math symbols (as math) and typographic marks (as LaTeX)
MATH_SYM = {"−": "-", "±": r"\pm", "×": r"\times", "·": r"\cdot", "≤": r"\leq", "≥": r"\geq", "≈": r"\approx",
            "≠": r"\neq", "∈": r"\in", "∉": r"\notin", "→": r"\rightarrow", "←": r"\leftarrow", "⇒": r"\Rightarrow",
            "∞": r"\infty", "∑": r"\sum", "∏": r"\prod", "√": r"\sqrt{}", "∝": r"\propto", "∼": r"\sim", "°": r"^\circ",
            "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta", "ε": r"\epsilon", "η": r"\eta", "θ": r"\theta",
            "κ": r"\kappa", "λ": r"\lambda", "μ": r"\mu", "ν": r"\nu", "π": r"\pi", "ρ": r"\rho", "σ": r"\sigma",
            "τ": r"\tau", "φ": r"\phi", "χ": r"\chi", "ψ": r"\psi", "ω": r"\omega", "Δ": r"\Delta", "Σ": r"\Sigma",
            "Ω": r"\Omega", "ℓ": r"\ell", "ℝ": r"\mathbb{R}", "⊂": r"\subset", "∪": r"\cup", "∩": r"\cap", "≡": r"\equiv"}
TEXT_SYM = {"–": "--", "—": "---", "“": "``", "”": "''", "‘": "`", "’": "'", "…": r"\ldots{}", " ": "~",
            " ": r"\,", "•": r"\textbullet{}"}


def unicode_math(math):
    """Inside $...$: symbols to commands (a space after a command keeps the next letter apart)."""
    return "".join(MATH_SYM[c] + (" " if MATH_SYM[c][-1].isalpha() else "") if c in MATH_SYM else c for c in math)


def inline(text):
    """Escape plain text, keep math, turn [@a; @b] into \\citep{a,b}, **b**, *i*, `code`."""
    stash = []

    def keep(s):
        stash.append(s)
        return f"\x00{len(stash) - 1}\x00"
    text = MATH_RE.sub(lambda m: keep(unicode_math(m.group(0))), text)
    text = CITE_RE.sub(lambda m: keep(r"\citep{" + ",".join(re.findall(r"@([\w:.-]+)", m.group(1))) + "}"), text)
    text = re.sub(r"`([^`]+)`", lambda m: keep(r"\texttt{" + escape(m.group(1)) + "}"), text)
    text = "".join(keep("$" + unicode_math(c) + "$") if c in MATH_SYM else keep(TEXT_SYM[c]) if c in TEXT_SYM else c
                   for c in text)
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\\emph{\1}", text)
    text = text.replace("[CITATION NEEDED]", r"\textbf{[CITATION NEEDED]}")
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


# "Table I: caption." / "**Table 2.** caption" (not a sentence such as "Table I states ...")
TABLE_CAPTION = re.compile(r"^\s*(?:\*\*)?Table\s+([IVXLC]+|\d+)\s*[.:](?:\*\*)?\s*(.*)$", re.S)


def table(lines, caption=None):
    """Markdown table -> LaTeX. Short columns stay 'l'; text columns become wrapping p{} columns sized by
    their content, so long cells fit the column instead of running off the page. Wide tables span both
    columns of a two-column layout (table*)."""
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines
            if not re.match(r"^\s*\|?\s*:?-{2,}", ln)]
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    longest = [max(len(r[j]) for r in rows) for j in range(ncol)]
    wide = ncol >= 5 or sum(longest) > 160
    short = [n <= 8 for n in longest]  # ids, tags, counts: no wrapping needed
    # share of the width left for the wrapping columns: minus the short columns and the column gaps
    room = max(0.2, 0.97 - 0.07 * sum(short) - 0.025 * ncol)
    text_total = sum(max(8, min(n, 120)) for n, s in zip(longest, short) if not s) or 1
    spec = "".join("l" if s else r">{\raggedright\arraybackslash}p{%.3f\linewidth}" % (room * max(8, min(n, 120)) / text_total)
                   for n, s in zip(longest, short))
    env = "table*" if wide else "table"
    size = r"\small" if len(rows) <= 16 else r"\footnotesize"
    # a float can't break across pages: long tables go out in chunks, the header repeated
    head, data, per = rows[0], rows[1:], int(os.environ.get("TABLE_CHUNK_ROWS", 15))
    chunks = [data[i:i + per] for i in range(0, len(data), per)] or [[]]
    out = []
    for n, chunk in enumerate(chunks):
        out += [rf"\begin{{{env}}}[t]\centering{size}", r"\setlength{\tabcolsep}{4pt}"]
        if caption and n == 0:
            out.append(rf"\caption{{{inline(caption)}}}")
        elif n:
            out.append(r"\vspace{-2pt}{\footnotesize\emph{(continued)}}\par\vspace{2pt}")
        out += [r"\begin{tabular}{" + spec + "}", r"\toprule", " & ".join(inline(c) for c in head) + r" \\", r"\midrule"]
        out += [" & ".join(inline(c) for c in r) + r" \\" for r in chunk]
        out += [r"\bottomrule", r"\end{tabular}", rf"\end{{{env}}}"]
    return out


# project bookkeeping that belongs in the audit trail, not the manuscript
INTERNAL_TERMS = re.compile(
    r"`?\b(?:experiments|research|build|comms|papers)/[\w./-]+`?"   # repository file paths
    r"|\b[Rr]ound\s+\d+\b"                                          # pipeline rounds
    r"|\b[vV]\d{1,2}\b"                                             # internal version tags (v12, V11)
    r"|\bVERIFIED_FINDINGS\b|\bfile of record\b|\b(?:this|previous|preceding|earlier) revision\b")


def internal_terms(md):
    """Distinct internal-bookkeeping terms in the draft's text, most frequent first (references aside)."""
    md = re.split(r"^#+\s*(?:\d+\.?\s*)?(?:References|Bibliography)\s*$", md or "", flags=re.M | re.I)[0]
    found = {}
    for m in INTERNAL_TERMS.finditer(md):
        t = m.group(0).strip("`")
        found[t] = found.get(t, 0) + 1
    return [f"{t} ({n}x)" if n > 1 else t for t, n in sorted(found.items(), key=lambda kv: -kv[1])]


def md_to_latex(md):
    """Small, predictable Markdown -> LaTeX for the drafts this team writes. Returns (title, abstract, body)."""
    title, abstract, body = "Untitled", "", []
    blocks = re.split(r"\n\s*\n", (md or "").replace("\r", ""))
    section, last_para = None, None
    for block in blocks:
        b = block.strip("\n")
        if not b.strip():
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", b.strip())
        if m and "\n" not in b.strip():
            level, head = len(m.group(1)), m.group(2).strip()
            if level == 1 and title == "Untitled" and not body and not abstract:
                title = inline(head)
                continue
            section = re.sub(r"^\d+(\.\d+)*\.?\s+", "", head).lower()
            if section in ("abstract", "references", "bibliography"):
                continue
            if level <= 2 and section.startswith("appendix") and APPENDIX_MARK not in body:
                body.append(APPENDIX_MARK)  # build() moves everything after this behind the references
            star = "*" if APPENDIX_MARK in body else ""  # appendix headings keep their own lettering
            body.append(f"\\{SECTION.get(level, 'paragraph')}{star}{{{inline(re.sub(r'^[0-9.]+ +', '', head))}}}")
            continue
        if section in ("references", "bibliography"):
            continue  # natbib builds the reference list from references.bib
        lines = b.splitlines()
        img = re.match(r"^\s*!\[(.*?)\]\((.+?)\)\s*$", b.strip())
        if img:
            body += [r"\begin{figure}[t]\centering", rf"\includegraphics[width=0.9\linewidth]{{{img.group(2).strip()}}}",
                     rf"\caption{{{inline(img.group(1))}}}", r"\end{figure}"]
        elif all(ln.strip().startswith("|") for ln in lines) and len(lines) >= 2:
            caption = None  # a "Table I: ..." paragraph right before the table becomes its caption
            if last_para is not None and body and body[-1] == last_para[1]:
                m = TABLE_CAPTION.match(last_para[0])
                if m and len(last_para[0]) < 400:
                    body.pop()
                    caption = m.group(2).strip() or None
            body.append("\n".join(table(lines, caption)))  # one block: no blank lines inside the tabular
        elif all(re.match(r"^\s*([-*•])\s+", ln) for ln in lines):
            body += [r"\begin{itemize}"] + [r"\item " + inline(re.sub(r"^\s*[-*•]\s+", "", ln)) for ln in lines] + [r"\end{itemize}"]
        elif all(re.match(r"^\s*\d+[.)]\s+", ln) for ln in lines):
            body += [r"\begin{enumerate}"] + [r"\item " + inline(re.sub(r"^\s*\d+[.)]\s+", "", ln)) for ln in lines] + [r"\end{enumerate}"]
        elif b.strip().startswith("```"):
            code = re.sub(r"^```\w*\n?|\n?```$", "", b.strip())
            body += [r"\begin{verbatim}", code, r"\end{verbatim}"]
        elif b.strip().startswith("$$") or b.strip().startswith(r"\["):
            body.append(b.strip())
        else:
            raw = " ".join(ln.strip() for ln in lines)
            text = inline(raw)
            if section == "abstract":
                abstract += ("\n\n" if abstract else "") + text
            else:
                body.append(text)
                last_para = (raw, text)
                continue
        last_para = None
    abs_tex = f"\\begin{{abstract}}\n{abstract}\n\\end{{abstract}}" if abstract else ""
    return title, abs_tex, "\n\n".join(body)


def page_limit(brief):
    for pat in (r"max(?:imum)?\.?\s*(?:of\s*)?(\d+)\s*pages", r"(\d+)\s*-?\s*pages?\s*(?:of\s*)?(?:main|limit|max)",
                r"page\s*limit\D{0,12}(\d+)", r"(\d+)\s*-\s*page", r"length\W{0,12}(\d+)\s*pages?"):
        m = re.search(pat, brief or "", re.I)
        if m:
            return int(m.group(1))
    venue = re.search(r"^#+\s*Target venue and format\s*\n(.*?)(?=^#|\Z)", brief or "", re.S | re.M | re.I)
    m = re.search(r"\b(\d{1,2})\s*pages?\b", venue.group(1)) if venue else None  # "6 pages" in the venue section
    return int(m.group(1)) if m else None


def template_for(brief):
    """The brief's venue format picks the template: IEEE two-column, else the generic one-column article."""
    m = re.search(r"^#+\s*Target venue and format\s*\n(.*?)(?=^#|\Z)", brief or "", re.S | re.M | re.I)
    venue = m.group(1) if m else brief or ""
    name = "ieee.tex" if re.search(r"\bIEEE", venue) else "article.tex"
    return REPO / "templates" / "latex" / name


def bib_for_build(paper):
    """references.bib with entry types fixed from literature.jsonl venues (conference -> inproceedings,
    arXiv -> misc). Written to build/ only; the team's references.bib is not rewritten."""
    pdir = paper_dir(paper)
    by_key = {e["key"]: e for e in read_jsonl(pdir / "research" / "literature.jsonl")}
    text = read(pdir / "references.bib")

    def fix(m):
        key = m.group(2)
        typ, _ = lit.entry_type((by_key.get(key) or {}).get("venue"))
        return f"@{typ}{{{key}," if typ != "article" else m.group(0)
    text = re.sub(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", fix, text)
    # journal= on a conference entry -> booktitle=, on arXiv -> howpublished=
    out, cur = [], None
    for ln in text.splitlines():
        t = re.match(r"@(\w+)\{", ln)
        if t:
            cur = t.group(1).lower()
        if cur == "inproceedings":
            ln = re.sub(r"^(\s*)journal(\s*=)", r"\1booktitle\2", ln)
        elif cur == "misc":
            ln = re.sub(r"^(\s*)journal(\s*=)", r"\1howpublished\2", ln)
        out.append(ln)
    return "\n".join(out) + "\n"


def engine():
    for name in ("tectonic", "latexmk", "pdflatex"):
        if shutil.which(name):
            return name
    return None


def _run(cmd, cwd, timeout=240):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace", timeout=timeout,
                           stdin=subprocess.DEVNULL)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def compile_pdf(build):
    eng = engine()
    for old in build.glob("paper.*"):  # start clean: stale .aux/.bbl from another template break the build
        if old.suffix not in (".tex", ".pdf"):
            old.unlink(missing_ok=True)
    if not eng:
        return None, False, "no TeX engine installed (sudo apt-get install -y latexmk texlive-latex-extra)"
    if eng == "tectonic":
        rc, log = _run(["tectonic", "--keep-logs", "--keep-intermediates", "paper.tex"], build)
    elif eng == "latexmk":
        rc, log = _run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], build)
    else:
        log = ""
        for step in (["pdflatex", "-interaction=nonstopmode", "paper.tex"], ["bibtex", "paper"],
                     ["pdflatex", "-interaction=nonstopmode", "paper.tex"], ["pdflatex", "-interaction=nonstopmode", "paper.tex"]):
            rc, out = _run(step, build)
            log += out
        rc = 0 if (build / "paper.pdf").exists() else 1
    return eng, rc == 0 and (build / "paper.pdf").exists(), log


def pages(build, log):
    """(total pages, main-text pages before the references). Read from the .aux labels the template
    sets (refsstart, lastpage), which every engine writes; the log / PDF are fallbacks."""
    aux = read(build / "paper.aux")
    lab = lambda name: re.search(r"\\newlabel\{" + name + r"\}\{\{(?:[^{}]|\{[^{}]*\})*\}\{(\d+)\}", aux)  # page field may nest: {\mbox {X-D}}  # noqa: E731
    # the larger of the lastpage label and the compiler's count: floats deferred to the end of the document
    # land after the label (tectonic writes no "Output written" line, so the label alone is used there)
    m = re.search(r"Output written on paper\.pdf \((\d+) pages?", read(build / "paper.log") + log)
    counts = [int(m.group(1))] if m else []
    if lab("lastpage"):
        counts.append(int(lab("lastpage").group(1)))
    total = max(counts) if counts else None
    if total is None:
        if (build / "paper.pdf").exists():
            counts = re.findall(rb"/Type\s*/Pages[^>]*?/Count\s+(\d+)", (build / "paper.pdf").read_bytes())
            total = max(map(int, counts)) if counts else None
    ref = lab("refsstart")
    main = int(ref.group(1)) - 1 if ref else total  # references start on a fresh page (\clearpage)
    return total, main


def package(paper):
    """build/reproducibility_package.zip: the PDF with the data, codebook, ledger, results, scripts and
    protocol check it rests on, plus MANIFEST.json (sha256 of every file, coded tallies). Archived files
    (experiments/archive/) and versioned copies stay out, so the package holds one consistent version."""
    import hashlib
    import zipfile
    pdir = paper_dir(paper)
    exp = pdir / "experiments"
    files = [pdir / "build" / "paper.pdf", exp / "PROTOCOL_CHECK.md"]
    for sub, pats in (("data", ("*.csv", "*.json")), ("results", ("*.json", "*.csv", "*.md", "*.tex")),
                      ("scripts", ("*.py", "*.txt"))):
        files += sorted(p for pat in pats for p in (exp / sub).glob(pat)
                        if not re.match(r"coded_evidence_.+\.csv$", p.name))
    files = [f for f in files if f.is_file()]
    if not files:
        return None
    out = pdir / "build" / "reproducibility_package.zip"
    manifest = {"paper": paper, "timestamp": now_iso(), "files": {}}
    summary = exp / "results" / "coding_summary.json"
    if summary.exists():
        s = json.loads(read(summary) or "{}")
        manifest["tallies"] = {k: s.get(k) for k in ("units", "dimensions", "decisions", "sources", "by_status")}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            arc = f.relative_to(pdir).as_posix()
            z.write(f, arc)
            manifest["files"][arc] = hashlib.sha256(f.read_bytes()).hexdigest()
        z.writestr("MANIFEST.json", json.dumps(manifest, indent=1))
    return {"path": out.relative_to(pdir).as_posix(), "files": len(files)}


def build(paper):
    pdir = paper_dir(paper)
    out = pdir / "build"
    out.mkdir(exist_ok=True)
    tmpl = read(os.environ.get("LATEX_TEMPLATE") or template_for(read(pdir / "brief.md")))
    title, abstract, body = md_to_latex(read(pdir / "draft.md"))
    body, _, appendix = body.partition(APPENDIX_MARK)
    tex = tmpl.replace("$title$", title).replace("$abstract$", abstract).replace("$body$", body)
    if appendix.strip():  # after the reference list, before the last-page label
        tex = tex.replace(r"\label{lastpage}", "\\clearpage\n" + appendix.strip() + "\n" + r"\label{lastpage}")
    if r"\citep{" not in abstract + body:  # nothing cited: an empty reference list is a LaTeX error
        tex = re.sub(r"^\\(bibliographystyle|bibliography)\{[^}]*\}\s*$", "", tex, flags=re.M)
    (out / "paper.tex").write_text(tex, encoding="utf-8")
    (out / "references.bib").write_text(bib_for_build(paper), encoding="utf-8")
    eng, ok, log = compile_pdf(out)
    report = {"timestamp": now_iso(), "engine": eng, "compiled": ok, "limit": page_limit(read(pdir / "brief.md"))}
    if eng is None:
        report["why"] = log
    elif not ok:
        errs = [ln for ln in (read(out / "paper.log") + log).splitlines() if ln.startswith("!") or "error:" in ln.lower()]
        report["why"] = "compile failed: " + ("; ".join(errs[:3]) or log[-300:])
    if ok:
        report["pages_total"], report["pages_main"] = pages(out, log)
        final = read(out / "paper.log") or log  # the last pass only: early passes always warn before bibtex ran
        undefined = sorted(set(re.findall(r"Citation [`'](\S+?)' (?:on page|undefined)", final)))
        report["undefined_citations"] = undefined
        report["internal_terms"] = internal_terms(read(pdir / "draft.md")) if os.environ.get("INTERNAL_TERMS_CHECK", "1") != "0" else []
        report["pass"] = ((report["limit"] is None or (report["pages_main"] or 0) <= report["limit"]) and not undefined
                          and not report["internal_terms"])
        report["package"] = package(paper)
    (out / "latex_check.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(json.dumps(build(sys.argv[1]), indent=1))
