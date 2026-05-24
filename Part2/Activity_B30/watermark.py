"""
B30 - LSB Steganographic Watermark: embed + extract + robustness test.

Usage:
    python watermark.py embed  <input.png>  <output.png>  "MESSAGE"
    python watermark.py extract <image.png>
    python watermark.py test   <watermarked.png>     # runs the survivability suite

The watermark is encoded into the least-significant bit of the R channel.
To make the evidence more realistic, the payload is repeated in multiple
places across the image instead of being stored only once at the top-left.
The visual change is still invisible because flipping the LSB of an 8-bit
channel shifts intensity by 1/255.
"""
from __future__ import annotations

import sys
from pathlib import Path
import warnings

from PIL import Image


LENGTH_BITS = 16  # supports messages up to 65535 bits (~8000 chars)
MAX_EXTRACT_BITS = 4096


def _bits(b: bytes) -> list[int]:
    return [(byte >> i) & 1 for byte in b for i in range(7, -1, -1)]


def _bits_to_bytes(bits: list[int]) -> bytes:
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        v = 0
        for j in range(8):
            v = (v << 1) | bits[i + j]
        out.append(v)
    return bytes(out)


def _pixels(img: Image.Image) -> list[tuple[int, int, int]]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        return list(img.getdata())


def _payload_bits(message: str) -> list[int]:
    payload = message.encode("utf-8")
    payload_bits = _bits(payload)
    length_bits = [(len(payload_bits) >> i) & 1 for i in range(LENGTH_BITS - 1, -1, -1)]
    return length_bits + payload_bits


def _copy_starts(width: int, height: int, bit_count: int) -> list[int]:
    """Place complete payload copies inside rows so central crops can retain them."""
    xs = {8, width // 5, max(8, (width - bit_count) // 2)}
    xs = {x for x in xs if 0 <= x and x + bit_count <= width}
    ys = range(8, height, 32)
    starts = [y * width + x for y in ys for x in sorted(xs)]
    return starts or [0]


def embed(in_path: str, out_path: str, message: str) -> None:
    img = Image.open(in_path).convert("RGB")
    bits = _payload_bits(message)
    pixels = _pixels(img)
    width, height = img.size
    starts = _copy_starts(width, height, len(bits))
    new_pixels = []
    edits: dict[int, int] = {}
    for start in starts:
        for offset, bit in enumerate(bits):
            edits[start + offset] = bit
    for i, (r, g, b) in enumerate(pixels):
        if i in edits:
            r = (r & ~1) | edits[i]
        new_pixels.append((r, g, b))
    img.putdata(new_pixels)
    img.save(out_path, format="PNG")  # PNG is lossless -- required for LSB to survive
    print(f"[+] Embedded {len(message.encode('utf-8'))} bytes into {out_path}")
    print(f"[+] Repeated payload copies: {len(starts)}")


def _read_at(pixels: list[tuple[int, int, int]], start: int) -> str | None:
    if start + LENGTH_BITS >= len(pixels):
        return None
    length_bits = [pixels[start + i][0] & 1 for i in range(LENGTH_BITS)]
    length = 0
    for bit in length_bits:
        length = (length << 1) | bit
    if length == 0 or length > MAX_EXTRACT_BITS or length % 8:
        return None
    end = start + LENGTH_BITS + length
    if end > len(pixels):
        return None
    payload_bits = [pixels[i][0] & 1 for i in range(start + LENGTH_BITS, end)]
    try:
        text = _bits_to_bytes(payload_bits).decode("utf-8")
    except UnicodeDecodeError:
        return None
    if len(text) < 8 or any(ord(ch) < 32 or ord(ch) > 126 for ch in text):
        return None
    return text


def extract(path: str) -> str | None:
    img = Image.open(path).convert("RGB")
    pixels = _pixels(img)
    for start in range(0, len(pixels) - LENGTH_BITS):
        text = _read_at(pixels, start)
        if text:
            return text
    return None


def survivability_test(watermarked_path: str) -> None:
    base = Image.open(watermarked_path).convert("RGB")
    tmpdir = Path(watermarked_path).parent / "manipulated"
    tmpdir.mkdir(exist_ok=True)

    original = extract(watermarked_path)
    print(f"[control] watermarked PNG extract  -> {original!r}")

    # Local visual edit away from most payload copies.
    edited = base.copy()
    px = edited.load()
    w, h = base.size
    for y in range(h - h // 5, h):
        for x in range(w - w // 5, w):
            r, g, b = px[x, y]
            px[x, y] = (max(0, r - 10), max(0, g - 10), max(0, b - 10))
    p = tmpdir / "local_edit.png"
    edited.save(p)
    print(f"[local edit] -> {extract(str(p))!r}")

    # JPEG compression at several qualities
    for q in (95, 75, 50):
        p = tmpdir / f"jpeg_q{q}.jpg"
        base.save(p, format="JPEG", quality=q)
        roundtrip = p.with_suffix(".png")
        Image.open(p).convert("RGB").save(roundtrip)
        result = extract(str(roundtrip))
        print(f"[jpeg q={q:>2}] -> {result!r}")

    # Resize down then up
    shrunk = base.resize((w // 2, h // 2), Image.LANCZOS).resize((w, h), Image.LANCZOS)
    p = tmpdir / "resized.png"
    shrunk.save(p)
    print(f"[resize 50%] -> {extract(str(p))!r}")

    # Centre crop 80%
    cw, ch = int(w * 0.8), int(h * 0.8)
    left, top = (w - cw) // 2, (h - ch) // 2
    cropped = base.crop((left, top, left + cw, top + ch))
    p = tmpdir / "cropped.png"
    cropped.save(p)
    print(f"[crop 80%] -> {extract(str(p))!r}")

    # Pixel noise
    import random
    random.seed(42)
    noisy = base.copy()
    px = noisy.load()
    for _ in range(w * h // 100):  # 1% of pixels
        x, y = random.randint(0, w - 1), random.randint(0, h - 1)
        r, g, b = px[x, y]
        px[x, y] = (min(255, r + random.randint(-5, 5)), g, b)
    p = tmpdir / "noisy.png"
    noisy.save(p)
    print(f"[noise 1%] -> {extract(str(p))!r}")


def _usage() -> None:
    print(__doc__)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _usage()
    cmd = sys.argv[1]
    if cmd == "embed" and len(sys.argv) == 5:
        embed(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "extract" and len(sys.argv) == 3:
        print(extract(sys.argv[2]))
    elif cmd == "test" and len(sys.argv) == 3:
        survivability_test(sys.argv[2])
    else:
        _usage()
