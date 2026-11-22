# -*- coding: utf-8 -*-
"""Build a print-ready DOCX for the Lab3 gate-formation checklist."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CJK = "微软雅黑"
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
USABLE = 18.0  # cm


def fnt(run, size=9.5, bold=False, color=None, mono=False):
    run.font.name = "Consolas" if mono else LATIN
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)
    rPr = run._element.get_or_add_rPr()
    rPr.get_or_add_rFonts().set(qn("w:eastAsia"), CJK)


def rich(p, text, size=9.5, bold=False, color=None):
    for i, seg in enumerate(text.split("**")):
        if not seg:
            continue
        fnt(p.add_run(seg), size, bold or i % 2 == 1, color)


def para(text="", size=9.5, bold=False, color=None, before=0, after=2, indent=0.0, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    if align:
        p.alignment = align
    rich(p, text, size, bold, color)
    return p


def h1(text):
    p = doc.add_paragraph()
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


def box(text, fill="F4F7FB", size=9.5):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    c = t.cell(0, 0)
    c.width = Cm(USABLE)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    c._tc.get_or_add_tcPr().append(shd)
    c.paragraphs[0].paragraph_format.space_after = Pt(1)
    rich(c.paragraphs[0], text, size)
    return t


def checkbox(text, size=9.5, indent=0.35):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_after = Pt(1)
    fnt(p.add_run("☐  "), size + 1)
    rich(p, text, size)
    return p


def shade(cell, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shd)


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
    """Keep rows intact across page breaks; repeat header rows."""
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


# ══════════════════════════════ 标题 ══════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(1)
fnt(p.add_run("LAB3  Gate Formation"), 19, True, (0x1B, 0x24, 0x30))
fnt(p.add_run("　实验日检查清单"), 13, False, (0x5B, 0x66, 0x73))

para("目标：在 SiO₂ 硬掩模上定义栅条，用 RIE 依次刻穿 硬掩模 → p⁺ poly → TiN（仅 PFET），"
     "**停在栅氧上**。窗口 10:00–16:00（含午饭）。**12:30 的显影后检验，是唯一可返工的窗口。**",
     size=8.8, color=(0x3A, 0x45, 0x52), after=4)

para("日期 ____________　姓名 ____________　片号 ____________　助教 ____________　"
     "步进机 # ________　RIE # ________", size=9, after=2)

# ══════════════════════════════ 0 ══════════════════════════════
h1("0　出发前（进洁净室之前）")
for t in [
    "手册已读，第 1 节的四个厚度已填好",
    "配方号、剂量、焦距已**写在纸上**（洁净室里没时间查资料）",
    "过刻时间与栅氧损耗已算好（见第 2 节）",
    "步进机 / RIE 机时已确认预约",
    "着装：长裤、包脚鞋、不戴首饰、不化浓妆",
    "携带：无尘笔、本清单打印件",
]:
    checkbox(t)

# ══════════════════════════════ 1 ══════════════════════════════
h1("1　关键参数速查（进场前填满）")
table(
    ["项目", "数值", "来源"],
    [
        ["硬掩模 SiO₂ 厚度", "________ nm", "手册 / 助教"],
        ["p⁺ poly 厚度", "________ nm", "手册 / 助教"],
        ["TiN 厚度", "________ nm", "手册 / 助教"],
        ["**栅氧厚度**", "________ nm", "手册 / 助教"],
        ["poly 刻蚀速率", "________ nm/min", "手册"],
        ["对栅氧选择比", "________ : 1", "手册"],
        ["曝光剂量", "________ mJ/cm²", "助教"],
        ["焦距（focus）", "________ µm", "助教"],
        ["软烘　温度 / 时间", "______ °C / ______ s", "手册"],
        ["PEB　温度 / 时间", "______ °C / ______ s", "手册"],
        ["显影　药液 / 时间", "__________ / ______ s", "手册"],
        ["硬烘　温度 / 时间", "______ °C / ______ s", "手册"],
    ],
    [6.4, 6.0, 5.6],
)
para("", after=1)
para("**四个必问助教的问题：**", size=9.2, before=2)
for t in [
    "栅氧厚度是多少？",
    "poly / TiN / 硬掩模各多厚？",
    "RIE 用哪个配方号？是同一腔体换气，还是分腔？",
    "对准标记被叠层盖住后，信号还够吗？",
]:
    checkbox(t)

# ══════════════════════════════ 2 ══════════════════════════════
h1("2　两个必须现场算的数")
box("**① 主刻时间**　　 t_main = poly 厚度 ÷ 刻蚀速率 = ________ ÷ ________ = ________ s", "F4F7FB")
para("", after=1)
box("**② 过刻与栅氧损耗**", "F4F7FB")
for line in [
    "t_over = t_main × (10 ~ 30%)  = ________ s",
    "Δox = ( r_Si ÷ S ) × t_over = ( ________ ÷ ________ ) × ________ = ________ nm",
    "栅氧剩余 = 栅氧厚度 − Δox = ________ − ________ = ________ nm",
]:
    first = doc.add_table(rows=1, cols=1)
    first.style = "Table Grid"
    c = first.cell(0, 0)
    c.width = Cm(USABLE)
    shade(c, "F4F7FB")
    pp = c.paragraphs[0]
    pp.paragraph_format.space_after = Pt(0)
    fnt(pp.add_run(line), 9, False)
para("**判据：栅氧剩余 ≥ 原厚度的 70% 才算安全。** 算不过就找助教调选择比，不要硬刻。",
     size=8.8, before=3, color=(0xA0, 0x3A, 0x2A))

# ══════════════════════════════ 3 ══════════════════════════════
h1("3　时间轴")
table(
    ["时间", "阶段", "动作", "✓", "实际"],
    [
        ["10:00", "—", "安全培训 / 更衣", "☐", ""],
        ["10:35", "A", "取片、来料检查", "☐", ""],
        ["10:50", "B", "脱水烘 + HMDS", "☐", ""],
        ["11:05", "B", "甩胶 + 软烘", "☐", ""],
        ["11:25", "C", "装片、粗对准", "☐", ""],
        ["11:45", "C", "精对准 + 设参数", "☐", ""],
        ["11:55", "C", "逐场曝光", "☐", ""],
        ["12:10", "D", "PEB", "☐", ""],
        ["12:15", "D", "显影 + 冲洗 + 甩干", "☐", ""],
        ["12:20", "D", "硬烘", "☐", ""],
        ["**12:30**", "**D**", "**★ 显影后检验（决策点）**", "☐", ""],
        ["12:45", "—", "午饭", "☐", ""],
        ["13:35", "E", "RIE 装片、抽真空、确认配方", "☐", ""],
        ["13:50", "E", "段1　破口", "☐", ""],
        ["13:55", "E", "段2　主刻 poly（看终点）", "☐", ""],
        ["14:10", "E", "段3　刻 TiN（仅 PFET 区）", "☐", ""],
        ["14:25", "E", "过刻", "☐", ""],
        ["14:35", "F", "出片检验（显微镜）", "☐", ""],
        ["14:45", "F", "去胶：O₂ 灰化", "☐", ""],
        ["15:00", "F", "去胶：湿法 + 冲洗", "☐", ""],
        ["15:15", "F", "量测：CD-SEM / 光学", "☐", ""],
        ["15:40", "—", "数据整理、交接、更衣出", "☐", ""],
    ],
    [2.2, 1.5, 9.9, 1.2, 3.2],
    size=8.2,
)

# ══════════════════════════════ 4 ══════════════════════════════
h1("4　分阶段检查与记录")

h2("阶段 A · 来料（10:35）")
for t in [
    "片号与交接单一致",
    "显微镜：无大颗粒、无划伤、无前道异常",
    "表面颜色均匀（叠层厚度均匀）",
    "硬掩模厚度已记录",
]:
    checkbox(t)
table(["检查项", "实测 / 观察"], [["表面缺陷", ""], ["边缘状态", ""], ["备注", ""]],
      [5.0, 13.0], height=0.72)

h2("阶段 B · 表面准备与涂胶（10:50）")
for t in [
    "脱水烘：________ °C / ________ s",
    "HMDS：☐ 气相　☐ 旋涂；时间 ________",
    "甩胶：转速 ________ rpm；目视均匀、无色差条纹",
    "软烘：________ °C / ________ s；表面无气泡、无云雾",
    "边缘无明显厚边",
]:
    checkbox(t)
para("自检：如果省略 HMDS，问题会先在 **显影** 还是 **刻蚀** 暴露？________________________",
     size=8.8, before=2, color=(0x4A, 0x54, 0x60))

h2("阶段 C · 对准与曝光（11:25）")
for t in [
    "预对准成功（notch 定位）",
    "粗对准：成功　/　失败 ______ 次",
    "精对准残差：______ nm（x）　______ nm（y）",
    "剂量 ______ mJ/cm²，焦距 ______ µm，照明模式 __________",
    "曝光场数 ______",
]:
    checkbox(t)
para("**若对准失败：先确认标记可见性，不要盲目重试超过 3 次**（会累积机时损失）。",
     size=8.8, before=2, color=(0xA0, 0x3A, 0x2A))

h2("阶段 D · 显影与检验（12:10）　★ 全程唯一决策点")
for t in [
    "PEB：________ °C / ________ s",
    "显影：________ s；DI 冲洗；甩干",
    "硬烘：________ °C / ________ s",
    "显微镜检查完成",
]:
    checkbox(t)
table(
    ["检查项", "结果", "合格"],
    [
        ["线条连续、无断线", "", "☐"],
        ["无残渣（scum）", "", "☐"],
        ["无桥接", "", "☐"],
        ["CD（顶视）", "________ µm", "☐"],
        ["缺陷", "", "☐"],
    ],
    [6.6, 8.4, 3.0],
)
para("", after=1)
para("**决策（必须勾一个）：**", size=9.2, before=2)
checkbox("**合格 → 进 RIE**（不可逆）")
checkbox("**可接受偏差 → 记录后继续**（偏差：____________________________）")
checkbox("**不合格 → 去胶重做**（预计 +______ min）")
para("一旦进 RIE，就没有第二次机会。**这一栏的勾选，是全程最重要的一个动作。**",
     size=8.8, before=2, color=(0xA0, 0x3A, 0x2A))

h2("阶段 E · RIE（13:35）")
table(
    ["段", "配方号", "压力", "功率", "气体 / 流量", "时间", "终点信号"],
    [
        ["1 破口", "", "", "", "", "", ""],
        ["2 主刻 poly", "", "", "", "", "", ""],
        ["3 刻 TiN", "", "", "", "", "", ""],
        ["4 过刻", "", "", "", "", "", ""],
    ],
    [2.4, 2.6, 1.9, 1.9, 4.6, 1.9, 2.7],
    height=0.62,
)
para("", after=1)
for t in [
    "硬掩模已刻透（无残留）",
    "PFET 区已露出 TiN 并刻净",
    "NFET 区未过刻到栅氧",
    "终点曲线已存图 / 记录",
    "侧壁无明显 notching（如可观察）",
]:
    checkbox(t)
para("风险：场区下方是 145 nm BOX（完全绝缘），**充电无处泄放 → notching 风险高于体硅**。",
     size=8.8, before=2, color=(0x4A, 0x54, 0x60))

h2("阶段 F · 去胶与量测（14:45）")
for t in [
    "O₂ 灰化：________ W / ________ s（下游、无偏压）",
    "湿法：__________ ；温度 ______ °C ；时间 ______",
    "DI 冲洗（建议 ≥ 80 °C 以去 Cl）",
    "**硬掩模“帽”仍在栅顶**（显微镜确认颜色差）",
    "无残胶",
]:
    checkbox(t)
table(
    ["量测项", "数值", "手段"],
    [
        ["CD（刻蚀后）", "________ µm", "CD-SEM"],
        ["CD（显影后，回填）", "________ µm", "CD-SEM / 光学"],
        ["**CD bias**", "________ nm", "计算"],
        ["剖面角", "________ °", "X-SEM（如做）"],
        ["poly 方阻", "________ Ω/sq", "四探针（如做）"],
    ],
    [6.2, 7.4, 4.4],
    height=0.6,
)

# ══════════════════════════════ 5 ══════════════════════════════
h1("5　异常与偏差记录")
table(["时间", "现象", "可能原因", "处理", "影响后续？"],
      [["", "", "", "", ""] for _ in range(4)],
      [1.8, 4.4, 5.0, 4.4, 2.4], height=0.78)

# ══════════════════════════════ 6 ══════════════════════════════
h1("6　交接单")
for t in [
    "片号 ____________　交给 ____________　时间 ________",
    "栅条 CD ____________　剖面：☐ 未测　☐ 正常　☐ 异常",
    "已知缺陷：________________________________________________",
    "需要 LAB4 特别注意：______________________________________",
]:
    para(t, size=9.2, after=2)
para("", after=1)
checkbox("片子未破、未污染")
checkbox("数据已记录完整（含终点曲线）")

# ══════════════════════════════ 7 ══════════════════════════════
h1("7　失效速查（现场对照）")
table(
    ["症状", "最可能原因", "现场处理"],
    [
        ["对准反复报警", "标记被埋 / 信号弱、片放偏", "找助教确认标记，勿盲试"],
        ["整片图形模糊", "焦距偏、未吸平、吸盘有颗粒", "检查吸盘与平整度"],
        ["全场 CD 同向偏", "剂量、或 PEB / 显影条件", "查参数一致性"],
        ["仅局部 CD 偏", "平整度、台阶、颗粒", "查局部"],
        ["显影后有残渣", "软烘不足、显影不足、过曝", "视程度决定是否重做"],
        ["线条断 / 桥接", "剂量偏、掩模缺陷", "记录，重做"],
        ["刻蚀后 CD 变宽", "硬掩模被侧向削、聚合物裙边", "看剖面"],
        ["刻蚀后 CD 变窄", "侧壁倾斜、过刻", "看剖面"],
        ["PFET 区短路", "TiN 未刻净", "返工或报废，必须记录"],
        ["栅漏电（电测才发现）", "栅氧被打穿", "无法挽回，写进交接单"],
    ],
    [4.6, 7.4, 6.0],
    size=8.3,
)

# ══════════════════════════════ 8 ══════════════════════════════
h1("8　出门前看一眼")
for t in [
    "我在 **12:30** 做过一次真正的判断吗？（不是“看着差不多”，是有判据的）",
    "我的**终点曲线和参数**都记下来了吗？（没有记录 = 没做过）",
    "下一个做 LAB4 的人，能从我的**交接单**里知道什么？",
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.space_after = Pt(2)
    fnt(p.add_run("▍ "), 9.5, False, (0x2C, 0x4A, 0x7A))
    rich(p, t, 9.2)

# ── 页脚 ──
footer = sec.footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fnt(fp.add_run("LAB3 Gate Formation · 实验日检查清单　　第 "), 8, False, (0x8D, 0x99, 0xA8))
r = fp.add_run()
fnt(r, 8, False, (0x8D, 0x99, 0xA8))
f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " PAGE "
f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
r._r.append(f1); r._r.append(it); r._r.append(f2)
fnt(fp.add_run(" 页"), 8, False, (0x8D, 0x99, 0xA8))

out = "labs/LAB3_checklist.docx"
doc.save(out)

# ── 复核 ──
chk = Document(out)
texts = [p.text for p in chk.paragraphs]
assert any("实验日检查清单" in t for t in texts), "标题缺失"
assert any("12:30" in t for t in texts), "决策点缺失"
assert len(chk.tables) >= 9, f"表格数量异常: {len(chk.tables)}"
print("OK  paragraphs=%d  tables=%d" % (len(chk.paragraphs), len(chk.tables)))
