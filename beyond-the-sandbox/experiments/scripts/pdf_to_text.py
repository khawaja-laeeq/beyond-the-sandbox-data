"""Extract text from a cached PDF: pdf_to_text.py IN.pdf OUT.txt (pypdf; read-only)."""
import sys

from pypdf import PdfReader

r = PdfReader(sys.argv[1])
with open(sys.argv[2], "w") as f:
    for i, p in enumerate(r.pages, 1):
        f.write(f"\n[[page {i}]]\n" + (p.extract_text() or ""))
print(len(r.pages), "pages")
