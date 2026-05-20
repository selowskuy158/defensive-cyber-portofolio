# B15 — Teach an Elderly Person About Online Scams

## Topic
Scam types that target older Australians: fake SMS impersonation (ATO,
Australia Post), tech-support phone scams, and romance / pretexting
scams. Source: ACCC Scamwatch annual report — Australians aged 65+
report the highest per-victim losses of any age group.

## Session
I sat with my grandmother (74) at home and walked through the three
scam categories above, using examples on her own phone where possible:

1. **Fake SMS.** I showed her a screenshot of a real Australia Post
   impersonation SMS, pointed out the URL not ending in
   `auspost.com.au`, and explained that AusPost never asks for
   redelivery fees via SMS.
2. **Tech-support phone scams.** Explained that no one from Telstra,
   Microsoft, or her bank will phone her to fix a virus. The right
   response is always "I'll call you back" — then hang up and call
   the number on the back of her bank card or the official site.
3. **Romance / pretexting scams.** Covered the typical pattern (build
   emotional connection → invent a crisis → ask for money) since she
   uses Facebook to keep in touch with family.

## Artefact produced
A printed wallet-sized rule card she can keep near the phone, with the
five rules:
1. Never click links in SMS / email from unknown numbers.
2. Never give remote access to your computer.
3. Never share your PIN, password, or one-time code.
4. Always type the website address yourself (or use a bookmark).
5. When in doubt — stop, hang up, call family first.

The PDF is in this folder: [`rule_card.pdf`](rule_card.pdf), built by
the included [`build_rule_card.py`](build_rule_card.py) script.

## Evidence
- [`rule_card.pdf`](rule_card.pdf) — the actual printable card.
- `evidence/b15-rule-card-photo.png` — photo of the card next to her
  phone after the session.
- `evidence/b15-call-log.png` — call log entry confirming the
  conversation took place.

## What I learned
The "rule card" framing was much more effective than abstract advice.
She remembers concrete rules ("never share my code") far better than
principles ("be careful online"), and having a physical reminder by
the phone gives her a moment to pause before responding to a scam.

Older relatives are often the first line of defence for the rest of
the family — once she understood the pattern, she started asking me
about specific texts she received in the weeks after, instead of just
acting on them.
