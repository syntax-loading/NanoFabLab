# -*- coding: utf-8 -*-
"""Build a print-ready ENGLISH DOCX for the Lab3 gate-formation checklist."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CJK = "Microsoft YaHei"
LATIN = "Segoe UI"

doc = Document()
st = doc.styles["Normal"]
st.font.name = LATIN
st.font.size = Pt(9.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), CJK)
st.paragraph_format.space_after = Pt(2)
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.line_spacing = 1.05

sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin = sec.bottom_margin = Cm(1.3)
sec.left_margin = sec.right_margin = Cm(1.5)
USABLE = 18.0


def fnt(run, size=9.5, bold=False, color=None, mono=False):
    run.font.name = "Consolas" if mono else LATIN
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), CJK)


def rich(p, text, size=9.5, bold=False, color=None):
    for i, seg in enumerate(text.split("**")):
        if seg:
            fnt(p.add_run(seg), size, bold or i % 2 == 1, color)


def para(text="", size=9.5, bold=False, color=None, before=0, after=2, indent=0.0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    rich(p, text, size, bold, color)
    return p


def h1(text, break_before=False):
    p = doc.add_paragraph()
    if break_before:
        p.paragraph_format.page_break_before = True
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    fnt(p.add_run(text), 12, True, (0x1B, 0x24, 0x30))
    return p


def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    fnt(p.add_run(text), 10, True, (0x2C, 0x4A, 0x7A))
    return p


def shade(cell, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shd)


def onecell(text, fill="F4F7FB", size=9.5):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    c = t.cell(0, 0)
    c.width = Cm(USABLE)
    shade(c, fill)
    c.paragraphs[0].paragraph_format.space_after = Pt(0)
    rich(c.paragraphs[0], text, size)
    return t


def checkbox(text, size=9.5, indent=0.35):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_after = Pt(1)
    fnt(p.add_run("☐  "), size + 1)
    rich(p, text, size)
    return p


def cell_margins(table, top=25, bottom=25, left=55, right=55):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for side, w in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement("w:" + side)
        el.set(qn("w:w"), str(w))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    look = tblPr.find(qn("w:tblLook"))
    if look is not None:
        look.addprevious(mar)
    else:
        tblPr.append(mar)


def row_props(row, header=False):
    trPr = row._tr.get_or_add_trPr()
    trPr.insert(0, OxmlElement("w:cantSplit"))
    if header:
        trPr.append(OxmlElement("w:tblHeader"))


def table(headers, rows, widths, size=8.5, height=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.autofit = False
    cell_margins(t)
    row_props(t.rows[0], header=True)
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.width = Cm(widths[i])
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        shade(c, "E8EFF7")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        fnt(p.add_run(h), size, True)
    for row in rows:
        cells = t.add_row().cells
        if height:
            t.rows[-1].height = Cm(height)
        row_props(t.rows[-1])
        for i, v in enumerate(row):
            cells[i].width = Cm(widths[i])
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            rich(p, str(v), size)
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    return t


# ══════════════════════════════ TITLE ══════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(1)
fnt(p.add_run("LAB3  Gate Formation"), 19, True, (0x1B, 0x24, 0x30))
fnt(p.add_run("   Lab-Day Checklist"), 13, False, (0x5B, 0x66, 0x73))

para("Goal: define the gate lines in the SiO₂ hard mask, then use RIE to etch through "
     "hard mask → p⁺ poly → TiN (PFET only) and **stop on the gate oxide**. "
     "Window 10:00–16:00 (lunch included). **The 12:30 post-develop inspection is the only rework window.**",
     size=8.8, color=(0x3A, 0x45, 0x52), after=4)

para("Date ____________   Name ____________   Wafer ID ____________   TA ____________   "
     "Stepper # ________   RIE # ________", size=9, after=2)

# ══════════════════════════════ 0 ══════════════════════════════
h1("0   Before you enter the cleanroom")
for t in [
    "Manual read; the four thicknesses in Section 1 are filled in",
    "Recipe ID, dose and focus **written down on paper** (no time to look things up inside)",
    "Over-etch time and gate-oxide loss already calculated (Section 2)",
    "Stepper and RIE slots confirmed",
    "Dress code: long trousers, closed shoes, no jewellery, no heavy makeup",
    "Bring: lint-free pen, a printed copy of this checklist",
]:
    checkbox(t)

# ══════════════════════════════ 1 ══════════════════════════════
h1("1   Key parameters (fill in before entry)")
table(
    ["Item", "Value", "Source"],
    [
        ["Hard mask SiO₂ thickness", "________ nm", "Manual / TA"],
        ["p⁺ poly thickness", "________ nm", "Manual / TA"],
        ["TiN thickness", "________ nm", "Manual / TA"],
        ["**Gate oxide thickness**", "________ nm", "Manual / TA"],
        ["poly etch rate", "________ nm/min", "Manual"],
        ["Selectivity to gate oxide", "________ : 1", "Manual"],
        ["Exposure dose", "________ mJ/cm²", "TA"],
        ["Focus", "________ µm", "TA"],
        ["Soft bake  T / t", "______ °C / ______ s", "Manual"],
        ["PEB  T / t", "______ °C / ______ s", "Manual"],
        ["Develop  chemistry / time", "__________ / ______ s", "Manual"],
        ["Hard bake  T / t", "______ °C / ______ s", "Manual"],
    ],
    [6.4, 6.0, 5.6],
)
para("", after=1)
para("**Four questions you must ask the TA:**", size=9.2, before=2)
for t in [
    "What is the gate-oxide thickness?",
    "How thick are poly / TiN / hard mask?",
    "Which RIE recipe? Same chamber with gas swaps, or separate chambers?",
    "Are the alignment marks still visible under the blanket stack?",
]:
    checkbox(t)

# ══════════════════════════════ 2 ══════════════════════════════
h1("2   Two numbers you must calculate on site")
onecell("**① Main etch time**      t_main = poly thickness ÷ etch rate = ________ ÷ ________ = ________ s")
para("", after=1)
onecell("**② Over-etch and gate-oxide budget**")
for line in [
    "t_over = t_main × (10 – 30%)   = ________ s",
    "Δox = ( r_Si ÷ S ) × t_over   = ( ________ ÷ ________ ) × ________ = ________ nm",
    "Oxide remaining = t_ox − Δox  = ________ − ________ = ________ nm",
]:
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    c = t.cell(0, 0)
    c.width = Cm(USABLE)
    shade(c, "F4F7FB")
    pp = c.paragraphs[0]
    pp.paragraph_format.space_after = Pt(0)
    fnt(pp.add_run(line), 9, False)
para("**Criterion: oxide remaining ≥ 70 % of the original thickness.** "
     "If the numbers do not work, ask the TA for a better selectivity — do not just etch.",
     size=8.8, before=3, color=(0xA0, 0x3A, 0x2A))

# ══════════════════════════════ 3 ══════════════════════════════
h1("3   Timeline", break_before=True)
table(
    ["Time", "Stage", "Action", "✓", "Actual"],
    [
        ["10:00", "—", "Safety briefing / gowning", "☐", ""],
        ["10:35", "A", "Take wafer, incoming inspection", "☐", ""],
        ["10:50", "B", "Dehydration bake + HMDS", "☐", ""],
        ["11:05", "B", "Spin coat + soft bake", "☐", ""],
        ["11:25", "C", "Load wafer, coarse alignment", "☐", ""],
        ["11:45", "C", "Fine alignment + set parameters", "☐", ""],
        ["11:55", "C", "Field-by-field exposure", "☐", ""],
        ["12:10", "D", "PEB", "☐", ""],
        ["12:15", "D", "Develop + rinse + spin dry", "☐", ""],
        ["12:20", "D", "Hard bake", "☐", ""],
        ["**12:30**", "**D**", "**★ Post-develop inspection (decision point)**", "☐", ""],
        ["12:45", "—", "Lunch", "☐", ""],
        ["13:35", "E", "RIE load, pump down, confirm recipe", "☐", ""],
        ["13:50", "E", "Step 1  breakthrough", "☐", ""],
        ["13:55", "E", "Step 2  main poly etch (watch endpoint)", "☐", ""],
        ["14:10", "E", "Step 3  TiN etch (PFET areas only)", "☐", ""],
        ["14:25", "E", "Over-etch", "☐", ""],
        ["14:35", "F", "Post-etch inspection (microscope)", "☐", ""],
        ["14:45", "F", "Resist strip: O₂ ash", "☐", ""],
        ["15:00", "F", "Resist strip: wet clean + rinse", "☐", ""],
        ["15:15", "F", "Metrology: CD-SEM / optical", "☐", ""],
        ["15:40", "—", "Data, handover, gown out", "☐", ""],
    ],
    [2.2, 1.5, 9.9, 1.2, 3.2],
    size=8.2,
)

# ══════════════════════════════ 4 ══════════════════════════════
h1("4   Stage-by-stage checks and records")

h2("Stage A · Incoming (10:35)")
for t in [
    "Wafer ID matches the handover sheet",
    "Microscope: no large particles, no scratches, no upstream defects",
    "Uniform surface colour (uniform stack thickness)",
    "Hard-mask thickness recorded",
]:
    checkbox(t)
table(["Check", "Observed"], [["Surface defects", ""], ["Edge condition", ""], ["Remarks", ""]],
      [5.0, 13.0], height=0.72)

h2("Stage B · Surface preparation and coating (10:50)")
for t in [
    "Dehydration bake: ________ °C / ________ s",
    "HMDS: ☐ vapour  ☐ spin; time ________",
    "Spin coat: ________ rpm; visually uniform, no streaks",
    "Soft bake: ________ °C / ________ s; no bubbles, no haze",
    "No pronounced edge bead",
]:
    checkbox(t)
para("Ask yourself: if HMDS is skipped, will the problem show up first in **develop** or in **etch**? "
     "____________________", size=8.8, before=2, color=(0x4A, 0x54, 0x60))

h2("Stage C · Alignment and exposure (11:25)")
for t in [
    "Pre-alignment OK (notch located)",
    "Coarse alignment: OK  /  failed ______ times",
    "Fine-alignment residual: ______ nm (x)   ______ nm (y)",
    "Dose ______ mJ/cm², focus ______ µm, illumination ______",
    "Number of fields exposed ______",
]:
    checkbox(t)
para("**If alignment fails: first confirm the marks are visible; do not blindly retry more than 3 times** "
     "(it burns machine time).", size=8.8, before=2, color=(0xA0, 0x3A, 0x2A))

h2("Stage D · Develop and inspect (12:10)   ★ the only decision point")
for t in [
    "PEB: ________ °C / ________ s",
    "Develop: ________ s; DI rinse; spin dry",
    "Hard bake: ________ °C / ________ s",
    "Microscope inspection done",
]:
    checkbox(t)
table(
    ["Check", "Result", "Pass"],
    [
        ["Lines continuous, no breaks", "", "☐"],
        ["No scum / residue", "", "☐"],
        ["No bridging", "", "☐"],
        ["CD (top view)", "________ µm", "☐"],
        ["Defects", "", "☐"],
    ],
    [6.6, 8.4, 3.0],
)
para("", after=1)
para("**Decision — tick exactly one:**", size=9.2, before=2)
checkbox("**Pass → go to RIE** (irreversible)")
checkbox("**Acceptable deviation → record and continue** (deviation: ______________________)")
checkbox("**Fail → strip and redo** (estimate +______ min)")
para("Once you enter the RIE there is no second chance. "
     "**This tick is the single most important action of the day.**",
     size=8.8, before=2, color=(0xA0, 0x3A, 0x2A))

h2("Stage E · RIE (13:35)")
table(
    ["Step", "Recipe", "Pressure", "Power", "Gas / flow", "Time", "Endpoint"],
    [
        ["1 Breakthrough", "", "", "", "", "", ""],
        ["2 Main poly", "", "", "", "", "", ""],
        ["3 TiN", "", "", "", "", "", ""],
        ["4 Over-etch", "", "", "", "", "", ""],
    ],
    [2.7, 2.6, 1.9, 1.9, 4.4, 1.8, 2.7],
    height=0.62,
)
para("", after=1)
for t in [
    "Hard mask fully open (no residue)",
    "PFET areas: TiN exposed and cleared",
    "NFET areas: gate oxide not over-etched",
    "Endpoint trace saved / recorded",
    "No obvious notching (if visible)",
]:
    checkbox(t)
para("Risk: the field sits on 145 nm BOX (a perfect insulator) — **charge has nowhere to bleed, "
     "so notching risk is higher than in bulk CMOS**.", size=8.8, before=2, color=(0x4A, 0x54, 0x60))

h2("Stage F · Resist strip and metrology (14:45)")
for t in [
    "O₂ ash: ________ W / ________ s (downstream, no bias)",
    "Wet clean: __________ ; temperature ______ °C ; time ______",
    "DI rinse (≥ 80 °C recommended, to remove Cl)",
    "**Hard-mask cap still on top of the gate** (colour contrast under the microscope)",
    "No resist residue",
]:
    checkbox(t)
table(
    ["Measurement", "Value", "Method"],
    [
        ["CD after etch", "________ µm", "CD-SEM"],
        ["CD after develop (back-fill)", "________ µm", "CD-SEM / optical"],
        ["**CD bias**", "________ nm", "calculated"],
        ["Profile angle", "________ °", "X-SEM (if done)"],
        ["poly sheet resistance", "________ Ω/sq", "4-point probe (if done)"],
    ],
    [6.2, 7.4, 4.4],
    height=0.6,
)

# ══════════════════════════════ 5 ══════════════════════════════
h1("5   Anomalies and deviations")
table(["Time", "Observation", "Likely cause", "Action", "Affects later steps?"],
      [["", "", "", "", ""] for _ in range(4)],
      [1.8, 4.4, 5.0, 4.4, 2.4], height=0.78)

# ══════════════════════════════ 6 ══════════════════════════════
h1("6   Handover sheet")
for t in [
    "Wafer ID ____________   handed to ____________   time ________",
    "Gate CD ____________   profile: ☐ not measured  ☐ normal  ☐ abnormal",
    "Known defects: ________________________________________________",
    "Notes for LAB4: _______________________________________________",
]:
    para(t, size=9.2, after=2)
para("", after=1)
checkbox("Wafer intact and uncontaminated")
checkbox("Data complete (endpoint trace included)")

# ══════════════════════════════ 7 ══════════════════════════════
h1("7   Failure quick reference")
table(
    ["Symptom", "Most likely cause", "What to do"],
    [
        ["Alignment alarms repeatedly", "Buried marks / weak signal, wafer misplaced", "Ask TA about mark visibility; do not blind-retry"],
        ["Whole field blurred", "Focus off, wafer not flat, particle on chuck", "Check chuck and wafer flatness"],
        ["CD off in the same direction everywhere", "Dose, or PEB / develop conditions", "Check parameter consistency"],
        ["CD off only locally", "Flatness, topography, particles", "Investigate locally"],
        ["Residue after develop", "Under-baked, under-developed, over-exposed", "Decide whether to redo"],
        ["Broken lines / bridging", "Dose error, mask defect", "Record and redo"],
        ["CD wider after etch", "Hard mask eroded laterally, polymer fence", "Look at the profile"],
        ["CD narrower after etch", "Tapered sidewall, over-etch", "Look at the profile"],
        ["PFET areas shorted", "TiN not cleared", "Rework or scrap — must be recorded"],
        ["Gate leakage (only seen electrically)", "Gate oxide punched through", "Irreversible — write it in the handover"],
    ],
    [4.6, 7.4, 6.0],
    size=8.3,
)

# ══════════════════════════════ 8 ══════════════════════════════
h1("8   One last look before you leave")
for t in [
    "Did I make a **real decision at 12:30** — against a criterion, not a gut feeling?",
    "Are the **endpoint trace and all parameters** written down? (No record = it never happened.)",
    "What will the person doing **LAB4** learn from my handover sheet?",
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.space_after = Pt(2)
    fnt(p.add_run("▍ "), 9.5, False, (0x2C, 0x4A, 0x7A))
    rich(p, t, 9.2)

# ── footer ──
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fnt(fp.add_run("LAB3 Gate Formation · Lab-Day Checklist      Page "), 8, False, (0x8D, 0x99, 0xA8))
r = fp.add_run()
fnt(r, 8, False, (0x8D, 0x99, 0xA8))
f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " PAGE "
f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
r._r.append(f1); r._r.append(it); r._r.append(f2)
fnt(fp.add_run(" of "), 8, False, (0x8D, 0x99, 0xA8))
r2 = fp.add_run()
fnt(r2, 8, False, (0x8D, 0x99, 0xA8))
g1 = OxmlElement("w:fldChar"); g1.set(qn("w:fldCharType"), "begin")
g2 = OxmlElement("w:instrText"); g2.set(qn("xml:space"), "preserve"); g2.text = " NUMPAGES "
g3 = OxmlElement("w:fldChar"); g3.set(qn("w:fldCharType"), "end")
r2._r.append(g1); r2._r.append(g2); r2._r.append(g3)

out = "labs/LAB3_checklist_EN.docx"
doc.save(out)

chk = Document(out)
texts = [p.text for p in chk.paragraphs]
assert any("Lab-Day Checklist" in t for t in texts)
assert any("12:30" in t for t in texts)
assert len(chk.tables) >= 9
print("OK  paragraphs=%d  tables=%d" % (len(chk.paragraphs), len(chk.tables)))
