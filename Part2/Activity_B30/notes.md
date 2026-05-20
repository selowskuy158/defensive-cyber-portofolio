# B30 — AI Image + Imperceptible Watermark + Survival Test

## What I did
Generated an AI-created image, applied an imperceptible
steganographic watermark using least-significant-bit (LSB) encoding,
and tested whether the watermark survives a battery of common image
manipulations.

## Artefacts
- [`watermark.py`](watermark.py) — the LSB embed / extract /
  survivability-test script.
- `evidence/original.png` — the unwatermarked AI-style image.
- `evidence/watermarked.png` — the same image after embedding the
  payload `"AI-GENERATED-CITS2006-2026-CRA-24654019"`.
- `evidence/manipulated/` — the same watermarked image after
  JPEG compression (q95 / q75 / q50), resize, crop, and pixel noise.
- `evidence/test_output.txt` — the extraction results from each
  manipulation.

## Method

### Embedding
Each character of the payload is converted to bits; the bits are
written into the least-significant bit of the R channel of
successive pixels, prefixed by a 16-bit length header so the
extractor knows when to stop. Because a single-bit flip in an 8-bit
channel changes intensity by 1/255 (~0.4%), the watermark is
invisible to the human eye.

### Extraction
The extractor reads the first 16 R-channel LSBs to recover the
length, then reads `length` more bits, regroups them into bytes, and
decodes as UTF-8.

### Survivability test
The script runs the watermarked PNG through five manipulations and
attempts extraction after each.

## Results
```
[control] watermarked PNG extract   -> 'AI-GENERATED-CITS2006-2026-CRA-24654019'
[jpeg q=95]                          -> None
[jpeg q=75]                          -> None
[jpeg q=50]                          -> None
[resize 50%]                         -> None
[crop 80%]                           -> None
[noise 1%]                           -> 'AI-GGNERATED-CITS2006-2026-CZA-24654019'
```

### Interpretation
- **PNG (lossless) round-trip:** watermark recovered exactly. This
  confirms the implementation is correct.
- **JPEG at any quality:** watermark destroyed. JPEG is lossy and
  quantises DCT coefficients, which obliterates the LSB plane.
- **Resize:** destroyed. Pixel interpolation averages neighbouring
  values, mixing LSBs.
- **Centre crop 80%:** destroyed. Even though the watermark bits are
  spatially distributed across the image, the length prefix lives in
  the first 16 pixels which the crop removes.
- **1% pixel noise:** partially survived. Most characters recovered,
  but two bit-flips (`E→G`, `R→Z`) — bit errors are visible because
  there's no error-correcting code on the payload.

## Discussion: what this tells us about real watermarking
LSB steganography is **fragile**. Any operation that re-quantises
pixel intensities — JPEG re-encoding, resize, social-media upload
pipelines — destroys it. Real production watermarking
(Google DeepMind's *SynthID*, Microsoft / Adobe C2PA content
credentials) embeds the watermark in the **frequency domain** (DCT /
wavelet coefficients) with redundancy and error-correcting codes,
which is what makes them survive screenshotting and JPEG re-encoding.

The LSB demo here is sufficient for the educational point — it shows
both the principle (you *can* hide data invisibly in pixels) and the
limitation (you can't keep it there if anyone touches the image).
Anyone deploying watermarking in the real world needs the SynthID /
C2PA class of solution, not LSB.

## Reflection
The biggest insight is that "watermark survives" is a *gradient*,
not a binary. Even the partially-survived noise case is interesting:
it tells you the image has *probably* been watermarked, even if you
can't recover the original payload. For provenance applications
("was this image AI-generated?") that probabilistic signal is
sometimes enough.
