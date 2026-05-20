"""Build the master Part 2 submission PDF.

Output: Part2/SUBMISSION.pdf

  Cover page  (name, ID, repo URL, date)
  Self-assessment table (one row per activity)
  Each activity's notes.md rendered in order

Run:
    pip install reportlab markdown
    python build_submission_pdf.py
"""
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Preformatted,
                                Spacer, Table, TableStyle, KeepTogether)


# ------------------------ config -----------------------------
STUDENT_NAME = "Christopher Raphael Armando"
STUDENT_ID = "24654019"
UNIT = "CITS2006 — Defensive Cybersecurity"
PART = "Part 2 — Portfolio Activities (B-series)"
REPO_URL = "https://github.com/selowskuy158/defensive-cyber-portofolio"
SUBMISSION_DATE = "21 May 2026"

# Activity order + claimed marks (defensible, conservative)
# B1-B3:  1 mark each  (observation-and-write-up tier)
# B12-B15, B26: 2 marks each  (one-off discovery/teaching with evidence)
# B16-B17: 2 marks each (research/design)
# B19-B21, B24, B25, B28-B30: 3 marks each (build artefact with evidence)
# B13: 2 marks (controlled experiment + screenshots)
ACTIVITIES = [
    ("B1",  "Discover 5 unique weak/vulnerable security implementations", 2),
    ("B2",  "Discover 5 unique strong security implementations", 2),
    ("B3",  "Discover 3 proactive security implementations in practice", 2),
    ("B12", "Discover two bias cases when using a generative AI system", 2),
    ("B13", "Perform a jailbreak attack on a generative AI assistant (controlled test)", 2),
    ("B14", "Teach friends about a cybersecurity topic (password hygiene)", 2),
    ("B15", "Teach an elderly person about online scams", 2),
    ("B16", "Survey the current state-of-the-art solutions in cybersecurity", 2),
    ("B17", "Implement / design a state-of-the-art solution (Zero Trust)", 3),
    ("B19", "Find and fix a vulnerability (XSS demo + 3-layer patch)", 3),
    ("B20", "Enhance the security of a GitHub project (this repo)", 3),
    ("B21", "Design and implement a cybersecurity learning activity (phishing quiz)", 3),
    ("B24", "Design and implement access control of your choice (Flask RBAC)", 3),
    ("B25", "Design and implement a threat-intelligence module", 3),
    ("B26", "Help a CITS2006 student understand public-key crypto", 2),
    ("B28", "Cyber-safety flyer for university students", 2),
    ("B29", "Fix a 2025 CVE using three AI systems and compare", 3),
    ("B30", "Generate an AI image + watermark + survival test", 3),
]

NAVY = HexColor("#0b1d3a")
ACCENT = HexColor("#1858b4")
GOLD = HexColor("#d4a017")
GREY = HexColor("#4a5468")
LIGHT_BG = HexColor("#eef1f6")

REPO_ROOT = Path(__file__).resolve().parent.parent
PART2 = REPO_ROOT / "Part2"
OUT = PART2 / "SUBMISSION.pdf"


# ------------------------ markdown -> reportlab flow ---------------
def md_to_flowables(md_text: str, styles) -> list:
    """Lightweight Markdown -> reportlab Platypus converter.
    Handles: # / ## / ### headings, paragraphs, bullet lists, fenced code blocks,
    inline code/bold/italic/links.
    """
    out: list = []
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # fenced code block
        if line.strip().startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # consume closing fence
            code = "\n".join(buf)
            out.append(Preformatted(code, styles["Code"]))
            out.append(Spacer(1, 4))
            continue

        # headings
        if line.startswith("### "):
            out.append(Paragraph(_inline(line[4:]), styles["H3"]))
            i += 1; continue
        if line.startswith("## "):
            out.append(Paragraph(_inline(line[3:]), styles["H2"]))
            i += 1; continue
        if line.startswith("# "):
            out.append(Paragraph(_inline(line[2:]), styles["H1"]))
            i += 1; continue

        # bullet list
        if re.match(r"^\s*[-*]\s+", line):
            bullets = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                bullets.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            for b in bullets:
                out.append(Paragraph("&bull;&nbsp;&nbsp;" + _inline(b), styles["Bullet"]))
            out.append(Spacer(1, 4))
            continue

        # numbered list  (1. ..)
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(lines[i])
                i += 1
            for item in items:
                m = re.match(r"^\s*(\d+)\.\s+(.*)", item)
                num, body = m.group(1), m.group(2)
                out.append(Paragraph(f"<b>{num}.</b>&nbsp;&nbsp;" + _inline(body), styles["Bullet"]))
            out.append(Spacer(1, 4))
            continue

        # blank line
        if line.strip() == "":
            out.append(Spacer(1, 4))
            i += 1; continue

        # default: paragraph (gather continuation lines)
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() != "" and not (
            lines[i].startswith(("#", "- ", "* ", "```"))
            or re.match(r"^\s*\d+\.\s+", lines[i])
        ):
            para.append(lines[i])
            i += 1
        out.append(Paragraph(_inline(" ".join(para)), styles["Body"]))
    return out


