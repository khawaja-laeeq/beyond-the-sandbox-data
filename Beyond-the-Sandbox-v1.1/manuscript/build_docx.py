"""Build revised_manuscript.docx from revised_manuscript.md (pandoc) and apply table layout. Then convert to PDF with
LibreOffice if it is installed. Number tags (HTML comments) are dropped by pandoc. Run from any directory:
    python3 manuscript/build_docx.py   (needs pandoc on PATH and python-docx)"""
import subprocess, os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
H=os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
subprocess.run(["pandoc","revised_manuscript.md","-o","_raw.docx","--resource-path=."+os.pathsep+".."],check=True)
d=Document('_raw.docx')
for sec in d.sections:
    sec.page_width=Inches(8.27); sec.page_height=Inches(11.69)
    sec.left_margin=sec.right_margin=Inches(0.8); sec.top_margin=sec.bottom_margin=Inches(0.8)
usable=8.27-1.6
tw=lambda x: str(int(x*1440))
for t in d.tables:
    hdr=[c.text.strip() for c in t.rows[0].cells]; n=len(hdr)
    if n==9: rel=[1.45,.32,.32,.32,.32,.32,1.2,1.15,1.1]
    elif n==6 and hdr[0].startswith('Claimed'): rel=[1.05,1.1,1.45,0.95,1.1,1.0]
    elif n==6 and hdr[0]=='Unit': rel=[1.3,1.15,1.05,1.15,0.8,1.0]
    elif n==6: rel=[0.5,0.85,1.6,1.6,1.1,0.6]
    elif n==5: rel=[2.7,0.9,0.6,1.1,1.1]
    elif n==3 and hdr[0]=='Label': rel=[0.75,0.95,4.9]
    elif n==3: rel=[2.4,2.1,2.1]
    elif n==4: rel=[3.0,1.2,1.2,1.2]
    elif n==2: rel=[3.6,3.0]
    else: rel=[1]*n
    k=usable/sum(rel); ws=[r*k for r in rel]
    tbl=t._tbl; tblPr=tbl.tblPr
    for tag in ('w:tblW','w:tblLayout'):
        for e in tblPr.findall(qn(tag)): tblPr.remove(e)
    w=OxmlElement('w:tblW'); w.set(qn('w:w'),tw(usable)); w.set(qn('w:type'),'dxa'); tblPr.append(w)
    lay=OxmlElement('w:tblLayout'); lay.set(qn('w:type'),'fixed'); tblPr.append(lay)
    t.alignment=WD_TABLE_ALIGNMENT.CENTER
    grid=tbl.tblGrid
    for gc in list(grid): grid.remove(gc)
    for x in ws:
        gc=OxmlElement('w:gridCol'); gc.set(qn('w:w'),tw(x)); grid.append(gc)
    small=8 if n>=6 else 9
    for ri,row in enumerate(t.rows):
        trPr=row._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:cantSplit'))
        if ri==0: trPr.append(OxmlElement('w:tblHeader'))
        for i,c in enumerate(row.cells):
            tcPr=c._tc.get_or_add_tcPr()
            for e in tcPr.findall(qn('w:tcW')): tcPr.remove(e)
            x=OxmlElement('w:tcW'); x.set(qn('w:w'),tw(ws[i])); x.set(qn('w:type'),'dxa'); tcPr.insert(0,x)
            for para in c.paragraphs:
                para.paragraph_format.space_after=Pt(1); para.paragraph_format.space_before=Pt(1)
                if ri<len(t.rows)-1 and len(t.rows)<14: para.paragraph_format.keep_with_next=True
                for r in para.runs:
                    r.font.size=Pt(small)
                    if ri==0: r.font.bold=True
    b=OxmlElement('w:tblBorders')
    for e in ('top','bottom','insideH'):
        x=OxmlElement(f'w:{e}'); x.set(qn('w:val'),'single'); x.set(qn('w:sz'),'4'); x.set(qn('w:color'),'999999'); b.append(x)
    tblPr.append(b)
for para in d.paragraphs:
    tx=para.text.strip()
    if tx.startswith(('Table ','Reading guide','Figure')): para.paragraph_format.keep_with_next=True
d.save('revised_manuscript.docx'); os.remove('_raw.docx')
import shutil
if shutil.which("soffice"):
    subprocess.run(["soffice","--headless","--convert-to","pdf","revised_manuscript.docx"],check=True,capture_output=True)
else:
    print("LibreOffice (soffice) not found: DOCX built, PDF not built. Make the PDF from the DOCX in Word.")
