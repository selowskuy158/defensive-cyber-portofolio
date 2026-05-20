"""B15 - Generates a single-page rule card to give an elderly family member.

Output: rule_card.pdf  (A6 size, prints 4-up on A4; can also be texted as JPG)
"""
from __future__ import annotations
from pathlib import Path

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


PAGE_W, PAGE_H = A6  # 105 x 148 mm
NAVY = HexColor("#1a2138")
WARN = HexColor("#c92d2d")
OK = HexColor("#1f8a4c")
SOFT = HexColor("#f1f3f7")


def build(path: str = "rule_card.pdf") -> None:
    c = canvas.Canvas(path, pagesize=A6)

    # Header
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 18 * mm, PAGE_W, 18 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 8 * mm, "STAY SAFE ONLINE")
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 13.5 * mm, "Keep this card near the phone.")

    rules = [
        ("Never click links in SMS or email from numbers you don't know.",
         "Real banks, the ATO, and Australia Post will NOT ask you to click a link to fix a problem."),
        ("Never give anyone remote access to your computer.",
         "If someone calls saying 'your computer has a virus' - hang up. It is a scam."),
        ("Never share your PIN, password or one-time code.",
         "No real bank, no real Telstra, no real Microsoft staff will EVER ask for these."),
        ("Always go to websites yourself.",
         "Type the address into your browser, or use a bookmark. Do not click links from messages."),
        ("If something feels wrong, stop. Call family first.",
         "When in doubt, ring your grandchild before you do anything. We don't mind."),
    ]

    y = PAGE_H - 24 * mm
    for i, (rule, why) in enumerate(rules, 1):
        # Card
        c.setFillColor(SOFT)
        c.roundRect(4 * mm, y - 19 * mm, PAGE_W - 8 * mm, 18 * mm, 2 * mm, fill=1, stroke=0)
        # Number
        c.setFillColor(WARN)
        c.circle(9 * mm, y - 6 * mm, 3.5 * mm, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(9 * mm, y - 7.5 * mm, str(i))
        # Rule
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 8.5)
        # word-wrap manually
        _draw_wrapped(c, rule, 14 * mm, y - 5 * mm, PAGE_W - 18 * mm, "Helvetica-Bold", 8.5, 10)
        c.setFillColor(HexColor("#404a5e"))
        c.setFont("Helvetica", 7.5)
        _draw_wrapped(c, why, 14 * mm, y - 11 * mm, PAGE_W - 18 * mm, "Helvetica", 7.5, 9)
        y -= 22 * mm

    # Footer
    c.setFillColor(OK)
    c.rect(0, 0, PAGE_W, 8 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(PAGE_W / 2, 3 * mm, "When in doubt - HANG UP. CALL FAMILY.")

    c.showPage()
    c.save()
    print(f"[+] Wrote {path}  ({Path(path).stat().st_size:,} bytes)")


def _draw_wrapped(c, text, x, y, max_w, font, size, leading):
    c.setFont(font, size)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            line = trial
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)


if __name__ == "__main__":
    build("rule_card.pdf")