def _inline(s: str) -> str:
    # Escape XML first
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Pull out inline code FIRST so its contents can't be mis-parsed
    # as bold/italic markers (e.g. `.env*` would otherwise eat an asterisk).
    code_chunks: list[str] = []
    def _stash_code(m):
        code_chunks.append(m.group(1))
        return f"\x00CODE{len(code_chunks) - 1}\x00"
    s = re.sub(r"`([^`]+)`", _stash_code, s)

    # Bold
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    # Italic (avoid clashing with bold)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", s)
    # Markdown links [text](url)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<link href="\2" color="#1858b4"><u>\1</u></link>', s)

    # Restore code chunks (also XML-escape the chunk body just in case)
    def _restore(m):
        idx = int(m.group(1))
        body = code_chunks[idx].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<font face="Courier" size="9" color="#0b3d68">{body}</font>'
    s = re.sub(r"\x00CODE(\d+)\x00", _restore, s)
    return s


# ------------------------ page templates -----------------------
def _draw_page_chrome(canvas, doc):
    canvas.saveState()
    # Footer
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(20 * mm, 12 * mm, f"{STUDENT_NAME}  |  {STUDENT_ID}  |  {UNIT}  |  Part 2")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"page {doc.page}")
    canvas.setStrokeColor(LIGHT_BG)
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
    canvas.restoreState()


def _draw_cover_chrome(canvas, doc):
    canvas.saveState()
    # Top band
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 50 * mm, A4[0], 50 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, A4[1] - 53 * mm, A4[0], 3 * mm, fill=1, stroke=0)
    # Bottom band
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], 22 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 22 * mm, A4[0], 2 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(20 * mm, 10 * mm, "Submitted via UWA LMS")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, SUBMISSION_DATE)
    canvas.restoreState()


def make_styles():
    base = getSampleStyleSheet()
    return {
        "Body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica",
                               fontSize=10, leading=14, textColor=GREY, spaceAfter=4),
        "Bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName="Helvetica",
                                  fontSize=10, leading=14, leftIndent=14, textColor=GREY,
                                  spaceAfter=2),
        "H1": ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=18, leading=22,
                              textColor=NAVY, spaceBefore=12, spaceAfter=10),
        "H2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=13, leading=17,
                              textColor=ACCENT, spaceBefore=10, spaceAfter=6),
        "H3": ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=11, leading=14,
                              textColor=NAVY, spaceBefore=8, spaceAfter=4),
        "Code": ParagraphStyle("Code", fontName="Courier", fontSize=8.5, leading=10.5,
                                textColor=HexColor("#0b3d68"), backColor=LIGHT_BG,
                                borderPadding=6, leftIndent=4, rightIndent=4),
        "CoverTitle": ParagraphStyle("CoverTitle", fontName="Helvetica-Bold", fontSize=28,
                                      leading=34, textColor=white, alignment=TA_LEFT),
        "CoverSub": ParagraphStyle("CoverSub", fontName="Helvetica", fontSize=13,
                                    leading=16, textColor=GOLD, alignment=TA_LEFT),
        "CoverField": ParagraphStyle("CoverField", fontName="Helvetica", fontSize=11,
                                      leading=18, textColor=GREY),
        "CoverFieldL": ParagraphStyle("CoverFieldL", fontName="Helvetica-Bold", fontSize=11,
                                       leading=18, textColor=NAVY),
    }


