"""B28 - Produces a single-page A4 cyber-safety flyer for UWA students.

Output: flyer.pdf  (A4 portrait, ~150 KB, prints on a standard printer)

Uses only the Python stdlib + reportlab. Install:
    pip install reportlab
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


PAGE_W, PAGE_H = A4
UWA_BLUE = HexColor("#0033A0")
UWA_GOLD = HexColor("#FFC72C")
DARK = HexColor("#1a2138")
LIGHT_BG = HexColor("#f4f6fa")
MUTED = HexColor("#5a6478")


def header(c: canvas.Canvas) -> None:
    # Blue band
    c.setFillColor(UWA_BLUE)
    c.rect(0, PAGE_H - 38 * mm, PAGE_W, 38 * mm, fill=1, stroke=0)
    # Gold accent
    c.setFillColor(UWA_GOLD)
    c.rect(0, PAGE_H - 41 * mm, PAGE_W, 3 * mm, fill=1, stroke=0)
    # Title text
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(15 * mm, PAGE_H - 22 * mm, "STAY CYBER SAFE AT UWA")
    c.setFont("Helvetica", 13)
    c.drawString(15 * mm, PAGE_H - 30 * mm, "A quick guide for students - 6 habits that protect everything else.")


def tip_box(c: canvas.Canvas, x, y, w, h, number, title, body):
    # Card background
    c.setFillColor(LIGHT_BG)
    c.roundRect(x, y, w, h, 4 * mm, fill=1, stroke=0)
    # Number circle
    cx, cy = x + 10 * mm, y + h - 11 * mm
    c.setFillColor(UWA_BLUE)
    c.circle(cx, cy, 6 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(cx, cy - 4, str(number))
    # Title
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(x + 22 * mm, y + h - 9 * mm, title)
    # Body lines (wrap manually -- short and known)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9.5)
    text_obj = c.beginText(x + 22 * mm, y + h - 16 * mm)
    text_obj.setLeading(12)
    for line in body:
        text_obj.textLine(line)
    c.drawText(text_obj)


def footer(c: canvas.Canvas) -> None:
    c.setFillColor(UWA_BLUE)
    c.rect(0, 0, PAGE_W, 18 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(15 * mm, 10 * mm, "Need help?  UWA IT Service Desk -- ask.uwa.edu.au  |  (08) 6488 1234")
    c.setFont("Helvetica", 8.5)
    c.drawString(15 * mm, 5 * mm, "Made by a CITS2006 student.  Print and stick this on your fridge.")
    c.setFillColor(UWA_GOLD)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawRightString(PAGE_W - 15 * mm, 7 * mm, "v1.0  |  CITS2006 / B28")


def build(path: str = "flyer.pdf") -> None:
    c = canvas.Canvas(path, pagesize=A4)
    header(c)
    footer(c)

    tips = [
        ("Use a Password Manager",
         ["Stop reusing passwords. Bitwarden is free for students.",
          "One strong master password, the manager handles the rest.",
          "Generates unique 20-character passwords for every site."]),
        ("Turn On Two-Factor Auth",
         ["Enable 2FA on Pheme, Microsoft 365, email, banking.",
          "Even if your password leaks, attackers cannot log in.",
          "Prefer authenticator apps over SMS where possible."]),
        ("Pause Before You Click",
         ["UWA students get phishing for scholarships, IT 'support', refunds.",
          "Check the sender domain. Hover over links to see the real URL.",
          "When in doubt, log in to the real site in a new tab."]),
        ("Be Wary on Public Wi-Fi",
         ["Cafe / library Wi-Fi can be sniffed by anyone nearby.",
          "Avoid logging in to banking or sensitive accounts.",
          "Use a VPN (Cloudflare WARP is free) or your phone hotspot."]),
        ("Update Everything Weekly",
         ["OS, browser, and apps. Most attacks exploit known unpatched bugs.",
          "Schedule one 10-minute Sunday-evening update window.",
          "Auto-update is fine -- leave it on."]),
        ("Lock Your Devices",
         ["Laptop in the library = thief in your inbox in under 60 seconds.",
          "Set a screen lock under 5 minutes. PIN > pattern.",
          "Enable Find My Device / Find My Mac so you can wipe remotely."]),
    ]

    # Two-column grid: 3 rows × 2 columns
    margin_x = 15 * mm
    top = PAGE_H - 46 * mm
    available_w = PAGE_W - 2 * margin_x
    gap_x, gap_y = 6 * mm, 6 * mm
    cell_w = (available_w - gap_x) / 2
    cell_h = 42 * mm

    for idx, (title, body) in enumerate(tips):
        row = idx // 2
        col = idx % 2
        x = margin_x + col * (cell_w + gap_x)
        y = top - (row + 1) * cell_h - row * gap_y
        tip_box(c, x, y, cell_w, cell_h, idx + 1, title, body)

    # Bottom call-out: emergency / report
    cy = top - 3 * cell_h - 2 * gap_y - 16 * mm
    c.setFillColor(DARK)
    c.roundRect(margin_x, cy, available_w, 14 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(UWA_GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_x + 6 * mm, cy + 8 * mm, "Been hacked? Lost your phone? Got a weird email?")
    c.setFillColor(white)
    c.setFont("Helvetica", 9.5)
    c.drawString(margin_x + 6 * mm, cy + 3 * mm,
                 "Don't wait. Email askit@uwa.edu.au immediately. UWA IT has a dedicated incident response process.")

    c.showPage()
    c.save()
    print(f"[+] Wrote {path}  ({Path(path).stat().st_size:,} bytes)")


if __name__ == "__main__":
    build("flyer.pdf")
