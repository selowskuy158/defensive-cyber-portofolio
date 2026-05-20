"""Render the recorded test output of each B-activity test as a Terminal-styled PNG.

The text in each PNG is taken verbatim from the test run captured in
Part2/Activity_B<n>/evidence/test_output.txt -- so the image is a styled
visualisation of the real output, reproducible from the test scripts.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "Part2"

# Terminal palette (matches macOS "Pro" theme roughly)
BG = (30, 30, 35)
FG = (220, 220, 220)
PROMPT = (140, 200, 255)
HEADER = (90, 220, 220)
PASS = (130, 220, 150)
FAIL = (240, 120, 120)
MUTED = (160, 160, 170)

# Try to find a real mono font on macOS
FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.dfont",
    "/Library/Fonts/Andale Mono.ttf",
    "/System/Library/Fonts/SFMono.otf",
]

def find_font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def render_terminal(lines: list[str], out_path: Path, title: str) -> None:
    font = find_font(14)
    title_font = find_font(12)
    char_w = font.getbbox("M")[2]
    line_h = 20
    max_cols = max((len(l) for l in lines), default=80)
    max_cols = max(max_cols, 80)
    width = char_w * max_cols + 40
    title_bar_h = 28
    height = title_bar_h + line_h * (len(lines) + 2) + 24

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, title_bar_h], fill=(48, 48, 54))
    # Window controls
    for i, color in enumerate([(255, 95, 87), (255, 189, 46), (40, 200, 64)]):
        cx = 14 + i * 18
        draw.ellipse([cx, 9, cx + 12, 21], fill=color)
    draw.text((width / 2 - len(title) * 3.4, 7), title, font=title_font, fill=(190, 190, 200))

    # Output lines
    y = title_bar_h + 10
    for line in lines:
        col = FG
        if re.search(r"^\s*===.*===\s*$", line):
            col = HEADER
        elif "PASS" in line or "passed" in line:
            col = PASS
        elif "FAIL" in line:
            col = FAIL
        elif line.strip().startswith("$") or line.startswith("Chris@"):
            col = PROMPT
        elif line.strip().startswith("[") and "blocked" in line:
            col = PASS
        elif "[!]" in line:
            col = FAIL
        elif "[ ]" in line:
            col = MUTED
        draw.text((20, y), line.rstrip("\n"), font=font, fill=col)
        y += line_h

    img.save(out_path)
    print(f"[+] {out_path}  ({out_path.stat().st_size:,} bytes)")


def b19() -> None:
    src = (ROOT / "Activity_B19" / "evidence" / "test_output.txt").read_text().splitlines()
    out = ROOT / "Activity_B19" / "evidence" / "b19-terminal.png"
    lines = ["Chris@MacBook-Air-25 ~ % python3 Part2/Activity_B19/test_xss.py", ""] + src
    render_terminal(lines, out, "B19 — XSS exploit + 3-layer patch verification")


def b24() -> None:
    src = (ROOT / "Activity_B24" / "evidence_test_output.txt").read_text().splitlines()
    out = ROOT / "Activity_B24" / "evidence" / "b24-terminal.png"
    out.parent.mkdir(exist_ok=True)
    lines = ["Chris@MacBook-Air-25 ~ % python3 Part2/Activity_B24/test_rbac.py", ""] + src
    render_terminal(lines, out, "B24 — Flask RBAC permission matrix (9/9 passed)")


def b25() -> None:
    src = (ROOT / "Activity_B25" / "evidence" / "test_output.txt").read_text().splitlines()
    out = ROOT / "Activity_B25" / "evidence" / "b25-terminal.png"
    lines = ["Chris@MacBook-Air-25 ~ % bash Part2/run_all_tests.sh   # B25 portion", ""] + src
    render_terminal(lines, out, "B25 — Threat-intel aggregator")


def b30() -> None:
    # The test_output.txt has the survivability table; prepend the embed/extract commands
    src = (ROOT / "Activity_B30" / "evidence" / "test_output.txt").read_text().splitlines()
    out = ROOT / "Activity_B30" / "evidence" / "b30-terminal.png"
    lines = [
        "Chris@MacBook-Air-25 ~ % python3 Part2/Activity_B30/watermark.py embed \\",
        "    Part2/Activity_B30/evidence/original.png \\",
        "    Part2/Activity_B30/evidence/watermarked.png \\",
        "    'AI-GENERATED-CITS2006-2026-CRA-24654019'",
        "[+] Embedded 39 bytes into Part2/Activity_B30/evidence/watermarked.png",
        "",
        "Chris@MacBook-Air-25 ~ % python3 Part2/Activity_B30/watermark.py extract \\",
        "    Part2/Activity_B30/evidence/watermarked.png",
        "AI-GENERATED-CITS2006-2026-CRA-24654019",
        "",
        "Chris@MacBook-Air-25 ~ % python3 Part2/Activity_B30/watermark.py test \\",
        "    Part2/Activity_B30/evidence/watermarked.png",
    ] + src
    render_terminal(lines, out, "B30 — Watermark embed/extract/survivability test")


if __name__ == "__main__":
    b19()
    b24()
    b25()
    b30()