def build_cover(styles) -> list:
    flow = [
        Spacer(1, 55 * mm),
        Paragraph(UNIT, styles["CoverSub"]),
        Paragraph("Portfolio Submission", styles["CoverTitle"]),
        Paragraph(PART, styles["CoverSub"]),
        Spacer(1, 30 * mm),
    ]
    rows = [
        ["Student name",      STUDENT_NAME],
        ["Student ID",        STUDENT_ID],
        ["Unit",              UNIT],
        ["Part",              PART],
        ["Submission date",   SUBMISSION_DATE],
        ["Repository",        REPO_URL],
        ["Activities claimed", f"{len(ACTIVITIES)}"],
    ]
    rows_styled = [[Paragraph(k, styles["CoverFieldL"]), Paragraph(v, styles["CoverField"])] for k, v in rows]
    t = Table(rows_styled, colWidths=[42 * mm, 120 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, LIGHT_BG),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 14 * mm))
    flow.append(Paragraph(
        "<i>This portfolio submits 18 of the 30 Part 2 activities, each backed by "
        "an evidence file in the linked GitHub repository. Code artefacts, generated "
        "PDFs, and test outputs are stored alongside their notes.md write-ups in "
        "Part2/Activity_B*. Markers can verify completion by cloning the repository "
        "and running the included test scripts.</i>",
        styles["Body"]))
    return flow


def build_self_assessment(styles) -> list:
    flow = [Paragraph("Self-Assessment Table", styles["H1"]),
            Paragraph("Marks claimed below reflect the level of evidence and depth produced for each activity. "
                      "Every claim is supported by files in the repository under "
                      "<font face='Courier' size='9'>Part2/Activity_B&lt;n&gt;/</font>.",
                      styles["Body"]),
            Spacer(1, 4)]
    header = ["ID", "Activity", "Evidence location", "Marks claimed"]
    data = [header]
    total = 0
    for code, title, marks in ACTIVITIES:
        loc = f"Part2/Activity_{code}/"
        data.append([code, title, loc, str(marks)])
        total += marks
    data.append(["", "", "Total marks claimed", str(total)])

    t = Table(data, colWidths=[14 * mm, 92 * mm, 50 * mm, 18 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",  (0, 0), (-1, 0), white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING",    (0, 0), (-1, 0), 6),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [white, LIGHT_BG]),
        ("BACKGROUND", (0, -1), (-1, -1), GOLD),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, -1), (-1, -1), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.25, GREY),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 6))
    flow.append(Paragraph(
        f"<b>Total: {total} marks claimed across {len(ACTIVITIES)} activities.</b>",
        styles["Body"]))
    return flow


def build_activity_section(code: str, title: str, marks: int, styles) -> list:
    folder = PART2 / f"Activity_{code}"
    notes_path = folder / "notes.md"
    flow: list = [Paragraph(f"{code} &mdash; {title}", styles["H1"]),
                  Paragraph(f"<b>Marks claimed:</b> {marks} &nbsp;&nbsp;|&nbsp;&nbsp; "
                            f"<b>Evidence:</b> <font face='Courier' size='9'>Part2/Activity_{code}/</font>",
                            styles["Body"]),
                  Spacer(1, 4)]
    if notes_path.exists():
        flow.extend(md_to_flowables(notes_path.read_text(), styles))
    else:
        flow.append(Paragraph(f"<i>notes.md not found at {notes_path}</i>", styles["Body"]))
    return flow


def build() -> None:
    styles = make_styles()

    doc = BaseDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=22 * mm, bottomMargin=20 * mm,
        title=f"{UNIT} — Part 2 Portfolio", author=STUDENT_NAME,
    )
    frame_cover = Frame(0, 0, A4[0], A4[1], id="cover",
                        leftPadding=20 * mm, rightPadding=20 * mm,
                        topPadding=0, bottomPadding=22 * mm)
    frame_body = Frame(doc.leftMargin, doc.bottomMargin,
                       doc.width, doc.height, id="body")
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[frame_cover], onPage=_draw_cover_chrome),
        PageTemplate(id="Body",  frames=[frame_body],  onPage=_draw_page_chrome),
    ])

    flow: list = []
    flow.extend(build_cover(styles))
    flow.append(NextPageTemplate("Body"))
    flow.append(PageBreak())

    flow.extend(build_self_assessment(styles))

    for code, title, marks in ACTIVITIES:
        flow.append(PageBreak())
        flow.extend(build_activity_section(code, title, marks, styles))

    doc.build(flow)
    print(f"[+] Wrote {OUT}  ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
