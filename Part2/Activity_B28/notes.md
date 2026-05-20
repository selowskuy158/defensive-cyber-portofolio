# B28 — Produce a Cyber-Safety Flyer for University Students

## What I produced
A single-page A4 cyber-safety flyer targeted at UWA students.
Generated programmatically as a PDF rather than designed in a GUI
tool, so it's reproducible from source.

**Files:**
- [`flyer.pdf`](flyer.pdf) — the finished flyer (4.5 KB, prints
  on any printer).
- [`build_flyer.py`](build_flyer.py) — the reportlab script that
  generates the PDF. Re-runs in <1 second.

## Audience
First- and second-year UWA students who are not in a cybersecurity
unit. The language deliberately avoids jargon ("authenticator app",
"WebAuthn", "MFA fatigue") in favour of concrete actions ("Turn on
2FA on Pheme", "Bitwarden is free for students").

## Content — the six habits
The flyer covers the six controls that, applied together, prevent
the majority of consumer-grade attacks:

1. **Use a password manager** (Bitwarden, free for students)
2. **Turn on 2FA** (Pheme, Microsoft 365, email, banking)
3. **Pause before you click** (the UWA-specific phishing patterns)
4. **Be wary on public Wi-Fi** (with a free VPN suggestion)
5. **Update everything weekly** (10-minute Sunday-evening window)
6. **Lock your devices** (5-minute lock + Find My Device)

Each tip is one card with three short bullet points — no walls of
text. The 80/20 rule: these six habits, done at the basic level,
defeat most attacks aimed at students.

## Design choices
- **UWA blue/gold colour scheme** so it's instantly recognisable as
  being for UWA.
- **Numbered circular badges** in cards — fast visual scanning.
- **Bottom call-out** with the incident-response contact (askit@uwa.edu.au)
  — students often don't know that UWA IT will help with their
  personal-account compromises if they ask.
- **Footer with "print and stick this on your fridge"** — sets the
  expected use, makes the artefact feel personal.

## Why generated, not designed in Canva
Generating from Python means:
- The flyer is reproducible from source — anyone with the script
  can rebuild the exact same PDF.
- Content changes are diff-able in git, not opaque binary edits.
- The file is small (4.5 KB vs ~500 KB for a Canva export).
- This is the pattern enterprises use for templated brand-compliant
  documents.

The trade-off is less visual polish than a designer would produce.
That trade is acceptable for an educational artefact.

## Evidence
- The PDF itself: [`flyer.pdf`](flyer.pdf)
- `evidence/b28-flyer-preview.png` — rendered preview of the PDF
  (so it can be embedded in the master submission PDF).
